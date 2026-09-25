# Multiplication Table Generator

A simple and interactive full-stack web application that generates a multiplication table based on a user-provided number and limit. The project uses React.js for the frontend and Python Flask for the backend, with REST API communication between them.

# Features
-Enter a number to generate its multiplication table
-Specify the multiplication limit
-Generate the table using a Python for loop
-React frontend with a simple and responsive interface
-Python Flask backend
-REST API communication
-Fetch API for frontend-backend communication

# Input validation
--Error handling for invalid inputs
--Formatted multiplication table
--Clear button to reset the inputs and results
--Supports different numbers and limits
--Responsive design
--Technologies Used

# Frontend
React.js, HTML, CSS, JavaScript, Vite
# Backend
Python, Flask, Flask-CORS, API & Communication, REST API, Fetch API, JSONDevelopment Tools, VS Code, Git, GitHub

# Project Structure
Task_6/
└── multiplication-table-generator/
    │
    ├── App.jsx
    ├── app.py
    ├── index.html
    ├── main.jsx
    ├── package.json
    ├── requirements.txt
    ├── script.css
    └── vite.config.js

# Installation and Setup
1. Clone the Repository
git clone <your-repository-url>
Navigate to the project:
cd Task_6/multiplication-table-generator

2. Install Python Dependencies
python -m pip install -r requirements.txt
The required Python packages are:
Flask
Flask-CORS

3. Install Frontend Dependencies
npm install
Running the Project
The frontend and backend run separately.
Start the Flask Backend
Open Terminal 1:
python app.py
The backend will run at:
http://127.0.0.1:5000
Start the React Frontend

Open Terminal 2:
npm run dev
The frontend will normally run at:
http://localhost:5173
Open the frontend URL in your browser.

Testing in Python CMD
The Python multiplication logic can also be tested directly from the terminal using the supported test mode:
python app.py test

Example:

==========================================
      MULTIPLICATION TABLE GENERATOR
==========================================

Enter the number: 7
Enter the limit: 5

Multiplication Table of 7
----------------------------------------
7 × 1 = 7
7 × 2 = 14
7 × 3 = 21
7 × 4 = 28
7 × 5 = 35
----------------------------------------
Table generated successfully!

# Core Python Logic

The multiplication table is generated using a for loop:
for i in range(1, limit + 1):
    result = number * i

This demonstrates the use of:

for loops
range()
Arithmetic operations
Input validation
Lists
JSON responses

# Learning Outcomes
This project provides practical experience with:

-Python and for loops
-React and state management
-Flask REST API development
-Fetch API and JSON
-Input validation and error handling
-Frontend-backend integration
-Git and GitHub

# Future Improvements
-Generate multiple tables
-Add calculation history
-Add download/print option
-Add dark mode
-Deploy the application online
