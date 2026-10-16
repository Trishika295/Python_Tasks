# Simple Python REST API Client

## Project Overview
The Simple Python REST API Client is a command-line application developed using Python. It consumes a public REST API, retrieves JSON data, and displays selected information in a readable format.

## Objective
To understand REST API consumption, HTTP GET requests, JSON response handling, and error management using Python.

## Technologies Used
- Python
- Requests library
- JSON
- JSONPlaceholder public REST API

## Features
1. Fetch data from a public REST API.
2. Retrieve 5 or 10 posts, or specify a custom number.
3. Display post ID, user ID, title, and body.
4. Check HTTP response status codes.
5. Handle connection failures and request timeouts.
6. Handle HTTP errors and invalid input.
7. Display API data in a formatted terminal output.
8. Use a timeout to prevent requests from waiting indefinitely.

## API Endpoint
https://jsonplaceholder.typicode.com/posts

## Installation

1. Install Python 3.
2. Open a terminal in the project directory.
3. Install dependencies:

   pip install -r requirements.txt

## Execution

Run the application using:

python api_client.py

Follow the menu displayed in the terminal to fetch API data.

## Example Output

============================================================
             PYTHON REST API CLIENT
============================================================
1. Fetch 5 posts
2. Fetch 10 posts
3. Fetch a custom number of posts
4. Exit

Enter your choice (1-4): 1

Connecting to the public API...

============================================================
          SIMPLE PYTHON API CLIENT
============================================================
HTTP Status Code : 200
Posts Retrieved  : 5
------------------------------------------------------------
Post ID : 1
User ID : 1
Title   : Sample post title
Body    : Sample post body
------------------------------------------------------------

Note: The actual title and body are returned by the API and may
differ from illustrative output.

## Error Handling
- Connection errors
- Request timeouts
- HTTP errors
- Invalid input
- Unexpected response formats

## Learning Outcomes
- Understanding REST APIs and HTTP GET requests.
- Using the requests library.
- Parsing JSON responses.
- Checking HTTP status codes.
- Implementing exception handling.
- Displaying structured data.

## Conclusion
This project demonstrates how Python can interact with a public REST API, process JSON responses, and present useful information through a command-line interface. It provides a foundation for developing larger API-driven applications.
