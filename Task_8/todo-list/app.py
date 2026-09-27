from flask import Flask, request, jsonify
from flask_cors import CORS

import json
import os
import sys
import threading
import time


# =========================================================
# FLASK SETUP
# =========================================================

app = Flask(__name__)
CORS(app)


# =========================================================
# FILE STORAGE
# =========================================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DATA_FILE = os.path.join(
    BASE_DIR,
    "tasks.json"
)

file_lock = threading.Lock()


# =========================================================
# LOAD TASKS
# =========================================================

def load_tasks():

    with file_lock:

        if not os.path.exists(DATA_FILE):
            return []

        try:

            with open(
                DATA_FILE,
                "r",
                encoding="utf-8"
            ) as file:

                data = json.load(file)

                if isinstance(data, list):
                    return data

                return []

        except (
            json.JSONDecodeError,
            OSError
        ):

            return []


# =========================================================
# SAVE TASKS
# =========================================================

def save_tasks(tasks):

    with file_lock:

        with open(
            DATA_FILE,
            "w",
            encoding="utf-8"
        ) as file:

            json.dump(
                tasks,
                file,
                indent=4
            )


# =========================================================
# GET NEXT TASK ID
# =========================================================

def get_next_id(tasks):

    if not tasks:
        return 1

    return max(
        int(task["id"])
        for task in tasks
    ) + 1


# =========================================================
# FIND TASK
# =========================================================

def find_task(tasks, task_id):

    for task in tasks:

        if int(task["id"]) == int(task_id):
            return task

    return None


# =========================================================
# FLASK API
# GET ALL TASKS
# =========================================================

@app.route(
    "/api/tasks",
    methods=["GET"]
)
def get_tasks():

    tasks = load_tasks()

    return jsonify(tasks), 200


# =========================================================
# FLASK API
# ADD TASK
# =========================================================

@app.route(
    "/api/tasks",
    methods=["POST"]
)
def add_task():

    data = request.get_json(
        silent=True
    )

    if not data:

        return jsonify({
            "error": "No task data received."
        }), 400

    title = str(
        data.get(
            "title",
            ""
        )
    ).strip()

    if not title:

        return jsonify({
            "error": "Task title cannot be empty."
        }), 400

    tasks = load_tasks()

    new_task = {
        "id": get_next_id(tasks),
        "title": title,
        "completed": False
    }

    tasks.append(new_task)

    save_tasks(tasks)

    return jsonify({
        "message": "Task added successfully.",
        "task": new_task
    }), 201


# =========================================================
# FLASK API
# UPDATE TASK
# =========================================================

@app.route(
    "/api/tasks/<int:task_id>",
    methods=["PUT"]
)
def update_task(task_id):

    tasks = load_tasks()

    task = find_task(
        tasks,
        task_id
    )

    if task is None:

        return jsonify({
            "error": "Task not found."
        }), 404

    data = request.get_json(
        silent=True
    )

    if not data:

        return jsonify({
            "error": "No update data received."
        }), 400

    # Update title
    if "title" in data:

        title = str(
            data.get(
                "title",
                ""
            )
        ).strip()

        if not title:

            return jsonify({
                "error": "Task title cannot be empty."
            }), 400

        task["title"] = title

    # Update completion status
    if "completed" in data:

        task["completed"] = bool(
            data["completed"]
        )

    save_tasks(tasks)

    return jsonify({
        "message": "Task updated successfully.",
        "task": task
    }), 200


# =========================================================
# FLASK API
# DELETE TASK
# =========================================================

@app.route(
    "/api/tasks/<int:task_id>",
    methods=["DELETE"]
)
def delete_task(task_id):

    tasks = load_tasks()

    task = find_task(
        tasks,
        task_id
    )

    if task is None:

        return jsonify({
            "error": "Task not found."
        }), 404

    tasks.remove(task)

    save_tasks(tasks)

    return jsonify({
        "message": "Task deleted successfully."
    }), 200


# =========================================================
# CLI
# ADD TASK
# =========================================================

def cli_add_task():

    tasks = load_tasks()

    print()
    print("-" * 50)
    print("                 ADD TASK")
    print("-" * 50)

    title = input(
        "Enter task title: "
    ).strip()

    if not title:

        print(
            "\nTask title cannot be empty."
        )

        return

    new_task = {
        "id": get_next_id(tasks),
        "title": title,
        "completed": False
    }

    tasks.append(new_task)

    save_tasks(tasks)

    print(
        "\nTask added successfully! ✓"
    )


# =========================================================
# CLI
# VIEW TASKS
# =========================================================

