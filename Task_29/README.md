# Python Web Scraper

## Overview
BookScope is a Python web scraping mini project with a
professional Streamlit frontend. It extracts book information
from the Books to Scrape practice catalog and exports the
collected data to CSV.

## Features
- Multi-page catalog scraping
- HTTP requests and HTML parsing
- robots.txt access checks
- Book title, price and availability extraction
- Rating and product URL extraction
- Image URL extraction
- Catalog page tracking
- Search and rating filters
- Book preview cards
- CSV export and download
- Request delays and error handling

## Technologies
- Python
- Requests
- BeautifulSoup
- Pandas
- Streamlit
- CSV

## Folder Structure
Task_29/
├── app.py
├── web_scraper.py
├── requirements.txt
├── README.md
└── scraped_data.csv

## Installation
Install the required dependencies:

    python -m pip install -r requirements.txt

## Run the Web Application

    python -m streamlit run app.py

Open the local URL displayed in the terminal.

## Run the Command-Line Version

    python web_scraper.py

Enter the number of catalog pages when prompted.

## CSV Fields
- title
- price
- availability
- rating
- product_url
- image_url
- page_number

## Learning Outcomes
- HTTP requests and responses
- HTML parsing with CSS selectors
- Pagination and link extraction
- Data filtering and presentation
- CSV file handling
- Streamlit frontend development
- Exception handling and responsible scraping

## Responsible Use
The project is designed for the Books to Scrape practice
website. Review website terms and access restrictions.
A missing robots.txt file is not, by itself, permission
to scrape a website.

## Conclusion
BookScope demonstrates how Python can collect structured
data from multiple catalog pages, present it in a web
interface, and export it for further analysis.
