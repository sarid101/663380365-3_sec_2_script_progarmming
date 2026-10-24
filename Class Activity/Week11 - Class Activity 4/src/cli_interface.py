# src/cli_interface.py
# User interface layer: menus, input validation and printing. Calls TaskManager for everything else.
import datetime


class CLIInterface:
    def __init__(self, task_manager):
        self.manager = task_manager

    # ---------- display ----------
    def display_menu(self):
        print("\n--- Enhanced Task Manager Menu (Week 11) ---")
        print("1. Add Normal Task")
        print("2. Add Due Date Task")
        print("3. Add Priority Task")
        print("4. List All Tasks")
        print("5. Complete Task")
        print("6. Delete Task")
        print("7. Search Tasks")
        print("8. Filter Tasks")
        print("9. Sort Tasks")
        print("0. Exit")
        print("--------------------------------------------")

    def show_tasks(self, tasks, title):
        if not tasks:
            print(f"No tasks found ({title}).")
            return
        print(f"\n--- {title} ({len(tasks)}) ---")
        for task in tasks:
            print(task)
        print("-" * 30)

    # ---------- input helpers ----------
    def get_task_description(self):
        while True:
            description = input("Enter task description: ").strip()
            if description:
                return description
            print("Task description cannot be empty. Please try again.")

    def get_due_date_input(self, prompt="Enter due date (YYYY-MM-DD): ", allow_blank=False):
        while True:
            text = input(prompt).strip()
            if allow_blank and not text:
                return None
            try:
                datetime.datetime.strptime(text, "%Y-%m-%d")
                return text
            except ValueError:
                print("Invalid date format. Please use YYYY-MM-DD (e.g., 2026-12-31).")

    def get_priority_input(self):
        while True:
            priority = input("Enter priority (High/Medium/Low): ").strip().capitalize()
            if priority in ("High", "Medium", "Low"):
                return priority
            print("Invalid priority. Please enter 'High', 'Medium', or 'Low'.")

    def get_tags_input(self):
        text = input("Enter tags (comma-separated, e.g. work,urgent - optional): ").strip()
        return [tag.strip().lower() for tag in text.split(",") if tag.strip()]

    def get_task_id(self, action):
        try:
            return int(input(f"Enter ID of task to {action}: ").strip())
        except ValueError:
            print("Invalid input. Please enter a number for Task ID.")
            return None

    # ---------- main loop ----------
    def run(self):
        while True:
            self.display_menu()
            choice = input("Enter your choice (0-9): ").strip()

            if choice == "1":
                task = self.manager.add_normal_task(self.get_task_description(), tags=self.get_tags_input())
                print(f"Normal Task '{task.description}' added with ID {task.id}.")
            elif choice == "2":
                description = self.get_task_description()
                due = self.get_due_date_input()
                task = self.manager.add_due_date_task(description, due, tags=self.get_tags_input())
                print(f"Due Date Task '{task.description}' (Due: {task.due_date:%Y-%m-%d}) added with ID {task.id}.")
            elif choice == "3":
                description = self.get_task_description()
                priority = self.get_priority_input()
                task = self.manager.add_priority_task(description, priority, tags=self.get_tags_input())
                print(f"Priority Task '{task.description}' (Priority: {task.priority}) added with ID {task.id}.")
            elif choice == "4":
                self.show_tasks(self.manager.get_all_tasks(), "Your Tasks")
            elif choice in ("5", "6"):
                action = "complete" if choice == "5" else "delete"
                task_id = self.get_task_id(action)
                if task_id is not None:
                    method = self.manager.complete_task if choice == "5" else self.manager.delete_task
                    print(method(task_id)[1])
            elif choice == "7":
                keyword = input("Enter search keyword (description or tag): ").strip()
                self.show_tasks(self.manager.search_tasks(keyword), f"Search Results for '{keyword}'")
            elif choice == "8":
                self.filter_menu()
            elif choice == "9":
                criterion = input("Sort by (id, due_date, priority - default: id): ").strip().lower() or "id"
                if criterion not in ("id", "due_date", "priority"):
                    print(f"Unknown criterion '{criterion}', using id.")
                    criterion = "id"
                reverse = input("Reverse order? (yes/no - default: no): ").strip().lower() == "yes"
                self.show_tasks(self.manager.sort_tasks(criterion, reverse), f"Sorted by {criterion}")
            elif choice == "0":
                print("Exiting Task Manager. Goodbye!")
                break
            else:
                print("Invalid choice. Please enter a number between 0 and 9.")

    def filter_menu(self):
        print("\n--- Filter Tasks (press Enter to skip a criterion) ---")
        status_text = input("Completed? (true/false): ").strip().lower()
        status = {"true": True, "false": False}.get(status_text)
        due_before = self.get_due_date_input("Due on or before (YYYY-MM-DD): ", allow_blank=True)
        priority = input("Priority (High/Medium/Low): ").strip().capitalize() or None
        if priority not in (None, "High", "Medium", "Low"):
            print(f"Unknown priority '{priority}', ignoring it.")
            priority = None
        tag = input("Tag: ").strip() or None
        tasks = self.manager.filter_tasks(status=status, due_date_before=due_before, priority=priority, tag=tag)
        self.show_tasks(tasks, "Filtered Tasks")
