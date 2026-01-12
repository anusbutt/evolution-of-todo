---
description: "Task breakdown for Phase 1 - Console Todo Application"
---

# Tasks: Phase 1 - Console Todo Application

**Input**: Design documents from `/specs/001-phase-01-console-todo/`
**Prerequisites**: plan.md (complete), spec.md (complete), research.md (complete), data-model.md (complete), contracts/cli-interface.md (complete)

**Tests**: Tests are NOT explicitly requested in the feature specification. Test tasks are included to meet Constitution requirement of 80% coverage minimum.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Single project**: `phase-01-console/src/`, `phase-01-console/tests/` at repository root
- Paths shown below follow plan.md structure

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [X] T001 Create phase-01-console/ directory at repository root
- [X] T002 Create project structure with src/, tests/, src/models/, src/services/, src/cli/ directories
- [X] T003 [P] Create __init__.py files in src/, src/models/, src/services/, src/cli/, tests/, tests/unit/, tests/integration/
- [X] T004 [P] Create pyproject.toml with UV configuration (Python 3.13+, pytest, pytest-cov)
- [X] T005 [P] Create .gitignore for Python (.venv/, __pycache__/, *.pyc, .pytest_cache/, .coverage)
- [X] T006 [P] Create README.md with project overview and setup instructions

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [X] T007 Create Task model in phase-01-console/src/models/task.py with attributes (id: int, title: str, description: str, completed: bool)
- [X] T008 Implement Task model validation in phase-01-console/src/models/task.py (title: 1-200 chars non-empty, description: 0-1000 chars)
- [X] T009 Implement Task model serialization methods (to_dict, __repr__) in phase-01-console/src/models/task.py
- [X] T010 Create TaskService class in phase-01-console/src/services/task_service.py with __init__ (tasks list, next_id counter)
- [X] T011 [P] Create Menu class skeleton in phase-01-console/src/cli/menu.py with display_menu method
- [X] T012 [P] Create Prompts module skeleton in phase-01-console/src/cli/prompts.py with input validation functions
- [X] T013 Create main.py entry point in phase-01-console/src/main.py with application lifecycle (startup, main loop, shutdown)

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 5 - Application Lifecycle (Priority: P1) 🎯 MVP Foundation

**Goal**: Establish application lifecycle with menu navigation, input prompts, and graceful shutdown to enable all other user stories

**Independent Test**: Launch application, verify welcome message and menu display, select invalid menu choice to verify error handling, select Exit option to verify farewell message and clean termination

### Tests for User Story 5 (Constitution: 80% coverage required)

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation**

- [X] T014 [P] [US5] Create test_app_workflow.py in phase-01-console/tests/integration/ with test_application_startup
- [X] T015 [P] [US5] Create test_menu.py in phase-01-console/tests/unit/ with test_display_menu, test_handle_choice
- [X] T016 [P] [US5] Create test_prompts.py in phase-01-console/tests/unit/ with test_get_menu_choice (valid, invalid, out-of-range)

### Implementation for User Story 5

- [X] T017 [US5] Implement Menu.display_menu() in phase-01-console/src/cli/menu.py (display 7 options with formatting)
- [X] T018 [US5] Implement Prompts.get_menu_choice() in phase-01-console/src/cli/prompts.py (validate 1-7, handle non-numeric, reprompt on error)
- [X] T019 [US5] Implement Menu.handle_choice() in phase-01-console/src/cli/menu.py (route to operation handlers, return continue/exit flag)
- [X] T020 [US5] Implement application startup in phase-01-console/src/main.py (welcome message, initialize TaskService, main loop)
- [X] T021 [US5] Implement application shutdown in phase-01-console/src/main.py (farewell message, KeyboardInterrupt handling, exit code 0)
- [X] T022 [US5] Implement main loop in phase-01-console/src/main.py (display menu, get choice, handle choice, repeat until exit)
- [X] T023 [US5] Add error message handling in phase-01-console/src/cli/prompts.py (invalid choice messages per cli-interface.md)

**Checkpoint**: At this point, User Story 5 should be fully functional - application can start, display menu, handle invalid input, and exit cleanly

---

## Phase 4: User Story 1 - Add and View Tasks (Priority: P1) 🎯 MVP Core

**Goal**: Enable users to add tasks with title/description and view their complete task list with status indicators

**Independent Test**: Launch app, add 3 tasks (1 with description, 2 title-only), view list to verify all tasks display with IDs, titles, descriptions, and incomplete status indicators

### Tests for User Story 1 (Constitution: 80% coverage required)

