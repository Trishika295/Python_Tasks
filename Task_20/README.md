## Project Description

The CSV Data Processor is a Python-based application that reads employee information from a CSV file and generates useful statistical summaries. It processes salary data, calculates totals and averages, identifies the highest and lowest salaries, and summarizes employee information by department.

The application also handles missing and invalid salary values and generates a formatted summary report.

## Technologies Used

- Python
- CSV module
- File handling
- Dictionaries and lists
- Functions and exception handling

## Key Features

1. Read employee records from a CSV file.
2. Validate the required CSV columns.
3. Handle missing and invalid salary values.
4. Calculate total and average salaries.
5. Identify the highest and lowest salaries.
6. Find the highest-paid employee.
7. Calculate department-wise employee counts and average salaries.
8. Generate a formatted report in the terminal.
9. Save the summary report to a text file.

## Project Structure

```text
Task_20/
├── csv_processor.py
├── employees.csv
├── summary_report.txt
└── README.md
```

## How to Run

1. Install Python 3.
2. Open the project folder in VS Code.
3. Open the terminal.
4. Run the following command:

```bash
python csv_processor.py
```

The application reads `employees.csv`, displays the calculated statistics, and generates `summary_report.txt`.

## Learning Outcomes

- Understanding CSV file processing.
- Using Python's built-in csv module.
- Performing calculations on structured data.
- Handling missing and invalid values.
- Using functions to organize program logic.
- Generating formatted reports using file handling.

## Conclusion

This project demonstrates how Python can process structured CSV data, calculate meaningful statistics, handle data-quality issues, and generate reports using built-in modules without requiring external libraries.