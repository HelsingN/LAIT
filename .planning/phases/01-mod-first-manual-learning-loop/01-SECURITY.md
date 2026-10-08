---
phase: "01"
slug: "mod-first-manual-learning-loop"
status: verified
threats_open: 0
asvs_level: 1
block_on: high
created: "2026-10-06"
updated: "2026-10-08"
---

# Phase 01 — Security

> Threat register verified against the implementation on 2026-10-06. ASVS L1. `threats_open` counts only open threats at or above `high`.

`01-16-PLAN.md` has no XML `<threat_model>` block. Its markdown `## Threat model` rows (`T-01-41`–`T-01-45`, `T-01-SC`) are in the register. Summary Threat Flags in 01-03, 01-08, and 01-09 are `None`. No other summary added an unregistered flag.

---

## Trust Boundaries

| Boundary | Description | Data Crossing |
|----------|-------------|---------------|
| Browser → HTTP | Learner SPA calls the local API | Lesson source, spans, attempts, session ids |
| HTTP → application | Routers are DTO peers over command/query names | Validated bodies, no repository imports |
| Application → SQLite | Repositories own persistence | Learner-owned text, attempts, one open session per lesson |
| Catalog → modules | Bundled manifests only | Module ids and capabilities, no dynamic load |

---

## Threat Register

| Threat ID | Plan | Category | Severity | Disposition | Status | Evidence |
|-----------|------|----------|----------|-------------|--------|----------|
| T-01-01 | 01-01 | Tampering | medium | mitigate | closed | `LessonCreateBody.source` length bounds; `EmptyLessonSourceError` |
| T-01-02 | 01-01 | Information Disclosure | low | accept | accepted | Local learner; `/health` returns `{"status": "ok"}` |
| T-01-03 | 01-01 | Denial of Service | medium | mitigate | closed | `MAX_SOURCE_LENGTH` / `LessonSourceTooLongError` |
| T-01-04 | 01-02 | Elevation of Privilege | high | mitigate | closed | `load_bundled_catalog` identifier-only `lait.modules.*`; `validate_catalog` |
| T-01-05 | 01-02 | Information Disclosure | medium | mitigate | closed | `ModuleDescription` exposes public fields only |
| T-01-06 | 01-02 | Spoofing | high | mitigate | closed | `list_visible_for` filters by audience; proof visibility is `maintainer` |
| T-01-07 | 01-03 | Tampering | high | mitigate | closed | Span bounds checked; stored text is `source[start:end]` |
| T-01-08 | 01-03 | Tampering | medium | mitigate | closed | Active-unit list filters `removed_at IS NULL`; new id on add |
| T-01-09 | 01-04 | Tampering | high | mitigate | closed | Drag grade compares `learning_unit_id` |
| T-01-10 | 01-04 | Spoofing | medium | mitigate | closed | Typed match is `strip().casefold()` inside `evaluate()` |
| T-01-11 | 01-04 | Information Disclosure | low | accept | accepted | Feedback `expected` is the same learner's unit text |
| T-01-12 | 01-05 | Tampering | high | mitigate | closed | Submit loads `evaluate`, then inserts the attempt |
| T-01-13 | 01-05 | Tampering | high | mitigate | closed | `reject_if_unit_set_frozen` on add/remove/accept |
| T-01-14 | 01-11 | Repudiation | medium | mitigate | closed | Start-over abandons; attempts are not deleted |
| T-01-15 | 01-06 | XSS | high | mitigate | closed | Source renders as React text; no `dangerouslySetInnerHTML` |
| T-01-16 | 01-06 | Information Disclosure | medium | mitigate | closed | Learner UI lists visible exercise types only |
| T-01-17 | 01-07 | Spoofing | high | mitigate | closed | Card label comes from the server category |
| T-01-18 | 01-07 | Elevation of Privilege | medium | mitigate | closed | Renderer registry requires the learner-visible type |
| T-01-19 | 01-07 | XSS | high | mitigate | closed | Feedback strings render as text nodes |
| T-01-20 | 01-08 | Tampering | high | mitigate | closed | `@hey-api/openapi-ts` pinned at `0.99.0` |
| T-01-21 | 01-08 | Information Disclosure | low | accept | accepted | Local schema; generated client scan found no secrets |
| T-01-22 | 01-09 | Tampering | medium | mitigate | closed | Proof-removal test copies manifests under `tmp_path` |
| T-01-23 | 01-09 | Elevation of Privilege | high | mitigate | closed | Application layer does not import FastAPI, SQLAlchemy, or persistence models |
| T-01-24 | 01-10 | Tampering | medium | mitigate | closed | Entrypoint migrates before uvicorn; healthcheck follows |
| T-01-25 | 01-10 | Information Disclosure | low | accept | accepted | `.env.example` has an empty `AI_API_KEY=` |
| T-01-26 | 01-12 | Tampering | high | mitigate | closed | One open session per lesson, check+insert, unique index |
| T-01-27 | 01-12 | Denial of Service | high | mitigate | closed | Pending session flag stays open across reload |
| T-01-28 | 01-12 | Tampering | high | mitigate | closed | Stale generation does not change the open session |
| T-01-29 | 01-12 | Information Disclosure | low | accept | accepted | Single local learner; session key is per lesson |
| T-01-30 | 01-12 | Elevation of Privilege | medium | mitigate | closed | HTTP start-over delegates to the command |
| T-01-SC | 01-12 | Tampering | high | mitigate | closed | No new package install |
| T-01-31 | 01-13 | Information Disclosure | medium | accept | accepted | Attempt list is scoped by `lesson_id` |
| T-01-32 | 01-13 | Tampering | high | mitigate | closed | `restorable` only when accepted ids still match |
| T-01-33 | 01-13 | Elevation of Privilege | medium | mitigate | closed | Snapshot compare stays in the command |
| T-01-34 | 01-13 | Repudiation | medium | mitigate | closed | Finish closes the named session id |
| T-01-SC | 01-13 | Tampering | high | mitigate | closed | No new package install |
| T-01-35 | 01-14 | Tampering | medium | mitigate | closed | Stage toggle is the header control only |
| T-01-36 | 01-14 | Tampering | medium | mitigate | closed | Remove renders only for the selected unit |
| T-01-SC | 01-14 | Tampering | high | mitigate | closed | No new package install |
| T-01-37 | 01-15 | Tampering | high | mitigate | closed | Chip order is permuted; grade still compares unit id |
| T-01-38 | 01-15 | Tampering | medium | mitigate | closed | Graded controls are disabled |
| T-01-39 | 01-15 | Tampering | high | mitigate | closed | `stripEmphasis` returns a string rendered as text |
| T-01-40 | 01-15 | Information Disclosure | low | mitigate | closed | Feedback heading does not paint the session id |
| T-01-SC | 01-15 | Tampering | high | mitigate | closed | No new package install |
| T-01-41 | 01-16 | Tampering | high | mitigate | closed | `corrected` only after an `incorrect` for the same unit id and mode |
| T-01-42 | 01-16 | Information Disclosure | medium | mitigate | closed | Show answer writes localStorage and paints `expected` as text |
| T-01-43 | 01-16 | Tampering | medium | mitigate | closed | Advance is idempotent per position; finish does not append |
| T-01-44 | 01-16 | Tampering | medium | mitigate | closed | Queue identity is unit id + mode; named target resolves the cursor copy |
| T-01-45 | 01-16 | Tampering | medium | mitigate | closed | Listed `pass_item_count` is the opening size |
| T-01-SC | 01-16 | Supply chain | high | mitigate | closed | No new package install |
| T-01-46 | 01-17 | Tampering | medium | mitigate | closed | `_saved_chunks` rejects non-list/non-string JSON; reopened repository tests preserve rich/empty payloads and reject malformed chunks. |
| T-01-47 | 01-17 | Tampering | medium | mitigate | closed | Repository → query → HTTP maps stored attempt/unit ids and every saved feedback field; no cursor mutation in the list query. |
| T-01-SC | 01-17 | Supply chain | high | mitigate | closed | Existing pinned exporter/generator reused; no dependency changes in the approved plan. |
| T-01-48 | 01-18 R2 | Information Disclosure | medium | mitigate | closed | Renderer paints expected only for Correct/Corrected or reveal; incorrect educational payload is not mounted. UAT tests 7/12 passed by user report. |
| T-01-49 | 01-18 R2 | Tampering | medium | mitigate | closed | Versioned exact attempt/session/item bindings and presentation epoch guards; exact-row/corrupt/stale restore tests exist, recorded green; UAT tests 11/12 passed. |
| T-01-50 | 01-18 R2 | Active content | high | mitigate | closed | Inline answer uses React text nodes; hostile-markup renderer assertion checks inert text. No HTML insertion on this path. |
| T-01-SC | 01-18 R2 | Supply chain | high | mitigate | closed | No new dependencies, installs or provider calls in R2; existing lockfiles retained. |

