---
status: complete
phase: 01-mod-first-manual-learning-loop
source: [01-01-SUMMARY.md, 01-02-SUMMARY.md, 01-03-SUMMARY.md, 01-04-SUMMARY.md, 01-05-SUMMARY.md, 01-06-SUMMARY.md, 01-07-SUMMARY.md, 01-08-SUMMARY.md, 01-09-SUMMARY.md, 01-10-SUMMARY.md, 01-11-SUMMARY.md, 01-12-SUMMARY.md, 01-13-SUMMARY.md, 01-14-SUMMARY.md, 01-15-SUMMARY.md, 01-16-SUMMARY.md, 01-17-SUMMARY.md, 01-18-SUMMARY.md]
started: 2026-10-07T02:45:49Z
updated: 2026-10-08T01:33:10Z
completed: 2026-10-08T01:33:10Z
session_id: 01-20261007-full-phase
gap_id_namespace: G-01-20261007
---

## Current Test

[testing complete]

## Tests

### 1. Запуск Docker с сохранёнными данными

expected: |
  В каталоге D:\Helsing\gitHub\LAIT выполните docker compose restart api web, не удаляя volume. После запуска откройте http://127.0.0.1:5173. Список уроков загружается без ошибки, ранее сохранённый урок открывается, его Source и learning units не потеряны. Не используйте docker compose down -v и не очищайте SQLite.
result: pass
reported: "pass"
evidence_source: user report; Docker restart/retained-data UI not independently observed by assistant.
source: human
coverage_id: cold-start, 01-10:D1
rationale: Safe service cold start: recreate process state, never erase durable learner data. This is not a new empty-volume test.

### 2. Создание и открытие урока

expected: |
  Создайте отдельный урок для этой проверки с названием Phase 1 UAT и Source: «I can **break down** complex tasks. I follow up with clients. I keep track of project risks. 👍». Урок появляется в списке; открытие по его ссылке показывает ровно сохранённый Source, включая ** и 👍. Исходные уроки не изменяйте.
result: pass
reported: "pass"
evidence_source: user report; create/list/open not independently observed by assistant.
source: human
coverage_id: 01-01:D4
rationale: Check the create/list/open journey on the Docker app. Existing nonempty volume is intentionally retained; historical empty-list coverage stays in 01-01.

### 3. Ручной выбор и принятие learning units

expected: |
  В новом уроке выделите break down, follow up и keep track, добавьте три learning units и примите их. Выделение и текст совпадают с Source, включая корректную работу рядом с Unicode; Source не переписывается. До практики можно удалить только тестовый draft и добавить его снова; принятие и список не теряются после reload.
result: pass
reported: "pass"
evidence_source: user report; selection, acceptance and reload not independently observed by assistant.
source: human
coverage_id: manual-unit-journey, 01-03, 01-06
rationale: Add a user-observable source-to-reviewed-units step to the automated unit/selection coverage.

### 4. Генерация и начало практики

expected: |
  Сгенерируйте Gap Fill по трём принятым units. Статус ready и Start Practice доступны; в выборе нет maintainer proof-модуля. Start Practice открывает практику без повторной генерации; исходный урок и units остаются теми же. Для нескольких units идут выбор вариантов, затем ввод; отдельный урок с одним принятым unit даёт только ввод.
result: pass
reported: "pass"
evidence_source: user report; generation and practice start not independently observed by assistant.
source: human
coverage_id: generation-journey, 01-05, 01-06, 01-07:D1
rationale: Exercise discovery and generation through the learner UI, not only transport/unit assertions.

### 5. Порядок вариантов и Start Over

expected: |
  В режиме выбора порядок вариантов не воспроизводит систематически порядок Source. Запомните порядок: reload сохраняет его. Start Over с подтверждением создаёт новый проход с новым порядком (при случайном совпадении повторите один раз), без прежнего выбранного ответа; отмена подтверждения ничего не меняет. Выбор правильной фразы оценивается по её unit, не позиции.
result: pass
reported: "pass"
evidence_source: user report; chip order, reload and Start Over not independently observed by assistant.
source: human
coverage_id: 01-15:D1
rationale: The user approved the Docker checkpoint on 2026-10-06. A real browser-process restart was not performed.

### 6. Ввод, контекст и Correct

expected: |
  В typed-задании видно, куда вводить ответ. Введите правильную фразу с другим регистром и пробелами по краям: Correct подставляет принятую фразу зелёным в единственный пропуск. Нет отдельной карточки ответа, дублирующего input или активного банка вариантов после оценки. В предложении нет буквальных ** из Source и двойного подчёркивания; Source при этом неизменён.
result: pass
reported: "pass"
evidence_source: user report; typed input and inline Correct not independently observed by assistant.
source: human
coverage_id: 01-15:D2
rationale: D-33 supersedes the historical disabled-input/card wording: controls are removed after grading, accepted phrase is inline.

### 7. Incorrect, Show answer, Try again и Corrected

expected: |
  Отправьте ошибочный ответ: в пропуске только ваш ответ, решение скрыто. Show answer заменяет его правильной фразой в пропуске, но категория остаётся Incorrect и балл не начисляется. Try again до и после раскрытия очищает результат и ответ, возвращая ввод для того же задания. Самостоятельное исправление даёт Corrected и зелёную принятую фразу один раз. Details, Chunks used/missed и повторяющей ответ карточки нет.
result: pass
reported: "pass"
evidence_source: user report; Incorrect, reveal, Try again and Corrected not independently observed by assistant.
source: human
coverage_id: 01-18:D1
rationale: Docker learner-visible states and 320px wrap require human judgment; user explicitly approved R2 without observations.

### 8. Повторные раунды и Continue

expected: |
  Оставьте одно ошибочное задание неисправленным и перейдите Continue, другое исправьте самостоятельно. На конце прохода Continue начинает новый раунд только с ещё неисправленными парами unit + mode в той же сессии; Corrected больше не включается. После исправления последнего оставшегося задания Continue завершает практику без нового пустого раунда.
result: pass
reported: "pass"
evidence_source: user report; retry rounds and Continue not independently observed by assistant.
source: human
coverage_id: 01-16:D1
rationale: The user approved the Docker checkpoint on 2026-10-06 after the repeat-copy cursor fix. A real browser-process restart was not performed.

### 9. Счёт первого прохода

expected: |
  Для трёх units исходный полный проход содержит шесть заданий. Проверьте итоговый счёт в Feedback: числитель — только правильные ответы с первой попытки, знаменатель остаётся 6. Corrected и Show answer не добавляют recall-балл; повторные попытки и раунды не меняют знаменатель на 7, 8 и далее. Категории показаны понятными labels, не UUID/техническим логом.
result: pass
reported: "Функционально pass, но мне не нравится как визуально выглядит раздел feedback"
evidence_source: user reports functional pass; visual preference not independently observed by assistant.
observation_id: O-01-9-visual
source: human
coverage_id: 01-16:D2
rationale: The user approved the Docker checkpoint on 2026-10-06. History still prints the expected phrase twice; that is deferred UX debt.

### 10. Полное завершение и досрочный Exit

expected: |
  После полного завершения вы возвращаетесь в workspace; история и Source сохранены, units снова редактируемы. Начните ещё одну тестовую практику и выйдите через Exit раньше конца: сохраняются уже отправленные попытки, workspace возвращается, units разблокированы. Открытие урока снова не возобновляет закрытую сессию и не стирает историю.
result: pass
reported: "pass"
prior_reported: "10 после выполнения нескольких заданий и выхода через exit новый Start Practice начинает все заново с первого задания"
confirmed_at: 2026-10-08T01:29:19Z
evidence_source: user report; completion, retained history/source and editable units after Exit not independently observed by assistant.
observation_id: O-01-10-exit
triage: Restart after Exit matches the close-not-pause contract; user subsequently confirmed the full Test 10 expectation with pass.
source: human
coverage_id: 01-13:D3
rationale: The user approved only this plan's six-scenario checkpoint. That approval does not close Phase 1.

