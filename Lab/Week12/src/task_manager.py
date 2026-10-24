# src/task_manager.py
# Business logic: add, list, complete, delete, tags, search, filter, sort
import datetime
import logging

from .task import Task, DueDateTask, PriorityTask
from .data_persistence import DataPersistence

logger = logging.getLogger(__name__)


class TaskManager:
    """
    Manages the collection of Task objects.
    Contains no input()/print() for menus - that is CLIInterface's job.
    """

    PRIORITY_MAP = {"High": 1, "Medium": 2, "Low": 3}
    SORT_CRITERIA = ("id", "description", "completed", "due_date", "priority")

    def __init__(self, data_file="data/tasks.json"):
        self.persistence = DataPersistence(data_file)
        self.tasks = self.persistence.load_tasks()
        self.next_id = self._get_next_task_id()

    def _get_next_task_id(self):
        """Generates the next unique ID for a new task."""
        return max((task.id for task in self.tasks), default=0) + 1

    def _save_changes(self):
        self.persistence.save_tasks(self.tasks)

    def _add(self, task):
        self.tasks.append(task)
        self.next_id += 1
        self._save_changes()
        logger.info("Task added: %r", task)
        return task

    # --- Basic CRUD ---
    def add_normal_task(self, description, tags=None):
        return self._add(Task(self.next_id, description, tags=tags))

    def add_due_date_task(self, description, due_date, tags=None):
        """due_date may be 'YYYY-MM-DD' or datetime.date. Returns None if invalid."""
        try:
            task = DueDateTask(self.next_id, description, due_date, tags=tags)
        except (ValueError, TypeError):
            logger.warning("Invalid due date: %r", due_date)
            return None
        return self._add(task)

    def add_priority_task(self, description, priority, tags=None):
        """Returns None if the priority is not High/Medium/Low."""
        try:
            task = PriorityTask(self.next_id, description, priority, tags=tags)
        except ValueError:
            logger.warning("Invalid priority: %r", priority)
            return None
        return self._add(task)

    def get_task_by_id(self, task_id):
        return next((task for task in self.tasks if task.id == task_id), None)

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

    # --- Tags ---
    def add_tags(self, task_id, tags):
        task = self.get_task_by_id(task_id)
        if task is None:
            return False, "Task not found."
        for tag in tags:
            task.add_tag(tag)
        self._save_changes()
        return True, f"Tags now: {', '.join(task.tags) if task.tags else '(none)'}"

    def remove_tag(self, task_id, tag):
        task = self.get_task_by_id(task_id)
        if task is None:
            return False, "Task not found."
        if not task.remove_tag(tag):
            return False, f"Task {task_id} has no tag '{tag.strip().lower()}'."
        self._save_changes()
        return True, f"Tag removed. Tags now: {', '.join(task.tags) if task.tags else '(none)'}"

    # --- Search / Filter / Sort ---
    def search_tasks(self, keyword):
        """Case-insensitive partial-match search in description and tags."""
        keyword = (keyword or "").strip().lower()
        if not keyword:
            return []
        return [
            t for t in self.tasks
            if keyword in t.description.lower() or any(keyword in tag for tag in t.tags)
        ]

    def filter_tasks(self, status=None, due_date_before=None, due_date_after=None,
                     priority_level=None, contains_tags=None):
        """
        Combines all given criteria with AND.
            status (bool): True = completed, False = pending
            due_date_before / due_date_after (datetime.date): inclusive range, DueDateTask only
            priority_level (str): High / Medium / Low, PriorityTask only
            contains_tags (list[str]): task must have ALL of these tags
        """
        result = list(self.tasks)
        if status is not None:
            result = [t for t in result if t.completed == status]
        if due_date_before is not None:
            result = [t for t in result if isinstance(t, DueDateTask) and t.due_date <= due_date_before]
        if due_date_after is not None:
            result = [t for t in result if isinstance(t, DueDateTask) and t.due_date >= due_date_after]
        if priority_level:
            result = [t for t in result if isinstance(t, PriorityTask) and t.priority == priority_level]
        if contains_tags:
            wanted = {tag.strip().lower() for tag in contains_tags if tag.strip()}
            result = [t for t in result if wanted.issubset(t.tags)]
        return result

    def sort_tasks(self, criterion="id", reverse=False, tasks=None):
        """
        Returns a new sorted list (does not change the stored order).
        Tasks without a due date / priority always go LAST, even when reverse=True.
        """
        tasks = list(self.tasks if tasks is None else tasks)
        if criterion not in self.SORT_CRITERIA:
            logger.warning("Unknown sort criterion %r; using id.", criterion)
            criterion = "id"

        if criterion == "id":
            return sorted(tasks, key=lambda t: t.id, reverse=reverse)
        # Sort by id first; Python's sort is stable, so tasks with an equal key
        # keep ascending id order even when reverse=True.
        tasks.sort(key=lambda t: t.id)
        if criterion == "description":
            return sorted(tasks, key=lambda t: t.description.lower(), reverse=reverse)
        if criterion == "completed":
            return sorted(tasks, key=lambda t: t.completed, reverse=reverse)

        if criterion == "due_date":
            has_value = [t for t in tasks if isinstance(t, DueDateTask)]
            key = lambda t: t.due_date
        else:  # priority: map High/Medium/Low -> 1/2/3 so they sort correctly
            has_value = [t for t in tasks if isinstance(t, PriorityTask)]
            key = lambda t: self.PRIORITY_MAP[t.priority]
        without_value = [t for t in tasks if t not in has_value]
        return sorted(has_value, key=key, reverse=reverse) + without_value
