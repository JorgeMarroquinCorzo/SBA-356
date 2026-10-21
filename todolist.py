# todolist.py
"""Functions to manage a list of Task objects (from task.py)."""

from datetime import datetime, date

from task import Task


def add_task(task_list, title, due_date=None):
    """Creates a new Task and adds it to the list.

    If due_date is a string, it is parsed into a datetime.date
    using the format "YYYY-MM-DD". Parsing errors are caught and
    reported to the user without adding a bogus due date.
    """
    if isinstance(due_date, str):
        try:
            due_date = datetime.strptime(due_date, "%Y-%m-%d").date()
        except ValueError:
            print(f"Error: '{due_date}' is not a valid date "
                  f"(expected format YYYY-MM-DD). Task added without a due date.")
            due_date = None

    task = Task(title, due_date)
    task_list.append(task)
    print(f"Added task: {task.title}")
    return task


def complete_task(task_list, index):
    """Marks the task at the given index as completed.

    Invalid indices are handled gracefully with a friendly message.
    """
    try:
        task = task_list[index]
    except (IndexError, TypeError):
        print(f"Error: no task at index {index}.")
        return None

    task.mark_complete()
    print(f"Completed task: {task.title}")
    return task


def delete_task(task_list, index):
    """Removes the task at the given index from the list.

    Invalid indices are handled gracefully with a friendly message.
    """
    try:
        task = task_list.pop(index)
    except (IndexError, TypeError):
        print(f"Error: no task at index {index}. Nothing deleted.")
        return None

    print(f"Deleted task: {task.title}")
    return task


def list_tasks(task_list):
    """Prints a formatted list of tasks showing index, status,
    title, and due date. Flags tasks that are overdue (due date
    in the past and not yet completed).
    """
    if not task_list:
        print("No tasks in your to-do list.")
        return

    today = date.today()
    for i, task in enumerate(task_list):
        overdue = (task.due_date
                   and task.due_date < today
                   and not task.completed)
        print(f"{i}: {task}" + ("   <-- OVERDUE" if overdue else ""))