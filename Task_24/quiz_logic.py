
import json
import random
from pathlib import Path

QUESTIONS_FILE = Path(__file__).with_name("questions.json")
VALID_OPTIONS = {"A", "B", "C", "D"}


def load_questions():
    """Load and validate quiz questions from JSON."""
    try:
        with QUESTIONS_FILE.open("r", encoding="utf-8") as file:
            data = json.load(file)
    except FileNotFoundError:
        raise ValueError("questions.json was not found.")
    except json.JSONDecodeError as error:
        raise ValueError(f"Invalid JSON file: {error}") from error

    if not isinstance(data, list) or not data:
        raise ValueError("The JSON file must contain a non-empty list.")

    questions = []

    for number, item in enumerate(data, start=1):
        if not isinstance(item, dict):
            continue

        question_text = item.get("question")
        options = item.get("options")
        answer = item.get("answer")

        if (
            not isinstance(question_text, str)
            or not question_text.strip()
            or not isinstance(options, dict)
            or set(options.keys()) != VALID_OPTIONS
            or not all(
                isinstance(options[key], str) and options[key].strip()
                for key in VALID_OPTIONS
            )
            or not isinstance(answer, str)
            or answer.upper() not in VALID_OPTIONS
        ):
            print(f"Skipping invalid question {number}.")
            continue

        questions.append({
            "question": question_text.strip(),
            "options": options,
            "answer": answer.upper()
        })

    if not questions:
        raise ValueError("No valid quiz questions were found.")

    return questions


def shuffle_questions(questions):
    """Return a shuffled copy of the question list."""
    shuffled = list(questions)
    random.shuffle(shuffled)
    return shuffled


def calculate_results(questions, answers):
    """Calculate score, percentage, and detailed answer results."""
    details = []
    score = 0

    for index, question in enumerate(questions):
        selected = answers.get(index)
        correct = question["answer"]
        is_correct = selected == correct

        if is_correct:
            score += 1

        details.append({
            "question": question["question"],
            "selected": selected,
            "correct": correct,
            "options": question["options"],
            "is_correct": is_correct
        })

    total = len(questions)
    percentage = (score / total * 100) if total else 0

    return {
        "total": total,
        "score": score,
        "wrong": total - score,
        "percentage": percentage,
        "grade": get_performance(percentage),
        "details": details
    }


def get_performance(percentage):
    """Return a performance label."""
    if percentage >= 90:
        return "Excellent"
    if percentage >= 75:
        return "Very Good"
    if percentage >= 60:
        return "Good"
    if percentage >= 40:
        return "Needs Improvement"
    return "Keep Practicing"


def run_cli():
    """Run the quiz in the command line."""
    try:
        questions = load_questions()
    except ValueError as error:
        print(f"Error: {error}")
        return

    print("\n" + "=" * 42)
    print("       PYTHON CLI QUIZ APPLICATION")
    print("=" * 42)
    print(f"Total questions: {len(questions)}")

    choice = input("Shuffle questions? (yes/no): ").strip().lower()

    if choice in {"yes", "y"}:
        questions = shuffle_questions(questions)

    answers = {}

    for index, question in enumerate(questions):
        print(f"\nQuestion {index + 1}/{len(questions)}")
        print(question["question"])

        for key, value in question["options"].items():
            print(f"{key}. {value}")

        while True:
            selected = input("Your answer (A/B/C/D): ").strip().upper()
            if selected in VALID_OPTIONS:
                answers[index] = selected
                break
            print("Invalid input. Enter A, B, C, or D.")

    results = calculate_results(questions, answers)

    print("\n========== FINAL RESULTS ==========")
    print(f"Correct answers: {results['score']}")
    print(f"Wrong answers:   {results['wrong']}")
    print(f"Score:           {results['score']}/{results['total']}")
    print(f"Percentage:      {results['percentage']:.2f}%")
    print(f"Performance:     {results['grade']}")
    print("===================================")


if __name__ == "__main__":
    run_cli()
