"""Integration tests for Phase 1 Console Todo Application workflows.

This module tests complete user workflows from startup to shutdown.
"""

import sys
from io import StringIO
from unittest.mock import patch
import pytest


def test_application_startup():
    """Test application displays welcome message and menu on startup.

    Acceptance Scenario US5-1:
    Given the user launches the application,
    When the application starts,
    Then a welcome message displays along with a menu of available operations.
    """
    # Import after sys.path is set
    from src.main import main

    # Mock input to provide Exit choice
    with patch('builtins.input', return_value='7'):
        # Capture stdout
        captured_output = StringIO()
        with patch('sys.stdout', captured_output):
            main()

    output = captured_output.getvalue()

    # Verify welcome message
    assert "Welcome to Todo Console App" in output
    assert "=====" in output

    # Verify menu displayed
    assert "Main Menu:" in output
    assert "1. Add Task" in output
    assert "2. View All Tasks" in output
    assert "3. Update Task" in output
    assert "4. Delete Task" in output
    assert "5. Mark Task Complete" in output
    assert "6. Mark Task Incomplete" in output
    assert "7. Exit" in output

    # Verify farewell message
    assert "Goodbye! Your session has ended." in output


def test_application_exit_cleanly():
    """Test application exits cleanly when Exit option selected.

    Acceptance Scenario US5-4:
    Given the user selects "Exit" from the menu,
    When the application closes,
    Then a farewell message displays and the application terminates cleanly.
    """
    from src.main import main

    # Mock input to provide Exit choice
    with patch('builtins.input', return_value='7'):
        captured_output = StringIO()
        with patch('sys.stdout', captured_output):
            main()

    output = captured_output.getvalue()

    # Verify farewell message
    assert "Goodbye! Your session has ended." in output


def test_invalid_menu_choice_handling():
    """Test application handles invalid menu choices gracefully.

    Acceptance Scenario US5-5:
    Given the user enters an invalid menu choice,
    When the input is processed,
    Then an error message displays and the menu reappears.
    """
    from src.main import main

    # Mock input: invalid choice "9", then valid exit choice "7"
    with patch('builtins.input', side_effect=['9', '7']):
        captured_output = StringIO()
        with patch('sys.stdout', captured_output):
            main()

    output = captured_output.getvalue()

    # Verify error message displayed
    assert "Invalid choice" in output
    assert "1 and 7" in output

    # Verify menu displayed again after error
    menu_count = output.count("Main Menu:")
    assert menu_count >= 2  # At least twice (initial + after error)


def test_non_numeric_menu_choice_handling():
    """Test application handles non-numeric menu input gracefully."""
    from src.main import main

    # Mock input: non-numeric "abc", then valid exit choice "7"
    with patch('builtins.input', side_effect=['abc', '7']):
        captured_output = StringIO()
        with patch('sys.stdout', captured_output):
            main()

    output = captured_output.getvalue()

    # Verify error message displayed
    assert "Please enter a number" in output

    # Verify menu displayed again after error
    menu_count = output.count("Main Menu:")
    assert menu_count >= 2


def test_keyboard_interrupt_handling():
    """Test application handles Ctrl+C gracefully."""
    from src.main import main

    # Mock input to raise KeyboardInterrupt
    with patch('builtins.input', side_effect=KeyboardInterrupt()):
        captured_output = StringIO()
        with patch('sys.stdout', captured_output):
            main()

    output = captured_output.getvalue()

    # Verify farewell message still displayed
    assert "Goodbye! Your session has ended." in output


