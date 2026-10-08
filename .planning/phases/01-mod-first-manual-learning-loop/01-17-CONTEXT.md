# Phase 01 EVAL-05 gap closure — approved feedback contract

Captured: 2026-10-07. Source: the user's explicit `gsd-plan-phase 01 --gaps` instruction. Status: approved input for planning; implementation and human verification are pending.

<domain>
Close the remaining EVAL-05 feedback gap through a compact in-session card, expandable Details, and faithful restoration of saved attempt feedback. Phase 01 stays open. PLAT-09 is already verified; any client regeneration needed for additional attempt DTO fields is contract maintenance, not a new PLAT-09 gap.
</domain>

<decisions>
## Locked decisions for this closure

- **D-24:** Render the learner's submitted answer once for every result, including correct, incorrect, and corrected. Details must not repeat the submitted answer or reference as an explanation template. Preserve the submitted text verbatim in storage and its primary display.
- **D-25:** After an incorrect result, withhold the correct/reference answer until Show answer or a later self-produced correct/corrected answer for the current target. Opening Details alone must not reveal the solution. The primary answer and reference may have the same value after a correct answer; avoid printing the same phrase twice.
- **D-26:** Details is collapsed initially and keyboard-accessible. It contains a concise meaningful deterministic explanation and the actual target chunks used or missed; solution-bearing explanation, chunk text, and a non-null natural alternative share the same disclosure gate as the reference. Before disclosure, explain the result safely without leaking the target. Hide an absent natural alternative; do not invent one.
- **D-27:** Read restored feedback from saved attempts through the persistence, domain/application query, HTTP DTO, generated client, and renderer boundaries. Preserve real chunks_used/chunks_missed, explanation, and optional natural alternative. Empty arrays are valid only when that saved result actually has empty arrays; never synthesize them to disguise missing saved data.
- **D-28:** Bind restored feedback/disclosure to the correct attempt and current practice item, including repeat copies of the same learning-unit id and mode. Page reload, direct URL entry, return from Lesson List, actual browser-process restart, and Docker/app restart with the named volume kept must preserve the saved feedback. No restored incorrect card may reveal a solution merely because stale client state belonged to another item. The plan must specify an explicit restore rule for Show answer and cover it with tests.
- **D-29:** Existing same-session retry rounds, corrected semantics, opening-pass score denominator, Continue advancement, Start Over, and Exit behavior are frozen. Feedback disclosure is presentation state; it cannot rewrite attempts, turn a revealed answer into independent recall, advance the queue, or change the score.
- **D-30:** Interpret EVAL-05 and Phase 01 success criterion 3 as full learning feedback available within the session under D-24–D-28, including user-requested Details and delayed solution disclosure. Preserve every educational field and make it recoverable. This supersedes only older immediate/reference-and-explanation copy assumptions such as D-18; it does not weaken the required learning content or count missing content as passing.
- **D-31:** Plan automated behavioral checks for disclosure, answer de-duplication, saved-data round trips, correct restored-attempt identity, and unchanged retry/score/Exit. Every learner-visible plan ends in exactly one `checkpoint:human-verify` with `gate="blocking-human"`, on Docker at http://127.0.0.1:5173. Include every D-28 entry/restart route and rebuild changed images without removing the volume. Record a separate phase-close learner-flow smoke as pending in VALIDATION; a plan checkpoint alone does not close Phase 01.
</decisions>

<constraints>
This turn authorizes planning and plan checking only. No implementation, application-source/test edits, running the planned Docker workflow, commit, push, phase completion, or execution auto-advance. Preserve existing uncommitted work and executed plans 01-01 through 01-16. Add the smallest executable closure plan set beginning at 01-17, referencing this approved contract explicitly.
</constraints>

<canonical_refs>
- `.planning/phases/01-mod-first-manual-learning-loop/01-CONTEXT.md` — original D-01–D-23; retained except the narrow disclosure/copy supersession above.
- `.planning/phases/01-mod-first-manual-learning-loop/01-16-PLAN.md` and `01-16-SUMMARY.md` — retry, corrected, score, Continue and Exit baseline.
- `.planning/phases/01-mod-first-manual-learning-loop/01-VERIFICATION.md` — latest 3/5 report; one feedback implementation gap remains; PLAT-09 closed.
- `.planning/REQUIREMENTS.md` and `.planning/ROADMAP.md` — preserve the educational payload and all other phase commitments.
- `docs/governance/MANUAL_UI_VERIFICATION.md` — blocking Docker checkpoint and separate phase-close smoke.
</canonical_refs>