### 11. Неизменность управления практикой

expected: |
  Проверьте вместе: Continue переводит к следующему заданию без лишней оценки; Show answer не создаёт попытку и не двигает очередь; Try again не начинает новую сессию; Start Over требует подтверждения, сбрасывает текущий проход, но сохраняет прежнюю историю; Exit остаётся существующим завершением сессии. Во время открытой практики принятый набор units заморожен.
result: pass
reported: "pass"
confirmed_at: 2026-10-08T01:30:32Z
evidence_source: user report; practice controls and frozen units not independently observed by assistant.
source: human
coverage_id: 01-18:D3
rationale: User approved the R2 checklist including frozen learner workflow; this is not phase-wide smoke approval.

### 12. Восстановление четырёх состояний после пяти способов открытия

expected: |
  Для состояний Correct, Corrected, Incorrect до Show answer и Incorrect после Show answer проверьте: reload; прямой URL урока; возврат из Lesson List; полное закрытие и повторный запуск браузера (не только вкладки); docker compose restart api web с тем же volume. В каждом случае сохраняются именно текущие задание, фраза, категория, скрытое/раскрытое решение, очередь и счёт; финальный успех не превращается в пустой ввод. После Try again и перехода Continue чужое/старое раскрытие не возвращается. Сохранённые payload проверяются отдельно автоматически: отсутствие Details не означает пустые chunks.
result: pass
reported: "pass"
confirmed_at: 2026-10-08T01:31:18Z
evidence_source: user report; four-state restoration across five opening/restart routes not independently observed by assistant.
source: human
coverage_id: 01-18:D2
rationale: Published four-state/five-route checklist approved by user report; automated payload digest independently proves data preservation, not visual restoration.

### 13. Узкий экран 320 px

expected: |
  На ширине 320 px предложение переносится, единственный пропуск остаётся внутри предложения. Ошибочный, раскрытый и зелёный правильный ответ не создают горизонтальную прокрутку страницы; доступные действия не обрезаны. Варианты прокручиваются внутри своего банка до оценки.
result: pass
reported: "pass"
confirmed_at: 2026-10-08T01:32:04Z
evidence_source: user report; 320px wrapping, overflow and available actions not independently observed by assistant.
source: human
coverage_id: 01-07:D5
rationale: Vitest asserts inline blank, overflow-wrap, and overflow-x hidden in CSS. A 320px browser viewport was not opened.

### 14. Workspace, Feedback и возврат к подготовке

expected: |
  На коротком окне раскройте workspace Feedback: он использует предусмотренный overlay; закрытие возвращает Source, units, выделение и scroll без потери. На 1280×800 рядом с прокручиваемой историей остаются видны заголовок Exercises и ready. При повторном входе в урок Feedback свёрнут; раскрытие показывает сохранённые проходы и счёт, а ссылка на unit возвращает к исходному фрагменту.
result: pass
reported: "pass"
confirmed_at: 2026-10-08T01:33:10Z
evidence_source: user report; workspace overlay, reopen/history and unit navigation not independently observed by assistant.
source: human
coverage_id: 01-14:D3
rationale: The user approved only this plan's three-scenario checkpoint on 2026-10-05. UX-20 did not reproduce. That approval does not close Phase 1.

### 15. lesson.create persists an exact UTF-8 paste, rejects empty or oversized source, and mints a distinct id per call

expected: lesson.create persists an exact UTF-8 paste, rejects empty or oversized source, and mints a distinct id per call
result: pass
source: automated
coverage_id: 01-01:D1
requirement: LESS-01
verification_refs: ["backend/tests/application/test_lesson_create.py#test_lesson_create_persists_exact_utf8_source","backend/tests/application/test_lesson_create.py#test_whitespace_only_source_writes_no_row","backend/tests/application/test_lesson_create.py#test_same_paste_twice_creates_distinct_immutable_ids"]
evidence_scope: Recorded passing SUMMARY coverage; latest regression evidence is the pre-commit 129 backend / 105 frontend / typecheck pass, not a new human observation.

### 16. lesson.list and lesson.get round-trip stored lessons, ordered by created_at descending then id

expected: lesson.list and lesson.get round-trip stored lessons, ordered by created_at descending then id
result: pass
source: automated
coverage_id: 01-01:D2
requirement: LESS-02
verification_refs: ["backend/tests/application/test_lesson_list.py#test_lesson_list_and_get_round_trip","backend/tests/application/test_lesson_create.py#test_list_orders_by_created_at_desc_then_id"]
evidence_scope: Recorded passing SUMMARY coverage; latest regression evidence is the pre-commit 129 backend / 105 frontend / typecheck pass, not a new human observation.

### 17. HTTP POST/GET map DTOs onto the handlers and do not call the persistence package

expected: HTTP POST/GET map DTOs onto the handlers and do not call the persistence package
result: pass
source: automated
coverage_id: 01-01:D3
requirement: MODL-12
verification_refs: ["backend/tests/application/test_lesson_create.py#test_http_maps_create_dto_and_rejects_empty_source","backend/tests/application/test_lesson_list.py#test_http_routers_delegate_to_handlers_not_repositories","backend/tests/application/test_lesson_create.py#test_application_handlers_do_not_import_fastapi_or_sqlalchemy"]
evidence_scope: Recorded passing SUMMARY coverage; latest regression evidence is the pre-commit 129 backend / 105 frontend / typecheck pass, not a new human observation.

### 18. Invalid, duplicate, empty, API-incompatible, and unresolved catalogs refuse startup; experimental visibility is rejected

expected: Invalid, duplicate, empty, API-incompatible, and unresolved catalogs refuse startup; experimental visibility is rejected
result: pass
source: automated
coverage_id: 01-02:D1
requirement: MODL-01
verification_refs: ["backend/tests/catalog/test_startup_validation.py#test_visibility_on_universal_manifest_refuses_startup","backend/tests/catalog/test_startup_validation.py#test_duplicate_module_id_refuses_startup","backend/tests/catalog/test_startup_validation.py#test_unresolved_dependency_refuses_startup","backend/tests/catalog/test_startup_validation.py#test_empty_catalog_refuses_startup","backend/tests/catalog/test_startup_validation.py#test_api_incompatible_manifest_refuses_startup","backend/tests/catalog/test_startup_validation.py#test_missing_exercise_type_refuses_startup","backend/tests/catalog/test_startup_validation.py#test_experimental_visibility_is_rejected"]
evidence_scope: Recorded passing SUMMARY coverage; latest regression evidence is the pre-commit 129 backend / 105 frontend / typecheck pass, not a new human observation.

### 19. module_registry.describe returns Gap Fill and proof with the public field set and activation_status active

expected: module_registry.describe returns Gap Fill and proof with the public field set and activation_status active
result: pass
source: automated
coverage_id: 01-02:D2
requirement: MODL-02
verification_refs: ["backend/tests/catalog/test_describe.py#test_describe_returns_public_active_rows","backend/tests/catalog/test_describe.py#test_http_module_registry_maps_describe"]
evidence_scope: Recorded passing SUMMARY coverage; latest regression evidence is the pre-commit 129 backend / 105 frontend / typecheck pass, not a new human observation.

### 20. list_visible_for(learner) returns Gap Fill and omits the maintainer proof contribution

expected: list_visible_for(learner) returns Gap Fill and omits the maintainer proof contribution
result: pass
source: automated
coverage_id: 01-02:D3
requirement: MODL-03
verification_refs: ["backend/tests/catalog/test_list_visible_for.py#test_learner_list_includes_gap_fill_and_omits_proof","backend/tests/catalog/test_list_visible_for.py#test_http_exercise_registry_learner_returns_gap_fill_only"]
evidence_scope: Recorded passing SUMMARY coverage; latest regression evidence is the pre-commit 129 backend / 105 frontend / typecheck pass, not a new human observation.

