# src/data_persistence.py
# Data layer: the ONLY module that reads/writes data/tasks.json
import json
import os

from .task import Task, DueDateTask, PriorityTask

TASK_CLASSES = {"Task": Task, "DueDateTask": DueDateTask, "PriorityTask": PriorityTask}


class DataPersistence:
    """Loads tasks from JSON (rebuilding the right class) and saves them back."""

    def __init__(self, data_file="data/tasks.json"):
        project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.data_file_path = os.path.join(project_root, data_file)

    def load_tasks(self):
        try:
            with open(self.data_file_path, "r", encoding="utf-8") as f:
                raw_tasks = json.load(f)
        except FileNotFoundError:
            return []
        except json.JSONDecodeError:
            print("Warning: tasks.json is empty or corrupted. Starting with an empty task list.")
            return []

        tasks = []
        for data in raw_tasks:
            data = dict(data)
            task_type = data.pop("_type", "Task")
            data.setdefault("tags", [])       # tasks saved before tags existed
            cls = TASK_CLASSES.get(task_type)
            if cls is None:
                print(f"Warning: unknown task type '{task_type}', skipping ID {data.get('id')}.")
                continue
            try:
                tasks.append(cls(**data))
            except (TypeError, ValueError) as e:
                print(f"Warning: skipping invalid task ID {data.get('id')}: {e}")
        return tasks

    def save_tasks(self, tasks):
        os.makedirs(os.path.dirname(self.data_file_path), exist_ok=True)
        with open(self.data_file_path, "w", encoding="utf-8") as f:
            json.dump([t.to_dict() for t in tasks], f, indent=4, ensure_ascii=False)
