# 01-18 checkpoint revision — approved scope decision, not behavior approval

Authority: the user's checkpoint observations on 2026-10-07 explicitly say **not approved** and authorize plan/check changes and implementation before repeating the checkpoint. This supersedes D-24–D-26 and D-30 only where the learner presentation/content acceptance conflicts. D-27–D-29/D-31 preservation, identity, regression and blocking-human gates remain binding. Historical 01-17 context and first-checkpoint evidence are retained.

<decisions>
- **D-32:** Phase 1 content narrowing. Remove Details and technical Chunks used/missed labels from the focus result. Detailed educational explanation, target-chunk analysis and optional alternative presentation are deferred to Phase 5's feedback design. Do not add LLM evaluation or new templated explanations in Phase 1. The original full EVAL-05 requirement remains unchecked and is **partially delivered / remaining content deferred**, not implemented in full by this amendment.

- **D-33:** Accepted result in context. For Correct/Corrected, fill the single current blank with the accepted reference phrase (`feedback.expected`) and highlight it green, using the existing accent token. Keep the result category visible as text. Do not repeat the answer in a separate feedback card or keep a duplicate input/chip bank after grading. Submitted raw text remains stored, not overwritten by the reference.

- **D-34:** Incorrect/reveal/retry. For Incorrect, show the submitted response in the blank without exposing the solution. Show answer replaces that inline response with the reference, while category stays Incorrect and gives no recall credit. Try again remains available both before and after reveal; it clears the blank/result and restores answer entry for the same item. Show answer is parameterless and presentation-only. Existing retry rounds, Continue, opening score, corrected exclusion, Start Over and Exit are frozen.

- **D-35:** Preserve durable data and restore safeguards. Do not roll back 01-17/01-18 persistence, complete saved-payload mapping, strict missing-field validation, full item/attempt/copy binding, pending success/final-success restoration, reveal records or late-response guards. Restore actual saved feedback; hidden educational content is deferred UI, never fabricated empty arrays/null in the data path. Historical explanations/chunks/alternatives remain recoverable unmodified through public reads.

- **D-36:** Verification scope and gate. Retarget automatic assertions to inline accepted/wrong/revealed/retry states, no Details/card/input duplication, exact restore, real payload forwarding, stale-reveal/late-response rejection and unchanged domain interactions. Keep saved rich-payload/repository/HTTP tests. Repeat the sole final blocking-human checkpoint on Docker, volume kept, with reload, direct URL, Lesson List return, genuine browser-process restart and Docker/app restart for all four result states. Phase-close smoke is separate; no commit, push or phase closure.

- **D-37:** Future compound exercise. Record a single shared task with multiple blanks and actual drag-and-drop as a future exercise/interaction design follow-up, proposed Phase 4 (with Phase 9 responsive validation). Do not implement it, add endpoints/dependencies or change the existing one-item queue/chip-selection mode now.
</decisions>

## Observation classification

| Observation | Class | Owner/disposition |
| --- | --- | --- |
| Remove Details/technical chunk labels; inline success; no duplicate input/card | UX debt + approved design revision | Phase 1, revised 01-18 |
| Hidden miss, inline Show answer, clearing Try again after reveal | workflow/design revision | Phase 1, revised 01-18; frozen domain rules |
| Detailed teaching/chunk analysis is no longer required for Phase 1 acceptance | deferred, explicit scope narrowing | Phase 5 feedback design; original EVAL-05 remains incomplete |
| Durable restore fixes must stay | bug-prevention invariant | Phase 1, regression gate; not rolled back |
| Shared multi-blank task and true drag-and-drop | deferred | Proposed Phase 4/9 follow-up; no current implementation |

The user's design approval is not T3 approval. No first-checkpoint route or new behavior is marked passed by these notes.
