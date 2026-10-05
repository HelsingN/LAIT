---
quick_id: 261005-sqr
date: 2026-10-05
status: planned
---

# UX-21: selection hint on the inactive Add button

Separate quick task. Do not reopen plan 01-14. Do not close Phase 1. Do not commit or push.

The line `Select text in the source before adding a unit.` under Add Learning Unit is removed.

When no source text is selected and units are not locked:

- The button stays in the tab order and creates nothing on click, Enter, or Space.
- The full sentence is a tooltip on hover and on keyboard focus.
- The tooltip is absolutely positioned and does not move the unit list.
- Escape hides it until the pointer leaves or focus returns.

When a selection exists, the button is active and the tooltip is not rendered. The frozen-practice line stays as it is. The empty-list sentence stays as it is.
