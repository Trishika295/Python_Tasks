
SUBJECTS = [
    "English",
    "Mathematics",
    "Science",
    "Social Science",
    "Computer"
]

PASS_MARK = 35


def calculate_result(marks):
    """Calculate total, percentage, grade and pass/fail status."""

    if not isinstance(marks, dict) or not marks:
        raise ValueError("Marks must contain at least one subject.")

    for subject in SUBJECTS:
        if subject not in marks:
            raise ValueError(f"Missing marks for {subject}.")

        score = marks[subject]

        if isinstance(score, bool) or not isinstance(score, (int, float)):
            raise ValueError(f"Invalid marks for {subject}.")

        if not 0 <= score <= 100:
            raise ValueError(f"{subject} marks must be between 0 and 100.")

    total = sum(marks[subject] for subject in SUBJECTS)
    maximum = len(SUBJECTS) * 100
    percentage = total / maximum * 100

    passed = all(marks[subject] >= PASS_MARK for subject in SUBJECTS)

    if not passed:
        grade = "F"
    elif percentage >= 90:
        grade = "A+"
    elif percentage >= 80:
        grade = "A"
    elif percentage >= 70:
        grade = "B"
    elif percentage >= 60:
        grade = "C"
    elif percentage >= 50:
        grade = "D"
    else:
        grade = "E"

    return {
        "total": round(total, 2),
        "maximum": maximum,
        "percentage": round(percentage, 2),
        "grade": grade,
        "status": "PASS" if passed else "FAIL"
    }
