## Quiz Application

## Project Description

The Quiz Application is a Python-based interactive quiz system
with a Streamlit frontend. It loads multiple-choice questions
from a JSON file, accepts user responses, calculates scores,
and displays a final result summary.

The application also supports command-line execution through
a separate quiz logic module.

## Objectives

- Practice Python dictionaries, lists, loops, and functions.
- Store quiz questions separately using JSON.
- Implement random question ordering.
- Validate user answers.
- Calculate scores and percentages.
- Build an interactive frontend using Streamlit.

## Technologies Used

- Python
- Streamlit
- JSON
- random
- pathlib

## Project Structure

Task_23/
    app.py
    quiz_logic.py
    questions.json
    requirements.txt
    README.md

## Features

1. Loads 15 multiple-choice questions from JSON.
2. Supports randomized question ordering.
3. Provides an interactive browser-based quiz.
4. Validates all submitted answers.
5. Calculates correct and incorrect answers.
6. Displays the final score and percentage.
7. Assigns a performance category.
8. Provides a detailed answer review.
9. Supports restarting the quiz.
10. Supports terminal-based execution.

## Installation

Install the required dependency:

    python -m pip install -r requirements.txt

## Run the Streamlit Application

    python -m streamlit run app.py

Open the local URL displayed in the terminal, usually:

    http://localhost:8501

## Run the CLI Version

    python quiz_logic.py

## Conclusion

This project demonstrates how Python and JSON can be used to
build a reusable quiz application. Streamlit provides an
interactive frontend, while a separate module manages question
loading, validation, scoring, and result calculation.

The project strengthens understanding of modular programming,
data handling, input validation, and application development.

## Live Demo: https://py-quiz.streamlit.app/
