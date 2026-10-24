# src/cli_interface.py
# User interaction only: menus, input validation, output. Calls TaskManager for all logic.
import datetime


def parse_date(text):
    """Returns a datetime.date from 'YYYY-MM-DD', or raises ValueError."""
    return datetime.datetime.strptime(text.strip(), "%Y-%m-%d").date()


def parse_tags(text):
    """'Work, Urgent ,home' -> ['work', 'urgent', 'home']"""
    return [tag.strip().lower() for tag in text.split(",") if tag.strip()]


class CLIInterface:
    """Handles all command-line interaction and delegates work to TaskManager."""

    MENU = [
        ("1", "Add Normal Task"),
        ("2", "Add Due Date Task"),
        ("3", "Add Priority Task"),
        ("4", "List All Tasks"),
        ("5", "Complete Task"),
        ("6", "Delete Task"),
        ("7", "Search Tasks"),
        ("8", "Filter Tasks"),
        ("9", "Sort Tasks"),
        ("10", "Add / Remove Tags"),
        ("0", "Exit"),
    ]

    def __init__(self, task_manager):
        self.manager = task_manager
        self.actions = {
            "1": self.add_normal_task,
            "2": self.add_due_date_task,
            "3": self.add_priority_task,
            "4": self.list_tasks,
            "5": self.complete_task,
            "6": self.delete_task,
            "7": self.search_tasks,
            "8": self.filter_tasks,
            "9": self.sort_tasks,
            "10": self.manage_tags,
        }

    # ---------- input helpers ----------
    def display_menu(self):
        print("\n===== Enhanced Task Manager =====")
        for key, label in self.MENU:
            print(f"{key:>2}. {label}")
        print("=================================")

    def get_task_description(self):
        while True:
            description = input("Enter task description: ").strip()
            if description:
                return description
            print("Task description cannot be empty. Please try again.")

    def get_due_date_input(self):
        while True:
            text = input("Enter due date (YYYY-MM-DD): ").strip()
            try:
                return parse_date(text)
            except ValueError:
                print("Invalid date. Please use YYYY-MM-DD (e.g., 2026-12-31).")

    def get_priority_input(self):
        while True:
            priority = input("Enter priority (High/Medium/Low): ").strip().capitalize()
            if priority in ("High", "Medium", "Low"):
                return priority
            print("Invalid priority. Please enter High, Medium, or Low.")

    def get_tags_input(self, prompt="Enter tags (comma-separated, optional): "):
        return parse_tags(input(prompt))

    def get_task_id(self, action):
        text = input(f"Enter ID of task to {action}: ").strip()
        try:
            return int(text)
        except ValueError:
            print("Invalid input. Please enter a number for Task ID.")
            return None

    def get_optional_date(self, prompt):
        while True:
            text = input(prompt).strip()
            if not text:
                return None
            try:
                return parse_date(text)
            except ValueError:
                print("Invalid date. Use YYYY-MM-DD or leave blank.")

    def _display_tasks(self, tasks, title="Tasks"):
        if not tasks:
            print(f"No tasks found ({title}).")
            return
        print(f"\n--- {title} ({len(tasks)}) ---")
        for task in tasks:
            print(task)
        print("-" * 40)

    # ---------- menu actions ----------
    def add_normal_task(self):
        description = self.get_task_description()
        task = self.manager.add_normal_task(description, tags=self.get_tags_input())
        print(f"Normal Task '{task.description}' added with ID {task.id}.")

    def add_due_date_task(self):
        description = self.get_task_description()
        due_date = self.get_due_date_input()
        task = self.manager.add_due_date_task(description, due_date, tags=self.get_tags_input())
        print(f"Due Date Task '{task.description}' (Due: {task.due_date:%Y-%m-%d}) added with ID {task.id}.")

    def add_priority_task(self):
        description = self.get_task_description()
        priority = self.get_priority_input()
        task = self.manager.add_priority_task(description, priority, tags=self.get_tags_input())
        print(f"Priority Task '{task.description}' (Priority: {task.priority}) added with ID {task.id}.")

    def list_tasks(self):
        self._display_tasks(self.manager.get_all_tasks(), "All Tasks")

    def complete_task(self):
        task_id = self.get_task_id("complete")
        if task_id is not None:
            print(self.manager.complete_task(task_id)[1])

    def delete_task(self):
        task_id = self.get_task_id("delete")
        if task_id is None:
            return
        task = self.manager.get_task_by_id(task_id)
        if task is None:
            print("Task not found.")
            return
        confirm = input(f"Delete '{task.description}'? (yes/no): ").strip().lower()
        if confirm in ("yes", "y"):
            print(self.manager.delete_task(task_id)[1])
        else:
            print("Delete cancelled.")

    def search_tasks(self):
        keyword = input("Enter search keyword (description or tags): ").strip()
        if not keyword:
            print("Please enter a keyword.")
            return
        self._display_tasks(self.manager.search_tasks(keyword), f"Search results for '{keyword}'")

    def filter_tasks(self):
        print("\n--- Filter Tasks (leave blank to skip a criterion) ---")
        status_text = input("Completed? (yes/no): ").strip().lower()
        status = {"yes": True, "y": True, "no": False, "n": False}.get(status_text)
        due_before = self.get_optional_date("Due on or before (YYYY-MM-DD): ")
        due_after = self.get_optional_date("Due on or after (YYYY-MM-DD): ")
        priority = input("Priority (High/Medium/Low): ").strip().capitalize()
        priority = priority if priority in ("High", "Medium", "Low") else None
        tags = self.get_tags_input("Must have ALL these tags (comma-separated): ") or None

        tasks = self.manager.filter_tasks(status=status, due_date_before=due_before,
                                          due_date_after=due_after, priority_level=priority,
                                          contains_tags=tags)
        self._display_tasks(tasks, "Filtered Tasks")

    def sort_tasks(self):
        print("\n--- Sort Tasks ---")
        print("Criteria: " + ", ".join(self.manager.SORT_CRITERIA))
        criterion = input("Sort by (default: id): ").strip().lower() or "id"
        if criterion not in self.manager.SORT_CRITERIA:
            print(f"Unknown criterion '{criterion}'. Sorting by id.")
            criterion = "id"
        reverse = input("Descending order? (yes/no, default: no): ").strip().lower() in ("yes", "y")
        order = "Descending" if reverse else "Ascending"
        self._display_tasks(self.manager.sort_tasks(criterion, reverse), f"Sorted by {criterion} ({order})")

    def manage_tags(self):
        task_id = self.get_task_id("edit tags")
        if task_id is None:
            return
        task = self.manager.get_task_by_id(task_id)
        if task is None:
            print("Task not found.")
            return
        print(task)
        action = input("(a)dd or (r)emove tags? ").strip().lower()
        if action in ("a", "add"):
            tags = self.get_tags_input("Tags to add (comma-separated): ")
            print(self.manager.add_tags(task_id, tags)[1] if tags else "No tags entered.")
        elif action in ("r", "remove"):
            tag = input("Tag to remove: ").strip()
            print(self.manager.remove_tag(task_id, tag)[1] if tag else "No tag entered.")
        else:
            print("Invalid choice. Enter 'a' or 'r'.")

    # ---------- main loop ----------
    def run(self):
        while True:
            self.display_menu()
            choice = input("Enter your choice (0-10): ").strip()
            if choice == "0":
                print("Exiting Task Manager. Goodbye!")
                break
            action = self.actions.get(choice)
            if action:
                action()
            else:
                print("Invalid choice. Please enter a number between 0 and 10.")