### 21. Universal manifests have no visibility field; lesson feature code does not call describe

expected: Universal manifests have no visibility field; lesson feature code does not call describe
result: pass
source: automated
coverage_id: 01-02:D4
requirement: MODL-02
verification_refs: ["backend/tests/catalog/test_startup_validation.py#test_universal_manifests_and_schema_omit_visibility","backend/tests/catalog/test_list_visible_for.py#test_lesson_feature_does_not_call_module_registry_describe"]
evidence_scope: Recorded passing SUMMARY coverage; latest regression evidence is the pre-commit 129 backend / 105 frontend / typecheck pass, not a new human observation.

### 22. learning_unit.add stores a draft whose text equals the selected source span

expected: learning_unit.add stores a draft whose text equals the selected source span
result: pass
source: automated
coverage_id: 01-03:D1
requirement: ANLY-08
verification_refs: ["backend/tests/application/test_learning_unit_add.py#test_add_stores_exact_span_text_as_draft","backend/tests/application/test_learning_unit_add.py#test_missing_span_writes_no_row"]
evidence_scope: Recorded passing SUMMARY coverage; latest regression evidence is the pre-commit 129 backend / 105 frontend / typecheck pass, not a new human observation.

### 23. Overlapping spans are rejected and the existing unit stays; touching edges create two units

expected: Overlapping spans are rejected and the existing unit stays; touching edges create two units
result: pass
source: automated
coverage_id: 01-03:D2
requirement: ANLY-08
verification_refs: ["backend/tests/domain/test_spans.py#test_overlapping_spans_are_rejected_by_predicate","backend/tests/domain/test_spans.py#test_touching_edges_do_not_overlap","backend/tests/application/test_learning_unit_add.py#test_overlap_of_rolling_out_keeps_existing_unit","backend/tests/application/test_learning_unit_add.py#test_touching_edges_create_two_units"]
evidence_scope: Recorded passing SUMMARY coverage; latest regression evidence is the pre-commit 129 backend / 105 frontend / typecheck pass, not a new human observation.

### 24. Accept moves a draft to accepted and list returns both live units

expected: Accept moves a draft to accepted and list returns both live units
result: pass
source: automated
coverage_id: 01-03:D3
requirement: ANLY-08
verification_refs: ["backend/tests/application/test_learning_unit_accept.py#test_accept_flips_draft_and_list_returns_both"]
evidence_scope: Recorded passing SUMMARY coverage; latest regression evidence is the pre-commit 129 backend / 105 frontend / typecheck pass, not a new human observation.

### 25. Logical remove keeps the row, hides it from list, and re-add of the same span inserts a new id

expected: Logical remove keeps the row, hides it from list, and re-add of the same span inserts a new id
result: pass
source: automated
coverage_id: 01-03:D4
requirement: ANLY-08
verification_refs: ["backend/tests/application/test_learning_unit_remove.py#test_remove_sets_removed_at_and_keeps_the_row","backend/tests/application/test_learning_unit_remove.py#test_logical_removed_span_can_be_readded_as_new_unit","backend/tests/application/test_learning_unit_add.py#test_same_phrase_in_two_places_creates_two_units"]
evidence_scope: Recorded passing SUMMARY coverage; latest regression evidence is the pre-commit 129 backend / 105 frontend / typecheck pass, not a new human observation.

### 26. Canonical offsets are Unicode code points. UTF-16 offsets past the source are rejected

expected: Canonical offsets are Unicode code points. UTF-16 offsets past the source are rejected
result: pass
source: automated
coverage_id: 01-03:D5
requirement: ANLY-08
verification_refs: ["backend/tests/application/test_learning_unit_add.py#test_offsets_are_unicode_code_points_not_utf16","backend/tests/application/test_learning_unit_add.py#test_http_maps_learning_unit_dtos"]
evidence_scope: Recorded passing SUMMARY coverage; latest regression evidence is the pre-commit 129 backend / 105 frontend / typecheck pass, not a new human observation.

### 27. A frozen port rejects add, remove, and accept before any write. The real port reports not frozen

expected: A frozen port rejects add, remove, and accept before any write. The real port reports not frozen
result: pass
source: automated
coverage_id: 01-03:D6
requirement: ANLY-08
verification_refs: ["backend/tests/application/test_learning_unit_remove.py#test_frozen_port_rejects_add_without_row_change","backend/tests/application/test_learning_unit_remove.py#test_frozen_port_rejects_remove_without_row_change","backend/tests/application/test_learning_unit_remove.py#test_frozen_port_rejects_accept_without_row_change","backend/tests/application/test_learning_unit_remove.py#test_not_frozen_port_allows_add"]
evidence_scope: Recorded passing SUMMARY coverage; latest regression evidence is the pre-commit 129 backend / 105 frontend / typecheck pass, not a new human observation.

### 28. HTTP routes map DTOs onto the handlers with stable operationIds and do not edit app.py

expected: HTTP routes map DTOs onto the handlers with stable operationIds and do not edit app.py
result: pass
source: automated
coverage_id: 01-03:D7
requirement: ANLY-08
verification_refs: ["backend/tests/application/test_learning_unit_add.py#test_http_maps_learning_unit_dtos","backend/tests/application/test_learning_unit_remove.py#test_learning_unit_migration_does_not_cascade_deletes"]
evidence_scope: Recorded passing SUMMARY coverage; latest regression evidence is the pre-commit 129 backend / 105 frontend / typecheck pass, not a new human observation.

### 29. One accepted unit produces one Gap Fill item that blanks only the target span and keeps the rest of the sentence literal

expected: One accepted unit produces one Gap Fill item that blanks only the target span and keeps the rest of the sentence literal
result: pass
source: automated
coverage_id: 01-04:D1
requirement: EXER-03
verification_refs: ["backend/tests/modules/exercise_gap_fill/test_generate.py#test_one_accepted_unit_blanks_only_the_target_span","backend/tests/modules/exercise_gap_fill/test_generate.py#test_sentence_window_keeps_only_the_target_sentence","backend/tests/modules/exercise_gap_fill/test_generate.py#test_sentence_window_uses_start_and_end_when_no_terminator","backend/tests/modules/exercise_gap_fill/test_generate.py#test_sentence_window_honors_exclamation_and_question_marks"]
evidence_scope: Recorded passing SUMMARY coverage; latest regression evidence is the pre-commit 129 backend / 105 frontend / typecheck pass, not a new human observation.

### 30. Multiple units order by span start then learning_unit_id, each item blanks only its own span, and generate exposes chip candidate ids

expected: Multiple units order by span start then learning_unit_id, each item blanks only its own span, and generate exposes chip candidate ids
result: pass
source: automated
coverage_id: 01-04:D2
requirement: EXER-03
verification_refs: ["backend/tests/modules/exercise_gap_fill/test_generate.py#test_items_order_by_span_start_then_learning_unit_id","backend/tests/modules/exercise_gap_fill/test_generate.py#test_equal_span_start_orders_by_learning_unit_id","backend/tests/modules/exercise_gap_fill/test_generate.py#test_two_units_in_one_sentence_blank_only_their_own_span","backend/tests/modules/exercise_gap_fill/test_generate.py#test_generate_exposes_chip_candidate_unit_ids"]
evidence_scope: Recorded passing SUMMARY coverage; latest regression evidence is the pre-commit 129 backend / 105 frontend / typecheck pass, not a new human observation.

### 31. Drag is correct only when the submitted learning_unit_id matches, even if the chip text is identical

expected: Drag is correct only when the submitted learning_unit_id matches, even if the chip text is identical
result: pass
source: automated
coverage_id: 01-04:D3
requirement: EVAL-01
verification_refs: ["backend/tests/modules/exercise_gap_fill/test_evaluate.py#test_drag_is_correct_when_submitted_learning_unit_id_matches","backend/tests/modules/exercise_gap_fill/test_evaluate.py#test_drag_is_incorrect_for_other_unit_id_even_when_text_matches"]
evidence_scope: Recorded passing SUMMARY coverage; latest regression evidence is the pre-commit 129 backend / 105 frontend / typecheck pass, not a new human observation.

