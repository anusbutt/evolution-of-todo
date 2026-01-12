# CLI Interface Contract: Phase 1 - Console Todo Application

**Date**: 2026-01-09
**Feature**: 001-phase-01-console-todo
**Purpose**: Define user interface behavior and interaction patterns

---

## Application Lifecycle

### Startup
**Trigger**: User executes `uv run python src/main.py`

**Behavior**:
1. Display welcome message
2. Initialize TaskService with empty task list
3. Display main menu

**Output**:
```
=====================================
   Welcome to Todo Console App
=====================================

Main Menu:
1. Add Task
2. View All Tasks
3. Update Task
4. Delete Task
5. Mark Task Complete
6. Mark Task Incomplete
7. Exit

Enter your choice (1-7):
```

### Shutdown
**Trigger**: User selects option 7 (Exit) OR presses Ctrl+C

**Behavior**:
1. Display farewell message
2. Terminate application (exit code 0)
3. Clear all in-memory data

**Output**:
```
Goodbye! Your session has ended.
```

---

## Main Menu

### Display Format
```
Main Menu:
1. Add Task
2. View All Tasks
3. Update Task
4. Delete Task
5. Mark Task Complete
6. Mark Task Incomplete
7. Exit

Enter your choice (1-7):
```

### Input Validation
- **Valid input**: Numbers 1-7
- **Invalid input**: Non-numeric, out-of-range, empty

**Error Handling**:
```
# Input: "abc"
Please enter a number

# Input: "9"
Invalid choice. Please select a number between 1 and 7

# Input: "" (empty)
Please enter a number
```

**Behavior**: After error, redisplay menu and reprompt

---

## Operation 1: Add Task

### Flow
```
User selects: 1
↓
Prompt: "Enter task title: "
User enters: "Buy groceries"
↓
Prompt: "Enter task description (optional, press Enter to skip): "
User enters: "Milk, eggs, bread" OR presses Enter
↓
Create task with auto-assigned ID
↓
Display: "✓ Task added successfully! (ID: 1)"
↓
Return to main menu
```

### Input Prompts
```
Enter task title: _
Enter task description (optional, press Enter to skip): _
```

### Success Output
```
✓ Task added successfully! (ID: 3)
```

### Error Cases

**Empty Title**:
```
Enter task title:
✗ Task title cannot be empty or whitespace only
Enter task title: _
```

**Title Too Long (>200 chars)**:
```
Enter task title: [201 characters]
✗ Task title must be 200 characters or less
Enter task title: _
```

**Description Too Long (>1000 chars)**:
```
Enter task description (optional, press Enter to skip): [1001 characters]
✗ Task description must be 1000 characters or less
Enter task description (optional, press Enter to skip): _
```

---

## Operation 2: View All Tasks

### Flow
```
User selects: 2
↓
Retrieve all tasks from TaskService
↓
Display formatted task list
↓
Return to main menu
```

### Output Format (Tasks Exist)
```
=====================================
           Your Tasks
=====================================

[1] [ ] Buy groceries
    Description: Milk, eggs, bread

[2] [X] Call dentist
    Description: Schedule annual checkup

[3] [ ] Finish report

=====================================
Total: 3 tasks (1 complete, 2 incomplete)
```

**Legend**:
- `[ ]` = Incomplete task
- `[X]` = Complete task
- Description shown only if non-empty

### Output Format (No Tasks)
```
=====================================
           Your Tasks
=====================================

Your task list is empty. Add your first task to get started!

=====================================
Total: 0 tasks
```

---

## Operation 3: Update Task

### Flow
```
User selects: 3
↓
Prompt: "Enter task ID to update: "
User enters: 2
↓
Retrieve task 2 from TaskService
↓
Prompt: "Enter new title (current: 'Call dentist', press Enter to keep): "
User enters: "Call dentist and book appointment" OR presses Enter
↓
Prompt: "Enter new description (current: 'Schedule annual checkup', press Enter to keep): "
User enters: "Schedule annual checkup and teeth cleaning" OR presses Enter
↓
Update task in TaskService
↓
Display: "✓ Task updated successfully!"
↓
Return to main menu
```

### Input Prompts
```
Enter task ID to update: _
Enter new title (current: 'Buy groceries', press Enter to keep): _
Enter new description (current: 'Milk, eggs', press Enter to keep): _
```

### Success Output
```
✓ Task updated successfully!
```

### Error Cases

**Task Not Found**:
```
Enter task ID to update: 999
✗ Task with ID 999 not found
```

**Invalid ID Format**:
```
Enter task ID to update: abc
✗ Invalid input. Please enter a numeric task ID
Enter task ID to update: _
```

**Negative ID**:
```
Enter task ID to update: -5
✗ Invalid task ID. Please enter a positive number
Enter task ID to update: _
```

**Empty Title (if user tries to clear it)**:
```
Enter new title (current: 'Buy groceries', press Enter to keep):
✗ Task title cannot be empty or whitespace only
Enter new title (current: 'Buy groceries', press Enter to keep): _
```

---

## Operation 4: Delete Task

