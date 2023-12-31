# SpyGex - Web Scraping Application 

SpyGex is a comprehensive web scraping application designed to extract content from websites using regular expressions. Built with Python, it offers a powerful yet user-friendly platform for data extraction and analysis. The application is designed to be used directly without the need for installing additional applications or browsers, providing a standalone solution for your scraping needs.

## Installation

1. **Clone or Download the Repository:**
   - `git clone https://github.com/AlexandreDeBarros/SpyGex.git` or download the ZIP from the repository.

2. **Install Dependencies:**
   - Ensure Python 3.11 is installed on your system.
   - Run `pip install -r requirements.txt` in the terminal within the project directory to install required libraries.

3. **Run the Application:**
   - Navigate to the `src` directory and run `python App.py` to start the application.

## Features

- **Customizable Settings:**
  - Configure scraping rules, output formats, and UI preferences.
  
- **Regular Expression Scraping:**
  - Employ powerful REGEX patterns for precise data targeting.

- **Multithreaded Crawling:**
  - Accelerate data collection with multi-threaded web crawling.

- **Diverse Data Export Options:**
  - Choose between CSV, JSON, or Excel formats for data export.

- **User-Friendly Interface:**
  - Engage with an intuitive GUI, simplifying the scraping process.

## Ideas for Future Improvements

- **Settings Memory:**
  - Implement functionality to remember user settings between searches, enhancing user experience by reducing setup time for frequent tasks.

- **Dynamic Page Handling:**
  - Introduce the execution of JavaScript to handle scraping from dynamically generated web pages, expanding the application's scraping capabilities to a broader range of websites.

## Architecture

SpyGex adopts the MVC (Model-View-Controller) architecture:

- **Model (`spygex_model.py`):** Manages the data logic and storage.
- **View (`spygex_view.py`):** Interfaces with the user, presenting data and options.
- **Controller (`spygex_controller.py`):** Connects the model and view, directing user commands.

## Project Structure

```
SpyGex/
│
├── config/
│   └── config.json (configuration file for REGEX)
│
├── resources/
│   └── ... (resource files like icons and logo)
│
└── src/
│   ├── controller/
│   │   └── spygex_controller.py (controller)
│   │
│   ├── model/
│   │   └── spygex_model.py (model)
│   │
│   ├── utils/
│   │   └── ... (utility module)
│   │
│   ├── view/
│   │   ├── custom_widget/
│   │   │   └── ... (custom widget for ctk)
│   │   └── spygex_view.py (view)
│   │
│   └── App.py (entry point)
├── .gitignore
├── README.md
└── requirements.txt
```

## Libraries Used

- **Data Manipulation:** `pandas`
- **Web Scraping:** `requests`, `BeautifulSoup`
- **Concurrency:** `concurrent.futures`
- **UI:** `tkinter`, `customtkinter`
- **Clipboard Operations:** `pyperclip`
- **Image Handling:** `PIL` (Python Imaging Library)
- **Utilities:** `json`, `re`, `threading`

## Usage

1. **Configure Settings:**
   - Set your preferences and rules for scraping within the application or config files.

2. **Specify the URL:**
   - Enter the website URL from which data needs to be scraped.

3. **Set up REGEX Patterns:**
   - Define the regular expressions for the data points to be extracted.

4. **Launch Scraping:**
   - Begin the scraping process with a single click.

5. **Export Data:**
   - Save the results in the desired format for further use or analysis.

## License

This project is open source and available under the [MIT License](LICENSE).

## Acknowledgments

- A special thanks to the main contributors: Inkoming and Karsov91, for their significant contributions to the development of this project.
