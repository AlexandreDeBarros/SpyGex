# Alert dialogs module
from tkinter import messagebox

# Handling HTTP requests module
import requests

class SpyGexController:
    """
    Controller for the SpyGex web scraping application.

    This class handles user interactions, processes web scraping tasks, updates the view,
    and manages communication between the model and the view.

    Attributes:
        model: The model part of the MVC architecture.
        view: The view part of the MVC architecture.
    """

    def __init__(self, model, view):
        """
        Initialize the controller with a model and a view.

        Args:
            model: The model instance of the application.
            view: The view instance of the application.
        """
        self.model = model
        self.view = view

    def start_search(self, url, regex):
        """
        Start the web scraping process with the given URL and regex.

        Args:
            url (str): The URL to scrape.
            regex (str): The regular expression pattern to use for scraping.
        """
        try:
            # Assign URL and regex to the model
            self.model.url = url
            self.model.regex = regex

            # Begin crawling process
            self.model.start_crawling()

            # Update the scrollable frame in the view with results
            self.view.update_scrollable_frame(
                self.model.df_result, self.model.url, self.model.regex)

            # Determine if results are found and notify the view
            if not self.model.df_result.empty:
                self.view.results_found()
            else:
                self.view.no_results_found()

        # Handle HTTP request exceptions
        except requests.RequestException as e:
            self.view.progress_bar.destroy()
            messagebox.showerror("HTTP Request Error", f"HTTP request error for URL: {e}")

        # Handle general exceptions
        except Exception as e:
            self.view.progress_bar.destroy()
            messagebox.showerror("Error", f"Error processing URL: {e}")

    def get_regex_patterns(self):
        """
        Retrieve regex patterns stored in the model.

        Returns:
            dict: A dictionary of regex patterns.
        """
        return self.model.regex_patterns

    def reset_model(self):
        """
        Reset the model to its initial state.
        """
        self.model = type(self.model)()

    def export_file(self, file_path):
        """
        Export the scraped data to a file.

        Args:
            file_path (str): The path where the file will be saved.
        """
        self.model.export_file(file_path)

    def get_number_of_workers(self):
        """
        Get the current number of workers used for parallel processing.

        Returns:
            int: The number of workers.
        """
        return self.model.workers_number
    
    def set_number_of_workers(self, workers_number):
        """
        Set the number of workers for parallel processing.

        Args:
            workers_number (int): The number of workers to use.
        """
        self.model.workers_number = workers_number