- [X] T024 [P] [US1] Create test_task_model.py in phase-01-console/tests/unit/ with test_task_creation, test_title_validation, test_description_validation
- [X] T025 [P] [US1] Create test_task_service.py in phase-01-console/tests/unit/ with test_add_task, test_get_all_tasks, test_auto_increment_id
- [X] T026 [P] [US1] Add integration test_add_and_view_workflow in phase-01-console/tests/integration/test_app_workflow.py

### Implementation for User Story 1

- [X] T027 [US1] Implement TaskService.add_task(title, description) in phase-01-console/src/services/task_service.py (create Task, assign ID, append to list, increment counter)
- [X] T028 [US1] Implement TaskService.get_all_tasks() in phase-01-console/src/services/task_service.py (return tasks list copy)
- [X] T029 [US1] Implement Prompts.get_task_title() in phase-01-console/src/cli/prompts.py (validate non-empty, max 200 chars, strip whitespace, reprompt on error)
- [X] T030 [US1] Implement Prompts.get_task_description() in phase-01-console/src/cli/prompts.py (optional, max 1000 chars, strip whitespace, reprompt on error)
- [X] T031 [US1] Implement Menu.handle_add_task() in phase-01-console/src/cli/menu.py (prompt for title/description, call service, display success message)
- [X] T032 [US1] Implement Menu.display_tasks() in phase-01-console/src/cli/menu.py (format per cli-interface.md: IDs, status indicators [ ]/[X], titles, descriptions, total count)
- [X] T033 [US1] Implement Menu.handle_view_tasks() in phase-01-console/src/cli/menu.py (call service, handle empty list, display formatted tasks)
- [X] T034 [US1] Connect menu choices 1 (Add Task) and 2 (View All Tasks) to handlers in phase-01-console/src/cli/menu.py

**Checkpoint**: At this point, User Story 1 should be fully functional - users can add tasks and view their complete list

---

## Phase 5: User Story 2 - Mark Tasks as Complete (Priority: P2)

**Goal**: Enable users to mark tasks as complete/incomplete and see status reflected in task list

**Independent Test**: Create 3 tasks, mark task ID 2 as complete, view list to verify [X] indicator, mark task ID 2 as incomplete, view list to verify [ ] indicator

### Tests for User Story 2 (Constitution: 80% coverage required)

- [X] T035 [P] [US2] Add test_mark_complete, test_mark_incomplete, test_mark_nonexistent_task in phase-01-console/tests/unit/test_task_service.py
- [X] T036 [P] [US2] Add integration test_mark_complete_workflow in phase-01-console/tests/integration/test_app_workflow.py

### Implementation for User Story 2

- [X] T037 [P] [US2] Implement TaskService.mark_complete(task_id) in phase-01-console/src/services/task_service.py (find task, set completed=True, return bool)
- [X] T038 [P] [US2] Implement TaskService.mark_incomplete(task_id) in phase-01-console/src/services/task_service.py (find task, set completed=False, return bool)
- [X] T039 [US2] Implement Prompts.get_task_id(operation_name) in phase-01-console/src/cli/prompts.py (validate numeric, positive, strip whitespace, reprompt on error)
- [X] T040 [US2] Implement Menu.handle_mark_complete() in phase-01-console/src/cli/menu.py (prompt for ID, call service, display success/error message)
- [X] T041 [US2] Implement Menu.handle_mark_incomplete() in phase-01-console/src/cli/menu.py (prompt for ID, call service, display success/error message)
- [X] T042 [US2] Connect menu choices 5 (Mark Complete) and 6 (Mark Incomplete) to handlers in phase-01-console/src/cli/menu.py

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently - users can add, view, and mark tasks complete/incomplete

---

## Phase 6: User Story 3 - Update Task Details (Priority: P3)

**Goal**: Enable users to update task titles and descriptions while preserving ID and status

**Independent Test**: Create task with title "Finish report" and description "Q4 summary", update to title "Finish quarterly report" and description "Q4 summary with charts", verify both changes persisted and ID/status unchanged

### Tests for User Story 3 (Constitution: 80% coverage required)

- [X] T043 [P] [US3] Add test_update_task, test_update_nonexistent_task, test_update_with_empty_title in phase-01-console/tests/unit/test_task_service.py
- [X] T044 [P] [US3] Add integration test_update_workflow in phase-01-console/tests/integration/test_app_workflow.py

### Implementation for User Story 3

- [X] T045 [US3] Implement TaskService.get_task_by_id(task_id) in phase-01-console/src/services/task_service.py (linear search, return Task or None)
- [X] T046 [US3] Implement TaskService.update_task(task_id, title, description) in phase-01-console/src/services/task_service.py (find task, update fields, validate title, return bool)
- [X] T047 [US3] Implement Prompts.get_updated_title(current_title) in phase-01-console/src/cli/prompts.py (show current, Enter to keep, validate if changed)
- [X] T048 [US3] Implement Prompts.get_updated_description(current_description) in phase-01-console/src/cli/prompts.py (show current, Enter to keep, validate if changed)
- [X] T049 [US3] Implement Menu.handle_update_task() in phase-01-console/src/cli/menu.py (prompt for ID, display current values, prompt for new values, call service, display success/error)
- [X] T050 [US3] Connect menu choice 3 (Update Task) to handler in phase-01-console/src/cli/menu.py

