# Phase 1: Console Todo Application

A simple in-memory Python console todo application for managing tasks through a text-based interface.

## Features

- ✅ Add tasks with title and optional description
- ✅ View all tasks with status indicators
- ✅ Update task details (title and description)
- ✅ Delete tasks by ID
- ✅ Mark tasks as complete or incomplete
- ✅ Interactive menu-driven interface
- ✅ Input validation and error handling

## Requirements

- Python 3.13 or higher
- UV (Python package manager)

## Installation

### 1. Install UV

**Windows (PowerShell)**:
```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

**macOS/Linux**:
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### 2. Create Virtual Environment

```bash
cd phase-01-console
uv venv
```

### 3. Activate Virtual Environment

**Windows (PowerShell)**:
```powershell
.venv\Scripts\Activate.ps1
```

**macOS/Linux**:
```bash
source .venv/bin/activate
```

### 4. Install Dependencies

```bash
uv pip install pytest pytest-cov
```

## Usage

### Run the Application

```bash
uv run python src/main.py
```

### Run Tests

```bash
# Run all tests
pytest

# Run with coverage report
pytest --cov=src --cov-report=term-missing

# Run specific test file
pytest tests/unit/test_task_model.py
```

## Project Structure

```
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
├── pyproject.toml
├── README.md
└── .gitignore
```

## Development

### Running Tests

```bash
# All tests
pytest

# With coverage
pytest --cov=src

# Specific test file
pytest tests/unit/test_task_model.py

# Verbose output
pytest -v
```

### Code Coverage

Target: Minimum 80% coverage (Constitution requirement)
**Current: 87.91% coverage** ✅

```bash
pytest --cov=src --cov-report=html
# Open htmlcov/index.html in browser
```

### Test Suite

**71 comprehensive tests** covering all features:
- 15 Model Tests (Task validation, constraints, edge cases)
- 31 Service Tests (CRUD operations, ID management, state consistency)
- 9 Menu Tests (Navigation, routing, handler invocation)
- 9 Prompt Tests (Input validation, error handling)
- 11 Integration Tests (End-to-end workflows, complex scenarios, performance)

## Architecture

- **Models** (`src/models/`): Data structures (Task entity)
- **Services** (`src/services/`): Business logic (TaskService with CRUD operations)
- **CLI** (`src/cli/`): User interface (Menu, Prompts)
- **Main** (`src/main.py`): Application orchestration

## Data Model

### Task Entity

| Attribute | Type | Constraints | Default |
|-----------|------|-------------|---------|
| `id` | int | Positive, unique, auto-incremented | Auto-assigned |
| `title` | str | 1-200 characters, non-empty | Required |
| `description` | str | 0-1000 characters | Empty string |
| `completed` | bool | True or False | False |

## License

Part of the "Evolution of Todo" 5-phase hackathon project.
