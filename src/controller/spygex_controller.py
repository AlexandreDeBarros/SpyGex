import requests

class SpyGexController:

    def __init__(self, model, view):
        self.model = model
        self.view = view

    def start_search(self, url, regex):
        try:
            # Assign URL and regex to the model
            self.model.url = url
            self.model.regex = regex

            # Begin crawling process
            self.model.start_crawling()
            print(self.model.df_result)

            # Update the scrollable frame in the view with results
            self.view.update_scrollable_frame(self.model.df_result, self.model.url, self.model.regex)

            # Show the detail view if results are found
            if not self.model.df_result.empty:
                self.view.show_detail_view()
            else:
                # No results message
                print("Info", "No results found.")

        # Handle HTTP request exceptions
        except requests.RequestException as e:
            print(f"HTTP request error for URL: {e}")

        # Handle general exceptions
        except Exception as e:
            print(f"Error processing URL: {e}")

    def get_regex_patterns(self):
        # Return regex patterns from the model
        return self.model.get_regex_patterns()
    
    def reset_model(self):
        # Create a new instance of the model
        self.model = type(self.model)()

    def export_csv(self, file_path):
        # Export data to CSV
        self.model.export_csv(file_path)
