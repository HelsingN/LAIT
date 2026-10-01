---
schema_version: 1
open_count: 1
waived_count: 0
fixed_count: 4
total_count: 5
last_updated: 2026-10-01T07:37:22.959Z
---

# Broken Windows Ledger

> Cross-phase defect register. With `workflow.windows_enforce` enabled, `/gsd-ship` blocks while `open_count > 0`.
> Waive with `gsd-tools windows waive <id> "<reason>"` (reason required).
> Mark fixed with `gsd-tools windows fixed <id>`.

| id | phase | kind | file | line | description | status | reason | recorded_at | resolved_at |
|----|-------|------|------|------|-------------|--------|--------|-------------|-------------|
| 1 | 01 | stub | backend/lait/adapters/persistence/repositories.py | 80 | has_open_practice_session returns false until plan 01-05 binds an open PracticeSession | open |  | 2026-10-01T06:23:57.512Z |  |
| 2 | 01 | deviation | frontend/.dockerignore |  | Context-local dockerignore so host node_modules are not copied into the web image | fixed |  | 2026-10-01T06:57:38.623Z | 2026-10-01T06:58:40.893Z |
| 3 | 01 | deviation | docker/web-nginx.conf |  | nginx proxies /api and /health so the static frontend can reach the api service | fixed |  | 2026-10-01T06:57:39.338Z | 2026-10-01T06:58:41.564Z |
| 4 | 01 | deviation | backend/lait/domain/exercise.py |  | Shared exercise types added so Gap Fill and proof share one public contract | fixed |  | 2026-10-01T07:35:58.283Z | 2026-10-01T07:37:22.322Z |
| 5 | 01 | deviation | backend/tests/modules/exercise_proof/test_contract.py |  | Proof contract test reads module source via inspect.getfile | fixed |  | 2026-10-01T07:35:58.919Z | 2026-10-01T07:37:22.959Z |

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
  },
  {
    "id": 2,
    "kind": "deviation",
    "phase": "01",
    "file": "frontend/.dockerignore",
    "line": null,
    "description": "Context-local dockerignore so host node_modules are not copied into the web image",
    "status": "fixed",
    "reason": "",
    "recorded_at": "2026-10-01T06:57:38.623Z",
    "resolved_at": "2026-10-01T06:58:40.893Z",
    "milestone": "v1.0"
  },
  {
    "id": 3,
    "kind": "deviation",
    "phase": "01",
    "file": "docker/web-nginx.conf",
    "line": null,
    "description": "nginx proxies /api and /health so the static frontend can reach the api service",
    "status": "fixed",
    "reason": "",
    "recorded_at": "2026-10-01T06:57:39.338Z",
    "resolved_at": "2026-10-01T06:58:41.564Z",
    "milestone": "v1.0"
  },
  {
    "id": 4,
    "kind": "deviation",
    "phase": "01",
    "file": "backend/lait/domain/exercise.py",
    "line": null,
    "description": "Shared exercise types added so Gap Fill and proof share one public contract",
    "status": "fixed",
    "reason": "",
    "recorded_at": "2026-10-01T07:35:58.283Z",
    "resolved_at": "2026-10-01T07:37:22.322Z",
    "milestone": "v1.0"
  },
  {
    "id": 5,
    "kind": "deviation",
    "phase": "01",
    "file": "backend/tests/modules/exercise_proof/test_contract.py",
    "line": null,
    "description": "Proof contract test reads module source via inspect.getfile",
    "status": "fixed",
    "reason": "",
    "recorded_at": "2026-10-01T07:35:58.919Z",
    "resolved_at": "2026-10-01T07:37:22.959Z",
    "milestone": "v1.0"
  }
]
````
