# Objective

The objective of this project is to practice Python dictionary and key-value data management concepts by creating a Contact Book application that supports:

-Adding contact records
-Viewing contact records
-Searching contacts
-Updating contact information
-Deleting contact records
-Validating contact details
-Preventing duplicate contacts
-Storing contact information using Python -dictionaries
-Running the application through both terminal and browser

# Features
-Add contact ID, name, phone number, and email
-View all contacts
-Search contacts by ID, name, phone, or email
-Support partial and case-insensitive searches
-Update existing contact information
-Delete contact records
-Validate contact IDs
-Prevent duplicate contact IDs
-Validate phone numbers
-Prevent duplicate phone numbers
-Validate email addresses
-Display contact count
-Store contact data using Python dictionaries
-Save contact data using JSON
-React–Flask REST API integration
-Responsive user interface
-Python command-line interface
-Browser-based interface
-Meaningful success and error messages

# Technologies Used
Frontend: React.js, JavaScript, HTML, CSS, Vite, Fetch API

Backend: Python, Flask, Flask-CORS, REST API

Data Structure: Python Dictionaries, Key-Value Pairs

Data Storage: JSON

Development Tools: VS Code, Node.js, npm

Version Control: Git & GitHub

# Project Structure
contact-book/
│
├── index.html
├── app.py
├── contacts.json
├── requirements.txt
│
├── App.jsx
├── main.jsx
├── style.css
│
├── package.json
└── vite.config.js

# Installation and Setup
1. Clone the Repository

Clone the project using: git clone <your-github-repository-url>

Navigate into the project: cd contact-book

Backend Setup

Create a Python virtual environment: python -m venv venv
Activate the virtual environment on Windows: venv\Scripts\activate
Install the required Python packages: pip install -r requirements.txt

Start the Flask backend: python app.py

The backend will run at: http://127.0.0.1:5000
Keep this terminal running.

3. Frontend Setup
Open a second terminal in the project directory.
Install the Node.js dependencies: npm install

Start the React development server: npm run dev

The frontend will be available at: http://localhost:5173
Open the URL in your browser.

# CRUD Operations
The application demonstrates the four basic CRUD operations:

Operation	Description
Create	Add a new contact
Read	View existing contacts
Update	Modify contact information
Delete	Remove a contact
Validation

The application validates:
Contact ID
Contact name
Phone number
Email address
Duplicate contact IDs
Duplicate phone numbers
Required fields

Invalid data produces an appropriate error message instead of being added to the Contact Book.

# Conclusion

The Contact Book Using Dictionaries project demonstrates how Python dictionaries can be used to build a practical contact-management application. It combines Python, Flask, React, REST APIs, JSON persistence, and a command-line interface to provide both terminal-based and browser-based contact management.

The project provides practical experience with Python dictionaries, CRUD operations, validation, REST API development, React, Flask, and frontend-backend integration.