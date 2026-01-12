---
id: 002
title: Phase 1 Console Todo Plan
stage: plan
date: 2026-01-09
surface: agent
model: claude-sonnet-4-5-20250929
feature: 001-phase-01-console-todo
branch: 001-phase-01-console-todo
user: Architect
command: /sp.plan
labels: ["phase-1", "console-app", "todo", "architecture", "design", "python", "in-memory", "cli"]
links:
  spec: specs/001-phase-01-console-todo/spec.md
  ticket: null
  adr: null
  pr: null
files:
 - specs/001-phase-01-console-todo/plan.md
 - specs/001-phase-01-console-todo/research.md
 - specs/001-phase-01-console-todo/data-model.md
 - specs/001-phase-01-console-todo/contracts/cli-interface.md
 - specs/001-phase-01-console-todo/quickstart.md
 - CLAUDE.md
tests:
 - None (planning phase - test strategy defined)
---

## Prompt

User invoked `/sp.plan` to generate implementation plan for Phase 1: Console Todo Application.

**Input Context**:
- Feature: 001-phase-01-console-todo
- Spec: `specs/001-phase-01-console-todo/spec.md` (5 user stories, 23 acceptance scenarios, 20 functional requirements)
- Constitution: `.specify/memory/constitution.md` (7 core principles, tech stack constraints)

## Response snapshot

Successfully created comprehensive implementation plan for Phase 1: Console Todo Application.

**Plan Details**:

**Technical Context**:
- Language: Python 3.13+
- Package Manager: UV
- Storage: In-memory (Python list)
- Testing: pytest with unittest.mock
- Coverage Target: Minimum 80%
- No external dependencies (standard library only)

**Constitution Check**: ✅ PASS
- All Phase 1 technology requirements satisfied
- No violations of core principles
- SDD loop enforced (spec → plan → tasks → implementation)

**Project Structure**:
```
phase-01-console/
├── src/
│   ├── models/
│   │   └── task.py           # Task data class
│   ├── services/
│   │   └── task_service.py   # Business logic (CRUD)
│   ├── cli/
│   │   ├── menu.py           # Menu display
│   │   └── prompts.py        # Input validation
│   └── main.py               # Entry point
├── tests/
│   ├── unit/
│   │   ├── test_task_model.py
│   │   └── test_task_service.py
│   └── integration/
│       └── test_app_workflow.py
```

**Component Design** (5 components):
1. **Task Model**: Data structure with validation (id, title, description, completed)
2. **Task Service**: Business logic with 7 CRUD methods (add, get_all, get_by_id, update, delete, mark_complete, mark_incomplete)
3. **Menu**: Navigation and display (display_menu, handle_choice, main loop)
4. **Prompts**: User input collection and validation (get_menu_choice, get_task_title, get_task_description, get_task_id)
5. **Main**: Application orchestration and error handling

**Data Flow Diagrams**:
- Add Task: User input → Prompts validation → Service creates Task → Menu confirms
- View Tasks: User choice → Service retrieves list → Menu formats display
- Mark Complete: User input ID → Service updates status → Menu confirms
- Error Handling: Invalid input → Prompts catch → Display error → Reprompt

**Error Handling Strategy**:
- **Validation Errors**: Model raises ValueError (title empty/too long, description too long)
- **Operational Errors**: Service returns None/False (task not found)
- **Menu Errors**: Prompts reprompt on invalid input (non-numeric, out-of-range)
- **System Errors**: Main catches KeyboardInterrupt for graceful exit

**Testing Strategy**:
- **Unit Tests**: Test each component in isolation (12 test files planned)
- **Integration Tests**: Test complete workflows (6 scenarios: add→view, mark→view, update→view, delete→view, error paths, exit)
- **Mocking**: Use unittest.mock.patch for stdin/stdout
- **Coverage**: pytest-cov with --cov=src flag, target 80%+

**Performance Considerations**:
- List-based storage acceptable for n≤100 tasks (O(n) operations <1ms)
- No premature optimization (YAGNI principle)
- Benchmark target: View 100 tasks in <1 second

**Security Considerations**:
- Input validation at prompt layer (prevent injection, validate types)
- No command execution (pure text input/output)
- Error message sanitization (no stack traces exposed)
- Resource limits (title 200 chars, description 1000 chars)

