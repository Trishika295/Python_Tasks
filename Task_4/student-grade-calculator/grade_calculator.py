def calculate_grade(percentage):

    if percentage >= 90:
        return "A+"

    elif percentage >= 80:
        return "A"

    elif percentage >= 70:
        return "B"

    elif percentage >= 60:
        return "C"

    elif percentage >= 50:
        return "D"

    else:
        return "F"


def calculate_result(marks):

    if not marks:
        raise ValueError(
            "No subject marks were provided."
        )


    # Validate every mark
    for subject, mark in marks.items():

        if not isinstance(mark, (int, float)):

            raise ValueError(
                f"Invalid mark entered for {subject}."
            )


        if mark < 0 or mark > 100:

            raise ValueError(
                f"{subject} marks must be between 0 and 100."
            )


    # Total marks
    total = sum(marks.values())


    # Maximum possible marks
    maximum_marks = len(marks) * 100


    # Percentage
    percentage = (
        total / maximum_marks
    ) * 100


    # Grade
    grade = calculate_grade(
        percentage
    )


    return {
        "total": total,
        "maximum_marks": maximum_marks,
        "percentage": round(
            percentage,
            2
        ),
        "grade": grade
    }