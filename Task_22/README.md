# Task 20 - Python File Organizer

## Project Description

The Python File Organizer is a simple filesystem automation application that scans a specified folder and organizes files into separate folders based on their file extensions.

The application uses Python's pathlib and shutil modules to manage directories and move files safely. It supports preview mode, duplicate filename handling, error handling, and automatic creation of category folders.

## Objective

To learn filesystem automation using Python and develop a practical tool for organizing files efficiently.

## Technologies Used

- Python
- pathlib
- shutil
- os (filesystem-related concepts)

## Key Features

1. Accept source and destination folder paths.
2. Scan files in the specified source folder.
3. Identify file types using their extensions.
4. Organize images, documents, spreadsheets, videos, audio, code, archives, and other files into separate folders.
5. Create category folders automatically.
6. Preview the planned file movements before organizing.
7. Handle duplicate filenames without overwriting existing files.
8. Handle filesystem errors and invalid folder paths.
9. Provide an interactive, menu-driven interface.

## Project Structure

```text
Task_20/
├── file_organizer.py
├── README.md
├── test_directory/
└── organized_files/