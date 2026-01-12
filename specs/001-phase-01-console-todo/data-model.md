# Data Model: Phase 1 - Console Todo Application

**Date**: 2026-01-09
**Feature**: 001-phase-01-console-todo
**Purpose**: Define entity structure and validation rules for Phase 1

---

## Entity: Task

### Overview
Represents a single todo item in the application. Each task has a unique identifier, required title, optional description, and completion status.

### Attributes

| Attribute | Type | Constraints | Default | Required | Description |
|-----------|------|-------------|---------|----------|-------------|
| `id` | int | Positive integer, unique, auto-incremented | Auto-assigned | Yes | Unique identifier (starts at 1, increments, never reused) |
| `title` | str | 1-200 characters, non-empty, not whitespace-only | None | Yes | Task name/summary |
| `description` | str | 0-1000 characters | Empty string | No | Optional detailed information |
| `completed` | bool | True or False | False | Yes | Completion status (False = incomplete, True = complete) |

### Validation Rules

#### Title Validation
- **Non-empty**: Must contain at least one character after stripping whitespace
- **Not whitespace-only**: String like "   " is invalid
- **Max length**: 200 characters (enforced after strip())
- **Error messages**:
  - Empty: "Task title cannot be empty or whitespace only"
  - Too long: "Task title must be 200 characters or less"

#### Description Validation
- **Optional**: Can be empty string
- **Max length**: 1000 characters
- **Error message**:
  - Too long: "Task description must be 1000 characters or less"

#### ID Validation
- **Auto-generated**: User cannot set ID directly
- **Uniqueness**: Managed by TaskService auto-increment counter
- **Immutable**: Once assigned, ID never changes
- **Non-reusable**: Deleted task IDs are not recycled

#### Completed Validation
- **Boolean only**: Must be True or False
- **Default**: False (incomplete) on task creation
- **Toggleable**: Can change between True ↔ False

### State Transitions

```
[Created] → completed=False (initial state)
    ↓
[Incomplete] ←→ [Complete] (toggle via mark_complete/mark_incomplete)
    ↓
[Deleted] (removed from list, ID not reused)
```

**Valid Transitions**:
- Created → Incomplete (automatic on add_task)
- Incomplete → Complete (mark_complete)
- Complete → Incomplete (mark_incomplete)
- Any state → Deleted (delete_task)

**Invalid Transitions**: None (all state changes are valid)

### Example Instances

#### Valid Task (Minimal)
```python
Task(id=1, title="Buy groceries", description="", completed=False)
```

#### Valid Task (Full)
```python
Task(
    id=5,
    title="Finish quarterly report",
    description="Include Q4 summary, charts, and budget forecast",
    completed=False
)
```

#### Invalid Task Examples
```python
# Empty title
Task(id=1, title="", description="", completed=False)  # ValueError

# Whitespace-only title
Task(id=1, title="   ", description="", completed=False)  # ValueError

# Title too long (>200 chars)
Task(id=1, title="x" * 201, description="", completed=False)  # ValueError

# Description too long (>1000 chars)
Task(id=1, title="Valid", description="x" * 1001, completed=False)  # ValueError
```

### Serialization

#### to_dict() Method
Converts Task to dictionary for display/testing:
```python
{
    "id": 1,
    "title": "Buy groceries",
    "description": "Milk, eggs, bread",
    "completed": False
}
```

#### __repr__() Method
String representation for debugging:
```python
"Task(id=1, title='Buy groceries', completed=False)"
```

### Relationships

**Phase 1**: No relationships (single entity, no foreign keys)

**Phase 2+**: Will add relationship to User entity:
- `Task.user_id` → `User.id` (foreign key)
- One user → Many tasks (one-to-many)

---

## Data Storage Strategy

### In-Memory Storage
- **Container**: Python list (`List[Task]`)
- **Location**: `TaskService.tasks` attribute
- **Lifetime**: Session-only (cleared on app exit)
- **Capacity**: Unlimited (relies on system memory)

