# Task 19 - Read and Process a Text File

## Project Description

The Read and Process a Text File project is a Python-based text processing application with a Streamlit frontend.

The application reads a text file and generates useful statistics such as line count, word count, character count, characters without spaces, and file size.

The project can be used through both the terminal and a browser-based Streamlit interface.

## Objective

The objective of this project is to learn Python file handling and text processing.

## Technologies Used

- Python
- Streamlit
- File Handling
- Text Processing
- Exception Handling
- Git & GitHub

## Project Structure

Task_19/
└── Read-&-Process-file/
    ├── app.py
    ├── README.md
    ├── requirements.txt
    ├── sample.txt
    └── text_processor.py

## Key Feature
1. Read a text file using Python.
2. Calculate the number of lines.
3. Calculate the number of words.
4. Calculate the number of characters.
5. Calculate characters without spaces.
6. Display the file size.
7. Display a preview of the text.
8. Support .txt files.
9. Handle missing files gracefully.
10. Handle invalid file content.
11. Process files line by line in terminal mode.
12. Provide a Streamlit browser interface.
13. Support both terminal and browser execution.

## Backend
The backend logic is implemented in:
text_processor.py
It contains reusable functions for:
- File validation
- File processing
- Text statistics
- Text preview
- File size formatting

## Frontend
The frontend is implemented using:
Streamlit
The browser interface allows the user to upload a .txt file and view the generated statistics.
File Handling
The project uses:
with open(file_path, "r", encoding="utf-8") as file:
The with statement automatically closes the file after processing.
# Reading Methods
Python provides several methods for reading files.
read()
Reads the complete file.
with open("sample.txt", "r") as file:    content = file.read()

# readline()
Reads one line at a time.
with open("sample.txt", "r") as file:    line = file.readline()
readlines()
Reads all lines and returns them as a list.
with open("sample.txt", "r") as file:    lines = file.readlines()


This project processes the file line by line in terminal mode to avoid unnecessarily loading large files into memory.
Exception Handling
The project handles the following exceptions:
- FileNotFoundError
- PermissionError
- UnicodeDecodeError
- ValueError
Errors are displayed clearly instead of causing the application to terminate unexpectedly.

## Installation
Install the required package using:
python -m pip install -r requirements.txt

If the python command is configured differently on your system, you can also use:
py -m pip install -r requirements.txt

Run in Terminal
Run the following command:
python app.py --terminal
Or:
py app.py --terminal

When prompted, enter:
sample.txt

The program will display the generated text statistics directly in the terminal.
Run in Browser
Start the Streamlit application using:
streamlit run app.py

Or:
python -m streamlit run app.py

If your system uses the Python launcher:
py -m streamlit run app.py

The application will open in the browser and allow you to upload a .txt file.
Run Both
To start the browser interface and terminal interface together, use:
python app.py --both

Or:
py app.py --both

## Generated Statistics
The application generates the following statistics:
1.Line Count: The total number of lines present in the text file.
2.Word Count: The total number of words present in the text file.
3.Character Count: The total number of characters, including whitespace characters.
4.Characters Without Spaces: The number of characters after removing spaces, tabs, and newline characters.
5.File Size: The size of the input text file displayed in a readable format such as Bytes, KB, MB, or GB.
6.File Processing Approach: The application uses:
with open(file_path, "r", encoding="utf-8") as file:

This ensures that the file is automatically closed after the operation is completed.
In terminal mode, the file is processed line by line:
for line in file:    ...

This approach avoids unnecessarily loading a large text file completely into memory.
Why Use with open()?
Using with open() is considered a safer and cleaner approach to file handling because Python automatically closes the file after the with block is completed.
Example:
with open("sample.txt", "r") as file:    content = file.read()
This eliminates the need to manually close the file using:
file.close()

## Difference Between read(), readline(), and readlines()
read()
The read() method reads the complete contents of a file.
with open("sample.txt", "r") as file:    content = file.read()

It is convenient for smaller files but may consume more memory when used with very large files.
readline()
The readline() method reads one line at a time.
with open("sample.txt", "r") as file:    line = file.readline()

It is useful when a specific line needs to be read.
readlines()
The readlines() method reads all lines and stores them in a list.
with open("sample.txt", "r") as file:    lines = file.readlines()

For large files, this can consume more memory because all lines are stored at once.
Approach Used in This Project
The terminal implementation processes the file line by line:
for line in file:    ...

This provides a more memory-efficient approach for processing text files.
Exception Handling Details
FileNotFoundError
This exception occurs when the specified file does not exist.
Example:
Enter file path: unknown.txt

The application displays an appropriate error message instead of terminating unexpectedly.
PermissionError
This exception occurs when the program does not have permission to access the specified file.
UnicodeDecodeError
This exception occurs when the text file cannot be decoded using UTF-8 encoding.
ValueError
This exception is used for invalid file conditions, such as unsupported file types.
Error Handling
The project uses specific exception classes instead of relying on a generic or bare except statement.
This makes the error-handling process clearer and allows the application to provide meaningful messages for different types of errors.
Backend and Frontend Separation
The project follows a modular structure.
Backend
The backend is implemented in:
text_processor.py

It contains reusable functions for:
- File validation
- File processing
- Line counting
- Word counting
- Character counting
- Text preview
- File size formatting
- Text statistics
Frontend
The frontend is implemented in:
app.py

The Streamlit interface allows users to upload a text file and view the generated statistics in a browser.
The same app.py also provides the terminal interface.
Learning Outcomes
After completing this project, the following concepts can be understood:
- Python file handling
- open()
- with open()
- read()
- readline()
- readlines()
- Line-by-line file processing
- String processing
- Word counting
- Character counting
- File validation
- File size calculation
- Exception handling
- FileNotFoundError
- PermissionError
- UnicodeDecodeError
- ValueError
- Streamlit
- Command-line programming
- Separation of backend and frontend logic
- Modular Python programming

## Future Enhancements
The application can be extended with additional features such as:
- Support for multiple file formats
- Downloadable statistics reports
- Sentence counting
- Paragraph counting
- Most frequently used words
- Word frequency analysis
- Text comparison between two files
- Graphical visualization of text statistics
- Export statistics to CSV or PDF

## Conclusion
The Read and Process a Text File project provides practical experience with Python file handling and text processing.
The application demonstrates how to safely open and read text files, calculate line, word, and character statistics, handle file-related exceptions, and process files efficiently.
The project also integrates a Streamlit browser interface with a Python command-line interface, providing two different ways to interact with the application.
Overall, the project strengthens understanding of Python file handling, string processing, exception handling, modular programming, memory-efficient file processing, and Streamlit-based application development.