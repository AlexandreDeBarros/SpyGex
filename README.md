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
  - Employ powerful regex patterns for precise data targeting.

- **Multithreaded Crawling:**
  - Accelerate data collection with multi-threaded web crawling.

- **Diverse Data Export Options:**
  - Choose between CSV, JSON, or Excel formats for data export.

- **User-Friendly Interface:**
  - Engage with an intuitive GUI, simplifying the scraping process.

## Ideas for Future Improvements and Enhancements

- **Settings Memory:**
   - Implement functionality to remember user settings between searches. This feature will enhance the user experience by reducing the setup time for frequent tasks. Remembering settings such as URLs, regular expressions, and output formats will streamline repetitive scraping activities.

- **Dynamic Page Handling:**
   - Introduce the capability to execute JavaScript, facilitating scraping from dynamically generated web pages. This improvement will expand the application's scraping capabilities to include websites that rely heavily on JavaScript for content generation, thereby accessing a wider range of data sources.

- **Centralizing Options Management:**
   - Shift the management of options and settings from the View to the Model. This architectural refinement will enhance the application's design by adhering more closely to the MVC principles. Centralizing settings management in the Model will simplify the process of storing and retrieving user preferences and make the application's codebase more organized and efficient.

## Architecture

SpyGex adopts the MVC (Model-View-Controller) architecture:

- **Model (`spygex_model.py`):** Manages the data logic and storage.
- **View (`spygex_view.py`):** Interfaces with the user, presenting data and options.
- **Controller (`spygex_controller.py`):** Connects the model and view, directing user commands.

The choice of MVC is driven by its ability to create a clear separation of concerns, making the code more modular, maintainable, and scalable.

## Project Structure

```
SpyGex/
│
├── config/
│   └── config.json (configuration file for regex)
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

https://github.com/AlexandreDeBarros/SpyGex/assets/45422062/d9cbe986-9f6c-45f4-b5db-b006c8a07372

2. **Specify the URL:**
   - Enter the website URL from which data needs to be scraped.

https://github.com/AlexandreDeBarros/SpyGex/assets/45422062/47322871-3761-43b0-85e5-8e93dae29b1f

3. **Set up Regex Patterns:**
   - Define the regular expressions for the data points to be extracted.

https://github.com/AlexandreDeBarros/SpyGex/assets/45422062/4bb6db34-0312-4372-b1f9-2ef147fb6ab8

4. **Launch Scraping:**
   - Begin the scraping process with a single click.

https://github.com/AlexandreDeBarros/SpyGex/assets/45422062/cd05266a-a420-4786-9105-3b37c5704f37

5. **Export Data:**
   - Save the results in the desired format for further use or analysis.

https://github.com/AlexandreDeBarros/SpyGex/assets/45422062/c5e75bfc-54ac-4cef-ae4e-6bb0afd290c5

## License

This project is open source and available under the [MIT License](LICENSE).

## Acknowledgments

- A special thanks to the main contributors: @Inkoming and @Karsov91, for their significant contributions to the development of this project.
