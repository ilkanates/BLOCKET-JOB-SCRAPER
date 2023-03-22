# Blocket Job Scraper

The Blocket Job Scraper is a Python script that extracts job postings from the Blocket job board based on user inputs such as job title, location, and search range. 

## Features

* Scrapes job postings from the Blocket job board
* Retrieves job ID, job title, company name, job creation date, last day to apply, days left to apply, job location, role category, match percentage, job description URL
* Matches user skills with job description and calculates relevance rate
* Exports data to an Excel file

## How it works

The Blocked Job Scraper uses the following libraries:

* Selenium: to interact with the Blocket job board
* BeautifulSoup, Requests, and Regex: to retrieve and manipulate data
* Microsoft Azure Translation API: to translate job descriptions from Swedish to English
