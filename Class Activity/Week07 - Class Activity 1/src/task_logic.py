# src/task_logic.py
# Business logic: add, list, complete, delete tasks.
# Each task is a dict: {"id": 1, "description": "Buy groceries", "completed": False}


def get_next_task_id(tasks):
    """Generates a unique ID for a new task (largest ID + 1)."""
    return max((task["id"] for task in tasks), default=0) + 1


def find_task(tasks, task_id):
    """Returns the task dict with this ID, or None if it does not exist."""
    for task in tasks:
        if task["id"] == task_id:
            return task
    return None


def add_task(tasks, description):
    """Adds a new pending task and returns it."""
    new_task = {
        "id": get_next_task_id(tasks),
        "description": description,
        "completed": False,
    }
    tasks.append(new_task)
    print(f"Task '{description}' added with ID {new_task['id']}.")
    return new_task


def list_tasks(tasks):
    """Prints all tasks as a table with [DONE] / [PENDING] status and a summary."""
    if not tasks:
        print("No tasks found. Choose 1 to add one.")
        return

    line = "=" * 60
    print(f"\n{line}")
    print(f"{'ID':<6}| {'Status':<11}| Description")
    print("-" * 60)
    for task in tasks:
        status = "[DONE]" if task["completed"] else "[PENDING]"
        print(f"#{task['id']:<5}| {status:<11}| {task['description']}")
    print(line)
    done = sum(1 for task in tasks if task["completed"])
    print(f"Summary: {done}/{len(tasks)} task(s) completed.")


def complete_task(tasks, task_id):
    """Marks a task as completed. Returns True if something changed."""
    task = find_task(tasks, task_id)
    if task is None:
        print(f"Error: Task with ID {task_id} not found.")
        return False
    if task["completed"]:
        print(f"Task ID {task_id} is already completed.")
        return False
    task["completed"] = True
    print(f"Task ID {task_id} marked as completed.")
    return True


def delete_task(tasks, task_id):
    """Deletes a task by ID. Returns True if a task was removed."""
    task = find_task(tasks, task_id)
    if task is None:
        print(f"Error: Task with ID {task_id} not found.")
        return False
    tasks.remove(task)
    print(f"Task ID {task_id} ('{task['description']}') deleted successfully.")
    return True
