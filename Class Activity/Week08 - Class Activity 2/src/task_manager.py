# src/task_manager.py
# The TaskManager class: owns the list of Task objects and does all operations + saving/loading
import json
import os

from .task import Task

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class TaskManager:
    """
    Manages the collection of Task objects: add, list, complete, delete,
    and loading/saving them to a JSON file.
    """

    def __init__(self, data_file="data/tasks.json"):
        """Loads existing tasks (if any) and works out the next free ID."""
        self.data_file = os.path.join(PROJECT_ROOT, data_file)
        self.tasks = self._load_tasks()
        self.next_id = self._get_next_task_id()

    # ---------- internal helpers ----------
    def _get_next_task_id(self):
        """Next unique ID = largest existing ID + 1 (or 1 if there are no tasks)."""
        return max((task.id for task in self.tasks), default=0) + 1

    def _load_tasks(self):
        """Reads JSON and converts each dict back into a Task object."""
        try:
            with open(self.data_file, "r", encoding="utf-8") as f:
                raw_tasks = json.load(f)
        except FileNotFoundError:
            return []          # first run, no file yet
        except json.JSONDecodeError:
            print("Warning: tasks.json is empty or corrupted. Starting with an empty task list.")
            return []

        tasks = []
        for data in raw_tasks:
            try:
                tasks.append(Task.from_dict(data))
            except (KeyError, TypeError):
                print(f"Warning: skipping an invalid task entry: {data}")
        return tasks

    def _save_tasks(self):
        """Converts each Task object to a dict and writes the list to JSON."""
        os.makedirs(os.path.dirname(self.data_file), exist_ok=True)
        with open(self.data_file, "w", encoding="utf-8") as f:
            json.dump([task.to_dict() for task in self.tasks], f, indent=4, ensure_ascii=False)

    def _find_task(self, task_id):
        """Returns the Task with this ID, or None."""
        for task in self.tasks:
            if task.id == task_id:
                return task
        return None

    # ---------- public operations ----------
    def add_task(self, description):
        """Creates a new Task object, stores it and saves."""
        new_task = Task(self.next_id, description)
        self.tasks.append(new_task)
        self.next_id += 1
        self._save_tasks()
        print(f"Task '{description}' added with ID {new_task.id}.")
        return new_task

    def list_tasks(self):
        """Prints every task - print(task) calls Task.__str__ automatically."""
        if not self.tasks:
            print("No tasks found.")
            return
        print("\n--- Your Tasks ---")
        for task in self.tasks:
            print(task)
        print("------------------")

    def complete_task(self, task_id):
        """Finds the task by ID and calls its mark_complete() method."""
        task = self._find_task(task_id)
        if task is None:
            print(f"Error: Task with ID {task_id} not found.")
        elif task.completed:
            print(f"Task ID {task_id} is already completed.")
        else:
            task.mark_complete()
            self._save_tasks()
            print(f"Task ID {task_id} marked as completed.")

    def delete_task(self, task_id):
        """Removes the task with this ID and saves."""
        task = self._find_task(task_id)
        if task is None:
            print(f"Error: Task with ID {task_id} not found.")
            return
        self.tasks.remove(task)
        self._save_tasks()
        print(f"Task ID {task_id} deleted successfully.")
