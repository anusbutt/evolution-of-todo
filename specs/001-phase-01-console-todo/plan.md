# Implementation Plan: Phase 1 - Console Todo Application

**Branch**: `001-phase-01-console-todo` | **Date**: 2026-01-09 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/001-phase-01-console-todo/spec.md`

## Summary

Build an in-memory Python console todo application that allows users to manage tasks through a text-based menu interface. The application provides CRUD operations (Create, Read, Update, Delete) for tasks, status management (mark complete/incomplete), and comprehensive input validation. All data is stored in memory during the session and cleared upon application exit. This phase establishes the foundation for the 5-phase "Evolution of Todo" project.

**Primary Requirement**: Implement all 5 Basic Level features (Add, Delete, Update, View, Mark Complete) as defined in Constitution §V.

**Technical Approach**: Single Python application with modular architecture separating concerns (models, services, CLI interface). Use built-in Python data structures (list/dict) for in-memory storage. Implement a menu-driven CLI with clear prompts, input validation, and error handling.

---

## Technical Context

**Language/Version**: Python 3.13+
**Package Manager**: UV
**Primary Dependencies**: None (standard library only for Phase 1)
**Storage**: In-memory (Python list/dict)
**Testing**: pytest
**Target Platform**: Cross-platform console (Windows, macOS, Linux)
**Project Type**: Single project (console application)
**Performance Goals**: <1 second for all operations with up to 100 tasks
**Constraints**: In-memory only (no file persistence), single-user, single-session
**Scale/Scope**: Support 100+ tasks per session without performance degradation

---

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

### Phase I Requirements from Constitution

**✅ Language**: Python 3.13+ (PASS)
**✅ Package Manager**: UV (PASS)
**✅ Storage**: In-memory (list/dict) (PASS)
**✅ Interface**: CLI with text prompts (PASS)
**✅ Testing**: pytest (PASS)
**✅ Coverage**: Minimum 80% (planned in tasks phase)

### Feature Scope Validation

**✅ Basic Level Features Only** (PASS):
- Add Task ✓
- Delete Task ✓
- Update Task ✓
- View Task List ✓
- Mark Complete ✓

**✅ No Intermediate/Advanced Features** (PASS):
- No Priorities/Tags
- No Search/Filter/Sort
- No Due Dates/Reminders
- No Recurring Tasks

### Quality Standards Compliance

**✅ Code Readability** (PASS):
- Clear variable names
- Functions do ONE thing
- Max 50 lines per function (hard limit: 100)
- Comments explain WHY

**✅ Project Structure** (PASS):
- `snake_case` for Python files
- Logical module grouping
- Separation of concerns

**✅ Error Handling** (PASS):
- Explicit error messages
- No silent failures
- User-friendly error guidance

**✅ Testing Requirements** (PASS):
- Unit tests for all task operations
- Edge cases covered (empty list, invalid IDs, boundary conditions)
- Target: 80% coverage

**Constitution Check Result**: ✅ **PASS** - All gates satisfied, no violations

---

## Project Structure

### Documentation (this feature)

```text
specs/001-phase-01-console-todo/
├── spec.md              # Feature requirements (complete)
├── plan.md              # This file (/sp.plan command output)
├── research.md          # Phase 0 output (Python best practices, design patterns)
├── data-model.md        # Phase 1 output (Task entity definition)
├── quickstart.md        # Phase 1 output (Setup and usage guide)
├── contracts/           # Phase 1 output (CLI interface contract)
│   └── cli-interface.md
└── tasks.md             # Phase 2 output (/sp.tasks command - NOT created by /sp.plan)
```

### Source Code (repository root)

```text
phase-01-console/
├── src/
│   ├── __init__.py
│   ├── models/
│   │   ├── __init__.py
│   │   └── task.py           # Task data class
│   ├── services/
│   │   ├── __init__.py
│   │   └── task_service.py   # Business logic (CRUD operations)
│   ├── cli/
│   │   ├── __init__.py
│   │   ├── menu.py           # Menu display and navigation
│   │   └── prompts.py        # User input collection and validation
│   └── main.py               # Application entry point
├── tests/
│   ├── __init__.py
│   ├── unit/
│   │   ├── __init__.py
│   │   ├── test_task_model.py
│   │   └── test_task_service.py
│   └── integration/
│       ├── __init__.py
│       └── test_app_workflow.py
├── pyproject.toml            # UV project configuration
├── README.md                 # Project overview and setup
└── .gitignore                # Python-specific ignores

