## Project Description

The Simple Expense Tracker is a Python application that records
daily expenses and generates useful spending summaries. It provides
a Streamlit web interface and a terminal-based interface.

Expense records are stored persistently in a CSV file.

## Objectives

- Record expense dates, categories, descriptions, and amounts.
- Validate expense information.
- Store records using CSV file handling.
- Calculate total spending.
- Generate category-wise spending summaries.
- Generate monthly spending reports.

## Features

1. Add new expense records.
2. View all saved expenses.
3. Calculate total spending.
4. Summarize expenses by category.
5. Filter expenses by month.
6. Download expense records as CSV.
7. Save data between application sessions.
8. Use the application through the browser or terminal.

## Technologies Used

- Python
- Streamlit
- Pandas
- CSV file handling
- Datetime module

## Folder Structure

Task_23/
- app.py
- expense_tracker.py
- expenses.csv
- README.md
- requirements.txt

## Installation

Install the dependencies:

    python -m pip install -r requirements.txt

## Run the Browser Application

    python -m streamlit run app.py

Open the local URL shown in the terminal.

## Run the Terminal Application

    python expense_tracker.py

## Data Storage

All expense records are saved in expenses.csv.
Both application interfaces use the same file.

## Interview Questions

### 1. How would you store expense records?

Expense records can be stored as dictionaries and persisted
in a CSV file containing date, category, description, and amount.

### 2. Why should application data be persisted?

Persistence prevents records from being lost when the application
closes and allows users to access them in future sessions.

### 3. How would you add monthly filtering?

Store dates in YYYY-MM-DD format and select records whose dates
begin with the requested YYYY-MM month.

## Conclusion

This project demonstrates Python functions, lists, dictionaries,
CSV file handling, input validation, exception handling, and
basic financial reporting in a practical application.
