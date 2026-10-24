# tests/test_task_manager.py
# Run from the Week12 folder:  python -m unittest discover tests -v
import datetime
import json
import os
import tempfile
import unittest

from src.task import Task, DueDateTask, PriorityTask
from src.task_manager import TaskManager


class TaskManagerTestCase(unittest.TestCase):
    def setUp(self):
        # Each test uses its own temporary tasks.json, so data/tasks.json is never touched
        self.tmpdir = tempfile.TemporaryDirectory()
        self.data_file = os.path.join(self.tmpdir.name, "tasks.json")
        self.tm = TaskManager(self.data_file)
        self.tm.add_normal_task("Buy milk", tags=["Home", "shopping"])
        self.tm.add_due_date_task("Submit lab", "2026-10-26", tags=["study", "urgent"])
        self.tm.add_priority_task("Final project slides", "High", tags=["study", "project"])
        self.tm.add_due_date_task("Project exam", "2026-11-05", tags=["project"])
        self.tm.add_priority_task("Clean repos", "Low")

    def tearDown(self):
        self.tmpdir.cleanup()

    def ids(self, tasks):
        return [t.id for t in tasks]

    # --- Task models ---
    def test_tags_are_normalized_and_unique(self):
        task = Task(1, "x", tags=[" Work", "work", "URGENT", ""])
        self.assertEqual(task.tags, ["work", "urgent"])
        self.assertTrue(task.remove_tag("WORK"))
        self.assertFalse(task.remove_tag("missing"))
        self.assertEqual(task.tags, ["urgent"])

    def test_str_shows_extra_field_before_tags(self):
        task = DueDateTask(2, "Lab", "2026-10-26", tags=["study"])
        self.assertEqual(str(task), "ID: 2 | Description: Lab | Status: Pending | Due: 2026-10-26 | Tags: study")

    def test_invalid_priority_and_date(self):
        self.assertIsNone(self.tm.add_priority_task("x", "Urgent"))
        self.assertIsNone(self.tm.add_due_date_task("x", "26/10/2026"))
        self.assertEqual(len(self.tm.tasks), 5)

    # --- Persistence ---
    def test_save_and_reload_keeps_types_and_tags(self):
        self.tm.complete_task(1)
        reloaded = TaskManager(self.data_file)
        self.assertEqual([type(t).__name__ for t in reloaded.tasks],
                         ["Task", "DueDateTask", "PriorityTask", "DueDateTask", "PriorityTask"])
        self.assertTrue(reloaded.get_task_by_id(1).completed)
        self.assertEqual(reloaded.get_task_by_id(2).due_date, datetime.date(2026, 10, 26))
        self.assertEqual(reloaded.get_task_by_id(3).tags, ["study", "project"])
        self.assertEqual(reloaded.next_id, 6)

    def test_old_json_without_tags_still_loads(self):
        with open(self.data_file, "w", encoding="utf-8") as f:
            json.dump([{"id": 1, "description": "old", "completed": False, "_type": "Task"}], f)
        self.assertEqual(TaskManager(self.data_file).tasks[0].tags, [])

    def test_corrupted_json_starts_empty(self):
        with open(self.data_file, "w", encoding="utf-8") as f:
            f.write("{not json")
        self.assertEqual(TaskManager(self.data_file).tasks, [])

    # --- CRUD ---
    def test_complete_and_delete(self):
        self.assertEqual(self.tm.complete_task(2), (True, "Task marked as completed."))
        self.assertEqual(self.tm.complete_task(2), (False, "Task is already completed."))
        self.assertEqual(self.tm.delete_task(99), (False, "Task not found."))
        self.assertTrue(self.tm.delete_task(1)[0])
        self.assertEqual(self.ids(self.tm.tasks), [2, 3, 4, 5])

    # --- Search ---
    def test_search_description_and_tags_case_insensitive(self):
        self.assertEqual(self.ids(self.tm.search_tasks("PROJECT")), [3, 4])
        self.assertEqual(self.ids(self.tm.search_tasks("shop")), [1])   # partial tag match
        self.assertEqual(self.tm.search_tasks("   "), [])

    # --- Filter ---
    def test_filter_combines_criteria(self):
        self.tm.complete_task(4)
        self.assertEqual(self.ids(self.tm.filter_tasks(status=False)), [1, 2, 3, 5])
        self.assertEqual(self.ids(self.tm.filter_tasks(due_date_before=datetime.date(2026, 10, 31))), [2])
        self.assertEqual(self.ids(self.tm.filter_tasks(due_date_after=datetime.date(2026, 11, 1))), [4])
        self.assertEqual(self.ids(self.tm.filter_tasks(priority_level="High")), [3])
        self.assertEqual(self.ids(self.tm.filter_tasks(contains_tags=["Study", "project"])), [3])
        self.assertEqual(self.ids(self.tm.filter_tasks(status=False, contains_tags=["project"])), [3])
        self.assertEqual(self.ids(self.tm.filter_tasks()), [1, 2, 3, 4, 5])

    # --- Sort ---
    def test_sort_by_due_date_puts_tasks_without_date_last(self):
        self.assertEqual(self.ids(self.tm.sort_tasks("due_date")), [2, 4, 1, 3, 5])
        self.assertEqual(self.ids(self.tm.sort_tasks("due_date", reverse=True)), [4, 2, 1, 3, 5])

    def test_sort_by_priority_maps_high_medium_low(self):
        self.tm.add_priority_task("Medium thing", "medium")
        self.assertEqual(self.ids(self.tm.sort_tasks("priority")), [3, 6, 5, 1, 2, 4])
        self.assertEqual(self.ids(self.tm.sort_tasks("priority", reverse=True)), [5, 6, 3, 1, 2, 4])
        # ties keep ascending id order even when descending
        self.tm.add_priority_task("Another high", "High")
        self.assertEqual(self.ids(self.tm.sort_tasks("priority", reverse=True)), [5, 6, 3, 7, 1, 2, 4])

    def test_sort_other_criteria_and_unknown(self):
        self.assertEqual(self.ids(self.tm.sort_tasks("description")), [1, 5, 3, 4, 2])
        self.assertEqual(self.ids(self.tm.sort_tasks("id", reverse=True)), [5, 4, 3, 2, 1])
        self.assertEqual(self.ids(self.tm.sort_tasks("nonsense")), [1, 2, 3, 4, 5])

    def test_empty_manager(self):
        empty = TaskManager(os.path.join(self.tmpdir.name, "empty.json"))
        self.assertEqual(empty.search_tasks("x"), [])
        self.assertEqual(empty.filter_tasks(status=True), [])
        self.assertEqual(empty.sort_tasks("priority"), [])
        self.assertEqual(empty.next_id, 1)


if __name__ == "__main__":
    unittest.main()
