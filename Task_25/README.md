
# Python Utility Toolkit

## 1. Project Description

Python Utility Toolkit is a mini-project that demonstrates
modular programming and code reusability in Python.

It provides reusable functions for data validation, formatting,
calculations, and file handling. The functions are stored in a
separate module and imported into an example application.

## 2. Objectives

- Understand Python modules and imports.
- Write reusable functions with clear responsibilities.
- Validate user input.
- Perform common formatting and mathematical operations.
- Read and write text files.
- Document functions using docstrings.

## 3. Technologies Used

- Python 3
- Python standard library
- pathlib for file handling
- re for email validation

No external packages are required.

## 4. Project Structure

Python_Utility_Module/
├── utility_module.py
├── main.py
├── README.md
└── sample_files/
    └── example.txt  (created automatically)

## 5. Function Documentation

### Validation Functions

- `is_valid_email(email)`: Checks a basic email format.
- `is_valid_phone(phone)`: Checks for exactly 10 digits.
- `is_number(value)`: Checks whether text represents a finite number.

### Formatting Functions

- `format_name(name)`: Removes extra spaces and capitalizes names.
- `format_currency(amount)`: Formats amounts in Indian Rupees.
- `format_text(text)`: Normalizes spacing and converts text to lowercase.

### Calculation Functions

- `calculate_percentage(value, total)`: Calculates a percentage.
- `calculate_average(numbers)`: Calculates the arithmetic mean.
- `calculate_total(numbers)`: Returns the sum of numbers.

### File Functions

- `file_exists(file_path)`: Checks whether a file exists.
- `read_text_file(file_path)`: Reads a UTF-8 text file.
- `write_text_file(file_path, content)`: Writes text to a file.

## 6. How to Run

1. Install Python 3 if it is not already installed.
2. Open a terminal in the project directory.
3. Run:

   `python main.py`

4. Select an option from the menu.
5. Follow the prompts to test the utilities.

On Windows, `py main.py` can be used if the Python launcher
is installed.

## 7. Error Handling

The application handles invalid numeric input, division by
zero, missing files, and file operation errors. Calculation
functions raise ValueError when an average cannot be calculated
or a percentage has a zero denominator.

## 8. Benefits

- Reduces duplicate code.
- Improves readability and maintenance.
- Separates reusable logic from the application interface.
- Makes individual functions easier to test.
- Encourages modular programming practices.

## 9. Conclusion

The Python Utility Toolkit demonstrates how a collection of
focused functions can be organized into a reusable module.
The example program shows how another Python file can import
and use these functions, fulfilling the core objectives of
modular programming and code reuse.
