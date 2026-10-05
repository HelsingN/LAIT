# Conventions

## Manual UI verification

Source: `docs/governance/MANUAL_UI_VERIFICATION.md`.

`workflow.human_verify_mode` is `mid-flight`.

A plan that creates or substantially changes learner-visible UI, navigation, interaction state, or persistence/reopen behavior ends with one `<task type="checkpoint:human-verify" gate="blocking-human">`. Vitest and pytest do not close it. The check runs on the Docker Compose app (`http://127.0.0.1:5173`), volume kept. Rebuild the serving image without deleting the volume when it does not contain the change.

Stateful plans include the applicable rows: page reload, direct URL navigation, return from the Lesson List, browser restart, Docker/app restart without deleting the volume.

Do not start the next wave that depends on that plan until the user replies `approved`.

Backend-only plans do not get this checkpoint.

Before `phase.complete`, run one manual learner-flow smoke on Docker for that phase's learner-visible success criteria. Put that smoke in the phase `*-VALIDATION.md` Manual-Only table.

After the checkpoint, classify each observation as bug, UX debt, visual, workflow, or deferred, and propose the phase. Do not treat the note as a blocker or as `approved` unless the user says so.
