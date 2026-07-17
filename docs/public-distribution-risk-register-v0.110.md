# Public Distribution Risk Register

日期：2026-07-18

## 当前事实

- GitHub remote `lin-qian123/PIC-tutor` 当前为 public repository。
- Git 当前跟踪 `references/` 下 `2,425` 个文件，约 `190,730,587` bytes，其中有 `52` 个 PDF 和 `2,259` 个图片。
- 根目录没有 `LICENSE*` 或 `COPYING*` 文件。
- `docs/v0.110-release-manifest.{json,md}` 排除 `references/`，但 manifest 只是未来 staging allowlist；它不会从已公开的分支、clone 或 Git 历史中移除任何文件。

因此，本仓库当前不能把“manifest 排除 references”写成第三方材料已经不再分发，也不能把“本机可读”写成有权公开再分发。

## 分类

`PUBLIC_REPOSITORY_THIRD_PARTY_ASSETS_TRACKED_REMEDIATION_REQUIRED`

这是一项发布边界，不是对任何单篇论文版权状态的判断。它说明公开仓库中仍有需要逐项确认授权的第三方材料，且项目本身尚未声明可供读者复用的许可证。

## 维护者决策

在确认每个第三方资产的公开再分发权之前，维护者需要决定以下策略之一：

1. 保持 public，但只在逐项授权确认后保留对应材料；
2. 从 public branch 移除未经确认的材料，并单独决定是否需要重写公开历史；
3. 临时改为 private，完成资产清单、权利确认和项目许可证选择后再发布。

本文件不执行删除、历史重写、仓库可见性变更或许可证选择。它只把这些操作必须先由维护者明确批准的原因记录下来。

## 可验收关闭条件

- 每个仍被 Git 跟踪的第三方 PDF、图片和转换产物都有可复核的再分发依据，或已从 public branch 中移除；
- 对历史中已公开的受限资产，已决定并执行保留、移除或历史重写策略；
- 为项目自有代码与书稿选择并提交明确许可证，且不把该许可证错误外推到第三方材料；
- `scripts/audit_public_distribution_boundary.py` 的 `remediation_open` 变为 `false`，并由人工复核确认。
