## Deferred Items

- Lesson list copy assertion still looks in LessonListPage.tsx
  status: open
  **What:** `test_lesson_list_ui_locks_copy_and_self_hosted_fonts` expects the string "Create Lesson" in `LessonListPage.tsx`. The button copy lives in `CreateLessonForm.tsx`. This failed before plan 01-08 and was not changed here.
- Lesson feature source scan includes test files
  status: open
  **What:** `test_lesson_feature_does_not_call_module_registry_describe` reads every `.ts`/`.tsx` under `frontend/src/features/lesson`, including tests that mention `/api/module-registry` as a negative assertion. This failed before plan 01-08.
