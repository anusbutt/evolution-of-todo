"""Prompts module for Phase 1 Console Todo Application.

This module provides user input collection and validation functionality.
"""

from typing import Optional


def get_menu_choice() -> Optional[int]:
    """Get and validate menu choice from user.

    Prompts user for menu choice (1-7) and validates input.
    Returns None on invalid input so caller can redisplay menu.

    Returns:
        Valid menu choice (1-7) or None if invalid
    """
    choice_str = input("Enter your choice (1-7): ").strip()

    # Check for empty input
    if not choice_str:
        print("x Please enter a number")
        return None

    # Check for numeric input
    try:
        choice = int(choice_str)
    except ValueError:
        print("x Please enter a number")
        return None

    # Check for valid range
    if choice < 1 or choice > 7:
        print("x Invalid choice. Please select a number between 1 and 7")
        return None

    return choice


def get_task_title() -> str:
    """Get and validate task title from user.

    Prompts user for task title and validates:
    - Non-empty (after stripping whitespace)
    - Max 200 characters

    Returns:
        Valid task title (stripped of whitespace)
    """
    while True:
        title = input("Enter task title: ").strip()

        # Check for empty input
        if not title:
            print("x Task title cannot be empty or whitespace only")
            continue

        # Check length
        if len(title) > 200:
            print("x Task title must be 200 characters or less")
            continue

        return title


def get_task_description() -> str:
    """Get and validate task description from user.

    Description is optional - user can press Enter to skip.
    Validates max 1000 characters.

    Returns:
        Task description (may be empty string)
    """
    while True:
        description = input("Enter task description (optional, press Enter to skip): ").strip()

        # Empty is valid (optional field)
        if not description:
            return ""

        # Check length
        if len(description) > 1000:
            print("x Task description must be 1000 characters or less")
            continue

        return description


def get_task_id(operation_name: str) -> int:
    """Get and validate task ID from user.

    Prompts user for task ID and validates:
    - Numeric input
    - Positive number

    Args:
        operation_name: Name of operation (e.g., "mark complete", "delete")

    Returns:
        Valid task ID (positive integer)
    """
    while True:
        id_str = input(f"Enter task ID to {operation_name}: ").strip()

        # Check for empty input
        if not id_str:
            print("x Invalid input. Please enter a numeric task ID")
            continue

        # Check for numeric input
        try:
            task_id = int(id_str)
        except ValueError:
            print("x Invalid input. Please enter a numeric task ID")
            continue

        # Check for positive number
        if task_id < 1:
            print("x Invalid task ID. Please enter a positive number")
            continue

        return task_id


def get_updated_title(current_title: str) -> Optional[str]:
    """Get updated title from user.

    Shows current title and prompts for new value.
    User can press Enter to keep current value.

    Args:
        current_title: Current task title

    Returns:
        New title if changed, None to keep current
    """
    while True:
        print(f"Current title: {current_title}")
        new_title = input("Enter new title (or press Enter to keep current): ").strip()

        # Empty input means keep current
        if not new_title:
            return None

        # Validate new title
        if len(new_title) > 200:
            print("x Task title must be 200 characters or less")
            continue

        return new_title


def get_updated_description(current_description: str) -> Optional[str]:
    """Get updated description from user.

    Shows current description and prompts for new value.
    User can press Enter to keep current value.

    Args:
        current_description: Current task description

    Returns:
        New description if changed, None to keep current
    """
    while True:
        if current_description:
            print(f"Current description: {current_description}")
        else:
            print("Current description: (none)")

        new_description = input("Enter new description (or press Enter to keep current): ").strip()

        # Empty input means keep current (return None, not empty string)
        if not new_description:
            return None

        # Validate new description
        if len(new_description) > 1000:
            print("x Task description must be 1000 characters or less")
            continue

        return new_description
