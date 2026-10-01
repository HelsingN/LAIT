---
schema_version: 1
open_count: 1
waived_count: 0
fixed_count: 2
total_count: 3
last_updated: 2026-10-01T06:58:41.564Z
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
  }
]
````
