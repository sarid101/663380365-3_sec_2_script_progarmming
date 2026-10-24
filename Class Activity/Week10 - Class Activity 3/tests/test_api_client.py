# tests/test_api_client.py
# Tests APIClient without using the internet: requests.get is replaced with a fake (mock).
# Run from this folder:  python -m unittest discover tests -v
import unittest
from unittest import mock

import requests

from src.api_client import APIClient


def fake_response(status=200, json_data=None, text=None):
    """Builds a real requests.Response object with the given status and body."""
    resp = requests.Response()
    resp.status_code = status
    resp._content = (text if text is not None else __import__("json").dumps(json_data)).encode()
    resp.url = "https://jsonplaceholder.typicode.com/test"
    return resp


class APIClientTest(unittest.TestCase):
    def setUp(self):
        self.client = APIClient()
        self.patcher = mock.patch("src.api_client.requests.get")
        self.get = self.patcher.start()
        self.addCleanup(self.patcher.stop)
        self.print_patch = mock.patch("builtins.print")   # keep test output quiet
        self.printed = self.print_patch.start()
        self.addCleanup(self.print_patch.stop)

    def test_single_todo_returns_dict_and_calls_right_url(self):
        todo = {"userId": 1, "id": 1, "title": "delectus aut autem", "completed": False}
        self.get.return_value = fake_response(json_data=todo)
        self.assertEqual(self.client.fetch_single_todo(1), todo)
        self.get.assert_called_once_with(
            "https://jsonplaceholder.typicode.com/todos/1", params=None, timeout=10)

    def test_all_posts_returns_list(self):
        posts = [{"id": i, "userId": 1, "title": f"t{i}", "body": "b"} for i in range(1, 101)]
        self.get.return_value = fake_response(json_data=posts)
        self.assertEqual(len(self.client.fetch_all_posts()), 100)

    def test_user_todos_uses_query_param(self):
        self.get.return_value = fake_response(json_data=[])
        self.assertEqual(self.client.fetch_user_todos(3), [])
        self.get.assert_called_once_with(
            "https://jsonplaceholder.typicode.com/todos", params={"userId": 3}, timeout=10)

    def test_404_returns_none(self):
        self.get.return_value = fake_response(status=404, json_data={})
        self.assertIsNone(self.client.fetch_single_todo(999999))

    def test_500_returns_none(self):
        self.get.return_value = fake_response(status=500, text="Server error")
        self.assertIsNone(self.client.fetch_all_posts())

    def test_connection_error_returns_none(self):
        self.get.side_effect = requests.exceptions.ConnectionError("no network")
        self.assertIsNone(self.client.fetch_all_posts())

    def test_timeout_returns_none(self):
        self.get.side_effect = requests.exceptions.Timeout("slow")
        self.assertIsNone(self.client.fetch_single_todo(1))

    def test_invalid_json_returns_none(self):
        self.get.return_value = fake_response(text="<html>not json</html>")
        self.assertIsNone(self.client.fetch_single_todo(1))
        messages = " ".join(str(c.args[0]) for c in self.printed.call_args_list)
        self.assertIn("not valid JSON", messages)


if __name__ == "__main__":
    unittest.main()
