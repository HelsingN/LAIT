---
status: diagnosed
trigger: "Find root causes only for five remaining Phase 1 practice/feedback UX symptoms from the 2026-10-06 browser verification. Do not edit application code or close the UAT gap."
created: 2026-10-05T21:48:00Z
updated: 2026-10-05T21:55:00Z
goal: find_root_cause_only
bug_class: Bohrbug
---

## Current Focus

```yaml
hypothesis: "All five symptoms are separate unimplemented behaviors on the current render and generate paths, not a 01-14 layout regression and not a runtime failure."
test: "Read GapFillRenderer, its CSS, gap-fill generate, practice.get, FeedbackStage, and the 01-13/01-14 scope notes against the browser report."
expecting: "Each symptom maps to a named function that never shuffles, never styles a visible typed field, never locks a graded answer, never renders a learner summary, and never strips source markdown."
next_action: "Return ROOT CAUSE FOUND. Do not edit application code."
known_pattern_candidate: "none — .planning/debug/knowledge-base.md is absent"
reasoning_checkpoint:
  hypothesis: "The five UX symptoms are deterministic omissions. generate() and GapFillRenderer keep span order; the typed input is an unlabeled borderless control under the sentence; graded answers stay editable because submit() bails while Continue replaces Submit; FeedbackStage prints the technical attempt log; sentence text is a raw source slice."
  confirming_evidence:
    - "Browser report on lesson 8530f437-cf76-42ed-a835-b6782381cc26: four choice questions and Start Over keep learning-unit order; empty Answer is unlabeled until focus; post-grade edits do not resubmit; Feedback shows UUID/mode/category; literal asterisks and the double-underscore blank remain. No console errors. Generation a0cc2517 was not edited."
    - "exercise_gap_fill.generate sets chip_unit_ids from units sorted by (start, learning_unit_id). GapFillRenderer maps that array in order. No shuffle symbol exists on that path."
    - "01-14-CONTEXT and 01-14-SUMMARY explicitly defer chip order, typed-field chrome, and the Feedback learning summary. 01-13 prohibitions defer chip shuffle and retry-after-incorrect. Tests lock the current technical Feedback text and the span-ordered chip ids."
  falsification_test: "A shuffle, markdown strip, disabled-after-grade guard, visible Answer label, or Current pass score heading anywhere on the live render path would falsify the unimplemented-behavior claim."
  fix_rationale: "Diagnose only. A fix would add the missing behaviors in the named functions; 01-14 layout CSS is not the cause."
  blind_spots: "Did not re-open the browser or read the SQLite row for generation a0cc2517. The report already states that generation, source, and units were unchanged and that chip order matched learning-unit order on every choice item and after Start Over."
  candidate_causes:
    - "code: render and generate functions omit shuffle, field chrome, post-grade lock, learner summary, and markdown stripping"
    - "data: persisted generation.chip_unit_ids and source slices already contain the stable order and the literal asterisks; Start Over reuses that generation"
  and_gate: "no — five independent omissions. They appear together because the later slices were not built. None is required for the others to show up."
```

## Symptoms

expected: Healthy only after migrations. Lesson appears on / and opens at /lessons/:id. The UAT text does not itself require shuffled chips, a visible typed field, a post-grade lock, a learner Feedback summary, or markdown stripping. The browser report treats those five as remaining UX on a lesson that already opens and practices.
actual: Compose and lesson open were not reported as failed. Browser verification on http://127.0.0.1:5173/lessons/8530f437-cf76-42ed-a835-b6782381cc26 completed with no console errors. Grading, Continue, Start Over, reload restore, full pass, early Exit, saved history, separated passes, collapsed Feedback on entry, and the checked layouts work. Remaining UX — (1) choice options stay in learning-unit order, including after Start Over; (2) empty Answer is nearly invisible until focus, below the sentence, not in the blank; (3) after grading the answer stays editable but Submit is already Continue, the grade stays on the old answer, and nothing says the edit will not be submitted; (4) Feedback is a technical log (session UUID, drag/typed, correct/incorrect, completed/left early) with an accessible Current pass name, no visible Current pass heading, and no short score; (5) literal markdown asterisks from Source show around the blank, and the blank is still a double line rather than one green line.
errors: none in the captured console
reproduction: Open the lesson above, Start Practice, answer the four choice items and the typed items, Start Over, Exit early, and expand Feedback. Confirmed in LAIT_BROWSER_VERIFICATION_2026-10-06.md. 11 attempts were added across 3 sessions. Source, units, and generation were not edited.
started: Present on the running Phase 1 build. 01-14 left these behaviors for later slices. Not a regression of the 01-14 layout work.

## Eliminated

- hypothesis: 01-14 workspace layout CSS broke chip order, the typed field, or Feedback content.
  evidence: 01-14-PLAN prohibits changing GapFillRenderer, FocusPracticeMode internals, chip order, retry, and Feedback row content. 01-14-SUMMARY says chip order, typed-field chrome, and the Feedback learning summary stay in later slices. The browser report says the checked layouts work.
  timestamp: 2026-10-05T21:52:00Z
- hypothesis: A runtime shuffle or markdown renderer failed (bad seed, thrown parser, console error).
  evidence: No shuffle and no practice-sentence markdown parser exist on the path. Captured console had no error or warning. Generation id stayed a0cc2517-e8cb-4725-992a-60762bab3a10.
  timestamp: 2026-10-05T21:52:00Z
- hypothesis: Compose health or lesson open is the UAT failure mechanism.
  evidence: The user did not report that Compose or lesson open failed. The same report records reload, direct URL, and list entry reaching Exercises are ready.
  timestamp: 2026-10-05T21:52:00Z

