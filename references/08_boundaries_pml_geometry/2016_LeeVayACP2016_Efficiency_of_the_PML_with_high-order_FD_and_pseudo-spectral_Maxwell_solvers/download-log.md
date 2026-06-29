# Download Log

- 2026-06-29: attempted official AIP PDF URL with `curl -L --fail --retry 2`.
- 2026-06-29: retried with browser-like user agent and AIP referrer.
- 2026-06-29: retried the `pubs.aip.org/aip/acp/article-pdf/.../050002_1_online.pdf` direct endpoint with browser-like user agent.
- Result: all attempts returned HTTP 403 from the PDF endpoint.
- Local status: no PDF saved; no MinerU extraction performed.
- Follow-up: obtain an authorized PDF for either DOI `10.1016/j.cpc.2015.04.004` or DOI `10.1063/1.4965625`, then rerun the paper workflow in this directory.
