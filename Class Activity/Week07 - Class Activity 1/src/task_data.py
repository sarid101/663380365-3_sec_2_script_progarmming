# src/task_data.py
# Persistence layer: load/save the task list (list of dicts) to data/tasks.json
import json
import os

TASKS_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data", "tasks.json")


def load_tasks():
    """Loads tasks from the JSON file. Returns [] if the file is missing or broken."""
    try:
        with open(TASKS_FILE, "r", encoding="utf-8") as f:
            tasks = json.load(f)
    except FileNotFoundError:
        # First run: no file yet
        return []
    except json.JSONDecodeError:
        print("Warning: tasks.json is empty or corrupted. Starting with an empty task list.")
        return []

    if not isinstance(tasks, list):
        print("Warning: tasks.json has an unexpected format. Starting with an empty task list.")
        return []
    return tasks


def save_tasks(tasks):
    """Saves tasks to the JSON file (creates the data folder if needed).
    Returns True on success, False if the file could not be written."""
    try:
        os.makedirs(os.path.dirname(TASKS_FILE), exist_ok=True)
        with open(TASKS_FILE, "w", encoding="utf-8") as f:
            json.dump(tasks, f, indent=4, ensure_ascii=False)
    except OSError as e:
        print(f"Error: could not save tasks ({e}).")
        return False
    return True
