# task.py

class Task:
    def __init__(self, title, due_date=None, completed=False):
        self.title = title
        self.due_date = due_date
        self.completed = completed  # Expects a boolean (True/False)

    def mark_complete(self):
        self.completed = True

    def __str__(self):
        status = "X" if self.completed else " "
        due_str = f" (due {self.due_date})" if self.due_date else ""
        return f"[{status}] {self.title}{due_str}"