```

**Structure Decision**: Single project structure (Option 1) selected because:
- Console application with no web/mobile components
- Self-contained Python app with clear separation of concerns
- `models/` for data definitions (Task)
- `services/` for business logic (TaskService)
- `cli/` for user interface (Menu, Prompts)
- `main.py` as entry point orchestrating CLI and services
- Standard test structure (`unit/`, `integration/`) for pytest

**Note**: This structure is specific to Phase 1. Future phases will add parallel directories (`phase-02-web/`, `phase-03-chatbot/`, etc.) as per user requirement: "every phase should have a separate folder."

---

## Complexity Tracking

> **No violations**: Constitution check passed completely. No additional complexity needed.

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| N/A | N/A | N/A |

---

## Phase 0: Research & Design Decisions

### Research Topics

1. **Python 3.13+ Best Practices for Console Applications**
   - Input/output handling patterns
   - Error handling conventions
   - Project structure for maintainability

2. **In-Memory Data Storage Patterns**
   - List vs dict tradeoffs for task storage
   - ID generation strategies
   - Data integrity in memory

3. **CLI Interface Design Patterns**
   - Menu-driven navigation
   - Input validation techniques
   - User-friendly error messages

4. **Testing Strategies for Console Apps**
   - Mocking user input (stdin)
   - Capturing console output (stdout/stderr)
   - Integration test patterns for CLI workflows

### Research Output

See [research.md](./research.md) for detailed findings and rationale for all technical decisions.

---

## Phase 1: Detailed Design

### Data Model

See [data-model.md](./data-model.md) for complete entity definitions.

**Summary**: Single `Task` entity with fields:
- `id`: int (auto-increment)
- `title`: str (1-200 chars, required)
- `description`: str (0-1000 chars, optional)
- `completed`: bool (default: False)

### CLI Interface Contract

See [contracts/cli-interface.md](./contracts/cli-interface.md) for complete interface specification.

**Summary**: Menu-driven interface with 7 options:
1. Add Task
2. View All Tasks
3. Update Task
4. Delete Task
5. Mark Task Complete
6. Mark Task Incomplete
7. Exit

Each operation includes:
- Input prompts with validation
- Success/error messages
- Return to main menu

### Quickstart Guide

See [quickstart.md](./quickstart.md) for setup and usage instructions.

**Summary**:
- UV installation and project setup
- Running the application
- Example workflows
- Troubleshooting common issues

---

## Architecture & Component Design

### Component Responsibilities

#### 1. Task Model (`src/models/task.py`)
**Responsibility**: Data structure representing a single task

**Attributes**:
- `id`: Unique identifier (int)
- `title`: Task name (str, 1-200 chars)
- `description`: Optional details (str, 0-1000 chars)
- `completed`: Status flag (bool)

**Methods**:
- `__init__()`: Initialize task with validation
- `__repr__()`: String representation for debugging
- `to_dict()`: Serialize to dictionary for display

**Validation**:
- Title: non-empty, not whitespace-only, max 200 chars
- Description: max 1000 chars (empty allowed)

#### 2. Task Service (`src/services/task_service.py`)
**Responsibility**: Business logic for task management

**Data Storage**: In-memory list of Task objects

**Methods**:
- `add_task(title, description)` → Task | ValidationError
- `get_all_tasks()` → List[Task]
- `get_task_by_id(task_id)` → Task | None
- `update_task(task_id, title, description)` → Task | ValidationError
- `delete_task(task_id)` → bool
- `mark_complete(task_id)` → bool
- `mark_incomplete(task_id)` → bool

**ID Management**: Auto-increment counter (starts at 1, never reused)

**Error Handling**:
- Raise `ValueError` for validation errors (empty title, invalid IDs)
- Return `None` or `False` for not-found scenarios

#### 3. Menu Interface (`src/cli/menu.py`)
**Responsibility**: Display menu and route user choices

**Methods**:
- `display_menu()`: Print menu options
- `get_user_choice()` → int: Capture and validate menu selection
- `handle_choice(choice)`: Route to appropriate handler
- `run()`: Main application loop

**Behavior**:
- Display menu after each operation
- Loop until user selects "Exit"
- Catch invalid menu choices (non-numeric, out-of-range)

#### 4. Prompts Interface (`src/cli/prompts.py`)
**Responsibility**: Collect and validate user inputs

**Methods**:
- `get_task_title()` → str: Prompt for title with validation
- `get_task_description()` → str: Prompt for description (optional)
- `get_task_id()` → int: Prompt for ID with validation
- `display_tasks(tasks)`: Format and print task list
- `display_message(msg, type)`: Print success/error/info messages

**Input Validation**:
- Strip whitespace from all inputs
- Reject empty/whitespace-only titles
- Validate task IDs (numeric, positive)
- Handle KeyboardInterrupt (Ctrl+C) gracefully

#### 5. Main Application (`src/main.py`)
**Responsibility**: Application entry point

**Flow**:
1. Initialize TaskService
2. Display welcome message
3. Start Menu loop
4. Handle graceful shutdown (Ctrl+C, Exit choice)
5. Display farewell message

---

## Data Flow

### Add Task Flow
```
User → Menu (choice 1) → Prompts.get_task_title() → Prompts.get_task_description()
     → TaskService.add_task() → Task() → TaskService.tasks.append()
     → Prompts.display_message("✓ Task added") → Menu (redisplay)