**Key Architectural Decisions** (4 decisions documented):
1. **List-based storage**: Simple, preserves order, performant at target scale
2. **Menu-driven CLI**: Matches spec requirement, testable, user-friendly
3. **Separation of concerns**: Models/Services/CLI for maintainability
4. **Standard library only**: No dependencies for Phase 1 simplicity

**Phase II Migration Strategy**:
- Task model → SQLModel (add user_id, timestamps)
- TaskService → SQLModel queries (minimal method changes)
- CLI → FastAPI endpoints (reuse validation logic)
- Testing → API integration tests (reuse test scenarios)

**Supporting Documents Created**:

1. **research.md** (195 lines): Technical decisions and alternatives considered
   - Python 3.13+ best practices
   - In-memory storage patterns (list vs dict analysis)
   - CLI design patterns (menu-driven vs REPL)
   - Testing strategies (pytest + mock)
   - Error handling conventions
   - Project structure rationale

2. **data-model.md** (259 lines): Complete Task entity definition
   - Attributes: id (int), title (str 1-200), description (str 0-1000), completed (bool)
   - Validation rules with error messages
   - State transitions (Created → Incomplete ↔ Complete → Deleted)
   - Serialization methods (to_dict, __repr__)
   - In-memory storage strategy (list with auto-increment IDs)
   - Performance characteristics (O(n) operations)
   - Phase II migration path (SQLModel conversion)

3. **contracts/cli-interface.md** (503 lines): Complete UI specification
   - Application lifecycle (startup, shutdown)
   - Main menu format (7 numbered options)
   - All 7 operations with detailed flows:
     - Operation 1: Add Task (prompts, success, errors)
     - Operation 2: View All Tasks (formatting, empty state)
     - Operation 3: Update Task (current values, Enter to keep)
     - Operation 4: Delete Task (confirmation)
     - Operation 5: Mark Complete (status change)
     - Operation 6: Mark Incomplete (status toggle)
     - Operation 7: Exit (graceful shutdown)
   - Status indicators (✓ ✗ [ ] [X])
   - Error message patterns (validation, operational, system)
   - Input handling standards (whitespace, case sensitivity, UTF-8)
   - Keyboard interrupt handling (Ctrl+C)
   - Performance requirements (<1 second response times)
   - Testing contract (mock patterns, test scenarios)

4. **quickstart.md** (366 lines): Setup and usage guide
   - Prerequisites (Python 3.13+, UV, Git)
   - Installation steps (5 steps: install UV → clone → create venv → activate → install deps)
   - Running the application (uv run python src/main.py)
   - 4 example workflows (add/view, mark complete, update, delete)
   - Running tests (pytest commands, coverage reports)
   - Development workflow (branch → change → test → commit → push)
   - Project structure overview
   - Troubleshooting (7 common issues with solutions)
   - Performance benchmarks (expected response times)
   - Manual testing checklist (40 test cases)

**Agent Context Update**:
- Updated `CLAUDE.md` with Phase 1 technologies:
  - Language: Python 3.13+
  - Framework: None (standard library only for Phase 1)
  - Database: In-memory (Python list/dict)

## Outcome

- ✅ Impact: Complete technical implementation plan for Phase 1 console todo app. All architectural decisions documented with rationale. Constitution compliance verified. Testing strategy defined with 80% coverage target. Ready for task breakdown phase.
- 🧪 Tests: N/A (planning phase - test strategy comprehensively defined in plan.md with unit/integration test patterns)
- 📁 Files: 6 files created/modified (plan.md: 556 lines, research.md: 195 lines, data-model.md: 259 lines, cli-interface.md: 503 lines, quickstart.md: 366 lines, CLAUDE.md: updated)
- 🔁 Next prompts: `/sp.tasks` to generate testable task breakdown from plan.md (awaiting user approval)
- 🧠 Reflection: Plan strictly separates HOW (technical architecture) from WHAT (spec requirements). All decisions traced to constitution principles or spec requirements. Phase II migration path documented to ensure forward compatibility. No implementation details in spec confirmed.

## Evaluation notes (flywheel)

- Failure modes observed: PowerShell script partial failure (branch created, argument parsing error) - resolved by manual directory creation. Agent context update succeeded on retry.
- Graders run and results (PASS/FAIL): Manual validation against plan checklist - PASS (constitution check ✅, all mandatory sections complete, no [NEEDS CLARIFICATION] markers)
- Prompt variant (if applicable): N/A (first plan for Phase 1)
- Next experiment (smallest change to try): N/A - plan complete and approved, awaiting user authorization to proceed to `/sp.tasks`