### Flow
```
User selects: 4
↓
Prompt: "Enter task ID to delete: "
User enters: 3
↓
Delete task 3 from TaskService
↓
Display: "✓ Task deleted successfully!"
↓
Return to main menu
```

### Input Prompt
```
Enter task ID to delete: _
```

### Success Output
```
✓ Task deleted successfully!
```

### Error Cases
Same as Update Task (Task Not Found, Invalid ID Format, Negative ID)

---

## Operation 5: Mark Task Complete

### Flow
```
User selects: 5
↓
Prompt: "Enter task ID to mark complete: "
User enters: 2
↓
Set task 2 completed=True in TaskService
↓
Display: "✓ Task marked as complete!"
↓
Return to main menu
```

### Input Prompt
```
Enter task ID to mark complete: _
```

### Success Output
```
✓ Task marked as complete!
```

### Error Cases
Same as Update Task (Task Not Found, Invalid ID Format, Negative ID)

**Additional Edge Case**:
```
# Empty task list
Enter task ID to mark complete: 1
✗ No tasks found. Please add a task first.
```

---

## Operation 6: Mark Task Incomplete

### Flow
```
User selects: 6
↓
Prompt: "Enter task ID to mark incomplete: "
User enters: 2
↓
Set task 2 completed=False in TaskService
↓
Display: "✓ Task marked as incomplete!"
↓
Return to main menu
```

### Input Prompt
```
Enter task ID to mark incomplete: _
```

### Success Output
```
✓ Task marked as incomplete!
```

### Error Cases
Same as Mark Complete

---

## Operation 7: Exit

### Flow
```
User selects: 7
↓
Display: "Goodbye! Your session has ended."
↓
Terminate application
```

**No confirmation prompt** (per spec acceptance scenario US5-4)

---

## Status Indicators

| Symbol | Meaning | Usage |
|--------|---------|-------|
| `✓` | Success | Operation completed successfully |
| `✗` | Error | Operation failed, user action required |
| `[ ]` | Incomplete | Task not yet complete |
| `[X]` | Complete | Task finished |

---

## Error Message Patterns

### Validation Errors
```
✗ {Validation rule violation}
```
Examples:
- "✗ Task title cannot be empty or whitespace only"
- "✗ Task title must be 200 characters or less"

### Operational Errors
```
✗ {Operation failure reason}
```
Examples:
- "✗ Task with ID 999 not found"
- "✗ Invalid input. Please enter a numeric task ID"

### System Errors
```
✗ An unexpected error occurred. Please try again.
```

**Principle**: Clear, actionable, user-friendly (no stack traces exposed)

---

## Input Handling Standards

### Whitespace Treatment
- **All inputs**: Strip leading/trailing whitespace via `.strip()`
- **Titles**: Reject if empty after strip
- **Descriptions**: Allow empty after strip
- **IDs**: Strip before int conversion

### Case Sensitivity
- **Task titles**: Case-sensitive ("Buy milk" ≠ "buy milk")
- **Task descriptions**: Case-sensitive
- **Menu choices**: Numeric only (no case)

### Special Characters
- **Allowed**: All UTF-8 characters in titles/descriptions
- **No escaping needed**: Pure text input (no shell commands executed)

---

## Keyboard Interrupt Handling

### Ctrl+C Behavior
```
# User presses Ctrl+C at any prompt
^C
Goodbye! Your session has ended.
```

**Implementation**: Catch `KeyboardInterrupt`, display farewell, exit cleanly

---

## Performance Requirements

| Operation | Max Response Time | Measurement Point |
|-----------|-------------------|-------------------|
| Display menu | <50ms | Menu print → prompt ready |
| Add task | <100ms | Input collected → success message |
| View tasks (100 items) | <1 second | Menu choice → list displayed |
| Update task | <100ms | ID validated → success message |
| Delete task | <100ms | ID validated → success message |
| Mark complete | <100ms | ID validated → success message |

**All operations must feel instant to the user**

---

## Accessibility Considerations

### Screen Reader Compatibility
- Use clear text labels (no ASCII art-only indicators)
- Status symbols supplemented with text ("✓ Success" not just "✓")

### Keyboard-Only Navigation
- All operations accessible via number keys
- No mouse required

### Error Recovery
- Invalid inputs reprompt (don't exit application)
- Clear guidance on valid input format

---

## Testing Contract

### Unit Test Requirements
- Mock `input()` for user input simulation
- Capture `print()` output for verification
- Test all error paths (invalid IDs, empty titles, etc.)

### Integration Test Requirements
- Simulate complete workflows (add → view → mark → delete)
- Verify menu redisplay after operations
- Test Ctrl+C handling

### Example Test Pattern
```python
@patch('builtins.input', side_effect=['1', 'Buy milk', '', '7'])
def test_add_task_workflow(mock_input, capsys):
    main()
    output = capsys.readouterr().out
    assert "✓ Task added successfully!" in output
    assert "Goodbye!" in output
```

---

**CLI Contract Status**: ✅ Complete
**All interactions defined**: Yes
**Ready for**: Implementation (tasks.md → code)
