# Plan 01-14 discussion

This file does not replace `01-CONTEXT.md`. Phase 1 decisions D-01 through D-23 stay in force.

## Locked by the user for this slice

- Wide workspace: Source beside a compact Learning Units list.
- Source, the unit list, and the main actions fit the window height. A fixed `52vh` pane is not the rule. The preparation area takes the height left after the header and the action cluster.
- Each selected phrase is shown once in the unit list.
- The selected unit shows a compact ×. The button's accessible name is `Remove {phrase}`. That sentence is not the visible label.
- Add Learning Unit stays visible on a wide screen while the unit list scrolls, and on a narrow screen as well.
- Collapsed sections show that they open and close.
- After a successful generation, the next step is practice, not a raw `completed` status and a second generate as the primary action.
- Practice renderer, Focus Practice, and Feedback content are out of this slice.
- Carry forward, do not design here: Feedback still looks like a technical log. A later slice needs a learner-facing summary (visible pass title, completed versus left early in plain language, choice versus recall, hard phrases, next step). UUID and mode names must not be the main information. That note is not a blocker of 01-13 and is not scope for 01-14.

## Proposed layout, shown in the sketch

Sketch: `.planning/sketches/01-14-workspace-layout.html`.

- Lesson List stays a narrow column. Only the lesson workspace widens.
- The workspace is a `100dvh` column, max-width 1120px, `overflow: hidden`. The preparation slot is `flex: 1 1 0`. From 960px its track is `minmax(188px, 1fr)`. Below 960px the tracks are source `minmax(88px, 1fr)` and units `minmax(232px, 1fr)`. Those narrow minima sum to 332px, which fits the measured 354px at 959×700. Two `12rem` tracks do not.
- Source and the unit list scroll inside the panes. `minmax(min-content, 1fr)` is withdrawn.
- Actions are capped with `calc(100dvh - 188px - 102px)` from 960px and `calc(100dvh - 332px - 102px)` below that.
- On a short window, Feedback does not keep a 26px body. While it is open and the viewport cannot also hold a 160px Feedback body, the Feedback panel covers the preparation slot. Preparation stays mounted, so the text range and the source and unit scroll positions remain. Closing Feedback uncovers the same panes. From 960px the test is `max-height: 693px`. Below 960px it is `max-height: 837px`. A taller window keeps preparation and Feedback together.
- The base layout stacks the panes. Side by side (`minmax(0, 1fr)` and `320px`) starts at `min-width: 960px`. A fractional width between 959 and 960, which happens at 125% display scaling, stays stacked and uses the narrow height test.
- Add Learning Unit sits in the units pane, above the scrolling list, on both sides of the 960px threshold. It is not inside the list scroller.
- If the viewport is so short that the header, the preparation floor, and the action cluster cannot all fit while Feedback is collapsed, the exercise-type list scrolls inside Exercises. Add, the ready line, and Start Practice stay reserved.
- A unit row is the phrase once. Draft still has Accept. Accepted does not print a status line. Selecting a row shows a 28px × button. Its accessible name is `Remove {phrase}`. The visible control is the cross.
- Every stage header is a button with a chevron and `aria-expanded`. The generate section is labeled Exercises. Its inner button stays Generate Exercises. Those two strings are not the same control.
- When `exercise.latest_completed` is restorable, or generate just succeeded for the current accepted set, the Exercises section shows "Exercises are ready" and Practice is expanded with Start Practice visible. Generate Exercises is not the primary action for an unchanged set. A changed accepted set still offers Generate Exercises. Failure copy is unchanged.
- Practice and Feedback keep their current inner UI, including the technical log. They only receive the same chevron header as the other sections.

## Not decided here

- Drag and drop (UX-11).
- Chip order, typed-field chrome, retry after incorrect, Start Over cancel, and the Feedback learning summary. Those stay in later slices.
