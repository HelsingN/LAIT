---
schema_version: 1
open_count: 1
waived_count: 0
fixed_count: 0
total_count: 1
last_updated: 2026-10-01T06:23:57.512Z
---

# Broken Windows Ledger

> Cross-phase defect register. With `workflow.windows_enforce` enabled, `/gsd-ship` blocks while `open_count > 0`.
> Waive with `gsd-tools windows waive <id> "<reason>"` (reason required).
> Mark fixed with `gsd-tools windows fixed <id>`.

| id | phase | kind | file | line | description | status | reason | recorded_at | resolved_at |
|----|-------|------|------|------|-------------|--------|--------|-------------|-------------|
| 1 | 01 | stub | backend/lait/adapters/persistence/repositories.py | 80 | has_open_practice_session returns false until plan 01-05 binds an open PracticeSession | open |  | 2026-10-01T06:23:57.512Z |  |

````json
[
  {
    "id": 1,
    "kind": "stub",
    "phase": "01",
    "file": "backend/lait/adapters/persistence/repositories.py",
    "line": 80,
    "description": "has_open_practice_session returns false until plan 01-05 binds an open PracticeSession",
    "status": "open",
    "reason": "",
    "recorded_at": "2026-10-01T06:23:57.512Z",
    "resolved_at": null,
    "milestone": "v1.0"
  }
]
````
