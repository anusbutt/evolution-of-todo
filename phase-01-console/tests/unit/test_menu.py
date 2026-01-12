"""Unit tests for Menu class.

This module tests menu display and choice handling functionality.
"""

import sys
from io import StringIO
from unittest.mock import patch
import pytest

# Add project root to path
from pathlib import Path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from src.services.task_service import TaskService
from src.cli.menu import Menu


def test_display_menu():
    """Test menu displays all 7 options correctly."""
    service = TaskService()
    menu = Menu(service)

    # Capture stdout
    captured_output = StringIO()
    with patch('sys.stdout', captured_output):
        menu.display_menu()

    output = captured_output.getvalue()

    # Verify all menu options displayed
    assert "Main Menu:" in output
    assert "1. Add Task" in output
    assert "2. View All Tasks" in output
    assert "3. Update Task" in output
    assert "4. Delete Task" in output
    assert "5. Mark Task Complete" in output
    assert "6. Mark Task Incomplete" in output
    assert "7. Exit" in output


def test_handle_choice_exit():
    """Test handle_choice returns False for exit option (7)."""
    service = TaskService()
    menu = Menu(service)

    # Choice 7 should signal exit
    should_continue = menu.handle_choice(7)
    assert should_continue is False


def test_handle_choice_continue():
    """Test handle_choice returns True for non-exit options."""
    service = TaskService()
    menu = Menu(service)

    # Mock input for operations that require it
    # Choice 1: Add Task - needs title, description
    # Choice 2: View - no input
    # Choice 3: Update - needs ID, then title update, then description update
    # Choice 4: Delete - needs ID
    # Choice 5: Mark Complete - needs ID
    # Choice 6: Mark Incomplete - needs ID
    with patch('builtins.input', side_effect=[
        'Test Task', '',           # Add Task (choice 1)
        '1', '', '',               # Update (choice 3): ID, keep title, keep description
        '1',                       # Delete (choice 4): ID
        '1',                       # Mark Complete (choice 5): ID
        '1'                        # Mark Incomplete (choice 6): ID
    ]):
        # Choices 1-6 should signal continue
        for choice in range(1, 7):
            should_continue = menu.handle_choice(choice)
            assert should_continue is True


def test_handle_choice_add_task():
    """Test handle_choice routes to add_task handler."""
    service = TaskService()
    menu = Menu(service)

    # Mock input for add task
    with patch('builtins.input', side_effect=['Test Task', '']):
        # Mock the handler
        with patch.object(menu, 'handle_add_task') as mock_handler:
            menu.handle_choice(1)
            mock_handler.assert_called_once()


def test_handle_choice_view_tasks():
    """Test handle_choice routes to view_tasks handler."""
    service = TaskService()
    menu = Menu(service)

    with patch.object(menu, 'handle_view_tasks') as mock_handler:
        menu.handle_choice(2)
        mock_handler.assert_called_once()


def test_handle_choice_update_task():
    """Test handle_choice routes to update_task handler."""
    service = TaskService()
    menu = Menu(service)

    with patch.object(menu, 'handle_update_task') as mock_handler:
        menu.handle_choice(3)
        mock_handler.assert_called_once()


def test_handle_choice_delete_task():
    """Test handle_choice routes to delete_task handler."""
    service = TaskService()
    menu = Menu(service)

    with patch.object(menu, 'handle_delete_task') as mock_handler:
        menu.handle_choice(4)
        mock_handler.assert_called_once()


def test_handle_choice_mark_complete():
    """Test handle_choice routes to mark_complete handler."""
    service = TaskService()
    menu = Menu(service)

    with patch.object(menu, 'handle_mark_complete') as mock_handler:
        menu.handle_choice(5)
        mock_handler.assert_called_once()


def test_handle_choice_mark_incomplete():
    """Test handle_choice routes to mark_incomplete handler."""
    service = TaskService()
    menu = Menu(service)

    with patch.object(menu, 'handle_mark_incomplete') as mock_handler:
        menu.handle_choice(6)
        mock_handler.assert_called_once()
