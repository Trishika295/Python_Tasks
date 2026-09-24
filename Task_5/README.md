# Number Guessing Game

A simple and interactive Number Guessing Game built with React.js and Python Flask. The application generates a random number between 1 and 100, and the player keeps guessing until the correct number is found.

The game provides instant feedback such as Too High, Too Low, or Correct, while tracking the number of attempts and previous guesses.

# Features
--Random number generation using Python
--Number range from 1 to 100
--High/low hints after every guess
--Automatic attempt counter
--Guess history
--Correct-answer detection
--Restart / Play Again option
--Input validation
--React frontend with Flask backend
--Responsive and clean user interface
--REST API communication between frontend and backend

# Technologies Used
-Frontend
-React.js
-JavaScript
-HTML5
-CSS3
-Vite
-Backend
-Python
-Flask
-Flask-CORS
-Python random module

# Project Structure
number-guess-game/
│
├── App.jsx
├── app.py
├── game.py
├── index.css
├── index.html
├── main.jsx
├── package.json
├── package-lock.json
├── requirements.txt
└── style.css

# Installation and Setup
1. Clone the Repository
   git clone YOUR_GITHUB_REPOSITORY_URL
   Navigate to the project: cd Python_Intern/Task_5/number-guess-game

2. Backend Setup
   python -m venv venv
   Activate it: venv\Scripts\activate
   pip install -r requirements.txt
   python app.py

3. Frontend Setup
   npm install
   npm run dev
