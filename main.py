# main.py


import csv
import os
from datetime import datetime

from task import Task
from todolist import add_task, complete_task, delete_task, list_tasks

TASKS_FILE = "tasks.csv"

MENU = """
===== TO-DO LIST MANAGER =====
(A) Add a new task
(C) Mark a task as completed
(D) Delete a task
(L) List all tasks
(Q) Quit
==============================
"""


def load_tasks(filename=TASKS_FILE):
    """Loads tasks from a CSV file, reconstructing Task objects.

    Returns an empty list if the file does not exist. Malformed
    lines and bad dates are skipped with a user-friendly message.
    """
    tasks = []
    if not os.path.exists(filename):
        return tasks

    try:
        with open(filename, newline="", encoding="utf-8") as f:
            reader = csv.reader(f)
            for line_no, row in enumerate(reader, start=1):
                if not row:                      # skip blank lines
                    continue
                if len(row) != 3:
                    print(f"Warning: skipping malformed line {line_no} in '{filename}'.")
                    continue
                title, due_str, completed_str = (field.strip() for field in row)
                due_date = None
                if due_str:
                    try:
                        due_date = datetime.strptime(due_str, "%Y-%m-%d").date()
                    except ValueError:
                        print(f"Warning: bad date '{due_str}' on line {line_no}; "
                              f"task '{title}' loaded without a due date.")
                tasks.append(Task(title, due_date, completed_str == "True"))
    except OSError as e:
        print(f"Error reading '{filename}': {e}. Starting with an empty list.")
        return []
    return tasks


def save_tasks(task_list, filename=TASKS_FILE):
    """Writes the task list to a CSV file: title, due_date, completed."""
    try:
        with open(filename, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            for task in task_list:
                due = task.due_date.isoformat() if task.due_date else ""
                writer.writerow([task.title, due, task.completed])
    except OSError as e:
        print(f"Error saving file '{filename}': {e}")
        return False
    print(f"Saved {len(task_list)} task(s) to '{filename}'.")
    return True


def prompt_index(prompt):
    """Asks the user for a task index; returns an int or None on bad input."""
    raw = input(prompt).strip()
    try:
        return int(raw)
    except ValueError:
        print(f"Error: '{raw}' is not a valid number.")
        return None


def main():
    tasks = load_tasks()
    if tasks:
        print(f"Loaded {len(tasks)} task(s) from '{TASKS_FILE}'.")

    while True:
        print(MENU)
        choice = input("Enter your choice (A/C/D/L/Q): ").strip().upper()

        if choice == "A":
            title = input("Task title: ").strip()
            if not title:
                print("Error: title cannot be empty.")
                continue
            due = input("Due date (YYYY-MM-DD, or press Enter to skip): ").strip()
            add_task(tasks, title, due or None)

        elif choice == "C":
            list_tasks(tasks)
            index = prompt_index("Enter the index of the task to complete: ")
            if index is not None:
                complete_task(tasks, index)

        elif choice == "D":
            list_tasks(tasks)
            index = prompt_index("Enter the index of the task to delete: ")
            if index is not None:
                delete_task(tasks, index)

        elif choice == "L":
            list_tasks(tasks)

        elif choice == "Q":
            save = input("Save task list before quitting? (y/n): ").strip().lower()
            if save == "y":
                save_tasks(tasks)
            print("Goodbye!")
            break

        else:
            print(f"Error: '{choice}' is not a valid option. Please choose A, C, D, L, or Q.")


if __name__ == "__main__":
    main()