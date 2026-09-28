# Phase 1: Mod-First Manual Learning Loop - Context

**Gathered:** 2026-09-28
**Status:** Ready for planning

<domain>
## Phase Boundary

A learner can launch the local application, paste a lesson, manually add and accept a source-linked learning unit, generate Gap Fill from accepted units, and complete that exercise one item at a time with deterministic feedback. A maintainer can see that the same workflow runs through documented public commands, queries, the exercise registry, and the renderer registry, including a proof exercise that is absent from the learner workflow and removable from the static catalog without Core changes.

This phase does not extract units with AI, does not ship Chunk Completion, Sentence Reconstruction, Keyword Recall, retry/reveal, session resume, semantic evaluation, a maintainer UI page, or an MCP adapter.

</domain>

<decisions>
## Implementation Decisions

### Learner path and screens
- **D-01:** The Lesson is the persistent primary workspace. The Lesson List is only the entry point.
- **D-02:** Stages are Source, Learning Units, Generate Exercises, Practice, and Feedback. Completing a stage unlocks and automatically expands the next stage. Every unlocked stage remains accessible and can be expanded or collapsed independently. Expanded and collapsed state is remembered per lesson.
- **D-03:** A title is suggested from the first meaningful source line or heading and is editable before creation. If no suitable title exists, use `Untitled Lesson`. The title is user-facing metadata only. Each lesson has an immutable internal ID.
- **D-04:** The full source is available in a collapsible panel. Learning units, exercises, and feedback show the relevant source excerpt with one-click navigation to that location in the full source.
- **D-05:** Starting practice enters a distraction-free Focus Practice Mode that shows only the exercise, feedback, and navigation. Ending practice restores the prior Lesson Workspace state. — **Reversibility:** costly — later exercise types and session modes reuse this workspace/practice split.
- **D-06:** Phase 1 uses clear panel and session-mode boundaries so later customization does not require a redesign.

### Manual learning-unit capture
- **D-07:** A Phase 1 learning unit is created only by selecting a span in the lesson source and pressing Add. The selection alone does not create a unit. Add with no selection does nothing. The stored unit text is exactly the selected span, and that span is the occurrence. The unit text is not editable in this phase (ANLY-06 is Phase 2).
- **D-08:** Add stores a draft. Accept moves the draft into the pool eligible for Gap Fill. Exercises are generated only from accepted units. — **Reversibility:** costly — Phase 2 AI candidates reuse draft/accepted.
- **D-09:** Before practice starts, the learner can add, delete, and re-add units. Delete applies to both drafts and accepted units. Spans must be disjoint. The same phrase in two non-overlapping places is two units. Touching edges are allowed. An overlapping selection is rejected and the existing unit stays.
- **D-10:** The unit set freezes when Focus Practice Mode starts. While that session is open, units cannot be added or removed. Closing the session returns to the Lesson Workspace and unfreezes the set. Starting over does not unfreeze the set and does not return to unit editing: it abandons the open session and starts a new practice session on the same accepted set.
- **D-11:** LLM generation of units from the source is Phase 2. It is not a Phase 1 mode.

### Gap Fill practice and feedback
- **D-12:** One accepted unit produces one Gap Fill item. The item shows the source sentence with only the current target unit's span blanked. Neighboring units in that sentence stay visible as ordinary text. The rest of the sentence is not modified.
- **D-13:** Gap Fill has two modes, both in this phase, both owned by `exercise-gap-fill`. Simple mode drags a chip into the blank. Hard mode types the unit. A session is two passes: every unit in drag mode, then the same units in typed mode. If the lesson has only one accepted unit, the drag pass is omitted.
- **D-14:** Drag chips are the current unit plus the other accepted units of the same lesson. The correct chip is that unit's identity, not a matching string. The correct chip is `correct`. Any other chip is `incorrect`.
- **D-15:** Both passes order items by span position in the source. Accept order is ignored. Equal positions use a stable secondary key, `learning_unit_id`.
- **D-16:** Typed answers match after trimming leading and trailing whitespace and ignoring case. Internal extra whitespace, punctuation, and apostrophes do not match. Full English normalization (EVAL-02) stays in Phase 3. — **Reversibility:** costly — later exercises inherit the Phase 1 comparison floor.
- **D-17:** Phase 1 Gap Fill emits only `correct` or `incorrect`. It does not emit `acceptable`, `partial`, or `uncertain`. A hit records the target chunk as used. A miss records it as missed.
- **D-18:** Explanation is required and deterministic. Natural alternative is nullable and may be absent. Templates: correct → `Correct. The expected answer is "{unit}".` Incorrect → `Your answer: "{submitted}". Expected: "{unit}".` Richer grammar explanation is later work.
- **D-19:** Recorded attempts are never deleted. Starting over drops only in-progress state that has not become an Attempt.

