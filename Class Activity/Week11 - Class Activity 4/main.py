# main.py
# Orchestrator: builds the TaskManager (logic + data) and the CLIInterface (UI), then starts the loop.
from src.task_manager import TaskManager
from src.cli_interface import CLIInterface


def main():
    manager = TaskManager()
    cli = CLIInterface(manager)
    cli.run()


if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        print("\nExiting Task Manager. Goodbye!")
