# src/task.py
# The Task class: one task = one object (data + behaviour together)


class Task:
    """Represents a single task in the task manager."""

    def __init__(self, id, description, completed=False):
        """
        Constructor - runs automatically when a Task object is created.

        Args:
            id (int): unique identifier
            description (str): what needs to be done
            completed (bool): completion status, defaults to False
        """
        self.id = id
        self.description = description
        self.completed = completed

    def mark_complete(self):
        """Marks this task as completed."""
        self.completed = True

    def to_dict(self):
        """Converts the Task object to a dict so it can be saved as JSON."""
        return {
            "id": self.id,
            "description": self.description,
            "completed": self.completed,
        }

    @classmethod
    def from_dict(cls, data):
        """Builds a Task object back from a dict loaded from JSON."""
        return cls(data["id"], data["description"], data.get("completed", False))

    def __str__(self):
        """User-friendly text, used by print(task)."""
        status = "Completed" if self.completed else "Pending"
        return f"ID: {self.id} | Description: {self.description} | Status: {status}"

    def __repr__(self):
        """Developer-friendly text, used in the debugger and repr(task)."""
        return f"Task(id={self.id}, description='{self.description}', completed={self.completed})"
