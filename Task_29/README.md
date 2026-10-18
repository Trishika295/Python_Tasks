
# Task 28: Python Web Scraper

## Overview
A beginner-friendly Python web scraping application that
extracts structured information from a permitted webpage
and exports the collected data to a CSV file.

## Features
- Sends HTTP requests using Requests
- Parses HTML using BeautifulSoup
- Extracts book titles, prices, availability and ratings
- Collects product page URLs
- Checks robots.txt before scraping
- Handles HTTP, timeout and network errors
- Exports data to CSV
- Supports a configurable webpage URL

## Technologies
- Python
- Requests
- BeautifulSoup4
- CSV
- HTML parsing

## Project Structure
Task_28_Web_Scraper/
├── web_scraper.py
├── requirements.txt
├── README.md
├── .gitignore
└── scraped_data.csv (generated)

## Installation

1. Install Python 3.10 or later.
2. Open a terminal in the project folder.
3. Install the dependencies:

   pip install -r requirements.txt

## Execution

Run the program:

   python web_scraper.py

Choose option 1 to use the default practice website.
The extracted records are saved to scraped_data.csv.

## CSV Fields
- title: Name of the book
- price: Displayed price
- availability: Stock availability text
- rating: Displayed star-rating category
- product_url: Link to the product page

## Learning Outcomes
- Understanding HTTP requests
- Learning HTML parsing and CSS selectors
- Extracting structured information
- Writing CSV files
- Handling network errors
- Understanding responsible scraping practices

## Responsible Usage
Only scrape webpages where automated access is permitted.
Respect robots.txt, website terms and request limits.
Avoid collecting personal or restricted information.

## Limitations
The extraction logic depends on the target webpage's HTML
structure. JavaScript-rendered pages may require a different
approach. A website's robots.txt rules can change over time.

## Conclusion
This project demonstrates the basic workflow of a web scraper:
requesting a webpage, parsing its HTML, extracting structured
data and storing the results in a reusable CSV dataset.