def cli_view_tasks():

    tasks = load_tasks()

    print()
    print("=" * 60)
    print("                     TO-DO LIST")
    print("=" * 60)

    if not tasks:

        print("No tasks available.")

        print("=" * 60)

        return

    for task in tasks:

        if task["completed"]:
            status = "Completed"
        else:
            status = "Pending"

        print(
            f'{task["id"]}. '
            f'{task["title"]} '
            f'[{status}]'
        )

    print("=" * 60)


# =========================================================
# CLI
# UPDATE TASK
# =========================================================

def cli_update_task():

    tasks = load_tasks()

    if not tasks:

        print(
            "\nNo tasks available."
        )

        return

    cli_view_tasks()

    try:

        task_id = int(
            input(
                "\nEnter task ID to update: "
            )
        )

    except ValueError:

        print(
            "\nPlease enter a valid number."
        )

        return

    task = find_task(
        tasks,
        task_id
    )

    if task is None:

        print(
            "\nTask not found."
        )

        return

    print(
        f'\nCurrent task: {task["title"]}'
    )

    new_title = input(
        "Enter new title "
        "(press Enter to keep current): "
    ).strip()

    if new_title:

        task["title"] = new_title

    print()
    print("Current status:")

    if task["completed"]:
        print("Completed")
    else:
        print("Pending")

    status = input(
        "\nMark as completed? "
        "(y/n/Enter to keep current): "
    ).strip().lower()

    if status == "y":

        task["completed"] = True

    elif status == "n":

        task["completed"] = False

    save_tasks(tasks)

    print(
        "\nTask updated successfully! ✓"
    )


# =========================================================
# CLI
# DELETE TASK
# =========================================================

def cli_delete_task():

    tasks = load_tasks()

    if not tasks:

        print(
            "\nNo tasks available."
        )

        return

    cli_view_tasks()

    try:

        task_id = int(
            input(
                "\nEnter task ID to delete: "
            )
        )

    except ValueError:

        print(
            "\nPlease enter a valid number."
        )

        return

    task = find_task(
        tasks,
        task_id
    )

    if task is None:

        print(
            "\nTask not found."
        )

        return

    tasks.remove(task)

    save_tasks(tasks)

    print(
        "\nTask deleted successfully! ✓"
    )


# =========================================================
# PYTHON CLI
# =========================================================

def run_cli():

    while True:

        print()
        print("=" * 60)
        print("              SIMPLE TO-DO LIST")
        print("              PYTHON COMMAND LINE")
        print("=" * 60)

        print("1. Add Task")
        print("2. View Tasks")
        print("3. Update Task")
        print("4. Delete Task")
        print("5. Exit")

        print("=" * 60)

        choice = input(
            "Enter your choice: "
        ).strip()

        if choice == "1":

            cli_add_task()

        elif choice == "2":

            cli_view_tasks()

        elif choice == "3":

            cli_update_task()

        elif choice == "4":

            cli_delete_task()

        elif choice == "5":

            print()
            print(
                "Thank you for using "
                "the To-Do List!"
            )

            print(
                "Goodbye! 👋"
            )

            break

        else:

            print(
                "\nInvalid choice."
            )

            print(
                "Please enter a number from 1 to 5."
            )


# =========================================================
# FLASK WEB SERVER
# =========================================================

def run_web():

    print()
    print("=" * 60)
    print("                FLASK BACKEND")
    print("=" * 60)

    print(
        "API running at:"
    )

    print(
        "http://127.0.0.1:5000"
    )

    print("=" * 60)

    app.run(
        host="127.0.0.1",
        port=5000,
        debug=False,
        use_reloader=False
    )


# =========================================================
# RUN BOTH
# =========================================================

def run_both():

    print()
    print(
        "Starting Flask backend..."
    )

    web_thread = threading.Thread(
        target=run_web,
        daemon=True
    )

    web_thread.start()

    time.sleep(1)

    print()
    print("=" * 60)
    print("          TO-DO LIST APPLICATION")
    print("=" * 60)

    print(
        "✓ Flask backend started"
    )

    print(
        "✓ Python CLI started"
    )

    print(
        "✓ Shared storage: tasks.json"
    )

    print()
    print(
        "Browser API:"
    )

    print(
        "http://127.0.0.1:5000/api/tasks"
    )

    print("=" * 60)

    run_cli()


# =========================================================
# MAIN
# =========================================================

if __name__ == "__main__":

    print(
        "\nStarting To-Do List application..."
    )

    if len(sys.argv) > 1:

        mode = sys.argv[1].lower()

        if mode == "cli":

            run_cli()

        elif mode == "web":

            run_web()

        elif mode == "both":

            run_both()

        else:

            print(
                "\nInvalid mode."
            )

            print()
            print("Use:")
            print("python app.py")
            print("python app.py cli")
            print("python app.py web")
            print("python app.py both")

    else:

        run_both()