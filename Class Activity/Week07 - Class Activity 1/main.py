# main.py
# Entry point: menu loop + user input. Logic lives in src/task_logic.py,
# file I/O lives in src/task_data.py
from src import task_data, task_logic


def display_menu():
    print("\n--- Task Manager Menu ---")
    print("1. Add Task")
    print("2. List Tasks")
    print("3. Complete Task")
    print("4. Delete Task")
    print("5. Exit")
    print("-------------------------")


def ask_task_id(action):
    """Asks for a task ID. Returns an int, or None if the input is not a number."""
    text = input(f"Enter ID of task to {action}: ").strip()
    try:
        return int(text)
    except ValueError:
        print(f"Invalid input '{text}'. Please enter a number for Task ID.")
        return None


def main():
    tasks = task_data.load_tasks()          # load at startup
    print(f"Loaded {len(tasks)} task(s).")

    while True:
        display_menu()
        choice = input("Enter your choice (1-5): ").strip()
        changed = False

        if choice == "1":
            description = input("Enter task description: ").strip()
            if description:
                task_logic.add_task(tasks, description)
                changed = True
            else:
                print("Task description cannot be empty.")
        elif choice == "2":
            task_logic.list_tasks(tasks)
        elif choice == "3":
            task_id = ask_task_id("complete")
            if task_id is not None:
                changed = task_logic.complete_task(tasks, task_id)
        elif choice == "4":
            task_id = ask_task_id("delete")
            if task_id is not None:
                changed = task_logic.delete_task(tasks, task_id)
        elif choice == "5":
            task_data.save_tasks(tasks)
            print("Saving tasks and exiting. Goodbye!")
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 5.")

        # Save after every change too, so nothing is lost if the program is closed
        if changed:
            task_data.save_tasks(tasks)


if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        print("\nExiting. Your last changes were already saved.")
