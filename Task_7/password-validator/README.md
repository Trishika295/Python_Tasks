# Objective

The objective of this project is to develop a password validation application that checks whether a password satisfies the following requirements:
Minimum 8 characters
At least one uppercase letter
At least one lowercase letter
At least one number
At least one special character

The project demonstrates the integration of a React frontend with a Python Flask backend through a REST API.

# Features
--Password validation
--Minimum 8-character requirement
--Uppercase letter validation
--Lowercase letter validation
--Number validation
--Special character validation
--Meaningful validation messages
--Clear/reset functionality
--React + Flask REST API integration
--JSON data communication
--Terminal/CMD execution support
--Responsive user interface
--Password is not stored by the application

# Technologies Used
-Frontend
-React.js
-HTML
-CSS
-JavaScript
-Backend
-Python
-Flask
-Flask-CORS
-API
-REST API
-Fetch API
-JSON
-Development Tool
-Vite
-Version Control
-Git
-GitHub

# Core Python Concepts
-Strings
-for loop
-if-elif conditions
-Input validation
-Functions

# Project Structure
password-validator/
│
├── App.jsx
├── app.py
├── index.html
├── main.jsx
├── package.json
├── requirements.txt
├── style.css
└── vite.config.js

# Working of the Project
User enters password
        ↓
React Frontend
        ↓
Basic Input Validation
        ↓
Fetch API
        ↓
POST /api/validate-password
        ↓
Python Flask Backend
        ↓
Password Validation
        ↓
Python for Loop
        ↓
Check Password Requirements
        ↓
JSON Response
        ↓
React Frontend
        ↓
Display Result

# Password Requirements

The password must satisfy all of the following:
Requirement	Description
Length	Minimum 8 characters
Uppercase	At least one uppercase letter
Lowercase	At least one lowercase letter
Number	At least one number
Special Character	At least one special character
Example
Valid Password
Hello@123

Result:

✓ Password is Valid
Invalid Password
Hello123

Result:

✕ Password is Invalid

Password must contain at least one special character.

# Installation and Setup
1. Clone the Repository
   git clone <your-github-repository-url>
   Navigate to the project: cd password-validator

2. Install Python Dependencies
Run: python -m pip install -r requirements.txt
The required packages are: Flask, Flask-CORS

3. Install React Dependencies
Run: npm install

4. Terminal 1: python app.py
   Terminal 2: npm run dev