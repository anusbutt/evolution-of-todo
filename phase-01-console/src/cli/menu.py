"""Menu module for Phase 1 Console Todo Application.

This module provides menu display and navigation functionality.
"""

from typing import Optional
from src.services.task_service import TaskService
from src.cli.prompts import (
    get_task_title,
    get_task_description,
    get_task_id,
    get_updated_title,
    get_updated_description
)


class Menu:
    """Menu class for displaying options and handling user choices.

    Attributes:
        service: TaskService instance for task operations
    """

    def __init__(self, service: TaskService):
        """Initialize Menu with TaskService.

        Args:
            service: TaskService instance for task operations
        """
        self.service = service

    def display_menu(self) -> None:
        """Display the main menu with all available options.

        Menu options:
        1. Add Task
        2. View All Tasks
        3. Update Task
        4. Delete Task
        5. Mark Task Complete
        6. Mark Task Incomplete
        7. Exit
        """
        print("\nMain Menu:")
        print("1. Add Task")
        print("2. View All Tasks")
        print("3. Update Task")
        print("4. Delete Task")
        print("5. Mark Task Complete")
        print("6. Mark Task Incomplete")
        print("7. Exit")
        print()

    def handle_choice(self, choice: int) -> bool:
        """Handle user menu choice and route to appropriate operation.

        Args:
            choice: Menu choice (1-7)

        Returns:
            True to continue main loop, False to exit application
        """
        if choice == 1:
            self.handle_add_task()
        elif choice == 2:
            self.handle_view_tasks()
        elif choice == 3:
            self.handle_update_task()
        elif choice == 4:
            self.handle_delete_task()
        elif choice == 5:
            self.handle_mark_complete()
        elif choice == 6:
            self.handle_mark_incomplete()
        elif choice == 7:
            return False  # Exit application
        return True  # Continue main loop

    def handle_add_task(self) -> None:
        """Handle Add Task operation.

        Prompts user for title and description, creates task, displays success message.
        """
        try:
            title = get_task_title()
            description = get_task_description()

            task = self.service.add_task(title, description)

            print(f"\n* Task added successfully! (ID: {task.id})\n")

        except ValueError as e:
            print(f"\nx Error: {e}\n")

    def handle_view_tasks(self) -> None:
        """Handle View All Tasks operation.

        Displays formatted task list.
        """
        self.display_tasks()

    def handle_update_task(self) -> None:
        """Handle Update Task operation.

        Prompts user for task ID, displays current values,
        prompts for new values, updates task, displays result.
        """
        task_id = get_task_id("update")

        # Get the task to display current values
        task = self.service.get_task_by_id(task_id)
        if not task:
            print(f"\nx Task with ID {task_id} not found\n")
            return

        # Show current task details
        print(f"\nUpdating Task {task_id}")
        print("=" * 37)

        # Prompt for updated title
        new_title = get_updated_title(task.title)

        # Prompt for updated description
        new_description = get_updated_description(task.description)

        # If both are None, no changes requested
        if new_title is None and new_description is None:
            print("\nNo changes made.\n")
            return

        # Update the task
        try:
            result = self.service.update_task(task_id, title=new_title, description=new_description)

            if result:
                print(f"\n* Task {task_id} updated successfully!\n")
            else:
                print(f"\nx Task with ID {task_id} not found\n")

        except ValueError as e:
            print(f"\nx Error: {e}\n")

    def handle_delete_task(self) -> None:
        """Handle Delete Task operation.

        Prompts user for task ID, deletes task, displays result.
        """
        task_id = get_task_id("delete")

        result = self.service.delete_task(task_id)

        if result:
            print(f"\n* Task {task_id} deleted successfully!\n")
        else:
            print(f"\nx Task with ID {task_id} not found\n")

    def handle_mark_complete(self) -> None:
        """Handle Mark Task Complete operation.

        Prompts user for task ID, marks task complete, displays result.
        """
        task_id = get_task_id("mark complete")

        result = self.service.mark_complete(task_id)

        if result:
            print(f"\n* Task {task_id} marked as complete!\n")
        else:
            print(f"\nx Task with ID {task_id} not found\n")

    def handle_mark_incomplete(self) -> None:
        """Handle Mark Task Incomplete operation.

        Prompts user for task ID, marks task incomplete, displays result.
        """
        task_id = get_task_id("mark incomplete")

        result = self.service.mark_incomplete(task_id)

        if result:
            print(f"\n* Task {task_id} marked as incomplete!\n")
        else:
            print(f"\nx Task with ID {task_id} not found\n")

    def display_tasks(self) -> None:
        """Display formatted task list per cli-interface.md specification.

        Format:
        [ID] [Status] Title
            Description: description (if non-empty)

        Status indicators:
        [ ] = Incomplete
        [X] = Complete
        """
        tasks = self.service.get_all_tasks()

        print("\n" + "=" * 37)
        print("           Your Tasks")
        print("=" * 37 + "\n")

        if not tasks:
            print("Your task list is empty. Add your first task to get started!\n")
        else:
            for task in tasks:
                # Status indicator
                status = "[X]" if task.completed else "[ ]"

                # Task line
                print(f"[{task.id}] {status} {task.title}")

                # Description (only if non-empty)
                if task.description:
                    print(f"    Description: {task.description}")

                print()  # Blank line after each task

        # Summary line
        complete_count = sum(1 for task in tasks if task.completed)
        incomplete_count = len(tasks) - complete_count

        print("=" * 37)
        if tasks:
            print(f"Total: {len(tasks)} tasks ({complete_count} complete, {incomplete_count} incomplete)")
        else:
            print("Total: 0 tasks")
        print()