**Checkpoint**: All user stories should now be independently functional - users can add, view, mark complete/incomplete, and update tasks

---

## Phase 7: User Story 4 - Delete Tasks (Priority: P3)

**Goal**: Enable users to permanently remove tasks from the list while preserving other task IDs

**Independent Test**: Create 4 tasks, delete task ID 2, view list to verify only 3 tasks remain (IDs 1, 3, 4), attempt to delete task ID 2 again to verify error handling

### Tests for User Story 4 (Constitution: 80% coverage required)

- [X] T051 [P] [US4] Add test_delete_task, test_delete_nonexistent_task, test_delete_preserves_ids in phase-01-console/tests/unit/test_task_service.py
- [X] T052 [P] [US4] Add integration test_delete_workflow in phase-01-console/tests/integration/test_app_workflow.py

### Implementation for User Story 4

- [X] T053 [US4] Implement TaskService.delete_task(task_id) in phase-01-console/src/services/task_service.py (find task, remove from list, return bool, do NOT decrement counter)
- [X] T054 [US4] Implement Menu.handle_delete_task() in phase-01-console/src/cli/menu.py (prompt for ID, call service, display success/error message)
- [X] T055 [US4] Connect menu choice 4 (Delete Task) to handler in phase-01-console/src/cli/menu.py

**Checkpoint**: All 5 basic CRUD operations complete - full feature set from spec.md implemented

---

## Phase 8: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories, edge case handling, and validation

- [X] T056 [P] Implement edge case handling for empty list operations in phase-01-console/src/cli/menu.py (mark complete/incomplete, update, delete)
- [X] T057 [P] Add comprehensive error messages per cli-interface.md in phase-01-console/src/cli/prompts.py (status indicators ✓ ✗ [ ] [X])
- [X] T058 [P] Add unit tests for edge cases in phase-01-console/tests/unit/ (whitespace titles, 200-char titles, 1000-char descriptions, empty list operations)
- [X] T059 [P] Add integration test for 20-task workflow in phase-01-console/tests/integration/test_app_workflow.py (add 10, mark 5 complete, update 3, delete 2, view list)
- [X] T060 [P] Verify 80% test coverage with pytest --cov=src --cov-report=term-missing
- [X] T061 [P] Create performance test for 100 tasks in phase-01-console/tests/integration/test_app_workflow.py (verify <1 second view time)
- [X] T062 Update README.md in phase-01-console/ with usage examples and testing instructions
- [X] T063 Validate against quickstart.md manual testing checklist
- [X] T064 Run all acceptance scenarios from spec.md and verify PASS

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3-7)**: All depend on Foundational phase completion
  - User Story 5 (Application Lifecycle) should complete first as it enables testing of other stories
  - User Stories 1, 2, 3, 4 can then proceed in parallel (if staffed) or sequentially in priority order
- **Polish (Phase 8)**: Depends on all user stories being complete

### User Story Dependencies

- **User Story 5 (P1 - Application Lifecycle)**: Can start after Foundational (Phase 2) - No dependencies on other stories (foundational for all)
- **User Story 1 (P1 - Add and View)**: Can start after User Story 5 - No dependencies on other stories (core MVP functionality)
- **User Story 2 (P2 - Mark Complete)**: Can start after User Story 1 - Depends on tasks existing but independently testable
- **User Story 3 (P3 - Update)**: Can start after User Story 1 - Depends on tasks existing but independently testable
- **User Story 4 (P3 - Delete)**: Can start after User Story 1 - Depends on tasks existing but independently testable

### Within Each User Story

- Tests (if included) MUST be written and FAIL before implementation
- Model validation before service methods
- Service methods before CLI handlers
- CLI handlers before menu integration
- Story complete before moving to next priority

### Parallel Opportunities

- **Phase 1 (Setup)**: T003, T004, T005, T006 can run in parallel (different files)
- **Phase 2 (Foundational)**: T011, T012 can run in parallel (menu.py and prompts.py are independent)
- **User Story 5 Tests**: T014, T015, T016 can run in parallel (different test files)
- **User Story 1 Tests**: T024, T025, T026 can run in parallel (different test files)
- **User Story 2 Tests**: T035, T036 can run in parallel (different test files)
- **User Story 2 Implementation**: T037, T038 can run in parallel (independent service methods)
- **User Story 3 Tests**: T043, T044 can run in parallel (different test files)
- **User Story 4 Tests**: T051, T052 can run in parallel (different test files)
- **Phase 8 (Polish)**: T056, T057, T058, T059, T060, T061 can run in parallel (different concerns)
- Once Foundational phase completes, User Stories 1-4 can be worked on in parallel by different team members (after US5 establishes lifecycle)

