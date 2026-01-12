---
id: 004
title: Phase 6 Update Task Implementation
stage: green
date: 2026-01-12
surface: agent
model: claude-sonnet-4-5-20250929
feature: 001-phase-01-console-todo
branch: master
user: PC
command: /sp.implement phase 6
labels: ["implementation", "update-task", "us3", "tdd"]
links:
  spec: ../../../specs/001-phase-01-console-todo/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - .gitignore
  - phase-01-console/tests/unit/test_task_service.py
  - phase-01-console/tests/integration/test_app_workflow.py
  - phase-01-console/src/cli/prompts.py
  - phase-01-console/src/cli/menu.py
  - phase-01-console/tests/unit/test_menu.py
  - specs/001-phase-01-console-todo/tasks.md
tests:
  - test_update_task
  - test_update_nonexistent_task
  - test_update_with_empty_title
  - test_update_title_only
  - test_update_description_only
  - test_update_workflow
---

## Prompt

User command: `/sp.implement phase 6`

User input: `phase 6`

The user requested implementation of Phase 6, which implements User Story 3 (Update Task Details - Priority P3). This phase enables users to update task titles and descriptions while preserving ID and status.

## Response snapshot

Implemented Phase 6 (User Story 3 - Update Task Details) following the TDD approach:

**Tests Created (T043-T044)**:
- Added 5 unit tests in `test_task_service.py`: test_update_task, test_update_nonexistent_task, test_update_with_empty_title, test_update_title_only, test_update_description_only
- Added integration test `test_update_workflow` in `test_app_workflow.py`
- Fixed existing test `test_handle_choice_continue` to provide mock inputs for update operation

**Implementation (T045-T050)**:
- T045-T046: TaskService methods (get_task_by_id, update_task) were already implemented in Phase 2
- T047: Implemented `get_updated_title()` in prompts.py - shows current title, validates new title, returns None if user presses Enter to keep current
- T048: Implemented `get_updated_description()` in prompts.py - shows current description, validates new description, returns None if user presses Enter to keep current
- T049: Implemented `handle_update_task()` in menu.py - prompts for ID, displays current values, prompts for updates, calls service, displays result
- T050: Menu routing already connected in Phase 2

**Project Setup**:
- Created .gitignore file with Python-specific patterns

**Results**:
- All 65 tests passing (100% pass rate)
- 85.13% test coverage (exceeds 80% Constitution requirement)
- Manual testing verified: task title and description update successfully, ID and status preserved

## Outcome

- ✅ Impact: User Story 3 fully implemented - users can now update task titles and descriptions while preserving ID and completion status
- 🧪 Tests: 65 tests passing, 85.13% coverage, added 6 new tests (5 unit + 1 integration)
- 📁 Files: Modified 6 files, created 1 file (.gitignore)
- 🔁 Next prompts: Phase 7 (US4 - Delete Tasks), Phase 8 (Polish & Cross-Cutting Concerns)
- 🧠 Reflection: Smooth implementation - service methods already existed from Phase 2, focused on prompt functions and menu handler. TDD approach caught test fixture issue early.

## Evaluation notes (flywheel)

- Failure modes observed: Test fixture `test_handle_choice_continue` needed additional mock inputs for update operation (title and description prompts). Fixed by adding '', '' to mock input sequence.
- Graders run and results (PASS/FAIL): All pytest tests PASS (65/65), coverage check PASS (85.13% > 80%)
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Continue with Phase 7 (Delete Task) - simpler implementation with fewer prompts