### Mod-First proof surface
- **D-20:** The proof exercise registers through the same public exercise contracts, static module catalog, and frontend renderer registry as Gap Fill. It does not appear in the normal learner workflow. Success means removing the proof module from the static catalog requires no Core or application changes, and Gap Fill plus LAIT still run. Tests can still instantiate the proof module and mount its renderer on maintainer/test paths.
- **D-21:** `visibility` is exercise-contribution metadata, not a field of the universal module manifest. Phase 1 values are `learner` (Gap Fill) and `maintainer` (proof). The lesson surface calls `exercise_registry.list_visible_for("learner")` and must not know the Gap Fill module id or special-case the proof module. Maintainer and conformance tests may read the full registry. `experimental` is a future value of the same field, not Phase 1 behavior. — **Reversibility:** one-way — contribution metadata is a published module contract; moving `visibility` onto the universal manifest later would touch every module category.
- **D-22:** MODL-02 is a documented read-only diagnostic query, `module_registry.describe()`. It is a different operation from the learner exercise list, not one endpoint filtered in the UI. It returns public registry metadata only: `module_id`, `module_version`, `category`, `capabilities`, and for exercise contributions `exercise_type`, `visibility`, `activation_status`. No private module internals. The lesson UI must not call it. There is no maintainer page in Phase 1. A process with an invalid catalog does not start, so every row in a live diagnostic has `activation_status: active`. Acceptance: the diagnostic shows Gap Fill and the proof module activated through the same public mechanism, while `visibility: maintainer` keeps the proof module out of the learner workflow.
- **D-23:** Phase 1 learner behavior goes through documented application commands and queries. HTTP handlers are transport adapters. They map request DTOs onto commands/queries and do not call repositories, registries, or module services directly. The same boundary is callable without HTTP. Phase 1 does not build a generic distributed command bus or an MCP adapter. An in-process typed handler boundary is enough. Replacing the FastAPI router with a future MCP adapter must not require changes to Core, the application workflow, or exercise modules. — **Reversibility:** one-way — command and query names are the application boundary ADR-014 preserves for peer adapters.

Commands:

```text
lesson.create
learning_unit.add
learning_unit.remove
learning_unit.accept
exercise.generate
practice.start
exercise.submit_attempt
practice.finish
```

Queries:

```text
lesson.get
lesson.list
learning_unit.list
practice.get
exercise_registry.list_visible_for("learner")
module_registry.describe
```

`module_registry.describe()` is maintainer diagnostics, not part of the learner workflow. `practice.finish` closes the session back to the workspace and unfreezes units. Start-over abandons the open session and opens another practice session without that unfreeze. Do not collapse those two outcomes into one unparameterized finish if finish means "return to the workspace".

### Claude's Discretion
- Represent start-over as abandon-plus-`practice.start` or as a distinct command intent. The learner-visible behavior is locked in D-10 and D-19. Do not delete attempts either way.
- Proof-module exercise body can be the smallest contract-valid generate/evaluate/renderer implementation. It must not be wired into the learner list.

</decisions>

<canonical_refs>
## Canonical References

**Downstream agents MUST read these before planning or implementing.**

### Phase scope
- `.planning/ROADMAP.md` — Phase 1 goal, success criteria, and requirement ids
- `.planning/REQUIREMENTS.md` — LESS-01, LESS-02, ANLY-08, EXER-01, EXER-02, EXER-03, EXER-07, EVAL-01, EVAL-04, EVAL-05, MODL-01, MODL-02, MODL-03, MODL-12, PLAT-03, PLAT-09, PLAT-10
- `.planning/PROJECT.md` — core value, vertical-slice roadmap decision, command boundary for future integrations
- `docs/prd/PRD.md` — learning-unit types, Gap Fill as exercise 1, module manifest shape, deterministic evaluation

### Application boundary
- `docs/versions/spec-v0.2.0.md` — HTTP and MCP are peer adapters over the same application use cases. MCP itself is not a Phase 1 deliverable.
- `docs/adr/ADR-014-external-integration-boundary-and-mcp.md` — commands/queries are the integration boundary. No private table access. MCP waits until a vertical slice exists.
- `docs/architecture/ARCHITECTURE-v0.2.0.md` — 0.2.0 architecture overlay

</canonical_refs>

<code_context>
## Existing Code Insights

### Reusable Assets
- No application source yet. There are no React components, FastAPI routers, or persistence adapters to reuse. `.planning/codebase/` maps do not exist.

### Established Patterns
- Spec 0.2.0 already separates transport adapters from application use cases. Phase 1 is the first implementation of that boundary, not a retrofit.
- Official modules, including the proof exercise, use the same public contracts as Gap Fill. Core must not special-case module ids.

### Integration Points
- Static module catalog and exercise-contribution metadata (`visibility`) are the only switch for learner versus maintainer exposure.
- HTTP adapters call the command/query handlers listed in D-23. Future MCP would call those same handlers.

</code_context>

<specifics>
## Specific Ideas

- Gap Fill sentence shape: `I was responsible for ______ the migration.` when the unit is `rolling out`. Neighboring units in that sentence stay visible.
- Drag bank for a unit is the other accepted units of the same lesson. One accepted unit means there is no drag pass.
- Typed match: `Rolling out` equals `rolling out`. An internal extra space, a period, or an apostrophe does not.
- Feedback copy is the D-18 templates, not a model-written explanation.
- Overlap example that must be rejected: `responsible for rolling out` together with `rolling out`.

</specifics>

<deferred>
## Deferred Ideas

- Full Workspace API and Workspace Module with movable, dockable, resizable panels, splits, tabs, saved layouts, and perspectives. Target later architecture work around Phases 6–8.
- Additional exercise-session modes such as Classic, Exam, Game, and Reading.
- LLM generation of learning units from the source. Phase 2.
- Editing unit text after capture. Phase 2 (ANLY-06).
- `visibility: experimental` as a live value. The field stays an enum that Phase 1 only accepts as `learner` or `maintainer`.
- A maintainer diagnostics page. Phase 1 is the `module_registry.describe()` query only.
- Full English answer normalization (whitespace, case, punctuation, contractions). Phase 3 (EVAL-02).
- Richer grammar explanation beyond the deterministic Gap Fill templates.
- MCP adapter implementation. The command/query boundary must be callable without HTTP, but the adapter is not built in this phase (ADR-014).
- Retry, reveal, and session resume. Later exercise phases.

</deferred>

---

*Phase: 1-Mod-First Manual Learning Loop*
*Context gathered: 2026-09-28*
