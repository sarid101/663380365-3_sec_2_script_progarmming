# main.py
# Entry point for the Enhanced Task Manager
#
# Note: the starter code added 'src' to sys.path and did `from task_manager import ...`,
# but task_manager.py uses relative imports (`from .task import ...`), which fails
# with "attempted relative import with no known parent package".
# Importing through the 'src' package fixes that.
import logging
import sys

from src.task_manager import TaskManager
from src.cli_interface import CLIInterface


def main():
    # Run `python main.py --debug` to see logging messages from TaskManager/DataPersistence
    level = logging.INFO if "--debug" in sys.argv else logging.WARNING
    logging.basicConfig(level=level, format="%(levelname)s - %(name)s - %(message)s")

    manager = TaskManager()
    cli = CLIInterface(manager)
    try:
        cli.run()
    except (KeyboardInterrupt, EOFError):
        print("\nExiting Task Manager. Goodbye!")


if __name__ == "__main__":
    main()