```

### View Tasks Flow
```
User → Menu (choice 2) → TaskService.get_all_tasks()
     → Prompts.display_tasks() → [Print formatted list]
     → Menu (redisplay)
```

### Mark Complete Flow
```
User → Menu (choice 5) → Prompts.get_task_id()
     → TaskService.mark_complete(id) → Find task → Set completed=True
     → Prompts.display_message("✓ Task marked complete") → Menu (redisplay)
```

### Error Flow (Invalid ID)
```
User → Menu (choice 5) → Prompts.get_task_id() → TaskService.mark_complete(999)
     → Task not found → Return False
     → Prompts.display_message("✗ Task 999 not found", type="error")
     → Menu (redisplay)
```

---

## Error Handling Strategy

### Validation Errors
- **Empty Title**: "Task title cannot be empty or whitespace only"
- **Title Too Long**: "Task title must be 200 characters or less"
- **Description Too Long**: "Task description must be 1000 characters or less"

### Operational Errors
- **Task Not Found**: "Task with ID {id} not found"
- **Invalid Task ID**: "Invalid input. Please enter a numeric task ID"
- **Negative Task ID**: "Invalid task ID. Please enter a positive number"

### Menu Errors
- **Invalid Choice**: "Invalid choice. Please select a number between 1 and 7"
- **Non-Numeric Input**: "Please enter a number"

### System Errors
- **KeyboardInterrupt (Ctrl+C)**: Graceful shutdown with "Goodbye! Your session has ended."
- **Unexpected Errors**: Log to stderr, display generic error, return to menu

---

## Testing Strategy

### Unit Tests (`tests/unit/`)

**test_task_model.py**:
- Task creation with valid/invalid data
- Title validation (empty, whitespace, max length)
- Description validation (max length)
- to_dict() serialization

**test_task_service.py**:
- Add task (valid, duplicate IDs, validation errors)
- Get all tasks (empty list, populated list)
- Get task by ID (existing, non-existent)
- Update task (title only, description only, both, validation errors)
- Delete task (existing, non-existent, preserve IDs)
- Mark complete/incomplete (existing, non-existent, toggle)

### Integration Tests (`tests/integration/`)

**test_app_workflow.py**:
- Complete user journeys from spec (User Stories 1-5)
- Add → View → Mark Complete → View workflow
- Add → Update → Delete → View workflow
- Edge cases (empty list operations, 1000 tasks, invalid inputs)

### Coverage Target
- **Minimum**: 80% (per Constitution)
- **Goal**: 90%+ for critical paths (task service, validation logic)

### Test Execution
```bash
# Run all tests
uv run pytest

# Run with coverage
uv run pytest --cov=src --cov-report=term-missing