### 32. Typed answers match after trimming ends and casefold only

expected: Typed answers match after trimming ends and casefold only
result: pass
source: automated
coverage_id: 01-04:D4
requirement: EVAL-01
verification_refs: ["backend/tests/modules/exercise_gap_fill/test_evaluate.py#test_typed_match_strips_ends_and_ignores_case_only"]
evidence_scope: Recorded passing SUMMARY coverage; latest regression evidence is the pre-commit 129 backend / 105 frontend / typecheck pass, not a new human observation.

### 33. The persistable result category has five values and Gap Fill emits only correct or incorrect

expected: The persistable result category has five values and Gap Fill emits only correct or incorrect
result: pass
source: automated
coverage_id: 01-04:D5
requirement: EVAL-04
verification_refs: ["backend/tests/modules/exercise_gap_fill/test_evaluate.py#test_gap_fill_emits_only_correct_or_incorrect"]
evidence_scope: Recorded passing SUMMARY coverage; latest regression evidence is the pre-commit 129 backend / 105 frontend / typecheck pass, not a new human observation.

### 34. Существующий deterministic educational payload сохраняет объяснение, used/missed chunks и nullable alternative; исторические D-18 шаблоны не расширяются. Полное EVAL-05 не объявляется реализованным.

expected: Существующий deterministic educational payload сохраняет объяснение, used/missed chunks и nullable alternative; исторические D-18 шаблоны не расширяются. Полное EVAL-05 не объявляется реализованным.
result: pass
source: automated
coverage_id: 01-04:D6
requirement: EVAL-05
verification_refs: ["backend/tests/modules/exercise_gap_fill/test_feedback.py#test_correct_explanation_matches_d18_and_records_used","backend/tests/modules/exercise_gap_fill/test_feedback.py#test_incorrect_explanation_matches_d18_and_records_missed"]
evidence_scope: Recorded passing SUMMARY coverage; latest regression evidence is the pre-commit 129 backend / 105 frontend / typecheck pass, not a new human observation.
scope_amendment: D-32–D-37 supersede the historical learner presentation; data preservation remains binding.
historical_description: "Explanations use the D-18 templates, natural_alternative is null, and a hit records used while a miss records missed"
current_regression_refs: frontend/src/registries/renderers/gapFillRenderer.test.tsx, frontend/src/features/lesson/FocusPracticeMode.test.tsx, backend/tests/adapters/http/test_http_dto_mapping.py

### 35. Proof generate and evaluate satisfy the same public protocol as Gap Fill and core does not special-case either module id

expected: Proof generate and evaluate satisfy the same public protocol as Gap Fill and core does not special-case either module id
result: pass
source: automated
coverage_id: 01-04:D7
requirement: MODL-03
verification_refs: ["backend/tests/modules/exercise_proof/test_contract.py#test_proof_satisfies_the_same_public_exercise_protocol_as_gap_fill","backend/tests/modules/exercise_proof/test_contract.py#test_core_does_not_special_case_exercise_module_ids"]
evidence_scope: Recorded passing SUMMARY coverage; latest regression evidence is the pre-commit 129 backend / 105 frontend / typecheck pass, not a new human observation.

### 36. exercise.generate stores completed with one definition per accepted unit, and failed with zero definitions when none are accepted

expected: exercise.generate stores completed with one definition per accepted unit, and failed with zero definitions when none are accepted
result: pass
source: automated
coverage_id: 01-05:D1
requirement: EXER-01
verification_refs: ["backend/tests/application/test_exercise_generate.py#test_generate_with_accepted_units_stores_completed_and_matching_count","backend/tests/application/test_exercise_generate.py#test_generate_with_zero_accepted_stores_failed_and_zero_definitions","backend/tests/application/test_exercise_generate.py#test_generate_skips_drafts_and_persists_only_terminal_status"]
evidence_scope: Recorded passing SUMMARY coverage; latest regression evidence is the pre-commit 129 backend / 105 frontend / typecheck pass, not a new human observation.

### 37. practice.start freezes add, remove, and accept while the session is open, and rejects a stale accepted-unit set

expected: practice.start freezes add, remove, and accept while the session is open, and rejects a stale accepted-unit set
result: pass
source: automated
coverage_id: 01-05:D2
requirement: EXER-02
verification_refs: ["backend/tests/application/test_practice_start.py#test_start_freezes_add_remove_and_accept","backend/tests/application/test_practice_start.py#test_start_rejects_stale_generation_after_accept_or_remove","backend/tests/application/test_practice_start.py#test_draft_only_add_does_not_invalidate_generation"]
evidence_scope: Recorded passing SUMMARY coverage; latest regression evidence is the pre-commit 129 backend / 105 frontend / typecheck pass, not a new human observation.

### 38. practice.get returns one current item; two units are drag then typed in span order, and one unit is typed only

expected: practice.get returns one current item; two units are drag then typed in span order, and one unit is typed only
result: pass
source: automated
coverage_id: 01-05:D3
requirement: EXER-02
verification_refs: ["backend/tests/application/test_practice_start.py#test_practice_get_returns_one_current_typed_item_for_one_unit","backend/tests/application/test_practice_start.py#test_two_unit_lesson_yields_drag_then_typed_in_span_order"]
evidence_scope: Recorded passing SUMMARY coverage; latest regression evidence is the pre-commit 129 backend / 105 frontend / typecheck pass, not a new human observation.

### 39. Submit stores feedback and an Attempt, advances the cursor, keeps the session open, and accepts a second submit of the same item

expected: Submit stores feedback and an Attempt, advances the cursor, keeps the session open, and accepts a second submit of the same item
result: pass
source: automated
coverage_id: 01-05:D4
requirement: EXER-07
verification_refs: ["backend/tests/application/test_submit_attempt.py#test_submit_stores_attempt_feedback_and_advances_while_session_stays_open","backend/tests/application/test_submit_attempt.py#test_same_item_accepted_twice_creates_two_attempts","backend/tests/application/test_submit_attempt.py#test_attempt_unit_fk_is_on_delete_restrict_and_copies_span_and_text"]
evidence_scope: Recorded passing SUMMARY coverage; latest regression evidence is the pre-commit 129 backend / 105 frontend / typecheck pass, not a new human observation.

### 40. HTTP maps generate, start, get, and submit, and does not add finish or start-over routes

expected: HTTP maps generate, start, get, and submit, and does not add finish or start-over routes
result: pass
source: automated
coverage_id: 01-05:D5
requirement: EXER-07
verification_refs: ["backend/tests/application/test_submit_attempt.py#test_http_maps_generate_start_get_and_submit_only"]
evidence_scope: Recorded passing SUMMARY coverage; latest regression evidence is the pre-commit 129 backend / 105 frontend / typecheck pass, not a new human observation.

### 41. Lesson workspace is a stage shell. Loading and load errors stay inside the stage column, and the column and source body scroll vertically.

expected: Lesson workspace is a stage shell. Loading and load errors stay inside the stage column, and the column and source body scroll vertically.
result: pass
source: automated
coverage_id: 01-06:D1
requirement: LESS-02
verification_refs: ["frontend/src/features/lesson/LessonWorkspacePage.test.tsx#shell-has-no-outer-empty-loading-error","frontend/src/features/lesson/LessonWorkspacePage.test.tsx#stage-column-scroll-fixed-labels","frontend/src/features/lesson/LessonWorkspacePage.test.tsx#source-panel-body-scrolls"]
evidence_scope: Recorded passing SUMMARY coverage; latest regression evidence is the pre-commit 129 backend / 105 frontend / typecheck pass, not a new human observation.

### 42. Add Learning Unit posts Unicode code points. A selection of out after U+1F44D sends start 1 and end 4.