*Status: closed · accepted · open. Only open threats at or above `high` count toward `threats_open`.*

---

## Accepted Risks Log

| Risk ID | Threat Ref | Rationale | Accepted By | Date |
|---------|------------|-----------|-------------|------|
| AR-01-02 | T-01-02 | One local learner; health exposes no secrets | plan register | 2026-10-06 |
| AR-01-11 | T-01-11 | Feedback expected text is that learner's own unit | plan register | 2026-10-06 |
| AR-01-21 | T-01-21 | OpenAPI schema stays on the local origin | plan register | 2026-10-06 |
| AR-01-25 | T-01-25 | Example env has an empty key, not a live secret | plan register | 2026-10-06 |
| AR-01-29 | T-01-29 | Session id is a per-lesson key for the single local learner | plan register | 2026-10-06 |
| AR-01-31 | T-01-31 | Attempt reads are lesson-scoped | plan register | 2026-10-06 |

---

## Security Audit Trail

| Audit Date | Threats Total | Closed | Accepted | Open blocking | Run By |
|------------|---------------|--------|----------|---------------|--------|
| 2026-10-06 | 50 | 44 | 6 | 0 | gsd-security-auditor |
| 2026-10-08 | 57 | 51 | 6 | 0 | Inline gsd-secure-phase completion audit; prior register retained, plans 01-17/18 added |

### Audit scope — 2026-10-08

Post-UAT ASVS L1 review incorporated the seven plan-time threat rows from 01-17/18. Direct source inspection covered saved JSON validation/projections, disclosure conditions, exact reveal binding, request epoch guards and inert answer text; corresponding behavioral tests have recorded passing evidence in 01-17/18 SUMMARYs. No new tests were run and no deeper ASVS claim is made. The prior 50 rows retain their historical evidence; this is not a fresh whole-application penetration test. Historical descriptions of the removed card/disabled input are superseded by R2 inline rendering, not new open threats. No new unregistered Summary Threat Flags were found in the follow-up summaries.

unregistered_flags: 0

---

## Sign-Off

- [x] All threats have a disposition (mitigate / accept / transfer)
- [x] Accepted risks documented in Accepted Risks Log
- [x] `threats_open: 0` confirmed
- [x] `status: verified` set in frontmatter

**Approval:** ASVS L1 plan-register verification updated 2026-10-08; zero blocking threats. This does not close canonical phase verification.