### ID Generation
- **Strategy**: Auto-increment counter
- **Implementation**: `TaskService.next_id` attribute (int, starts at 1)
- **Behavior**:
  ```python
  # Add first task
  task1 = Task(id=1, ...)  # next_id becomes 2

  # Add second task
  task2 = Task(id=2, ...)  # next_id becomes 3

  # Delete task 2
  delete_task(2)  # next_id stays 3 (ID not reused)

  # Add third task
  task3 = Task(id=3, ...)  # next_id becomes 4
  ```

### Indexing Strategy
- **Primary lookup**: Linear search by ID (`O(n)`)
- **Justification**: Acceptable for n≤100 tasks (spec requirement)
- **Future optimization**: If Phase 2+ exceeds 1000 tasks, consider dict-based index

---

## Validation Logic Location

### Model-Level Validation (Task class)
- Title: non-empty, max 200 chars
- Description: max 1000 chars
- Raise `ValueError` on violation

### Service-Level Validation (TaskService)
- ID existence checks (get_task_by_id)
- Business rules (e.g., can't update non-existent task)
- Return `None` or `False` on failure

### CLI-Level Validation (Prompts)
- Input type checks (numeric ID, non-empty strings)
- User-friendly error messages
- Reprompt on invalid input

**Principle**: Validate early (at input), fail fast (in model), provide context (in CLI)

---

## Data Integrity Rules

### Rule 1: ID Uniqueness
- **Enforcement**: TaskService manages IDs via auto-increment
- **Guarantee**: No two tasks ever have the same ID within a session

### Rule 2: ID Immutability
- **Enforcement**: Task.id is set on creation, never modified
- **Guarantee**: update_task() cannot change task ID

### Rule 3: ID Non-Reusability
- **Enforcement**: Deleted task IDs not recycled (counter never decrements)
- **Guarantee**: Historical integrity (ID 5 always refers to the same logical task)

### Rule 4: Title Required
- **Enforcement**: Model validation raises ValueError on empty title
- **Guarantee**: Every task in TaskService.tasks has valid title

### Rule 5: Status Boolean
- **Enforcement**: Type hints + boolean operations only
- **Guarantee**: completed is always True or False (no None, no strings)

---

## Performance Characteristics

| Operation | Complexity | Notes |
|-----------|------------|-------|
| Add task | O(1) | Append to list + increment counter |
| Get all tasks | O(n) | Return entire list |
| Get task by ID | O(n) | Linear search through list |
| Update task | O(n) | Linear search + attribute update |
| Delete task | O(n) | Linear search + list.remove() |
| Mark complete | O(n) | Linear search + boolean flip |

**Acceptable for Phase 1**: All operations <1ms for n≤100 tasks

---

## Migration Path to Phase 2

### Changes Required for SQLModel/Neon DB

```python
# Phase 1 (Python dataclass)
@dataclass
class Task:
    id: int
    title: str
    description: str
    completed: bool

# Phase 2 (SQLModel)
class Task(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id")  # NEW
    title: str = Field(min_length=1, max_length=200)
    description: str = Field(default="", max_length=1000)
    completed: bool = Field(default=False)
    created_at: datetime = Field(default_factory=datetime.utcnow)  # NEW
    updated_at: datetime = Field(default_factory=datetime.utcnow)  # NEW
```

**Key Changes**:
- Add `user_id` foreign key (multi-user support)
- Add `created_at`, `updated_at` timestamps
- ID becomes `Optional[int]` (DB auto-assigns)
- Field validators become SQLModel Field constraints

**Business Logic Compatibility**: TaskService methods remain largely unchanged (swap list → SQLModel queries)

---

**Data Model Status**: ✅ Complete
**Validation Rules**: Defined and testable
**Ready for**: CLI contract definition and implementation
