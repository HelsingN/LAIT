# Manual UI Verification

Execution rule for learner-visible work. It applies to every future phase plan. Already-executed plans are not rewritten.

Backend-only plans do not get an extra human-verify checkpoint.

## What makes a plan in scope

The plan creates or substantially changes any of:

- learner-visible UI
- navigation
- interaction state
- persistence or reopen behavior

Copy, comments, and token-only edits are out of scope. A plan that does not change those surfaces is backend-only for this rule, even if it is in the same phase as UI work.

## Checkpoint

An in-scope plan ends with one task, and no earlier human-verify task:

```xml
<task type="checkpoint:human-verify" gate="blocking-human">
  <what-built>What the Docker-served app now does.</what-built>
  <how-to-verify>
    Use the running Docker Compose application (web http://127.0.0.1:5173, API http://127.0.0.1:8000/health).
    Rebuild the affected service without deleting the volume when the running image does not contain the change.
    Do not treat the Vite dev server, Vitest, or pytest as this check.
    Steps the learner actually performs, then the expected screen and persisted result.
  </how-to-verify>
  <resume-signal>Reply approved, or send observations to classify. Observations are not approval and are not automatic blockers.</resume-signal>
</task>
```

`gate="blocking-human"` is required. `gate="blocking"` is auto-approved when an unattended chain is on, and this project runs with `mode: yolo`. The checkpoint exists so the next dependent UI wave cannot start without an explicit `approved`.

`workflow.human_verify_mode` is `mid-flight` so the planner emits this task and execution stops on it. Do not replace it with only a `<verify><human-check>` block. Vitest and pytest stay in `<automated>`. A green automated command does not close the checkpoint.

## Docker application

The human performs the check on the Compose stack:

- `docker compose up -d --wait` when the stack is not already up
- do not remove the named volume
- if the edit is not in the image currently serving port 5173, rebuild that service without `-v`

## Stateful checks

When the plan touches navigation, interaction state, or persistence/reopen, `how-to-verify` includes every row that applies:

| Check | What must hold |
| --- | --- |
| Page reload | The same lesson route still shows the persisted learner-visible state. |
| Direct navigation by URL | Opening `/lessons/:id` in a fresh load shows that state without create-flow React state. |
| Return from the Lesson List | Opening the lesson from `/` shows the same state. |
| Browser restart | The state survives a new browser session (server data, not a tab-only cache). |
| Docker/app restart without deleting the volume | After `docker compose restart` or a recreate that keeps the volume, the state is still there. |

Omit a row only when that surface is not part of the change, and say so in the checkpoint.

## Wave gate

Do not start a later wave that depends on an in-scope plan until the user replies `approved` to that plan's checkpoint.

A backend-only plan does not gain this checkpoint because it happens to follow a UI plan.

## Phase-close smoke

Before `phase.complete`, run one manual learner-flow smoke on the Docker app. Cover that phase's learner-visible success criteria, including reload and a Docker/app restart that keeps the volume.

Per-plan checkpoints do not replace the smoke. Automated suites do not replace the smoke. Record the smoke as a Manual-Only row in the phase `*-VALIDATION.md`.

## Observations are not automatic blockers

After a checkpoint, classify each user observation before opening a gap, reverting requirements, or treating the note as a failed check.

| Class | Meaning | Default phase |
| --- | --- | --- |
| bug | Behavior contradicts the plan contract or persisted data. | Current phase if it breaks the checkpoint's expected result. Otherwise name the phase. |
| UX debt | The flow works and is clumsy. | A later phase. |
| visual | Spacing, type, color, wrap, or truncation that does not block the action under test. | A later phase, usually the responsive-release phase, unless it hides the action. |
| workflow | The sequence or the check procedure, not a broken feature. | Name the phase or the governance doc. |
| deferred | Outside the current phase scope. | The phase that already owns that scope. |

Propose the phase in the same reply. Do not start a fix from the classification alone.

`approved` is the only resume that lets the next dependent UI wave start. A classified note is not `approved`. A classified note is also not a blocker until the user says that item blocks approval.