expected: Add Learning Unit posts Unicode code points. A selection of out after U+1F44D sends start 1 and end 4.
result: pass
source: automated
coverage_id: 01-06:D2
requirement: ANLY-08
verification_refs: ["frontend/src/features/lesson/LearningUnitsStage.test.tsx#converts a selection after an emoji to Unicode code points"]
evidence_scope: Recorded passing SUMMARY coverage; latest regression evidence is the pre-commit 129 backend / 105 frontend / typecheck pass, not a new human observation.

### 43. Generate Exercises shows Generating… then completed or the locked failure copy. Start Practice stays disabled until that generation matches the current accepted set.

expected: Generate Exercises shows Generating… then completed or the locked failure copy. Start Practice stays disabled until that generation matches the current accepted set.
result: pass
source: automated
coverage_id: 01-06:D3
requirement: EXER-01
verification_refs: ["frontend/src/features/lesson/LessonWorkspacePage.test.tsx#shows Generating… then the no-accepted failure copy","frontend/src/features/lesson/LessonWorkspacePage.test.tsx#enables Start Practice only for the generated accepted set"]
evidence_scope: Recorded passing SUMMARY coverage; latest regression evidence is the pre-commit 129 backend / 105 frontend / typecheck pass, not a new human observation.

### 44. Lesson list and create use the locked empty, loading, error, Untitled Lesson, and Creating… copy. The title field wraps to two lines.

expected: Lesson list and create use the locked empty, loading, error, Untitled Lesson, and Creating… copy. The title field wraps to two lines.
result: pass
source: automated
coverage_id: 01-06:D4
requirement: LESS-01
verification_refs: ["frontend/src/features/lesson/LessonListPage.test.tsx#shows the empty lesson list copy and Create Lesson","frontend/src/features/lesson/LessonListPage.test.tsx#suggests Untitled Lesson and wraps the title field to two lines"]
evidence_scope: Recorded passing SUMMARY coverage; latest regression evidence is the pre-commit 129 backend / 105 frontend / typecheck pass, not a new human observation.

### 45. Lesson UI does not call module_registry.describe or hard-code the Gap Fill module id.

expected: Lesson UI does not call module_registry.describe or hard-code the Gap Fill module id.
result: pass
source: automated
coverage_id: 01-06:D5
requirement: EXER-01
verification_refs: ["frontend/src/features/lesson/LessonWorkspacePage.test.tsx#does not reference module_registry.describe in lesson feature source"]
evidence_scope: Recorded passing SUMMARY coverage; latest regression evidence is the pre-commit 129 backend / 105 frontend / typecheck pass, not a new human observation.

### 46. Start Practice swaps the lesson route to Focus Practice and wires Submit Answer, Continue, Exit Practice, and confirmed Start Over.

expected: Start Practice swaps the lesson route to Focus Practice and wires Submit Answer, Continue, Exit Practice, and confirmed Start Over.
result: pass
source: automated
coverage_id: 01-07:D1
requirement: EXER-02
verification_refs: ["frontend/src/features/lesson/FocusPracticeMode.test.tsx#submits one typed answer then continues inside the session","frontend/src/features/lesson/FocusPracticeMode.test.tsx#exit practice calls finish and restores the workspace","frontend/src/features/lesson/FocusPracticeMode.test.tsx#start over confirms then calls start_over only"]
evidence_scope: Recorded passing SUMMARY coverage; latest regression evidence is the pre-commit 129 backend / 105 frontend / typecheck pass, not a new human observation.

### 47. Gap Fill показывает предложение, выбор по unit id или typed-ввод, Checking…, затем единственный inline-результат по D-33–D-34, без прежней карточки.

expected: Gap Fill показывает предложение, выбор по unit id или typed-ввод, Checking…, затем единственный inline-результат по D-33–D-34, без прежней карточки.
result: pass
source: automated
coverage_id: 01-07:D2
requirement: EXER-03
verification_refs: ["frontend/src/features/lesson/FocusPracticeMode.test.tsx#submits a drag chip by unit id and displays the server category","frontend/src/registries/renderers/gapFillRenderer.test.tsx#wraps the blank inline and scrolls the chip bank","frontend/src/features/lesson/FocusPracticeMode.test.tsx#renders server feedback as text and omits a null natural alternative"]
evidence_scope: Recorded passing SUMMARY coverage; latest regression evidence is the pre-commit 129 backend / 105 frontend / typecheck pass, not a new human observation.
scope_amendment: D-32–D-37 supersede the historical learner presentation; data preservation remains binding.
historical_description: "Gap Fill shows a blanked sentence, drag chips graded by unit id or typed input, Checking…, and one server feedback card."
current_regression_refs: frontend/src/registries/renderers/gapFillRenderer.test.tsx, frontend/src/features/lesson/FocusPracticeMode.test.tsx, backend/tests/adapters/http/test_http_dto_mapping.py

### 48. Workspace Feedback сохраняет историю категорий и переход к исходному unit; Start Over не стирает прежние попытки. Это не полное учебное содержание EVAL-05.

expected: Workspace Feedback сохраняет историю категорий и переход к исходному unit; Start Over не стирает прежние попытки. Это не полное учебное содержание EVAL-05.
result: pass
source: automated
coverage_id: 01-07:D3
requirement: EVAL-05
verification_refs: ["frontend/src/features/lesson/FeedbackStage.test.tsx#lists category explanation and an excerpt jump","frontend/src/features/lesson/FeedbackStage.test.tsx#keeps listed attempts after start over","frontend/src/features/lesson/FeedbackStage.test.tsx#shows the empty copy after leaving practice with no attempts"]
evidence_scope: Recorded passing SUMMARY coverage; latest regression evidence is the pre-commit 129 backend / 105 frontend / typecheck pass, not a new human observation.
scope_amendment: D-32–D-37 supersede the historical learner presentation; data preservation remains binding.
historical_description: "After Exit Practice the Feedback stage lists category, explanation, and an excerpt jump. Start Over does not clear those rows."
current_regression_refs: frontend/src/registries/renderers/gapFillRenderer.test.tsx, frontend/src/features/lesson/FocusPracticeMode.test.tsx, backend/tests/adapters/http/test_http_dto_mapping.py

### 49. ProofRenderer mounts from the registry by exercise_type in Vitest. Focus Practice does not select it.

expected: ProofRenderer mounts from the registry by exercise_type in Vitest. Focus Practice does not select it.
result: pass
source: automated
coverage_id: 01-07:D4
requirement: MODL-03
verification_refs: ["frontend/src/registries/renderers/proofRenderer.test.ts#mounts the proof renderer by exercise_type","frontend/src/registries/renderers/proofRenderer.test.ts#learner focus practice never selects the proof renderer"]
evidence_scope: Recorded passing SUMMARY coverage; latest regression evidence is the pre-commit 129 backend / 105 frontend / typecheck pass, not a new human observation.

### 50. OpenAPI 3.1 operationIds match the D-23 command and query names, including module_registry.describe.

expected: OpenAPI 3.1 operationIds match the D-23 command and query names, including module_registry.describe.
result: pass
source: automated
coverage_id: 01-08:D1
requirement: PLAT-09
verification_refs: ["backend/tests/adapters/http/test_openapi_contract.py#test_openapi_operation_ids_match_d23_names","backend/tests/adapters/http/test_openapi_contract.py#test_export_openapi_writes_openapi_31_without_secrets"]
evidence_scope: Recorded passing SUMMARY coverage; latest regression evidence is the pre-commit 129 backend / 105 frontend / typecheck pass, not a new human observation.

### 51. The committed TypeScript client matches a fresh export and generate.

expected: The committed TypeScript client matches a fresh export and generate.
result: pass
source: automated
coverage_id: 01-08:D2
requirement: PLAT-09
verification_refs: ["uv run python -m lait.adapters.http.export_openapi && npm --prefix frontend run openapi:generate && git diff --exit-code -- frontend/src/api/generated"]
evidence_scope: Recorded passing SUMMARY coverage; latest regression evidence is the pre-commit 129 backend / 105 frontend / typecheck pass, not a new human observation.

