# main.py
# Entry point: shows the menu and passes user choices to the TaskManager object.
#
# The starter code did sys.path.append('src') + `from task_manager import TaskManager`,
# but task_manager.py uses a relative import (`from .task import Task`), which then fails with
# "ImportError: attempted relative import with no known parent package".
# Importing through the src package avoids that.
from src.task_manager import TaskManager


def display_menu():
    print("\n--- OOP Task Manager Menu ---")
    print("1. Add Task")
    print("2. List Tasks")
    print("3. Complete Task")
    print("4. Delete Task")
    print("5. Exit")
    print("-------------------------")


def ask_task_id(action):
    """Returns the ID as an int, or None if the user did not type a number."""
    text = input(f"Enter ID of task to {action}: ").strip()
    try:
        return int(text)
    except ValueError:
        print("Invalid input. Please enter a number for Task ID.")
        return None


def main():
    manager = TaskManager()      # create one TaskManager object (loads saved tasks)

    while True:
        display_menu()
        choice = input("Enter your choice (1-5): ").strip()

        if choice == "1":
            description = input("Enter task description: ").strip()
            if description:
                manager.add_task(description)
            else:
                print("Task description cannot be empty.")
        elif choice == "2":
            manager.list_tasks()
        elif choice == "3":
            task_id = ask_task_id("complete")
            if task_id is not None:
                manager.complete_task(task_id)
        elif choice == "4":
            task_id = ask_task_id("delete")
            if task_id is not None:
                manager.delete_task(task_id)
        elif choice == "5":
            print("Exiting Task Manager. Goodbye!")
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 5.")


if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        print("\nExiting Task Manager. Goodbye!")
