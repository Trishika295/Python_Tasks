# Practice Exception Handling

## Project Overview

Practice Exception Handling is a Python mini-project designed to demonstrate how runtime errors can be safely handled using Python's exception handling mechanisms.

The project uses `try`, `except`, `else`, and `finally` to prevent the program from crashing and to provide meaningful error messages to users.

## Objective

The main objective of this project is to understand and implement practical exception handling for common runtime errors.

## Technologies Used

- Python
- Python Standard Library

## Exception Cases Handled

The project demonstrates six common exception types:

1. `ValueError`
   - Handles invalid numeric input.

2. `ZeroDivisionError`
   - Handles attempts to divide a number by zero.

3. `KeyError`
   - Handles attempts to access a missing dictionary key.

4. `IndexError`
   - Handles attempts to access an invalid list index.

5. `TypeError`
   - Handles operations between incompatible data types.

6. `FileNotFoundError`
   - Handles attempts to open a file that does not exist.

## Features

- Interactive command-line menu
- Specific exception handling
- Meaningful error messages
- Uses `try` blocks for risky operations
- Uses `except` blocks to handle errors
- Uses `else` for successful operations
- Uses `finally` for cleanup/completion messages
- Provides explanations of each exception
- Prevents unexpected program termination

## Project Structure

```text
exception-handling-practice/
│
├── app.py
├── README.md
└── requirements.txt