### 52. The lesson feature calls the generated SDK. Frontend tests and the production build pass against those types.

expected: The lesson feature calls the generated SDK. Frontend tests and the production build pass against those types.
result: pass
source: automated
coverage_id: 01-08:D3
requirement: MODL-12
verification_refs: ["npm --prefix frontend test","npm --prefix frontend run build"]
evidence_scope: Recorded passing SUMMARY coverage; latest regression evidence is the pre-commit 129 backend / 105 frontend / typecheck pass, not a new human observation.

### 53. CI exports OpenAPI, runs openapi:generate, and fails on a dirty frontend/src/api/generated tree.

expected: CI exports OpenAPI, runs openapi:generate, and fails on a dirty frontend/src/api/generated tree.
result: pass
source: automated
coverage_id: 01-08:D4
requirement: PLAT-09
verification_refs: ["git grep -n openapi:generate .github/workflows/ci.yml && git grep -n \\\"git diff --exit-code -- frontend/src/api/generated\\\" .github/workflows/ci.yml"]
evidence_scope: Recorded passing SUMMARY coverage; latest regression evidence is the pre-commit 129 backend / 105 frontend / typecheck pass, not a new human observation.

### 54. Removing the proof catalog entry leaves the app up, omits proof from describe, still lists Gap Fill, and generates from an accepted unit, with Core and application digests unchanged.

expected: Removing the proof catalog entry leaves the app up, omits proof from describe, still lists Gap Fill, and generates from an accepted unit, with Core and application digests unchanged.
result: pass
source: automated
coverage_id: 01-09:D1
requirement: MODL-03
verification_refs: ["backend/tests/catalog/test_proof_removal.py#test_proof_removal"]
evidence_scope: Recorded passing SUMMARY coverage; latest regression evidence is the pre-commit 129 backend / 105 frontend / typecheck pass, not a new human observation.

### 55. Application handlers and application tests do not import FastAPI or SQLAlchemy table modules. HTTP DTO tests live under the HTTP adapter suite.

expected: Application handlers and application tests do not import FastAPI or SQLAlchemy table modules. HTTP DTO tests live under the HTTP adapter suite.
result: pass
source: automated
coverage_id: 01-09:D2
requirement: MODL-12
verification_refs: ["backend/tests/application/test_handler_isolation.py#test_handler_isolation"]
evidence_scope: Recorded passing SUMMARY coverage; latest regression evidence is the pre-commit 129 backend / 105 frontend / typecheck pass, not a new human observation.

### 56. Domain, persistence, and module suites collect and pass on their own. An empty directory fails pytest collection.

expected: Domain, persistence, and module suites collect and pass on their own. An empty directory fails pytest collection.
result: pass
source: automated
coverage_id: 01-09:D3
requirement: PLAT-10
verification_refs: ["uv run pytest backend/tests/domain backend/tests/adapters/persistence backend/tests/modules backend/tests/application/test_handler_isolation.py -q"]
evidence_scope: Recorded passing SUMMARY coverage; latest regression evidence is the pre-commit 129 backend / 105 frontend / typecheck pass, not a new human observation.

### 57. Full phase pytest gate is green.

expected: Full phase pytest gate is green.
result: pass
source: automated
coverage_id: 01-09:D4
requirement: PLAT-10
verification_refs: ["uv run pytest -q"]
evidence_scope: Recorded passing SUMMARY coverage; latest regression evidence is the pre-commit 129 backend / 105 frontend / typecheck pass, not a new human observation.

### 58. docker compose up -d --wait reaches healthy api and web containers.

expected: docker compose up -d --wait reaches healthy api and web containers.
result: pass
source: automated
coverage_id: 01-09:D5
requirement: PLAT-03
verification_refs: ["docker compose up -d --wait"]
evidence_scope: Recorded passing SUMMARY coverage; latest regression evidence is the pre-commit 129 backend / 105 frontend / typecheck pass, not a new human observation.

### 59. OpenAPI export and generate leave frontend/src/api/generated clean.

expected: OpenAPI export and generate leave frontend/src/api/generated clean.
result: pass
source: automated
coverage_id: 01-09:D6
requirement: none
verification_refs: ["uv run python -m lait.adapters.http.export_openapi && npm run openapi:generate --prefix frontend && git diff --exit-code -- frontend/src/api/generated"]
evidence_scope: Recorded passing SUMMARY coverage; latest regression evidence is the pre-commit 129 backend / 105 frontend / typecheck pass, not a new human observation.

### 60. docker compose up -d --wait reaches a healthy API only after Alembic upgrade head

expected: docker compose up -d --wait reaches a healthy API only after Alembic upgrade head
result: pass
source: automated
coverage_id: 01-10:D1
requirement: PLAT-03
verification_refs: ["docker compose up -d --wait && curl.exe http://127.0.0.1:8000/health"]
evidence_scope: Recorded passing SUMMARY coverage; latest regression evidence is the pre-commit 129 backend / 105 frontend / typecheck pass, not a new human observation.

### 61. A fresh app-data volume reaches healthy without hand-editing SQLite

expected: A fresh app-data volume reaches healthy without hand-editing SQLite
result: pass
source: automated
coverage_id: 01-10:D2
requirement: PLAT-03
verification_refs: ["docker compose down -v && docker compose up -d --wait; alembic_version 20261001_0002"]
evidence_scope: Recorded passing SUMMARY coverage; latest regression evidence is the pre-commit 129 backend / 105 frontend / typecheck pass, not a new human observation.
historical_only: Fresh-volume verification from 01-10 is retained, not rerun now. NEVER execute the historical down -v reference against the learner volume; Test 1 and Test 12 verify kept-volume restart.

### 62. README documents the one-command Compose start

expected: README documents the one-command Compose start
result: pass
source: automated
coverage_id: 01-10:D3
requirement: PLAT-03
verification_refs: ["README.md#Docker Compose"]
evidence_scope: Recorded passing SUMMARY coverage; latest regression evidence is the pre-commit 129 backend / 105 frontend / typecheck pass, not a new human observation.

### 63. practice.finish closes the session, hides the current item, keeps Attempts, and unfreezes units

expected: practice.finish closes the session, hides the current item, keeps Attempts, and unfreezes units
result: pass
source: automated
coverage_id: 01-11:D1
requirement: EXER-07
verification_refs: ["backend/tests/application/test_practice_finish_and_start_over.py#test_finish_closes_session_and_unfreezes_units"]
evidence_scope: Recorded passing SUMMARY coverage; latest regression evidence is the pre-commit 129 backend / 105 frontend / typecheck pass, not a new human observation.

### 64. practice.start_over keeps Attempt rows, opens a new session via practice.start, and leaves units frozen

expected: practice.start_over keeps Attempt rows, opens a new session via practice.start, and leaves units frozen
result: pass
source: automated
coverage_id: 01-11:D2
requirement: EXER-07
verification_refs: ["backend/tests/application/test_practice_finish_and_start_over.py#test_start_over_keeps_attempts_and_leaves_units_frozen"]
evidence_scope: Recorded passing SUMMARY coverage; latest regression evidence is the pre-commit 129 backend / 105 frontend / typecheck pass, not a new human observation.

### 65. POST finish and POST start-over return 200 and the handler bodies only map DTOs onto practice.finish and practice.start_over

expected: POST finish and POST start-over return 200 and the handler bodies only map DTOs onto practice.finish and practice.start_over
result: pass
source: automated
coverage_id: 01-11:D3
requirement: EXER-07
verification_refs: ["backend/tests/application/test_practice_finish_and_start_over.py#test_http_finish_and_start_over_only_map_dtos"]
evidence_scope: Recorded passing SUMMARY coverage; latest regression evidence is the pre-commit 129 backend / 105 frontend / typecheck pass, not a new human observation.

### 66. A second practice.start returns the same session when the accepted-set snapshot matches, including after generate again.

