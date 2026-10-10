## Project Description

The JSON Data Processor is a Python-based application that reads
employee information from a JSON file and performs searching,
filtering, and summary operations.

It uses Python's built-in `json` module to load structured data,
validate records, and process nested dictionaries and lists.

## Technologies Used

- Python
- JSON
- Python built-in json module
- Git and GitHub

## Key Features

1. Read employee records from a JSON file.
2. Validate required fields and data types.
3. Display all valid employee records.
4. Search employees by name or EmployeeID.
5. Filter employees by department.
6. Filter employees by minimum salary.
7. Calculate total and average salary.
8. Identify the highest-paid and lowest-paid employees.
9. Summarize the number of employees in each department.
10. Handle missing files and invalid JSON data.

## Project Structure

Task_20/
├── json_processor.py
├── data.json
└── README.md

## How to Run

1. Install Python 3 if it is not already installed.
2. Open the terminal in the Task_20 folder.
3. Run the following command:

   python json_processor.py

4. Select an option from the menu.
5. Follow the instructions displayed in the terminal.

## Learning Outcomes

- Understanding JSON and Python dictionaries.
- Reading JSON files using json.load().
- Understanding lists and nested data.
- Validating records and handling exceptions.
- Applying searching, filtering, and aggregation.
- Organizing Python code using reusable functions.

## Future Enhancements

- Support employee, product, and student datasets.
- Add options to insert, update, and delete records.
- Export filtered results to a new JSON file.
- Add sorting by name, department, or salary.
