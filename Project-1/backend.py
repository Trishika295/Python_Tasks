
from datetime import datetime

from result_calculator import SUBJECTS, calculate_result
from storage import load_students, save_students


def get_all_students():
    """Return all student records."""
    return load_students()


def get_student(student_id):
    """Find a student by ID, ignoring letter case."""
    student_id = student_id.strip().casefold()

    for student in load_students():
        if student.get("student_id", "").casefold() == student_id:
            return student

    return None


def validate_student(student_id, name, student_class, marks):
    """Validate student details before saving."""
    if not student_id.strip():
        raise ValueError("Student ID is required.")

    if not name.strip():
        raise ValueError("Student name is required.")

    if not student_class.strip():
        raise ValueError("Class or section is required.")

    if not isinstance(marks, dict):
        raise ValueError("Marks must be supplied for all subjects.")

    # Reuse the result calculator for marks validation.
    calculate_result(marks)


def add_student(student_id, name, student_class, marks):
    """Create a new student record."""
    student_id = student_id.strip()
    name = name.strip()
    student_class = student_class.strip()

    validate_student(student_id, name, student_class, marks)

    students = load_students()

    if any(
        student.get("student_id", "").casefold() == student_id.casefold()
        for student in students
    ):
        raise ValueError("A student with this ID already exists.")

    student = {
        "student_id": student_id,
        "name": name,
        "class": student_class,
        "marks": dict(marks),
        "created_at": datetime.now().isoformat(timespec="seconds"),
        "updated_at": datetime.now().isoformat(timespec="seconds")
    }

    students.append(student)
    save_students(students)

    return student


def update_student(student_id, name, student_class, marks):
    """Update an existing student's details and marks."""
    name = name.strip()
    student_class = student_class.strip()

    validate_student(student_id, name, student_class, marks)

    students = load_students()

    for student in students:
        if student.get("student_id", "").casefold() == student_id.strip().casefold():
            student["name"] = name
            student["class"] = student_class
            student["marks"] = dict(marks)
            student["updated_at"] = datetime.now().isoformat(
                timespec="seconds"
            )

            save_students(students)
            return student

    raise ValueError("Student record was not found.")


def delete_student(student_id):
    """Delete a student record."""
    students = load_students()
    search_id = student_id.strip().casefold()

    remaining = [
        student for student in students
        if student.get("student_id", "").casefold() != search_id
    ]

    if len(remaining) == len(students):
        raise ValueError("Student record was not found.")

    save_students(remaining)


def get_result(student):
    """Calculate a student's current result."""
    return calculate_result(student["marks"])


def get_performance_summary():
    """Return class-wide academic statistics."""
    students = load_students()

    if not students:
        return {
            "total_students": 0,
            "average_percentage": 0,
            "pass_count": 0,
            "fail_count": 0,
            "pass_percentage": 0,
            "top_student": None,
            "grade_distribution": {}
        }

    results = [
        (student, calculate_result(student["marks"]))
        for student in students
    ]

    percentages = [result["percentage"] for _, result in results]
    pass_count = sum(
        result["status"] == "PASS" for _, result in results
    )

    grade_distribution = {}

    for _, result in results:
        grade = result["grade"]
        grade_distribution[grade] = grade_distribution.get(grade, 0) + 1

    top_student, top_result = max(
        results,
        key=lambda item: item[1]["percentage"]
    )

    return {
        "total_students": len(students),
        "average_percentage": round(sum(percentages) / len(percentages), 2),
        "pass_count": pass_count,
        "fail_count": len(students) - pass_count,
        "pass_percentage": round(pass_count / len(students) * 100, 2),
        "top_student": {
            "student_id": top_student["student_id"],
            "name": top_student["name"],
            "percentage": top_result["percentage"],
            "grade": top_result["grade"]
        },
        "grade_distribution": grade_distribution
    }


def build_student_table():
    """Return student data with calculated result fields."""
    rows = []

    for student in load_students():
        result = calculate_result(student["marks"])

        rows.append({
            "Student ID": student["student_id"],
            "Name": student["name"],
            "Class": student["class"],
            "Total": result["total"],
            "Percentage": result["percentage"],
            "Grade": result["grade"],
            "Status": result["status"]
        })

    return rows
