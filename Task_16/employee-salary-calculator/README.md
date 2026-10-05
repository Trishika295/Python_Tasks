# Employee Salary Calculator

## Task Description

The Employee Salary Calculator is a Python-based mini project that calculates employee gross salary, deductions, and net salary based on configurable salary rules.

The project demonstrates the use of Python dictionaries, lists, functions, conditions, input validation, and business-rule implementation.

---

## Objective

The objective of this project is to practice:

- Python dictionaries
- Python lists
- Functions
- Conditional statements
- Input validation
- Salary calculations
- Business-rule implementation
- Modular programming

---

## Features

- Accept employee details from the user
- Accept basic salary
- Calculate HRA
- Calculate DA
- Calculate Special Allowance
- Calculate Gross Salary
- Calculate PF
- Calculate Professional Tax
- Calculate Income Tax
- Calculate Total Deductions
- Calculate Net Salary
- Display a formatted salary slip
- Store employee records using dictionaries
- Store multiple employees using a list
- Use configurable salary rules
- Validate numeric inputs

---

## Salary Rules

The project uses configurable sample salary rules.

### Allowances

- HRA = 20% of Basic Salary
- DA = 10% of Basic Salary
- Special Allowance = 5% of Basic Salary

### Deductions

- PF = 12% of Basic Salary
- Professional Tax = ₹200
- Income Tax = 5% of Gross Salary

These values can be modified in `salary_rules.py`.

---

## Project Structure

```text
employee-salary-calculator/
│
├── app.py
├── salary_rules.py
├── employee_data.py
├── salary_calculator.py
├── requirements.txt
├── README.md
└── .gitignore