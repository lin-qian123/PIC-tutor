# Public distribution boundary

- classification: `PUBLIC_REPOSITORY_THIRD_PARTY_ASSETS_TRACKED_REMEDIATION_REQUIRED`
- tracked `references/` files: `2425`
- tracked reference bytes: `190730587`
- tracked reference PDFs: `52`
- tracked reference images: `2259`
- current candidate: `PIC-tutor v0.110` / `264` PDF pages
- candidate artifacts match release manifest: `True`
- release manifest excludes `references/`: `True`
- root license files: `none`
- public redistribution sign-off: `BLOCKED_PENDING_MAINTAINER_RIGHTS_AND_REPOSITORY_DECISION`

## Boundary

Local Git inventory only. A release manifest does not remove files already tracked by Git or control distribution through public repository history.

## Required Maintainer Decision

Confirm redistribution rights per tracked third-party item, or remove the items from the public branch and decide whether public history must be rewritten.

The reader-facing PDF passed its editorial and layout checks, but that evidence does not grant redistribution rights for third-party source material.

## Safe Decision Paths

1. Confirm rights item by item, record the evidence, then add an appropriate project license and sign the release checklist.
2. Remove unconfirmed third-party material from the public branch, then explicitly decide whether public Git history also needs remediation.
3. Temporarily make the repository private while the rights inventory and project licensing decision remain open.

This audit records the boundary only. It does not delete files, alter Git history, change repository visibility, or grant a license.
