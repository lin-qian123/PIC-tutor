#!/usr/bin/env python3

import argparse
import io
import json
import os
import shutil
import subprocess
import sys
import time
import urllib.error
import urllib.request
import zipfile
from pathlib import Path


BASE_URL = "https://mineru.net/api/v4"


def http_json(method, url, headers=None, payload=None):
    data = None
    req_headers = headers or {}
    if payload is not None:
        data = json.dumps(payload).encode("utf-8")
        req_headers = {**req_headers, "Content-Type": "application/json"}
    req = urllib.request.Request(url, data=data, headers=req_headers, method=method)
    with urllib.request.urlopen(req) as resp:
        return json.loads(resp.read().decode("utf-8"))


def http_put_file(url, path):
    result = subprocess.run(
        ["curl", "-fsSL", "-X", "PUT", "-T", str(path), url],
        check=False,
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        raise RuntimeError(result.stderr.strip() or "curl PUT upload failed")


def http_get_bytes(url, headers=None):
    req = urllib.request.Request(url, headers=headers or {})
    with urllib.request.urlopen(req) as resp:
        return resp.read()


def rename_main_md(target_dir, stem_name):
    target = Path(target_dir) / f"{stem_name}.md"
    if target.exists():
        return
    md_files = list(Path(target_dir).glob("*.md"))
    if md_files:
        md_files[0].rename(target)


def clean_directory(target_dir):
    for item in Path(target_dir).iterdir():
        keep = item.is_dir() and item.name == "images"
        keep = keep or (item.is_file() and item.suffix.lower() == ".md")
        if not keep:
            if item.is_dir():
                shutil.rmtree(item)
            else:
                item.unlink()


def extract_zip(content, output_dir, stem_name):
    target_dir = Path(output_dir) / stem_name
    target_dir.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(io.BytesIO(content)) as zf:
        zf.extractall(target_dir)
    rename_main_md(target_dir, stem_name)
    clean_directory(target_dir)
    return target_dir


def poll_result(batch_id, headers):
    url = f"{BASE_URL}/extract-results/batch/{batch_id}"
    while True:
        result = http_json("GET", url, headers=headers)
        if result.get("code") != 0:
            raise RuntimeError(f"API error: {result.get('msg')}")
        extract_results = result.get("data", {}).get("extract_result", [])
        if not extract_results:
            time.sleep(2)
            continue
        state = extract_results[0].get("state")
        if state == "done":
            return extract_results[0].get("full_zip_url")
        if state in {"error", "failed", "cancelled"}:
            raise RuntimeError(
                f"MinerU state={state}: {extract_results[0].get('err_msg')}"
            )
        progress = extract_results[0].get("extract_progress", {})
        current_page = progress.get("extracted_pages", 0)
        total_pages = progress.get("total_pages", "?")
        print(f"处理中... [{state}] 页数: {current_page}/{total_pages}", flush=True)
        time.sleep(3)


def main():
    parser = argparse.ArgumentParser(description="MinerU conversion without requests")
    parser.add_argument("filepath", help="PDF file path")
    parser.add_argument(
        "--output", "-o", default=".", help="output directory for extracted folder"
    )
    args = parser.parse_args()

    api_key = os.getenv("MINERU_API_KEY")
    if not api_key:
        print("MINERU_API_KEY is not set", file=sys.stderr)
        raise SystemExit(1)

    file_path = Path(args.filepath)
    if not file_path.exists():
        print(f"file does not exist: {file_path}", file=sys.stderr)
        raise SystemExit(1)

    headers = {"Authorization": f"Bearer {api_key}"}
    file_info = {"name": file_path.name, "size": file_path.stat().st_size}
    init_data = {"files": [file_info]}

    print(f"开始处理: {file_path.name}")
    init_result = http_json(
        "POST", f"{BASE_URL}/file-urls/batch", headers=headers, payload=init_data
    )
    if init_result.get("code") != 0:
        raise RuntimeError(f"API error: {init_result.get('msg')}")

    data = init_result["data"]
    batch_id = data["batch_id"]
    upload_url = data["file_urls"][0]
    print(f"正在上传 (Batch ID: {batch_id})...")
    http_put_file(upload_url, file_path)

    print("等待转换完成...")
    zip_url = poll_result(batch_id, headers=headers)
    print("正在下载结果...")
    content = http_get_bytes(zip_url)
    output = extract_zip(content, args.output, file_path.stem)
    print(f"成功转换并保存至: {output}")


if __name__ == "__main__":
    main()