expected: A second practice.start returns the same session when the accepted-set snapshot matches, including after generate again.
result: pass
source: automated
coverage_id: 01-12:D1
requirement: EXER-02
verification_refs: ["backend/tests/application/test_practice_start.py#test_second_start_returns_the_same_open_session","backend/tests/application/test_practice_start.py#test_generate_again_keeps_the_open_session_for_the_next_start"]
evidence_scope: Recorded passing SUMMARY coverage; latest regression evidence is the pre-commit 129 backend / 105 frontend / typecheck pass, not a new human observation.

### 67. A second open row for one lesson cannot commit, and a unique violation returns the winning session id.

expected: A second open row for one lesson cannot commit, and a unique violation returns the winning session id.
result: pass
source: automated
coverage_id: 01-12:D2
requirement: EXER-02
verification_refs: ["backend/tests/application/test_practice_start.py#test_second_open_row_for_one_lesson_is_rejected","backend/tests/application/test_practice_start.py#test_unique_violation_returns_the_winning_open_session"]
evidence_scope: Recorded passing SUMMARY coverage; latest regression evidence is the pre-commit 129 backend / 105 frontend / typecheck pass, not a new human observation.

### 68. A stored lait.practice-session id shows the frozen hint while practice.get is pending, then resumes Focus Practice when the session is open.

expected: A stored lait.practice-session id shows the frozen hint while practice.get is pending, then resumes Focus Practice when the session is open.
result: pass
source: automated
coverage_id: 01-12:D3
requirement: EXER-02
verification_refs: ["frontend/src/features/lesson/LessonWorkspacePage.test.tsx#resumes a stored open session into Focus Practice after the frozen hint","frontend/src/features/lesson/LessonWorkspacePage.test.tsx#isPracticeOpen locks while a stored session is pending and then follows session.open","frontend/src/features/lesson/LessonWorkspacePage.test.tsx#clears a stored session that is not open and leaves the workspace unlocked"]
evidence_scope: Recorded passing SUMMARY coverage; latest regression evidence is the pre-commit 129 backend / 105 frontend / typecheck pass, not a new human observation.

### 69. Start Practice stays disabled until the first start request settles, including when that request fails.

expected: Start Practice stays disabled until the first start request settles, including when that request fails.
result: pass
source: automated
coverage_id: 01-12:D4
requirement: EXER-02
verification_refs: ["frontend/src/features/lesson/stages/PracticeStage.test.tsx#disables Start Practice while the start request is pending","frontend/src/features/lesson/LessonWorkspacePage.test.tsx#disables Start Practice until the first start request settles","frontend/src/features/lesson/LessonWorkspacePage.test.tsx#enables Start Practice again after the start request rejects"]
evidence_scope: Recorded passing SUMMARY coverage; latest regression evidence is the pre-commit 129 backend / 105 frontend / typecheck pass, not a new human observation.

### 70. Reload restores a matching generation and saved attempts without exercise.generate. A mismatched accepted set stays locked.

expected: Reload restores a matching generation and saved attempts without exercise.generate. A mismatched accepted set stays locked.
result: pass
source: automated
coverage_id: 01-13:D1
requirement: EXER-02
verification_refs: ["backend/tests/application/test_lesson_reopen_reads.py","frontend/src/features/lesson/LessonWorkspacePage.test.tsx"]
evidence_scope: Recorded passing SUMMARY coverage; latest regression evidence is the pre-commit 129 backend / 105 frontend / typecheck pass, not a new human observation.

### 71. The last Continue closes the exhausted session and the summary contains only that session id. An early Exit is exited.

expected: The last Continue closes the exhausted session and the summary contains only that session id. An early Exit is exited.
result: pass
source: automated
coverage_id: 01-13:D2
requirement: EXER-07
verification_refs: ["frontend/src/features/lesson/stages/FeedbackStage.test.tsx"]
evidence_scope: Recorded passing SUMMARY coverage; latest regression evidence is the pre-commit 129 backend / 105 frontend / typecheck pass, not a new human observation.

### 72. From 960px Source and units sit side by side. Below that they stack. Add stays outside the unit scroller. The selected unit deletes with a compact × named Remove {phrase}.

expected: From 960px Source and units sit side by side. Below that they stack. Add stays outside the unit scroller. The selected unit deletes with a compact × named Remove {phrase}.
result: pass
source: automated
coverage_id: 01-14:D1
requirement: ANLY-08
verification_refs: ["frontend/src/features/lesson/LessonWorkspacePage.test.tsx","frontend/src/features/lesson/LearningUnitsStage.test.tsx"]
evidence_scope: Recorded passing SUMMARY coverage; latest regression evidence is the pre-commit 129 backend / 105 frontend / typecheck pass, not a new human observation.

### 73. A restorable generation says Exercises are ready. Generate Exercises is not the next step for an unchanged accepted set. Stage headers expose aria-expanded.

expected: A restorable generation says Exercises are ready. Generate Exercises is not the next step for an unchanged accepted set. Stage headers expose aria-expanded.
result: pass
source: automated
coverage_id: 01-14:D2
requirement: EXER-01
verification_refs: ["frontend/src/features/lesson/LessonWorkspacePage.test.tsx"]
evidence_scope: Recorded passing SUMMARY coverage; latest regression evidence is the pre-commit 129 backend / 105 frontend / typecheck pass, not a new human observation.

### 74. Fresh SQLite-to-HTTP reads retain rich and empty feedback, exact identity and original legacy/raw text.

expected: Fresh SQLite-to-HTTP reads retain rich and empty feedback, exact identity and original legacy/raw text.
result: pass
source: automated
coverage_id: 01-17:D1
requirement: EVAL-05
verification_refs: ["backend/tests/adapters/http/test_http_dto_mapping.py#test_reopened_http_lists_complete_saved_feedback_without_mutation","backend/tests/adapters/http/test_http_dto_mapping.py#test_http_maps_generate_start_get_and_submit_only"]
evidence_scope: Recorded passing SUMMARY coverage; latest regression evidence is the pre-commit 129 backend / 105 frontend / typecheck pass, not a new human observation.

### 75. Repository and application projections preserve real saved arrays, nullability, order and denominator; malformed arrays are rejected.

expected: Repository and application projections preserve real saved arrays, nullability, order and denominator; malformed arrays are rejected.
result: pass
source: automated
coverage_id: 01-17:D2
requirement: EVAL-05
verification_refs: ["backend/tests/adapters/persistence/test_lesson_reopen_reads.py#test_reopened_repository_preserves_complete_feedback_records","backend/tests/adapters/persistence/test_lesson_reopen_reads.py#test_reopened_repository_rejects_malformed_saved_chunks","backend/tests/application/test_lesson_reopen_reads.py#test_query_forwards_complete_saved_feedback_without_mutating_records","backend/tests/application/test_practice_retry.py","backend/tests/application/test_practice_finish_and_start_over.py"]
evidence_scope: Recorded passing SUMMARY coverage; latest regression evidence is the pre-commit 129 backend / 105 frontend / typecheck pass, not a new human observation.

### 76. Generated attempt DTO requires every saved field while existing operation bindings are retained.

expected: Generated attempt DTO requires every saved field while existing operation bindings are retained.
result: pass
source: automated
coverage_id: 01-17:D3
requirement: EVAL-05
verification_refs: ["generated_attempt_dto_requires_complete_saved_feedback (exact Node command under Verification)","npm --prefix frontend run typecheck","backend/tests/adapters/http/test_openapi_client_drift.py#test_typescript_client_matches_openapi_and_ci_rejects_drift"]
evidence_scope: Recorded passing SUMMARY coverage; latest regression evidence is the pre-commit 129 backend / 105 frontend / typecheck pass, not a new human observation.

## Summary

total: 76
passed: 76
issues: 0
pending: 0
skipped: 0
blocked: 0

## Gaps

<!-- None in this new session. Historical resolved G-01-1 is reserved: any new regression gets G-01-20261007-{test}, never reopens/reuses G-01-1. -->

