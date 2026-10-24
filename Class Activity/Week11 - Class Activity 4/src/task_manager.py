# src/task_manager.py
# Business logic layer: manages Task objects. No input()/print() menus and no file I/O here.
import datetime

from .task import Task, DueDateTask, PriorityTask
from .data_persistence import DataPersistence


class TaskManager:
    """Add, complete, delete, search, filter and sort tasks."""

    PRIORITY_ORDER = {"High": 1, "Medium": 2, "Low": 3}

    def __init__(self, data_file="data/tasks.json"):
        self.persistence = DataPersistence(data_file)
        self.tasks = self.persistence.load_tasks()
        self.next_id = max((t.id for t in self.tasks), default=0) + 1

    def _save_changes(self):
        self.persistence.save_tasks(self.tasks)

    def _add(self, task):
        self.tasks.append(task)
        self.next_id += 1
        self._save_changes()
        return task

    # --- CRUD ---
    def add_normal_task(self, description, tags=None):
        return self._add(Task(self.next_id, description, tags=tags))

    def add_due_date_task(self, description, due_date_str, tags=None):
        return self._add(DueDateTask(self.next_id, description, due_date_str, tags=tags))

    def add_priority_task(self, description, priority, tags=None):
        return self._add(PriorityTask(self.next_id, description, priority, tags=tags))

    def get_task_by_id(self, task_id):
        return next((t for t in self.tasks if t.id == task_id), None)

    def get_all_tasks(self):
        return list(self.tasks)

    def complete_task(self, task_id):
        task = self.get_task_by_id(task_id)
        if task is None:
            return False, "Task not found."
        if task.completed:
            return False, "Task is already completed."
        task.mark_complete()
        self._save_changes()
        return True, "Task marked as completed."

    def delete_task(self, task_id):
        task = self.get_task_by_id(task_id)
        if task is None:
            return False, "Task not found."
        self.tasks.remove(task)
        self._save_changes()
        return True, "Task deleted successfully."

    # --- Assignment: search / filter / sort ---
    def search_tasks(self, keyword):
        """Keyword in description or in any tag, case-insensitive."""
        keyword = keyword.strip().lower()
        if not keyword:
            return []
        return [t for t in self.tasks
                if keyword in t.description.lower() or any(keyword in tag.lower() for tag in t.tags)]

    def filter_tasks(self, status=None, due_date_before=None, priority=None, tag=None):
        """
        Every given criterion must match (AND). Leave a criterion as None to skip it.
            status: True (completed) / False (pending)
            due_date_before: 'YYYY-MM-DD' -> DueDateTasks due on or before that date
            priority: 'High' / 'Medium' / 'Low' -> PriorityTasks with that priority
            tag: a single tag the task must have
        """
        result = self.tasks
        if status is not None:
            result = [t for t in result if t.completed == status]
        if due_date_before:
            limit = datetime.datetime.strptime(due_date_before, "%Y-%m-%d").date()
            result = [t for t in result if isinstance(t, DueDateTask) and t.due_date <= limit]
        if priority:
            result = [t for t in result if isinstance(t, PriorityTask) and t.priority == priority]
        if tag:
            tag = tag.strip().lower()
            result = [t for t in result if tag in (x.lower() for x in t.tags)]
        return list(result)

    def sort_tasks(self, criterion="id", reverse=False):
        """
        criterion: 'id', 'due_date' or 'priority'.
        Tasks without a due date / priority are placed after the others.
        """
        if criterion == "due_date":
            key = lambda t: (0, t.due_date) if isinstance(t, DueDateTask) else (1, datetime.date.max)
        elif criterion == "priority":
            key = lambda t: (0, self.PRIORITY_ORDER[t.priority]) if isinstance(t, PriorityTask) else (1, 99)
        else:
            return sorted(self.tasks, key=lambda t: t.id, reverse=reverse)

        with_value = sorted((t for t in self.tasks if key(t)[0] == 0), key=key, reverse=reverse)
        without_value = [t for t in self.tasks if key(t)[0] == 1]
        return with_value + without_value