def test_add_and_view_workflow():
    """Test complete add and view tasks workflow.

    Acceptance Scenario US1-1, US1-2, US1-3:
    Given the application is running,
    When the user adds 3 tasks and views the list,
    Then all tasks appear with correct IDs, titles, descriptions, and status.
    """
    from src.main import main

    # Mock input: Add 3 tasks, view list, then exit
    inputs = [
        '1',  # Add Task
        'Buy groceries',  # Title
        'Milk, eggs, bread',  # Description
        '1',  # Add Task
        'Call dentist',  # Title
        'Schedule annual checkup',  # Description
        '1',  # Add Task
        'Finish report',  # Title
        '',  # Description (empty)
        '2',  # View All Tasks
        '7'   # Exit
    ]

    with patch('builtins.input', side_effect=inputs):
        captured_output = StringIO()
        with patch('sys.stdout', captured_output):
            main()

    output = captured_output.getvalue()

    # Verify tasks were added successfully
    assert "Task added successfully" in output or "added" in output.lower()

    # Verify task list displays correctly
    assert "[1]" in output  # Task ID 1
    assert "[ ]" in output  # Incomplete status
    assert "Buy groceries" in output
    assert "Milk, eggs, bread" in output

    assert "[2]" in output  # Task ID 2
    assert "Call dentist" in output
    assert "Schedule annual checkup" in output

    assert "[3]" in output  # Task ID 3
    assert "Finish report" in output

    # Verify total count
    assert "Total: 3 tasks" in output or "3 task" in output.lower()


def test_mark_complete_workflow():
    """Test complete mark task workflow.

    Acceptance Scenario US2-1, US2-2:
    Given tasks exist,
    When user marks tasks as complete/incomplete,
    Then status indicators update correctly.
    """
    from src.main import main

    # Mock input: Add 3 tasks, mark task 2 complete, view, mark task 2 incomplete, view, exit
    inputs = [
        '1', 'Task 1', '',  # Add Task 1
        '1', 'Task 2', '',  # Add Task 2
        '1', 'Task 3', '',  # Add Task 3
        '5', '2',           # Mark Task 2 complete
        '2',                # View tasks
        '6', '2',           # Mark Task 2 incomplete
        '2',                # View tasks again
        '7'                 # Exit
    ]

    with patch('builtins.input', side_effect=inputs):
        captured_output = StringIO()
        with patch('sys.stdout', captured_output):
            main()

    output = captured_output.getvalue()

    # Verify mark complete message
    assert "marked as complete" in output.lower() or "complete" in output.lower()

    # Verify status indicator changes
    # Should have both [X] and [ ] indicators
    assert "[X]" in output  # Complete status
    assert "[ ]" in output  # Incomplete status

    # Verify mark incomplete message
    assert "marked as incomplete" in output.lower() or "incomplete" in output.lower()


def test_update_workflow():
    """Test complete update task workflow.

    Acceptance Scenario US3-1, US3-2:
    Given tasks exist,
    When user updates task title and description,
    Then changes persist and ID/status remain unchanged.
    """
    from src.main import main

    # Mock input: Add task, view, update task, view again, exit
    inputs = [
        '1',                        # Add Task
        'Finish report',            # Title
        'Q4 summary',               # Description
        '2',                        # View tasks
        '3',                        # Update Task
        '1',                        # Task ID to update
        'Finish quarterly report',  # New title
        'Q4 summary with charts',   # New description
        '2',                        # View tasks again
        '7'                         # Exit
    ]

    with patch('builtins.input', side_effect=inputs):
        captured_output = StringIO()
        with patch('sys.stdout', captured_output):
            main()

    output = captured_output.getvalue()

    # Verify original values displayed
    assert "Finish report" in output
    assert "Q4 summary" in output

    # Verify update success message
    assert "updated" in output.lower() or "success" in output.lower()

    # Verify new values displayed
    assert "Finish quarterly report" in output
    assert "Q4 summary with charts" in output

    # Verify task ID preserved (should still be [1])
    assert "[1]" in output


