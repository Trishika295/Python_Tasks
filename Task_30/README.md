# Server Log File Analyzer

## Overview
A Python-based log analysis application that processes HTTP server
logs and summarizes request activity, HTTP errors, frequently
accessing IP addresses, and popular endpoints.

## Features
- Parse standard HTTP access log entries.
- Count total requests and unique IP addresses.
- Identify 4xx client errors and 5xx server errors.
- Find the most frequent IP addresses.
- Identify the most requested endpoints.
- Summarize HTTP methods and response status codes.
- Handle malformed log lines without stopping the analysis.
- Generate downloadable text reports and CSV files.
- Explore results through a Streamlit dashboard.

## Technologies
- Python
- Streamlit
- Pandas
- collections.Counter
- Regular expressions
- File handling

## Folder Structure
Task_30/
├── app.py
├── log_analyzer.py
├── requirements.txt
├── README.md
├── .gitignore
└── data/
    └── sample.log

## Installation

Create and activate a virtual environment:

python -m venv .venv

Windows:
.venv\Scripts\activate

Install dependencies:

pip install -r requirements.txt

## Run the Dashboard

streamlit run app.py

Open the local URL displayed in the terminal.

## Run the Command-Line Analyzer

python log_analyzer.py

The command-line version prints a summary of the included sample log.

## Supported Log Format
The parser supports common HTTP access logs in which the request
contains an HTTP method, endpoint, protocol, status code, and size.

## Limitations
The parser is designed for a common access-log format, not every
possible server log format. Unrecognized lines are skipped and counted.
The dashboard analyzes the file provided by the user; it does not
automatically connect to a live production server.

## Learning Outcomes
- Python file handling and string processing.
- Dictionaries and collections.Counter.
- Regular expressions and input validation.
- Basic data analysis and report generation.
- Building a dashboard with Streamlit.
