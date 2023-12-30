# Standard Python modules
from threading import Thread

# Tkinter and CustomTkinter modules
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import filedialog, messagebox
import customtkinter as ctk
from view import digit_spinbox as ds

# Third-party modules
import pyperclip
from PIL import Image

# Spygex utils modules
from utils import spygex_utils as utils

class SpyGexView(ctk.CTk):
    """
    Main view of the SpyGex application.

    This class manages the display and interactions of the user interface, 
    including setting up the main window, handling events, and updating the view.
    """

    def __init__(self, *args, **kwargs):
        """Initialize the main view of the application."""
        
        super().__init__(*args, **kwargs)

        # Set the geometry and properties of the main window
        self.geometry("930x550+130+100")
        self.resizable(False, False)
        self.title("SpyGex - Scraper")

        # Initialize the controller value
        self.controller = None  

        # Initialize the main view and detail view
        self.init_main_view()
        self.init_detail_view()

        # Show the main view by default
        self.show_main_view()

        # User configurable options
        self.options = {
            'export_format': ['csv', ['csv', 'json', 'xlsx']],
            'copy_to_clipboard': {'Match': True, 'Context': True, 'URL': True},
            'Delete_Previous_Entries': False,
        }

        # Load icons for the interface
        self.load_icons()

        # Set the default color theme and appearance mode
        ctk.set_default_color_theme("blue")
        ctk.set_appearance_mode("dark")

    def load_icons(self):
        """Load and set icons for the application."""

        # Icon for copy to clipboard functionality
        self.copy_icon = ctk.CTkImage(
            light_image=Image.open(utils.resolve_relative_path('../../resources/copy_solid_light_blue.png')),
            dark_image=Image.open(utils.resolve_relative_path('../../resources/copy_solid_blue.png')),
            size=(20, 20))

        # Icon for opening the options menu
        self.option_icon = ctk.CTkImage(
            light_image=Image.open(utils.resolve_relative_path('../../resources/option_light.png')),
            dark_image=Image.open(utils.resolve_relative_path('../../resources/option.png')),
            size=(40, 40))

        # Icon for toggling dark/light mode
        self.moon_icon = ctk.CTkImage(
            light_image=Image.open(utils.resolve_relative_path('../../resources/moon.png')),
            dark_image=Image.open(utils.resolve_relative_path('../../resources/sun.png')),
            size=(40, 40))

    def init_main_view(self):
        """Initialize the main view frame and its components."""

        # Fonts for the main view
        self.title_font = ctk.CTkFont('Helvetica', 14, 'bold')
        self.entry_font = ctk.CTkFont('Helvetica', 12, 'normal')
        self.combo_font = ctk.CTkFont('Helvetica', 12, 'normal')

        # Main view frame
        self.main_view_frame = ctk.CTkFrame(self)

    @staticmethod
    def center_text(text, fill_char, width):
        """
        Center a given text within a specified width.

        Args:
            text (str): The text to be centered.
            fill_char (str): The character used for padding.
            width (int): The total width of the resulting string.

        Returns:
            str: Centered text string.
        """

        text_len = len(text)
        if text_len >= width:
            return text
        pad_len = int(1.35 * (width - text_len))
        return f"{text}{fill_char * pad_len}"

    def setup_main_view_layout(self):
        """Set up the layout of the main view."""

        # Logo image
        image = Image.open(utils.resolve_relative_path('../../resources/logo.png'))
        image = ctk.CTkImage(light_image=image, dark_image=image, size=(200, 200))
        self.image_label = ctk.CTkLabel(self.main_view_frame, image=image, text='')
        self.image_label.place(relx=0.5, rely=0.24, anchor=tk.CENTER)

        # Offset for positioning elements below the image
        self.from_image_offset = 0.5

        # URL entry field
        self.url_entry = ctk.CTkEntry(
            self.main_view_frame, font=self.entry_font,
            placeholder_text="Enter the URL to scrap", width=500, height=40)
        self.url_entry.place(relx=0.5, rely=self.from_image_offset, anchor=tk.CENTER)

        # Entry field for custom regex
        self.regex_entry = ctk.CTkEntry(
            self.main_view_frame, font=self.entry_font,
            placeholder_text="Enter your own custom REGEX", width=500, height=40)
        self.regex_entry.place(relx=0.5, rely=self.from_image_offset + 0.1, anchor=tk.CENTER)

        # ComboBox for REGEX selection
        regex_options = list(self.controller.get_regex_patterns().keys()) + ["Custom REGEX"]
        self.regex_options = [SpyGexView.center_text(option, ' ', 100) for option in regex_options]
        self.regex_combo = ctk.CTkComboBox(
            self.main_view_frame, values=self.regex_options, width=500, height=40,
            command=self.callback_regex_combo, font=self.combo_font, state="readonly")
        self.regex_combo.bind('<Configure>', self.callback_regex_combo)
        self.regex_combo.place(relx=0.5, rely=self.from_image_offset + 0.2, anchor=tk.CENTER)
        self.regex_combo.set(self.regex_options[-1])

        # Search button
        self.search_button = ctk.CTkButton(
            self.main_view_frame, text="Scrap", command=self.start_search,
            width=100, height=40)
        self.search_button.place(relx=0.5, rely=self.from_image_offset + 0.4, anchor=tk.CENTER)

        # Option button
        self.option_button = ctk.CTkButton(
            self.main_view_frame, command=self.open_options, hover=False,
            width=20, height=20, corner_radius=5, image=self.option_icon,
            fg_color="transparent", text='')
        self.option_button.place(relx=0.05, rely=self.from_image_offset + 0.4, anchor='c')

        # Pack the main view frame
        self.main_view_frame.pack(fill="both", expand=True)

    def change_theme(self):
        """Change the appearance mode of the application."""

        current_appearance_mode = ctk.get_appearance_mode()
        if current_appearance_mode == "Dark":
            ctk.set_appearance_mode("light")
        else:
            ctk.set_appearance_mode("dark")

    def open_options(self):
        """Open the options/settings window."""

        self.config_frame = ctk.CTkToplevel(self)
        self.config_frame.geometry('400x420')
        self.config_frame.title("SpyGex - Settings")
        self.config_frame.resizable(False, False)
        self.config_frame.grab_set()
        self.init_options_view()

    def init_options_view(self):
        """Initialize the options/settings view."""

        self.theme_button = ctk.CTkButton(
            self.config_frame, command=self.change_theme, hover=False,
            width=20, height=20, corner_radius=5, image=self.moon_icon,
            fg_color="transparent", text='')
        self.theme_button.place(relx=0.9, rely=(0.07 * 500) / 320, anchor='e')

        self.mode_label = ctk.CTkLabel(
            self.config_frame, text="Toggle dark/light mode", font=self.entry_font)
        self.mode_label.place(relx=0.10, rely=(0.07 * 500) / 320, anchor='w')

        # Separator
        separator = ttk.Separator(self.config_frame, orient='horizontal')
        separator.place(relx=0.5, rely=(0.16 * 500) / 320, anchor=tk.CENTER, relwidth=0.8)

        self.export_label = ctk.CTkLabel(
            self.config_frame, text="Export format", font=self.entry_font)
        self.export_label.place(relx=0.1, rely=(0.24 * 500) / 320, anchor='w')

        self.format_combo = ctk.CTkComboBox(
            self.config_frame, values=self.options['export_format'][1],
            width=125, height=40, font=self.combo_font, state="readonly",
            command=self.config_export_format)
        self.format_combo.place(relx=0.9, rely=(0.24 * 500) / 320, anchor='e')
        self.format_combo.set(self.options['export_format'][0])

        # Separator
        separator = ttk.Separator(self.config_frame, orient='horizontal')
        separator.place(relx=0.5, rely=(0.32 * 500) / 320, anchor=tk.CENTER, relwidth=0.8)

        self.copy_label = ctk.CTkLabel(
            self.config_frame, text="Copy options", font=self.entry_font)
        self.copy_label.place(relx=0.1, rely=(0.40 * 500) / 320, anchor='w')

        self.match_check_var = tk.BooleanVar(value=self.options['copy_to_clipboard']['Match'])
        self.match_check = ctk.CTkCheckBox(
            self.config_frame, text="Match", onvalue=True, offvalue=False,
            font=self.entry_font, variable=self.match_check_var,
            command=self.update_copy_to_clipboard)
        self.match_check.place(relx=0.62, rely=(0.40 * 500) / 320, anchor='e')

        self.context_check_var = tk.BooleanVar(value=self.options['copy_to_clipboard']['Context'])
        self.context_check = ctk.CTkCheckBox(
            self.config_frame, text="Context", onvalue=True, offvalue=False,
            variable=self.context_check_var, command=self.update_copy_to_clipboard)
        self.context_check.place(relx=0.795, rely=(0.40 * 500) / 320, anchor='e')

        self.url_check_var = tk.BooleanVar(value=self.options['copy_to_clipboard']['URL'])
        self.url_check = ctk.CTkCheckBox(
            self.config_frame, text="URL", onvalue=True, offvalue=False,
            font=self.entry_font, variable=self.url_check_var,
            command=self.update_copy_to_clipboard)
        self.url_check.place(relx=1.0, rely=(0.40 * 500) / 320, anchor='e')

        # Separator
        separator = ttk.Separator(self.config_frame, orient='horizontal')
        separator.place(relx=0.5, rely=(0.48 * 500) / 320, anchor=tk.CENTER, relwidth=0.8)

        self.delete_prev = ctk.CTkLabel(
            self.config_frame, text="Delete previous entries", font=self.entry_font)
        self.delete_prev.place(relx=0.1, rely=(0.56 * 500) / 320, anchor='w')

        self.radio_bool = tk.BooleanVar(value=self.options['Delete_Previous_Entries'])
        ctk.CTkRadioButton(
            self.config_frame, text="Yes", value=True, font=self.entry_font,
            command=self.update_delete_entries, variable=self.radio_bool).place(relx=0.85, rely=(0.56 * 500) / 320, anchor='e')
        ctk.CTkRadioButton(
            self.config_frame, text="No", value=False, font=self.entry_font,
            command=self.update_delete_entries, variable=self.radio_bool).place(relx=1.03, rely=(0.56 * 500) / 320, anchor='e')
        
        # Separator avant les Worker Count Settings
        separator = ttk.Separator(self.config_frame, orient='horizontal')
        separator.place(relx=0.5, rely=0.68, anchor=tk.CENTER, relwidth=0.8)

        # Worker Count Setting
        self.worker_label = ctk.CTkLabel(
            master=self.config_frame, text="Number of Workers", font=self.entry_font)
        self.worker_label.place(relx=0.1, rely=0.74, anchor='w')

        self.worker_spinbox = ds.DigitSpinbox(
            master=self.config_frame, width=120, height=25,
            command=self.update_number_of_workers)
        self.worker_spinbox.set(self.controller.get_number_of_workers())
        self.worker_spinbox.place(relx=0.6, rely=0.74, anchor='w')

    def update_delete_entries(self, event=None):
        """Update the delete previous entries option."""

        self.options['Delete_Previous_Entries'] = self.radio_bool.get()

    def update_copy_to_clipboard(self, event=None):
        """Update the copy to clipboard options."""

        self.options['copy_to_clipboard']['Match'] = self.match_check_var.get()
        self.options['copy_to_clipboard']['Context'] = self.context_check_var.get()
        self.options['copy_to_clipboard']['URL'] = self.url_check_var.get()

        if not self.options['copy_to_clipboard']['Match'] and not self.options['copy_to_clipboard']['Context'] and not self.options['copy_to_clipboard']['URL']:
            self.match_check_var.set(True)
            self.options['copy_to_clipboard']['Match'] = True

    def config_export_format(self, event=None):
        """Update the export file format option."""

        self.options['export_format'][0] = self.format_combo.get()

    def init_detail_view(self):
        """Initialize the detail view frame and its components."""

        self.detail_view_frame = ctk.CTkFrame(self)

        self.info_frame = ctk.CTkFrame(
            self.detail_view_frame, bg_color='transparent', fg_color="transparent")
        self.info_frame.place(relx=0.5, rely=0.02, anchor='n', relwidth=0.98, relheight=0.15)

        # Configure the scrollable frame
        self.scrollable_frame = ctk.CTkScrollableFrame(self.detail_view_frame)
        self.scrollable_frame.place(relwidth=0.98, relheight=0.61, anchor='n', relx=0.5, rely=0.26)

        # Frame for buttons
        button_frame = ctk.CTkFrame(
            self.detail_view_frame, bg_color='transparent', fg_color="transparent")
        button_frame.place(relx=0.5, rely=0.97, anchor='s', relwidth=0.98, relheight=0.1)

        # "New Search" button
        new_search_button = ctk.CTkButton(
            button_frame, text="New scrap", command=self.new_search, font=self.entry_font)
        new_search_button.place(anchor='e', relx=0.97, rely=0.6, relwidth=0.1, relheight=0.7)

        # "Export" button
        export_button = ctk.CTkButton(
            button_frame, text="Export", command=self.export_file, font=self.entry_font)
        export_button.place(anchor='e', relx=0.85, rely=0.6,
                            relwidth=0.1, relheight=0.7)

    def update_scrollable_frame(self, df, url, regex_to_use):    
        """
        Update the scrollable frame with search results.

        Displays the domain name, the regex used, and the number of matches found. 
        Also populates the frame with individual match details.

        Args:
            df (DataFrame): The DataFrame containing the search results.
            url (str): The URL where the search was performed.
            regex_to_use (str): The regex pattern used for the search.
        """
        
        ctk.CTkLabel(self.info_frame, text="Domain name:", font=self.entry_font).place(
            anchor='e', relx=0.12, rely=0.20)

        ctk.CTkLabel(self.info_frame, text=f"{url}", font=self.entry_font).place(
            anchor='w', relx=0.13, rely=0.20)

        if len(regex_to_use) > 155:
            regex_to_use = regex_to_use[:155] + ' ...'

        ctk.CTkLabel(self.info_frame, text="Regex used:", font=self.entry_font).place(
            anchor='e', relx=0.12, rely=0.50)

        ctk.CTkLabel(self.info_frame, text=f"{regex_to_use}", font=self.entry_font).place(
            anchor='w', relx=0.13, rely=0.50)

        ctk.CTkLabel(self.info_frame, text="Matches found:", font=self.entry_font).place(
            anchor='e', relx=0.12, rely=0.8)

        ctk.CTkLabel(self.info_frame, text=f"{df.shape[0]}", font=self.entry_font).place(
            anchor='w', relx=0.13, rely=0.8)

        # Create and add column headers
        header_frame = ctk.CTkFrame(self.detail_view_frame, corner_radius=0)
        header_frame.place(relx=0.5, rely=0.25, anchor='s',
                           relwidth=0.98, relheight=0.06)
        ctk.CTkLabel(header_frame, text="Match", font=self.title_font).place(
            anchor='c', relx=0.10, rely=0.5, )
        ctk.CTkLabel(header_frame, text="Context", font=self.title_font).place(
            anchor='c', relx=0.40, rely=0.5)
        ctk.CTkLabel(header_frame, text="URL", font=self.title_font).place(
            anchor='c', relx=0.75, rely=0.5)

        # Add new data
        for index, row in df.iterrows():
            row_frame = ctk.CTkFrame(self.scrollable_frame, height=35)
            row_frame.pack(fill='x', padx=0, pady=3)
            ctk.CTkLabel(row_frame, text=row['Match'][:25], font=self.entry_font).place(
                anchor='c', relx=0.1, rely=0.5)
            ctk.CTkLabel(row_frame, text=str(row['Line'])[:30], font=self.entry_font).place(
                anchor='c', relx=0.40, rely=0.5)

            url = row['Url']
            if len(url) > 24:
                url = url[:24] + ' ...'
            ctk.CTkLabel(row_frame, text=url, font=self.entry_font).place(
                anchor='c', relx=0.75, rely=0.5)
            ctk.CTkButton(row_frame, 20, 20, text="", image=self.copy_icon, fg_color="transparent", command=lambda row=row: self.copy_to_clipboard(
                row)).place(
                anchor='c', relx=0.95, rely=0.5)
        self.scrollable_frame.update_idletasks()

    def start_search(self):
        """
        Initiates the search process based on user inputs.

        Validates the URL and regex input, then starts a new thread to perform the search without blocking the UI.
        """

        url = self.url_entry.get()
        regex_to_use = self.regex_entry.get()

        # Validate URL and regex input
        if not url.strip() or not regex_to_use.strip():
            messagebox.showerror("Missing patterns", "Please enter a valid URL and a REGEX pattern.")
            return

        # Create a progress bar and start it
        self.progress_bar = ctk.CTkProgressBar(self.main_view_frame, width=500, height=5, mode='indeterminate', indeterminate_speed=1)
        self.progress_bar.place(relx=0.5, rely=0.5 + 0.30, anchor=tk.CENTER)
        self.progress_bar.start()

        # Start the search in a new thread to keep the UI responsive
        new_thread = Thread(target=self.controller.start_search, args=(url, regex_to_use), daemon=True)
        new_thread.start()

    def callback_regex_combo(self, event=None):
        """
        Callback function for regex combo box selection.

        Updates the regex entry based on the user's selection from the combo box.

        Args:
            event: The event triggering this callback (unused in this method).
        """

        selected_regex = self.regex_combo.get().strip(' ')
        regex_dict = self.controller.get_regex_patterns()
    
        # Update regex entry based on user selection
        if selected_regex in regex_dict:
            self.regex_entry.delete(0, 'end')
            self.regex_entry.insert(0, regex_dict[selected_regex])
        elif selected_regex == "Custom REGEX":
            self.regex_entry.delete(0, 'end')

    def show_main_view(self):
        """
        Switches to the main view of the application.
        """

        self.detail_view_frame.pack_forget()
        self.main_view_frame.pack(fill="both", expand=True)

    def show_detail_view(self):
        """
        Switches to the detail view of the application.
        """

        self.main_view_frame.pack_forget()
        self.detail_view_frame.pack(fill="both", expand=True)

    def run(self):
        """
        Sets up the main view layout and starts the application's main loop.
        """

        self.setup_main_view_layout()
        self.mainloop()

    def copy_to_clipboard(self, row):
        """
        Copies the selected row to the clipboard based on user preferences.

        Args:
            row: The row data to be copied.
        """

        text_to_copy = ''
        if self.options['copy_to_clipboard']['Match']:
            text_to_copy += 'Match:\n' + row['Match'] + '\n'

        if self.options['copy_to_clipboard']['Context']:
            text_to_copy += 'Context:\n' + str(row['Line']) + '\n'

        if self.options['copy_to_clipboard']['URL']:
            text_to_copy += 'URL:\n' + row['Url']

        pyperclip.copy(text_to_copy)
        messagebox.showinfo("Information", "Successfully copied to clipboard.")

    def new_search(self):
        """
        Resets input fields and prepares for a new search.
        """

        if self.options['Delete_Previous_Entries']:
            self.url_entry.delete(0, 'end')
            self.regex_entry.delete(0, 'end')
            self.regex_combo.set(self.regex_options[-1])

        # Destroy the progress bar if it exists
        self.progress_bar.destroy()  

        # Clear data displayed in the detail view frame
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()
        for widget in self.info_frame.winfo_children():
            widget.destroy()

        # Reset the model for a new search
        self.controller.reset_model()

        # Return to the main view
        self.show_main_view()  

    def export_file(self):
        """
        Exports the search results to a file.

        Allows the user to select the export format and save the file.
        """
        if self.options['export_format'][0] == 'csv':
            file_path = filedialog.asksaveasfilename(defaultextension='.csv', filetypes=[("CSV files", '*.csv')], title="Save As")
        elif self.options['export_format'][0] == 'json':
            file_path = filedialog.asksaveasfilename(defaultextension='.json', filetypes=[("JSON files", '*.json')], title="Save As")
        elif self.options['export_format'][0] == 'xlsx':
            file_path = filedialog.asksaveasfilename(defaultextension='.xlsx', filetypes=[("Excel files", '*.xlsx')], title="Save As")

        if file_path:

            # Call the export method in the controller
            self.controller.export_file(file_path)  
    
    def update_number_of_workers(self, event=None):
        """
        Update the number of workers in the model.

        Args:
            event: The event that triggered this callback.
        """

        # Update the model with the new number of workers
        self.controller.set_number_of_workers(int(self.worker_spinbox.get()))
    
    def results_found(self):
        """
        Updates the UI to display the detail view with search results.
        """
        self.show_detail_view()

    def no_results_found(self):
        """
        Updates the UI when no search results are found, including removing the progress bar,
        showing an information message, and reverting to the main view.
        """
        self.progress_bar.destroy()
        messagebox.showinfo("Information", "No results found.")
        self.show_main_view()
