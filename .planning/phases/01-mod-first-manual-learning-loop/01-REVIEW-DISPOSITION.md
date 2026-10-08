---
phase: 01
review: 01-REVIEW.md
titles: json
findings:
  - id: CR-01
    severity: critical
    disposition: open
    title: "An open practice session the UI no longer holds freezes the lesson permanently"
  - id: WR-01
    severity: warning
    disposition: open
    title: "Omitting `target_learning_unit_id` grades the current step with the wrong mode and advances it"
  - id: WR-02
    severity: warning
    disposition: open
    title: "`add_attempt` writes a stale cursor over a newer one"
  - id: WR-03
    severity: warning
    disposition: open
    title: "A selection anchored on the highlight element is measured as the end of the source"
  - id: WR-04
    severity: warning
    disposition: open
    title: "Every learning-unit 422 is shown as an overlap"
  - id: WR-05
    severity: warning
    disposition: open
    title: "Overlap is checked and inserted in two transactions"
  - id: WR-06
    severity: warning
    disposition: open
    title: "`exercise.generate` turns every module exception into a failed generation and drops the error"
  - id: WR-07
    severity: warning
    disposition: open
    title: "Recorded attempts disappear from the workspace after reload, and the last Continue renders a blank pass"
  - id: IN-01
    severity: info
    disposition: open
    title: "Lesson list failure uses the workspace error copy"
open: 9
total: 9
recorded: 2026-10-02T01:11:51.950Z
---

# Phase 01: Code Review Disposition

| Finding | Severity | Disposition | Source |
|---------|----------|-------------|--------|
| CR-01 | critical | open | - |
| WR-01 | warning | open | - |
| WR-02 | warning | open | - |
| WR-03 | warning | open | - |
| WR-04 | warning | open | - |
| WR-05 | warning | open | - |
| WR-06 | warning | open | - |
| WR-07 | warning | open | - |
| IN-01 | info | open | - |

Dispositions: `open` (recorded, not yet triaged), `fixed`, `skipped`, `deferred`.
Set `deferred` by hand and put the reason in the Source cell; both are preserved. A `|` in the reason is kept as prose and escaped on the next run.
Re-running the gate keeps every row it can. A row the current review no longer reports is kept and its Source cell flagged, so a finding does not leave this record silently. ONE exception: when a finding id is REUSED by a different finding, the earlier decision cannot keep a row — the id is taken — and it is dropped. A RECORDED decision (anything but `open`) is named on the console when that happens; a row still at `open` is replaced silently, because `open` records no decision to lose.
