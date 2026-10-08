# Phase 01 historical UAT

[01-UAT-HISTORY-2026-10-06.md](./01-UAT-HISTORY-2026-10-06.md) was moved here on 2026-10-08 to distinguish a historical diagnosed session from the active [01-UAT.md](../01-UAT.md). The GSD active-UAT scan reads immediate phase-directory files, so nested history is not treated as current acceptance.

SHA-256 before and after the move: `DD8DEA68E6D76754BA95184D659D6B2D798A7018E368E0829ABFFFB613578818`. Original bytes, diagnosed header, issue row, G-01-1 resolution and original path references are retained. The archive's `source: [01-VERIFICATION.md]` refers to the parent phase report; dated historical verification is also retained under [verification-evidence](../verification-evidence/).

Resolved gap evidence: [01-15-SUMMARY.md](../01-15-SUMMARY.md), current [01-UAT.md](../01-UAT.md) 76/76, and [01-VERIFICATION.md](../01-VERIFICATION.md) passed 5/5. No old issue was rewritten as pass and no GSD predicate was bypassed.

## Historical audit snapshots — archived 2026-10-08

The four local pre-closeout reports are preserved below, together with the two October 2 review/ledger versions previously committed to merged main. Original findings, statuses, scores, snippets and line endings are unchanged. [audit-archive-index.json](./audit-archive-index.json) records each source, byte count and SHA-256. Local `.gitattributes` disables text conversion for dated 01-*.md snapshots so Git checkout preserves these bytes.

| Snapshot | Source / historical scope |
|---|---|
| [01-REVIEW-2026-10-02.md](./01-REVIEW-2026-10-02.md) | Tracked October 2 review, 52 files; original CR-01/WR-01–WR-07/IN-01 meanings retained. |
| [01-REVIEW-DISPOSITION-2026-10-02.md](./01-REVIEW-DISPOSITION-2026-10-02.md) | Tracked October 2 ledger with nine original open IDs; no retrospective status rewrite. |
| [01-REVIEW-2026-10-06.md](./01-REVIEW-2026-10-06.md) | Local October 6 post-01-12 review; three warnings, with different WR meanings. |
| [01-REVIEW-DISPOSITION-2026-10-06.md](./01-REVIEW-DISPOSITION-2026-10-06.md) | Local October 6 ledger with three original open findings. |
| [01-PATTERNS-2026-10-07.md](./01-PATTERNS-2026-10-07.md) | Local D-24–D-31 pattern map; presentation later superseded by D-32–D-37. |
| [01-UI-REVIEW-2026-10-06.md](./01-UI-REVIEW-2026-10-06.md) | Local code-only historical UI audit, 14/24, warnings and no blocker; no fresh score claim. |

Current status is reconciled in [01-REVIEW.md](../01-REVIEW.md) and [01-REVIEW-DISPOSITION.md](../01-REVIEW-DISPOSITION.md): October 6 WR-02 fixed by 01-19; WR-01/WR-03 remain open nonblocking advisories without an approved deferral. The stable [PATTERNS](../01-PATTERNS.md) and [UI-REVIEW](../01-UI-REVIEW.md) paths index their dated originals so existing completed-plan references keep resolving. No new audit, implementation change or Phase 1 scope expansion.
