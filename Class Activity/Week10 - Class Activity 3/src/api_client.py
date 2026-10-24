# src/api_client.py
# All communication with the JSONPlaceholder API lives here.
import requests


class APIClient:
    """A small client for the JSONPlaceholder fake REST API."""

    BASE_URL = "https://jsonplaceholder.typicode.com"

    def __init__(self, base_url=None, timeout=10):
        self.base_url = base_url or self.BASE_URL
        self.timeout = timeout

    def _make_request(self, endpoint, params=None):
        """
        Sends a GET request and returns the parsed JSON (dict or list).
        Returns None if anything goes wrong, after printing what happened.
        """
        url = f"{self.base_url}{endpoint}"
        print(f"[INFO] GET {url}" + (f" params={params}" if params else ""))
        try:
            response = requests.get(url, params=params, timeout=self.timeout)
            print(f"[INFO] Status code: {response.status_code}")
            response.raise_for_status()      # 4xx / 5xx -> HTTPError
            return response.json()           # JSON text -> Python dict / list
        except requests.exceptions.HTTPError as e:
            if e.response is not None and e.response.status_code == 404:
                print("Error 404: Not found. The ID probably does not exist.")
            else:
                print(f"HTTP Error: {e}")
        except requests.exceptions.ConnectionError:
            print("Connection Error: could not reach the server. Check your internet connection.")
        except requests.exceptions.Timeout:
            print(f"Timeout Error: the server did not answer within {self.timeout} seconds.")
        except requests.exceptions.JSONDecodeError:
            # must come before RequestException because it is a subclass of it
            print("Error: the server response was not valid JSON.")
        except requests.exceptions.RequestException as e:
            print(f"Unexpected request error: {e}")
        return None

    def fetch_single_todo(self, todo_id):
        """GET /todos/<id> -> one TODO dict."""
        return self._make_request(f"/todos/{todo_id}")

    def fetch_all_posts(self):
        """GET /posts -> list of 100 post dicts."""
        return self._make_request("/posts")

    def fetch_user_todos(self, user_id):
        """GET /todos?userId=<id> -> list of that user's TODO dicts."""
        return self._make_request("/todos", params={"userId": user_id})