---

## Parallel Example: User Story 1

```bash
# Launch all tests for User Story 1 together:
Task T024: "Create test_task_model.py with test_task_creation, test_title_validation, test_description_validation"
Task T025: "Create test_task_service.py with test_add_task, test_get_all_tasks, test_auto_increment_id"
Task T026: "Add integration test_add_and_view_workflow in test_app_workflow.py"

# After tests are written and failing, launch parallel implementation tasks:
Task T027: "Implement TaskService.add_task(title, description)"
Task T028: "Implement TaskService.get_all_tasks()"
# (T029-T030 can start in parallel as they're in prompts.py)
Task T029: "Implement Prompts.get_task_title()"
Task T030: "Implement Prompts.get_task_description()"
```

---

## Implementation Strategy

### MVP First (User Stories 5 + 1 Only)

1. Complete Phase 1: Setup (T001-T006)
2. Complete Phase 2: Foundational (T007-T013) - CRITICAL - blocks all stories
3. Complete Phase 3: User Story 5 - Application Lifecycle (T014-T023)
4. Complete Phase 4: User Story 1 - Add and View Tasks (T024-T034)
5. **STOP and VALIDATE**: Test User Stories 5 + 1 independently
6. Run manual testing checklist from quickstart.md
7. Verify acceptance scenarios US5 and US1 from spec.md

**MVP Scope**: Application starts, displays menu, accepts add task operations, displays task list, exits cleanly

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. Add User Story 5 → Test independently → Foundation validated
3. Add User Story 1 → Test independently → MVP ready (can add and view tasks)
4. Add User Story 2 → Test independently → Can mark tasks complete
5. Add User Story 3 → Test independently → Can update task details
6. Add User Story 4 → Test independently → Can delete tasks (full CRUD complete)
7. Add Phase 8 Polish → All edge cases handled, 80% coverage verified
8. Each story adds value without breaking previous stories

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup + Foundational together (T001-T013)
2. One developer completes User Story 5 (Application Lifecycle) first
3. Once US5 is done:
   - Developer A: User Story 1 (Add and View)
   - Developer B: User Story 2 (Mark Complete)
   - Developer C: User Story 3 (Update)
   - Developer D: User Story 4 (Delete)
4. Stories complete and integrate independently
5. Team completes Polish phase together

---

## Task Summary

- **Total Tasks**: 64
- **Setup Phase**: 6 tasks
- **Foundational Phase**: 7 tasks (BLOCKS all user stories)
- **User Story 5 (Application Lifecycle - P1)**: 10 tasks (3 tests + 7 implementation)
- **User Story 1 (Add and View - P1)**: 11 tasks (3 tests + 8 implementation)
- **User Story 2 (Mark Complete - P2)**: 8 tasks (2 tests + 6 implementation)
- **User Story 3 (Update - P3)**: 8 tasks (2 tests + 6 implementation)
- **User Story 4 (Delete - P3)**: 5 tasks (2 tests + 3 implementation)
- **Polish Phase**: 9 tasks (cross-cutting concerns)

**Parallel Opportunities**: 20 tasks marked [P] can run in parallel with other tasks in their phase

**Independent Test Criteria**:
- **US5**: Application starts, displays menu, handles invalid input, exits cleanly
- **US1**: Can add 3 tasks and view complete list with all details
- **US2**: Can mark tasks complete/incomplete and verify status indicators
- **US3**: Can update task title/description while preserving ID and status
- **US4**: Can delete tasks while preserving other task IDs

**Suggested MVP Scope**: Phase 1 (Setup) + Phase 2 (Foundational) + Phase 3 (US5) + Phase 4 (US1) = 34 tasks

---

## Notes

- [P] tasks = different files, no dependencies within the phase
- [Story] label maps task to specific user story for traceability (US1, US2, US3, US4, US5)
- Each user story should be independently completable and testable
- All tests must FAIL before implementing the corresponding functionality (TDD)
- Commit after each task or logical group of tasks
- Stop at any checkpoint to validate story independently
- Avoid: vague tasks, same file conflicts, cross-story dependencies that break independence
- Constitution requirement: Minimum 80% test coverage (pytest --cov)
- Performance requirement: All operations <1 second for lists up to 100 tasks
- Error handling: All error cases from spec.md edge cases must be covered
