# src/data_persistence.py
# Handles loading/saving tasks to a JSON file
import json
import logging
import os

from .task import Task, DueDateTask, PriorityTask

logger = logging.getLogger(__name__)

# Map the '_type' field stored in JSON to the class that rebuilds it
TASK_TYPES = {
    "Task": Task,
    "DueDateTask": DueDateTask,
    "PriorityTask": PriorityTask,
}

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class DataPersistence:
    """
    Centralizes all file I/O and serialization/deserialization logic.
    A relative data_file path is resolved from the project root, so the app
    works no matter which folder it is started from.
    """

    def __init__(self, data_file="data/tasks.json"):
        if os.path.isabs(data_file):
            self.data_file_path = data_file
        else:
            self.data_file_path = os.path.join(PROJECT_ROOT, data_file)

    def load_tasks(self):
        """Loads tasks from JSON and rebuilds the correct Task subclass for each one."""
        if not os.path.exists(self.data_file_path):
            logger.info("No data file yet at %s; starting empty.", self.data_file_path)
            return []
        try:
            with open(self.data_file_path, "r", encoding="utf-8") as f:
                raw_tasks = json.load(f)
        except json.JSONDecodeError:
            print("Warning: tasks.json is empty or corrupted. Starting with an empty task list.")
            return []
        except OSError as e:
            print(f"Warning: could not read tasks file ({e}). Starting with an empty task list.")
            return []

        loaded_tasks = []
        for t_dict in raw_tasks:
            t_dict = dict(t_dict)                    # don't mutate the raw data
            task_type = t_dict.pop("_type", "Task")
            t_dict.setdefault("tags", [])            # old tasks may not have tags yet
            cls = TASK_TYPES.get(task_type)
            if cls is None:
                print(f"Warning: Unknown task type '{task_type}'. Skipping task ID {t_dict.get('id', 'N/A')}.")
                continue
            try:
                loaded_tasks.append(cls(**t_dict))
            except (TypeError, ValueError) as e:
                print(f"Warning: Skipping invalid task ID {t_dict.get('id', 'N/A')}: {e}")
        logger.info("Loaded %d task(s).", len(loaded_tasks))
        return loaded_tasks

    def save_tasks(self, tasks):
        """Saves Task objects to JSON using each object's to_dict() (polymorphism)."""
        os.makedirs(os.path.dirname(self.data_file_path), exist_ok=True)
        with open(self.data_file_path, "w", encoding="utf-8") as f:
            json.dump([task.to_dict() for task in tasks], f, indent=4, ensure_ascii=False)
        logger.info("Saved %d task(s).", len(tasks))