# Run specific test file
uv run pytest tests/unit/test_task_service.py -v
```

---

## Performance Considerations

### Goals (from spec SC-003, FR-019, FR-020)
- Support at least 100 tasks without performance degradation
- All operations complete in <1 second for lists up to 100 tasks
- Display all tasks in <1 second

### Optimization Strategies
- **Task Lookup**: Use list with linear search (acceptable for 100 tasks, O(n) = ~100 ops)
- **ID Generation**: Simple counter increment (O(1))
- **Display**: Stream output line-by-line (no buffering delays)
- **Memory**: Estimate ~1KB per task → 100 tasks = ~100KB (negligible)

### Performance Testing
- Create 100 tasks and measure operation times
- Verify <1 second for:
  - add_task() × 100
  - get_all_tasks() with 100 tasks
  - mark_complete() on task #50
  - delete_task() on task #50

**Future Optimization** (Phase II+):
- If task count grows >1000, consider dict lookup by ID (O(1))
- For Phase 1, simplicity > premature optimization

---

## Security Considerations

### Input Validation
- **SQL Injection**: N/A (no database in Phase 1)
- **Command Injection**: N/A (no shell commands executed)
- **Buffer Overflow**: Prevented by max-length validation (title: 200, description: 1000)
- **Path Traversal**: N/A (no file operations)

### Error Information Disclosure
- Do not expose internal paths or stack traces to users
- Log detailed errors to stderr for debugging (dev only)
- Display generic user-friendly messages

### Resource Limits
- Max task count: Not enforced (rely on system memory limits)
- Max string lengths: Enforced (title: 200, description: 1000)
- Graceful degradation if memory exhausted (system-level)

**Note**: Phase 1 has minimal security surface (single-user console, no network, no persistence). Security becomes critical in Phase II (web + auth) and beyond.

---

## Development Workflow

### Setup
1. Install UV: `curl -LsSf https://astral.sh/uv/install.sh | sh`
2. Clone repository: `git clone <repo> && cd hackathon_II`
3. Checkout branch: `git checkout 001-phase-01-console-todo`
4. Initialize project: `cd phase-01-console && uv sync`

### Development Cycle
1. Read task from `tasks.md` (created by `/sp.tasks`)
2. Write test first (TDD per Constitution if specified)
3. Implement feature in appropriate module
4. Run tests: `uv run pytest`
5. Verify coverage: `uv run pytest --cov=src`
6. Commit with task reference: `git commit -m "[Task T-001] Add Task model"`
7. Repeat for next task

### Manual Testing
```bash
# Run application
uv run python src/main.py

# Test workflow:
# 1. Add 3 tasks
# 2. View list
# 3. Mark task 2 complete
# 4. View list (verify [X] indicator)
# 5. Update task 1 title
# 6. Delete task 3
# 7. View list (verify 2 tasks remain)
# 8. Exit
```

---

## Future Phase Preparation

### Phase II Considerations (Not Implemented Yet)
- **Persistence**: Replace in-memory list with SQLModel + Neon DB
- **Multi-user**: Add `user_id` to Task model
- **Web Interface**: Add REST API endpoints, Next.js frontend
- **Authentication**: Integrate Better Auth (JWT)

### Code Migration Strategy
- Core `Task` model can be adapted to SQLModel with minimal changes
- `TaskService` business logic remains largely unchanged (swap storage layer)
- CLI can be preserved as alternative interface alongside web UI

### Architectural Decisions for Phase II
- **Monorepo Structure**: Add `phase-02-web/` alongside `phase-01-console/`
- **Shared Code**: Consider extracting common logic to `shared/` if duplication emerges
- **Database Schema**: Design in Phase II plan (users, tasks tables)

**Important**: Do NOT implement Phase II features in Phase I. Maintain strict phase boundaries per Constitution §IV.

---

## Appendix: Key Decisions

### Decision 1: No External Dependencies
**Rationale**: Phase 1 requirements achievable with Python standard library. Avoids dependency management complexity in foundation phase.

**Alternatives Considered**:
- Click/Typer for CLI: Rejected (overkill for simple menu)
- Pydantic for validation: Rejected (deferred to Phase II with FastAPI)

### Decision 2: List Storage for Tasks
**Rationale**: Simple, performant for <100 tasks, easy to test.

**Alternatives Considered**:
- Dict with ID keys: Rejected (premature optimization, adds complexity)
- Separate completed/incomplete lists: Rejected (complicates operations)

### Decision 3: Menu-Driven Interface
**Rationale**: Clear, testable, matches spec requirements for "text-based menu".

**Alternatives Considered**:
- Command-line arguments (`todo add "Buy milk"`): Rejected (spec requires interactive menu)
- REPL-style commands: Rejected (more complex to implement and test)

### Decision 4: Separate Concerns (Models/Services/CLI)
**Rationale**: Maintainability, testability, prepares for Phase II migration.

**Alternatives Considered**:
- Single-file monolith: Rejected (poor maintainability, hard to test)
- Layered architecture with repositories: Rejected (over-engineered for Phase 1)

---

**Plan Status**: ✅ Complete - Ready for `/sp.tasks` command

**Next Steps**:
1. Review this plan for architectural approval
2. Run `/sp.tasks` to generate task breakdown
3. Begin implementation following SDD loop (tasks → code)
