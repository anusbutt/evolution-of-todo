# Research: Phase 1 - Console Todo Application

**Date**: 2026-01-09
**Feature**: 001-phase-01-console-todo
**Purpose**: Research technical decisions and best practices for Python console application

---

## 1. Python 3.13+ Best Practices for Console Applications

### Decision: Use standard library with modular architecture

**Research Findings**:
- Python 3.13+ supports enhanced error messages and performance improvements
- Standard library (`input()`, `print()`, built-in data structures) sufficient for console I/O
- Modular structure (models/services/cli) improves maintainability and testability
- Type hints improve code clarity without runtime overhead

**Rationale**:
- No external dependencies reduces complexity
- Standard library stable and well-documented
- Modular architecture prepares for Phase II migration

**Alternatives Considered**:
- **Rich/Textual**: Rejected (overkill for simple menu, adds dependency)
- **Click/Typer**: Rejected (designed for command-line args, not interactive menus)
- **Curses**: Rejected (platform-specific, unnecessary complexity)

**Best Practices Adopted**:
- Use `input().strip()` to handle whitespace
- Catch `KeyboardInterrupt` for graceful Ctrl+C handling
- Use `sys.stdout`/`sys.stderr` for output control
- Implement `__repr__()` for debugging

---

## 2. In-Memory Data Storage Patterns

### Decision: Use Python list to store Task objects

**Research Findings**:
- **List**: O(n) lookup by ID, simple append/remove, preserves order
- **Dict**: O(1) lookup by ID key, requires manual ordering
- **Deque**: O(1) append/pop but O(n) lookup/delete by ID

**Rationale**:
- Phase 1 spec requires ≤100 tasks → O(n) acceptable (n=100 is trivial)
- List naturally preserves creation order (spec requirement)
- Simpler code → easier to test and maintain
- Premature optimization avoided (YAGNI principle)

**Alternatives Considered**:
- **Dict with {id: Task}**: Rejected (adds complexity for negligible performance gain at n=100)
- **Two lists (complete/incomplete)**: Rejected (complicates operations, violates single source of truth)

**ID Generation Strategy**:
- **Decision**: Simple counter (starts at 1, increments, never reused)
- **Rationale**: Predictable, testable, matches spec requirement "preserve original IDs"
- **Alternative Rejected**: UUID/random IDs (overkill for single-session app)

---

## 3. CLI Interface Design Patterns

### Decision: Menu-driven interface with numbered choices

**Research Findings**:
- **Menu-driven**: Clear navigation, easy to test, matches spec requirement
- **Command-line args**: Better for scriptable tools, not interactive apps
- **REPL/shell-style**: More flexible but harder to test and validate

**Rationale**:
- Spec explicitly requires "text-based menu of available operations"
- Numbered choices (1-7) easy for users to select
- Loop-based flow (display menu → execute → return to menu) natural for console apps
- Testable via stdin/stdout mocking

**Alternatives Considered**:
- **CLI arguments** (`todo add "Buy milk"`): Rejected (spec requires interactive menu)
- **REPL** (`> add task ...`): Rejected (more complex parsing, unclear error handling)

**Input Validation Pattern**:
- **Decision**: Validate at input collection (prompts.py), not in service layer
- **Rationale**: Separation of concerns (UI validates format, service validates business rules)

---

## 4. Testing Strategies for Console Apps

### Decision: Use pytest with unittest.mock for stdin/stdout

**Research Findings**:
- **Mocking stdin**: Use `unittest.mock.patch('builtins.input', return_value="value")`
- **Capturing stdout**: Use `pytest capsys` fixture or `io.StringIO`
- **Integration tests**: Mock full user workflows with sequences of inputs

**Rationale**:
- pytest widely adopted, excellent documentation
- Mock library standard, no additional dependencies
- Capsys fixture simple for output verification

**Alternatives Considered**:
- **Subprocess testing**: Rejected (slower, harder to debug)
- **Manual testing only**: Rejected (Constitution requires 80% coverage)

**Coverage Strategy**:
- **Unit tests**: Test each function in isolation (models, service methods)
- **Integration tests**: Test complete workflows (add → view → mark → delete)
- **Edge case tests**: Empty list, invalid IDs, boundary values (200-char titles)

---

## 5. Error Handling Conventions

### Decision: Use exceptions for validation, return None/False for not-found

**Research Findings**:
- **Exceptions**: Appropriate for exceptional conditions (invalid input, validation failures)
- **Return values**: Appropriate for expected scenarios (task not found)
- **Python convention**: "Easier to ask forgiveness than permission" (EAFP)

**Rationale**:
- Validation errors are exceptional → raise `ValueError`
- Task not found is expected → return `None` or `False`
- Clear error messages per Constitution requirement

**Error Message Standards**:
- **Validation**: "Task title cannot be empty or whitespace only"
- **Not Found**: "Task with ID {id} not found"
- **User Guidance**: "Invalid choice. Please select a number between 1 and 7"

---

## 6. Project Structure for Maintainability

### Decision: Separate models/services/cli with single responsibility

**Research Findings**:
- **Models**: Data structures only (Task class)
- **Services**: Business logic (TaskService with CRUD operations)
- **CLI**: User interface (Menu for navigation, Prompts for I/O)
- **Main**: Entry point orchestration

**Rationale**:
- Single Responsibility Principle → easier to test and modify
- Prepare for Phase II: models → SQLModel, services reusable, add web CLI
- Clear boundaries → parallel development possible

**Alternatives Considered**:
- **Single file monolith**: Rejected (poor maintainability, hard to test)
- **Layered architecture with repositories**: Rejected (over-engineered for Phase 1)

---

## 7. Performance Optimization Guidelines

### Decision: Optimize only if needed, measure first

**Research Findings**:
- **Premature optimization**: Root of all evil (Donald Knuth)
- **Phase 1 scale**: 100 tasks = trivial for modern hardware
- **Measurement**: Use `time.perf_counter()` for benchmarks

**Rationale**:
- Spec requires <1 second for 100 tasks → easily achievable with list
- Simplicity > performance at this scale
- Defer optimization to Phase II if needed

**Benchmark Plan**:
- Create 100 tasks and measure:
  - `add_task()` average time
  - `get_all_tasks()` total time
  - `mark_complete()` on task #50
- Target: All operations <10ms (well under 1-second budget)

---

## Summary: Key Technical Decisions

| Decision Area | Chosen Approach | Primary Rationale |
|---------------|-----------------|-------------------|
| **Language** | Python 3.13+ standard library | Simple, no dependencies, future-proof |
| **Storage** | List of Task objects | Preserves order, simple, performant at n=100 |
| **CLI Pattern** | Menu-driven with numbered choices | Matches spec, testable, user-friendly |
| **Testing** | pytest + unittest.mock | Industry standard, excellent tooling |
| **Error Handling** | Exceptions for validation, None for not-found | Python convention, clear semantics |
| **Project Structure** | Models/Services/CLI separation | Maintainability, testability, Phase II prep |
| **Performance** | Measure before optimizing | YAGNI, sufficient for Phase 1 scale |

---

**Research Status**: ✅ Complete
**All NEEDS CLARIFICATION resolved**: Yes
**Ready for**: Phase 1 Design (data-model.md, contracts/, quickstart.md)
