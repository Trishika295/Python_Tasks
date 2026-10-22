
import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
DATA_FILE = DATA_DIR / "students.json"


def initialize_storage():
    DATA_DIR.mkdir(parents=True, exist_ok=True)

    if not DATA_FILE.exists():
        DATA_FILE.write_text("[]", encoding="utf-8")


def load_students():
    initialize_storage()

    try:
        with DATA_FILE.open("r", encoding="utf-8") as file:
            students = json.load(file)
    except json.JSONDecodeError as error:
        raise ValueError(
            "students.json is invalid. Restore a valid backup before continuing."
        ) from error

    if not isinstance(students, list):
        raise ValueError("Student data must be stored as a JSON list.")

    for student in students:
        if not isinstance(student, dict):
            raise ValueError("Invalid student record found in storage.")

    return students


def save_students(students):
    initialize_storage()

    temporary_file = DATA_DIR / "students.tmp"

    try:
        with temporary_file.open("w", encoding="utf-8") as file:
            json.dump(students, file, indent=4, ensure_ascii=False)
            file.write("\n")

        temporary_file.replace(DATA_FILE)

    finally:
        if temporary_file.exists():
            temporary_file.unlink()