## Completion Evidence — 2026-10-08

- All 14 Docker learner-flow tests passed by explicit user reports; 62 automated entries retain their recorded SUMMARY coverage. No fresh suite or independent browser observation is claimed.
- Tests 10–14 were explicitly passed in this resumed session. Test 12 includes four feedback states across reload, direct URL, Lesson List return, full browser-process restart and Docker/app restart with the volume kept; Test 13 covers 320px.
- Separate whole-phase learner smoke recorded in `01-VALIDATION.md` Manual-Only table. Plan 01-18 approval remains distinct from this UAT result.
- Zero current-session gaps, pending, blocked or skipped tests. This completes the UAT session, not Phase 1: canonical verification remains `gaps_found` until re-verification; original full EVAL-05 remains partial/deferred to Phase 5.
- O-01-9-visual remains UX/visual debt with phase ownership and acceptance impact undecided. Test 14 pass confirms expected workspace behavior; it does not authorize the proposed redesign or imply its deferral is accepted.
- Historical `01-UAT-HISTORY-2026-10-06.md` is preserved verbatim. Its old issue is not a fresh current-session failure.
- UI post-hook: user selected option 1 (View existing report). `01-UI-REVIEW.md` is retained unchanged at its historical 2026-10-06 score of 14/24; no fresh audit or current-score claim. Validation/security post-hook evidence is recorded in their respective reports.
- Shared completion predicate still rejects phase transition: the historical UAT file is included as diagnosed/issue, and canonical `01-VERIFICATION.md` remains `gaps_found`. These bookkeeping/history and re-verification conditions do not change this current session's 76 passed results. Do not rewrite historical results or force phase.complete to bypass them.

## Session Scope and History

- User selected option 1: a new whole-phase UAT, not a resume of the old single-check session.
- Old session is preserved verbatim in [01-UAT-HISTORY-2026-10-06.md](./01-UAT-HISTORY-2026-10-06.md); G-01-1 remains resolved by 01-15. Historical observations are not fresh gaps.
- 01-18 R2 blocking-human checkpoint was explicitly approved. That approval remains valid but does not substitute for this separate whole-phase learner smoke.
- Serving target: Docker Compose http://127.0.0.1:5173; API http://127.0.0.1:8000/health. Readiness before this session: api healthy, web running, volume kept. No service restart or learner data write was performed by the assistant to create this session.
- D-32–D-37 govern current acceptance: no focus Details/Chunks used/missed, no added LLM or explanation templates, a single inline result and genuine saved-payload restoration. Existing workspace history is not the focus answer card.
- Original full EVAL-05 is partially delivered, with detailed teaching/chunk/alternative presentation deferred to Phase 5. Automated data-path passes are not a full-requirement checkbox or phase-completion claim.
- PLAT-09 remains closed: do not generate a repeated plan for it. Retry rounds, opening score, Continue, Start Over and Exit are frozen.
- Shared multi-blank tasks and actual drag-and-drop remain proposed Phase 4/9 follow-ups, not this session's criteria.
- Manual tests 1–14 form the separate full-phase learner smoke. Record its actual user-reported outcome in 01-VALIDATION.md only when performed; no inferred approval from automated suites.
- Browser automation fallback: no eligible Playwright-MCP / opted-in live DOM tool; 0 UI checkpoints auto-observed, 14 queued for human review. User confirms one test at a time.
- Do not implement fixes, commit/push session artifacts, or close Phase 1 while this UAT is pending. Historical 01-VERIFICATION.md gaps_found is not a newly diagnosed gap or a reason to relaunch completed plans automatically.

## Evidence Reconciliation

- All 18 SUMMARY coverage blocks classified successfully, with no malformed-block errors: 62 automated entries and 11 human-judgment entries. Every human entry maps to its own checkpoint above; tests 1, 3 and 4 add safe startup and the complete source-to-practice journey.
- Bounded Git checks for plans 01–12 and 17–18 agree with their recorded actuals.commits; plan-time before/after windows are historical, not measured against current HEAD. Plans 13–16 lack bounded HEAD metadata: their aggregate commit claims are not independently countable and are not treated as blockers or rewritten.
- Accepted implementation HEAD and remote branch: 0f3038853fe5f51274870b6bfda107848b57114a on phase/01-execution. The five pre-existing historical audit artifacts stay outside this session's edits.


## Observations

- observation_id: O-01-9-visual
  test: 9
  reported: "Функционально pass, но мне не нравится как визуально выглядит раздел feedback"
  classification: UX debt + visual; information overload in workspace Feedback, not a reported grading failure
  functional_result: pass
  suggested_phase: Phase 9 — Responsive Local Release
  disposition: Concrete simplification requested; acceptance impact still awaiting user decision. Phase 9 remains a proposed owner, not an agreed deferral or permission to implement.
  blocks_approval: Not declared by user; observation alone is not a blocker or phase approval.
  action: Recorded immediately, including buffered passes 6–8. No gap plan, implementation, commit, push or phase closure. Keep approved inline UX, retry, score, Exit and saved-payload safeguards unchanged.
  recorded_at: 2026-10-07T18:53:47Z
  clarified_at: 2026-10-07T19:01:44Z
  user_detail: "мне кажется это избыточным мне кажется это избыточным перегружает интерфейс не доет никакой пользы, максимум результаты последней попытки информация где сделаны ошибки и общий счет все этого достаточно, позже когда будет прикручен LLM можно добавить еще его коментарий"
  evidence: User pasted Current pass 3/6 completed plus Choice/Typed attempt rows, repeated match/nonmatch explanations and Earlier passes with completed/left early groups. No screenshot or independent assistant UI inspection.
  requested_presentation:
    - "A compact result for the most recent practice pass: overall score and where mistakes occurred; clarify if 'last attempt' means a different scope before planning."
    - "Do not show Earlier passes or the full repetitive attempt-by-attempt log in the default Feedback presentation."
    - "Remove generic repeated 'The response matches/does not match the target for this exercise' text from this proposed summary."
    - "Optional LLM comment later with AI feedback scope (Phase 5); do not add LLM or new explanation templates now."
  preservation: Presentation-only proposal; never delete saved attempts/feedback/chunks or change retry rounds, corrected exclusion, opening denominator, Continue, Start Over or Exit.
  current_uat: This message answers the Feedback clarification, not Test 10. Tests 1–9 retain functional pass; Test 10 remains pending.

- observation_id: O-01-10-exit
  test: 10
  reported: "10 после выполнения нескольких заданий и выхода через exit новый Start Practice начинает все заново с первого задания"
  classification: workflow / expectation clarification; no contradiction with the current contract identified
  assessment: Exit calls practice.finish, which closes the session and unfreezes units. A later Start Practice creates a new session at cursor 0; only still-open sessions resume. Retained attempt history is independent of the new cursor.
  evidence_refs:
    - frontend/src/features/lesson/LessonWorkspacePage.tsx#handleExit-and-closeSession
    - backend/lait/application/commands/practice_finish.py#handle
    - backend/lait/application/commands/practice_start.py#handle
    - backend/lait/adapters/persistence/repositories.py#insert_open_practice_session
    - .planning/phases/01-mod-first-manual-learning-loop/01-CONTEXT.md#D-10
    - backend/tests/application/test_practice_finish_and_start_over.py#test_finish_closes_session_and_unfreezes_units
  verification_scope: Read-only contract/source inspection and existing test assertions, not a newly executed suite or independently observed UI.
  disposition: Expected close-not-pause behavior explained; user explicitly reported pass for Test 10 on 2026-10-08, confirming retained history and editable units. No change to Exit required.
  action: No gap plan, code change, commit, push or phase closure. Compact Feedback observation O-01-9-visual remains unresolved separately.
  recorded_at: 2026-10-07T19:24:17Z
  confirmed_at: 2026-10-08T01:29:19Z
  confirmation: "pass"
