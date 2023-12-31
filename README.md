# SpyGex - Web Scraping Application

SpyGex is a comprehensive web scraping application designed to extract content from websites using regular expressions. It's built using Python, making it a powerful yet user-friendly tool for data extraction and analysis.

## Installation

To install and run SpyGex, follow these steps:

1. **Clone or Download the Repository:**
   - Use `git clone` or download the ZIP from the repository.
   
2. **Install Dependencies:**
   - Ensure Python 3 is installed on your system.
   - Install required libraries by running `pip install -r requirements.txt` in the terminal within the project directory.

3. **Run the Application:**
   - Execute the main script: `python App.py`.

## Features

1. **Adjust Settings:**
   - Customize the scraping settings and UI preferences as needed.

2. **Regular Expression Based Scraping:**
   - Utilize custom or predefined regular expressions for targeted scraping.
  
3. **Concurrent Web Crawling:**
   - Speed up the scraping process with adjustable parallel processing capabilities.

4. **Data Export:**
   - Export scraped data in CSV, JSON, or Excel format.

5. **User Interface:**
   - Intuitive GUI built with Tkinter for easy interaction and monitoring.

## Architecture

SpyGex follows the MVC (Model-View-Controller) architecture, providing a clear separation between the user interface, data handling, and control logic:

- **Model (`SpyGexModel`):** Handles data manipulation, web scraping logic, and stores results.
  
- **View (`SpyGexView`):** Manages the user interface, displaying results and accepting user inputs.

- **Controller (`SpyGexController`):** Acts as an intermediary between the model and view, handling user requests and updating the view accordingly.

## Libraries Used

- **Data Manipulation:** `pandas`
- **Web Scraping:** `requests`, `BeautifulSoup`
- **Parallel Processing:** `ThreadPoolExecutor` from `concurrent.futures`
- **User Interface:** `tkinter`, `customtkinter`
- **Utilities:** `json`, `re` (Regular Expressions)

## Usage

After launching SpyGex, follow these steps:

1. **Adjust Settings:**
   - Customize the scraping settings and UI preferences as needed.

https://github.com/AlexandreDeBarros/SpyGex/assets/45422062/77c194c5-71fe-410a-9867-c4a9a0ade994

2. **Enter the Target URL:**
   - Specify the website URL you wish to scrape.

3. **Input or Select a Regular Expression:**
   - Use a predefined pattern or enter a custom regex.

4. **Start Scraping:**
   - Initiate the scraping process and view real-time results.

5. **Export Data:**
   - Save the extracted data in your preferred format.

SpyGex provides a versatile and user-friendly platform for web scraping enthusiasts and professionals alike, combining powerful scraping capabilities with an intuitive interface.