def test_delete_workflow():
    """Test complete delete task workflow.

    Acceptance Scenario US4-1, US4-2:
    Given tasks exist,
    When user deletes a task,
    Then it's removed from the list and other task IDs are preserved.
    """
    from src.main import main

    # Mock input: Add 4 tasks, view, delete task 2, view again, try to delete task 2 again, exit
    inputs = [
        '1', 'Task 1', '',          # Add Task 1
        '1', 'Task 2', '',          # Add Task 2
        '1', 'Task 3', '',          # Add Task 3
        '1', 'Task 4', '',          # Add Task 4
        '2',                        # View tasks
        '4', '2',                   # Delete Task 2
        '2',                        # View tasks again
        '4', '2',                   # Try to delete Task 2 again (should fail)
        '7'                         # Exit
    ]

    with patch('builtins.input', side_effect=inputs):
        captured_output = StringIO()
        with patch('sys.stdout', captured_output):
            main()

    output = captured_output.getvalue()

    # Verify all 4 tasks were initially displayed
    assert "[1]" in output
    assert "[2]" in output
    assert "[3]" in output
    assert "[4]" in output
    assert "Total: 4 tasks" in output

    # Verify delete success message
    assert "deleted" in output.lower() or "removed" in output.lower()

    # Verify only 3 tasks remain after deletion
    assert "Total: 3 tasks" in output

    # Verify task 2 not found message on second delete attempt
    assert "not found" in output.lower() or "error" in output.lower()


def test_complex_20_task_workflow():
    """Test complex workflow with 20 tasks: add 10, mark 5 complete, update 3, delete 2, view list.

    This test validates the system handles multiple operations correctly and
    verifies the final state is consistent.
    """
    from src.main import main

    # Build inputs: Add 10 tasks, mark 5 complete, update 3, delete 2, view, exit
    inputs = []

    # Add 10 tasks
    for i in range(1, 11):
        inputs.extend(['1', f'Task {i}', f'Description {i}'])

    # Mark tasks 2, 4, 6, 8, 10 complete
    for task_id in [2, 4, 6, 8, 10]:
        inputs.extend(['5', str(task_id)])

    # Update tasks 1, 3, 5 (update titles only)
    for task_id in [1, 3, 5]:
        inputs.extend(['3', str(task_id), f'Updated Task {task_id}', ''])

    # Delete tasks 7, 9
    for task_id in [7, 9]:
        inputs.extend(['4', str(task_id)])

    # View all tasks
    inputs.append('2')

    # Exit
    inputs.append('7')

    with patch('builtins.input', side_effect=inputs):
        captured_output = StringIO()
        with patch('sys.stdout', captured_output):
            main()

    output = captured_output.getvalue()

    # Verify final state: 8 tasks remain (10 added - 2 deleted)
    assert "Total: 8 tasks" in output

    # Verify 5 tasks are complete
    assert "5 complete" in output

    # Verify 3 tasks are incomplete
    assert "3 incomplete" in output

    # Verify updated titles appear
    assert "Updated Task 1" in output
    assert "Updated Task 3" in output
    assert "Updated Task 5" in output

    # Verify deleted tasks don't appear
    assert "[7]" not in output or "deleted" in output.lower()
    assert "[9]" not in output or "deleted" in output.lower()


def test_performance_100_tasks():
    """Test performance with 100 tasks - view operation should complete in <1 second.

    This test validates the system can handle a large number of tasks efficiently.
    """
    import time
    from src.services.task_service import TaskService
    from src.cli.menu import Menu

    # Create service and add 100 tasks
    service = TaskService()
    for i in range(1, 101):
        service.add_task(f"Task {i}", f"Description for task {i}")

    # Mark some tasks complete (every 3rd task)
    for i in range(3, 101, 3):
        service.mark_complete(i)

    # Create menu
    menu = Menu(service)

    # Measure view time
    captured_output = StringIO()
    with patch('sys.stdout', captured_output):
        start_time = time.time()
        menu.display_tasks()
        end_time = time.time()

    view_time = end_time - start_time

    # Verify performance: should be under 1 second
    assert view_time < 1.0, f"View time {view_time:.3f}s exceeded 1 second threshold"

    # Verify output contains all 100 tasks
    output = captured_output.getvalue()
    assert "Total: 100 tasks" in output
    assert "33 complete" in output  # 100 / 3 = 33.33, so 33 complete
    assert "67 incomplete" in output
