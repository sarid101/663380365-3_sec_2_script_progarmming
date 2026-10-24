# main.py
# CLI menu: asks the user what to fetch, calls APIClient, and prints the JSON data nicely.
from src.api_client import APIClient

POSTS_TO_SHOW = 5


def display_menu():
    print("\n--- API Data Fetcher Menu ---")
    print("1. Fetch a Single TODO Item")
    print("2. Fetch All Posts")
    print("3. Fetch TODOs by User ID")
    print("4. Exit")
    print("----------------------------")


def ask_positive_int(prompt):
    """Returns a positive int, or None (with a message) for invalid input."""
    text = input(prompt).strip()
    try:
        value = int(text)
    except ValueError:
        print(f"Invalid input '{text}'. Please enter a whole number.")
        return None
    if value <= 0:
        print("The number must be positive (1 or more).")
        return None
    return value


def shorten(text, length=50):
    text = (text or "").replace("\n", " ")
    return text if len(text) <= length else text[:length] + "..."


def show_single_todo(client):
    todo_id = ask_positive_int("Enter TODO ID (e.g., 1, 5, 10): ")
    if todo_id is None:
        return
    todo = client.fetch_single_todo(todo_id)
    if todo is None:
        return
    print("\n--- TODO Item Details ---")
    print(f"ID        : {todo.get('id')}")
    print(f"User ID   : {todo.get('userId')}")
    print(f"Title     : {todo.get('title')}")
    print(f"Completed : {todo.get('completed')}")
    print("-------------------------")


def show_all_posts(client):
    posts = client.fetch_all_posts()
    if posts is None:
        return
    print(f"\n--- First {min(POSTS_TO_SHOW, len(posts))} of {len(posts)} Posts ---")
    for post in posts[:POSTS_TO_SHOW]:
        print(f"[Post {post.get('id')}] User ID: {post.get('userId')}")
        print(f"  Title: {post.get('title')}")
        print(f"  Body : {shorten(post.get('body'))}")
    if len(posts) > POSTS_TO_SHOW:
        print(f"... and {len(posts) - POSTS_TO_SHOW} more posts not shown.")
    print("-----------------------------")


def show_user_todos(client):
    user_id = ask_positive_int("Enter User ID (e.g., 1, 2, 3): ")
    if user_id is None:
        return
    todos = client.fetch_user_todos(user_id)
    if todos is None:                  # request failed
        print(f"Could not retrieve TODOs for User ID {user_id}.")
        return
    print(f"\n--- TODOs for User ID {user_id} ---")
    if not todos:                      # request worked but the list is empty
        print("No TODOs found for this user (JSONPlaceholder has users 1-10).")
        return
    for todo in todos:
        status = "Completed" if todo.get("completed") else "Pending"
        print(f"ID: {todo.get('id'):>3} | {status:<9} | {todo.get('title')}")
    done = sum(1 for todo in todos if todo.get("completed"))
    print(f"Summary: {done}/{len(todos)} completed")
    print("-----------------------------")


def main():
    client = APIClient()
    actions = {"1": show_single_todo, "2": show_all_posts, "3": show_user_todos}

    while True:
        display_menu()
        choice = input("Enter your choice (1-4): ").strip()
        if choice == "4":
            print("Exiting API Data Fetcher. Goodbye!")
            break
        action = actions.get(choice)
        if action:
            action(client)
        else:
            print("Invalid choice. Please enter a number between 1 and 4.")


if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        print("\nExiting API Data Fetcher. Goodbye!")
