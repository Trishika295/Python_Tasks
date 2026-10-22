
# Student Result & Grade Management System

A Python-based student management application with a Streamlit
frontend and a modular Python backend.

## Features

- Dashboard with academic performance metrics
- Add, view, search, update, and delete student records
- Five-subject marks entry and validation
- Automatic total, percentage, grade, and pass/fail calculation
- Class performance summary and grade distribution
- Subject-wise average marks charts
- CSV export for student results
- Persistent JSON storage

## Technologies

- Python 3
- Streamlit
- Pandas
- JSON
- Git and GitHub

## Project Structure

Task_31/
- app.py
- backend.py
- result_calculator.py
- storage.py
- requirements.txt
- README.md
- data/students.json
- screenshots/

## Installation

1. Install Python 3.
2. Open the project folder in VS Code.
3. Open a terminal.
4. Install the dependencies:

   pip install -r requirements.txt

5. Start the application:

   streamlit run app.py

6. Open the local URL displayed in the terminal.

## Grade Criteria

| Percentage | Grade |
|---|---|
| 90 and above | A+ |
| 80 to below 90 | A |
| 70 to below 80 | B |
| 60 to below 70 | C |
| 50 to below 60 | D |
| Below 50, if passed | E |
| Any subject below 35 | F (Fail) |

## Data Storage

Student records are stored in data/students.json.
The application creates the data directory and file automatically.

## Testing

- Add a student with valid marks.
- Verify grade and percentage calculations.
- Test duplicate student IDs.
- Search for existing and missing records.
- Update marks and verify recalculation.
- Delete a student after confirmation.
- Restart the application and check data persistence.
- Export records to CSV.

## Limitations

This project uses local JSON storage and is intended for
educational use. It does not provide authentication, role-based
access, concurrent-user safeguards, or production database
management.

## Author

Name: Your Name

Internship: Veda Technology

Task: Day 31 - Student Result & Grade Management System
