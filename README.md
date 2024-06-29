# Scraper Project

This project is a web scraping tool developed using the Python FastAPI framework. The tool automates the process of scraping product information from the target website [Dentalstall](https://dentalstall.com/shop/). The scraper extracts the product name, price, and image from each page of the catalog.

## Features

- Scrapes product information (name, price, image) from the specified website.
- Supports optional settings for limiting the number of pages to scrape and using a proxy.
- Stores scraped information in a local JSON file with easy integration for other storage strategies.
- Notifies designated recipients about the scraping status, with easy integration for other notification strategies.
- Implements in-memory caching to avoid updating products with unchanged prices.
- Includes simple authentication using a static token.
- Uses type validation and data integrity methods.
- Implements a retry mechanism for handling page load errors.

## Requirements

- Python 3.7+
- FastAPI
- Requests
- BeautifulSoup4
- Pydantic
- Uvicorn

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yashjoshi17/scraper-project.git
   cd scraper-project

2. Create and activate a virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate

3. Install the required dependencies:
   ```bash
   pip install -r requirements.txt

## Usage

1. Start the FastAPI server:
   ```bash
   uvicorn main:app --reload

2. Send a POST request to the /scrape endpoint with the necessary parameters.
    ```bash
   curl -X POST "http://127.0.0.1:8000/scrape" -H "accept: application/json" -H "token: your_static_token" -H "Content-Type: application/json" -d '{"limit": 5, "proxy": "http://yourproxy:port", "storage": "json", "notification": "console"}'
