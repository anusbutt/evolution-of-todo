# Quickstart Guide: Phase 1 - Console Todo Application

**Date**: 2026-01-09
**Feature**: 001-phase-01-console-todo
**Purpose**: Setup instructions and usage guide for development

---

## Prerequisites

- **Python**: 3.13 or higher
- **UV**: Python package manager (install from https://docs.astral.sh/uv/)
- **Git**: For version control
- **Terminal**: Command-line interface (PowerShell, bash, zsh, etc.)

---

## Installation

### 1. Install UV (if not already installed)

**Windows (PowerShell)**:
```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

**macOS/Linux**:
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### 2. Clone and Navigate to Repository

```bash
git clone <repository-url>
cd hackathon_II
git checkout 001-phase-01-console-todo
```

### 3. Create Python Virtual Environment

```bash
cd phase-01-console
uv venv
```

### 4. Activate Virtual Environment

**Windows (PowerShell)**:
```powershell
.venv\Scripts\Activate.ps1
```

**macOS/Linux**:
```bash
source .venv/bin/activate
```

### 5. Install Dependencies

```bash
uv pip install pytest pytest-cov
```

---

## Running the Application

### Start the Todo Console App

```bash
uv run python src/main.py
```

You should see:
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

### Exit the Application

- Select option `7` from the menu
- Or press `Ctrl+C` at any time

---

## Example Workflows

### Workflow 1: Add and View Tasks

1. Launch application: `uv run python src/main.py`
2. Select `1` (Add Task)
3. Enter title: `Buy groceries`
4. Enter description: `Milk, eggs, bread` (or press Enter to skip)
5. See confirmation: `✓ Task added successfully! (ID: 1)`
6. Select `2` (View All Tasks)
7. See your task displayed:
   ```
   [1] [ ] Buy groceries
       Description: Milk, eggs, bread
   ```

### Workflow 2: Mark Task Complete

1. Add a task (see Workflow 1)
2. Select `5` (Mark Task Complete)
3. Enter task ID: `1`
4. See confirmation: `✓ Task marked as complete!`
5. Select `2` (View All Tasks)
6. See updated status:
   ```
   [1] [X] Buy groceries
       Description: Milk, eggs, bread
   ```

### Workflow 3: Update Task Details

1. Add a task (see Workflow 1)
2. Select `3` (Update Task)
3. Enter task ID: `1`
4. Enter new title (or press Enter to keep current)
5. Enter new description (or press Enter to keep current)
6. See confirmation: `✓ Task updated successfully!`

### Workflow 4: Delete Task

1. Add a task (see Workflow 1)
2. Select `4` (Delete Task)
3. Enter task ID: `1`
4. See confirmation: `✓ Task deleted successfully!`
5. Select `2` (View All Tasks)
6. Task is no longer displayed

---

## Running Tests

### Run All Tests

```bash
pytest tests/
```

### Run with Coverage Report

```bash
pytest --cov=src --cov-report=term-missing tests/
```

**Expected Coverage**: Minimum 80% (Constitution requirement)

### Run Specific Test Files

```bash
# Unit tests only
pytest tests/unit/

# Integration tests only
pytest tests/integration/

# Specific test file
pytest tests/unit/test_task_model.py
```

### Run Tests with Verbose Output

```bash
pytest -v tests/
```

---

## Development Workflow

### 1. Create Feature Branch

```bash
git checkout -b feature/your-feature-name
```

### 2. Make Changes

- Edit files in `src/` directory
- Follow PEP 8 style guide
- Add type hints to all functions

### 3. Write Tests

- Create corresponding test files in `tests/unit/` or `tests/integration/`
- Ensure coverage remains above 80%

### 4. Run Tests

```bash
pytest --cov=src tests/
```

### 5. Commit Changes

```bash
git add .
git commit -m "feat: your feature description"
```

### 6. Push to Remote

```bash
git push origin feature/your-feature-name
```

---

## Project Structure

```
phase-01-console/
├── src/
│   ├── models/
│   │   └── task.py           # Task data class
│   ├── services/
│   │   └── task_service.py   # Business logic (CRUD operations)
│   ├── cli/
│   │   ├── menu.py           # Menu display and navigation
│   │   └── prompts.py        # User input collection and validation
│   └── main.py               # Application entry point
├── tests/
│   ├── unit/
│   │   ├── test_task_model.py
│   │   └── test_task_service.py
│   └── integration/
│       └── test_app_workflow.py
├── .venv/                    # Virtual environment (created by UV)
└── README.md
```

---

## Troubleshooting

### Issue: `uv: command not found`

**Solution**: Ensure UV is installed and added to PATH
```bash
# Verify installation
uv --version

# Reinstall if needed (see Installation section)
```

### Issue: `ModuleNotFoundError: No module named 'pytest'`

**Solution**: Install dependencies in virtual environment
```bash
# Activate virtual environment first
source .venv/bin/activate  # macOS/Linux
.venv\Scripts\Activate.ps1  # Windows

# Install dependencies
uv pip install pytest pytest-cov
```

### Issue: Application doesn't start

**Solution**: Verify Python version and virtual environment
```bash
# Check Python version (must be 3.13+)
python --version

# Ensure virtual environment is activated
# You should see (.venv) prefix in terminal prompt

# Try running with explicit python path
uv run python src/main.py
```

### Issue: Tests failing with import errors

**Solution**: Ensure PYTHONPATH includes src directory
```bash
# Run from project root (phase-01-console/)
export PYTHONPATH=src:$PYTHONPATH  # macOS/Linux
$env:PYTHONPATH="src;$env:PYTHONPATH"  # Windows PowerShell

pytest tests/
```

### Issue: Coverage below 80%

**Solution**: Identify untested code
```bash
# Generate detailed coverage report
pytest --cov=src --cov-report=html tests/

# Open htmlcov/index.html in browser to see line-by-line coverage
```

### Issue: Ctrl+C doesn't exit cleanly

**Solution**: This is a bug - KeyboardInterrupt should be handled in main.py
- Check that `try/except KeyboardInterrupt` block exists around main loop
- Verify farewell message is printed before exit

---

## Performance Benchmarks

### Expected Performance (n=100 tasks)

| Operation | Target Time | Measurement |
|-----------|-------------|-------------|
| Add Task | <100ms | Input → success message |
| View All Tasks | <1 second | Menu choice → list displayed |
| Update Task | <100ms | ID validated → success message |
| Delete Task | <100ms | ID validated → success message |
| Mark Complete | <100ms | ID validated → success message |

### Running Benchmarks

```bash
# Create 100 tasks and measure view time
# (Manual test - no automated benchmark in Phase 1)

# Add 100 tasks via automation:
# 1. Modify main.py temporarily to auto-add tasks
# 2. Time the View All Tasks operation
# 3. Verify display completes in <1 second
```

---

## Manual Testing Checklist

### Basic Operations
- [ ] Add task with title and description
- [ ] Add task with title only (empty description)
- [ ] View empty task list
- [ ] View task list with 1 task
- [ ] View task list with multiple tasks
- [ ] Update task title
- [ ] Update task description
- [ ] Update task title and description
- [ ] Delete task by ID
- [ ] Mark task as complete
- [ ] Mark task as incomplete
- [ ] Exit application via menu option 7
- [ ] Exit application via Ctrl+C

### Error Handling
- [ ] Add task with empty title (should reject)
- [ ] Add task with whitespace-only title (should reject)
- [ ] Add task with 201-character title (should reject)
- [ ] Add task with 1001-character description (should reject)
- [ ] Update non-existent task ID (should show error)
- [ ] Delete non-existent task ID (should show error)
- [ ] Mark complete non-existent task ID (should show error)
- [ ] Enter non-numeric menu choice (should reprompt)
- [ ] Enter out-of-range menu choice (should reprompt)

### Edge Cases
- [ ] Add 100 tasks and verify view displays in <1 second
- [ ] Delete all tasks and verify empty list message
- [ ] Mark task complete, then mark incomplete (toggle)
- [ ] Update task with Enter (keep existing values)

---

## Next Steps

After completing Phase 1:
1. Review acceptance criteria in `specs/001-phase-01-console-todo/spec.md`
2. Verify all 10 success criteria are met
3. Run full test suite with coverage report
4. Prepare for Phase 2: Full-Stack Web Application

---

## Additional Resources

- **Specification**: `specs/001-phase-01-console-todo/spec.md`
- **Implementation Plan**: `specs/001-phase-01-console-todo/plan.md`
- **Data Model**: `specs/001-phase-01-console-todo/data-model.md`
- **CLI Contract**: `specs/001-phase-01-console-todo/contracts/cli-interface.md`
- **Constitution**: `.specify/memory/constitution.md`

---

**Quickstart Status**: ✅ Complete
**Ready for**: Development setup and testing
