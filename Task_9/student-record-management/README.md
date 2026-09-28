# Objective

The objective of this project is to practice Python list-processing concepts by creating a student records application that supports:
--Adding student records
--Viewing student records
--Searching students by name
--Sorting students by marks
--Finding the highest score
--Finding the lowest score
--Calculating the average score
--Deleting student records
--Validating student marks

# Features
-Add student name and marks
-Search students by name
-Sort marks from highest to lowest
-Sort marks from lowest to highest
-Display highest score
-Display lowest score
-Calculate average score
-Display total number of students
-Delete student records
-Validate marks between 0 and 100
-React–Flask REST API integration
-Responsive user interface

# Technologies Used
Frontend: React.js, JavaScript, HTML, CSS, Vite, Fetch API
Backend: Python, Flask, Flask-CORS, REST API, Data Structure, Python Lists, Python Dictionaries
Built-in functions such as: sorted(), max(), min(), sum()

# Project Structure
student-records-management/
│
├── index.html
├── app.py
├── student_manager.py
├── requirements.txt
│
├── StudentForm.jsx
├── StudentList.jsx
├── SearchStudent.jsx
├── Statistics.jsx
├── App.jsx
├── style.css
├── main.jsx
│
├── package.json
└── vite.config.js

# Installation and Setup
1. Clone the Repository
git clone <your-github-repository-url>
Navigate into the project: cd student-records-management

2. Backend Setup
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