## Evidence

- timestamp: 2026-10-05T21:49:00Z
  checked: LAIT_BROWSER_VERIFICATION_2026-10-06.md and 01-UAT.md gap G-01-1
  found: Functional practice flows passed. Five UX items were confirmed on lesson 8530f437-cf76-42ed-a835-b6782381cc26. Generation was not regenerated.
  implication: Diagnosis is about current UI behavior, not a failed open or a dirty generation.

- timestamp: 2026-10-05T21:50:00Z
  checked: backend/lait/modules/exercise_gap_fill/generate.py generate and _item_for; backend/tests/modules/exercise_gap_fill/test_generate.py test_generate_exposes_chip_candidate_unit_ids
  found: generate sorts accepted units by (start, learning_unit_id) and sets chip_unit_ids to that id tuple. _item_for copies source[window_start:unit.start] and source[unit.end:window_end] into PromptSegment text and sets the blank segment to BLANK = "______". The test expects chip_unit_ids == ("responsible", "rolling"), which is span order.
  implication: Choice order is the persisted learning-unit order. Asterisks in Source are copied into sentence segments. Nothing strips emphasis markers.

- timestamp: 2026-10-05T21:51:00Z
  checked: exercise_generate._definitions_for, practice_get.view_for, practice_start.handle, practice_start_over.handle, practice router _current_response
  found: chip ids are stored in generator order with only a duplicate filter. view_for copies generation.chip_unit_ids onto every current item. Start Over abandons the open session and calls start_practice, which reuses latest_completed_generation when the accepted set matches. The HTTP DTO forwards chip_unit_ids and segment text unchanged.
  implication: Start Over cannot reshuffle. The same generation row is what the report left untouched.

- timestamp: 2026-10-05T21:51:00Z
  checked: frontend/src/registries/renderers/GapFillRenderer.tsx and GapFillRenderer.module.css
  found: Chip bank is item.chip_unit_ids.map into ChipButton with no sort. The typed control is an input.answer with only aria-label="Answer", rendered after the sentence paragraph, not inside the blank span. .answer sets border: 0 and background var(--color-dominant). .blank is display:inline with border-bottom: 2px solid var(--color-accent) around the text "______". submit() returns immediately when feedback is set. The Submit button is replaced by Continue when feedback is set. ChipButton and the input stay enabled and keep updating draft/selectedUnitId. FeedbackCard keeps showing the already returned grade.
  implication: Symptoms 1, 2, 3, and the double-line blank are this render path. There is no retry and no copy that a new edit will not be submitted.

- timestamp: 2026-10-05T21:52:00Z
  checked: frontend/src/features/lesson/stages/FeedbackStage.tsx and FeedbackStage.test.tsx; domain/lesson.py suggest_title
  found: FeedbackStage renders section aria-label="Current pass" with passLabel (completed / left early / abandoned / open), the raw session id, and AttemptRows of mode, category, and explanation. Only Earlier passes has an h3. No score such as correct/total is computed. The test expects the region to contain the session id and the mode string "typed", and looks up "Current pass" by accessible name only. suggest_title strips a leading heading marker for the lesson title only. It is not called for practice segments.
  implication: Symptom 4 is the implemented technical log. A learner heading and score were never rendered. Asterisks are not a broken title stripper.

- timestamp: 2026-10-05T21:53:00Z
  checked: 01-13-PLAN prohibitions, 01-14-PLAN, 01-14-CONTEXT, 01-14-SUMMARY, STATE.md deferred UX row
  found: 01-13 says do not implement chip shuffle or retry-after-incorrect. 01-14 says do not change GapFillRenderer, chip order, retry, or Feedback row content, and carries the technical-log summary into a later slice. STATE records that summary as deferred on 2026-10-02, not a 01-14 blocker.
  implication: Chip order, typed-field visibility, and the learner-facing Feedback summary are unimplemented later slices, not regressions of 01-14 layout work. Post-grade editability is the same class of omission (retry and a lock were out of scope). The single green blank line was a separate wish and is also unimplemented.

## Resolution

root_cause: "Five separate unimplemented behaviors, not a 01-14 regression and not a failed lesson open. (1) Choice order is learning-unit span order because exercise_gap_fill.generate sorts units by (start, learning_unit_id) and stores that as chip_unit_ids, practice_get.view_for copies generation.chip_unit_ids onto the current item, practice.start_over reuses the same completed generation, and GapFillRenderer maps item.chip_unit_ids in that order with no shuffle. (2) The empty typed answer is nearly invisible because GapFillRenderer renders a borderless input (GapFillRenderer.module.css .answer { border: 0 }) with only aria-label Answer, after the sentence, not inside the blank. (3) After grading, submit() returns when feedback is set and the Submit button is replaced by Continue, while ChipButton and the typed input stay enabled, so a new edit cannot be submitted and nothing tells the learner that; FeedbackCard keeps the original grade. (4) FeedbackStage renders a technical log: passLabel, the session UUID, and AttemptRows of mode, category, and explanation. Current pass is only an aria-label; Earlier passes is the only visible heading; no correct/total score is computed. (5) _item_for copies the source window into text segments with no markdown strip, and GapFillRenderer prints segment.text as text, so Source asterisks stay literal. The blank is still BLANK \"______\" plus .blank border-bottom 2px; a single green line was never implemented. suggest_title strips a heading marker for the title only. Chip order, typed-field chrome, and the learner Feedback summary were explicitly deferred past 01-14."
fix: ""
verification: "Code-path diagnosis only. Application code was not changed. Browser re-check was not repeated; the 2026-10-06 report is the observed behavior."
files_changed: []
oracle_type: specified
---
