"""Main entry point for Phase 1 Console Todo Application.

This module orchestrates application lifecycle: startup, main loop, shutdown.
"""

import sys
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.services.task_service import TaskService
from src.cli.menu import Menu
from src.cli.prompts import get_menu_choice


def main():
    """Main application function.

    Lifecycle:
    1. Startup: Display welcome message and initialize TaskService
    2. Main loop: Display menu, get choice, handle choice, repeat
    3. Shutdown: Display farewell message and exit cleanly
    """
    try:
        # Startup
        print("=" * 37)
        print("   Welcome to Todo Console App")
        print("=" * 37)

        # Initialize service and menu
        service = TaskService()
        menu = Menu(service)

        # Main loop
        while True:
            menu.display_menu()
            choice = get_menu_choice()

            # If invalid input, redisplay menu and reprompt
            if choice is None:
                continue

            should_continue = menu.handle_choice(choice)

            if not should_continue:
                break

        # Shutdown
        print("\nGoodbye! Your session has ended.")

    except KeyboardInterrupt:
        # Handle Ctrl+C gracefully
        print("\n\nGoodbye! Your session has ended.")
    except Exception as e:
        # Handle unexpected errors
        print(f"\nx An unexpected error occurred: {e}")
        print("Please try again.")


if __name__ == "__main__":
    main()
