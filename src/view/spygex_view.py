import os
import tkinter as tk
import tkinter.ttk as ttk
from threading import Thread
from tkinter import filedialog, messagebox

import customtkinter as ctk
import pyperclip
from PIL import Image


# Helper function to resolve relative paths
def resolve_relative_path(path: str) -> str:
    return os.path.abspath(os.path.join(os.path.dirname(__file__), path))


# Icon used for copy to clipboard
copy_icon = ctk.CTkImage(light_image=Image.open(resolve_relative_path('../../resources/copy_solid_light_blue.png')),
                         dark_image=Image.open(resolve_relative_path('../../resources/copy_solid_blue.png')), size=(20, 20))

# Icon used to open the Options Menu
option_icon = ctk.CTkImage(light_image=Image.open(resolve_relative_path('../../resources/option_light.png')),
                           dark_image=Image.open(resolve_relative_path('../../resources/option.png')), size=(40, 40))


moon_icon = ctk.CTkImage(light_image=Image.open(resolve_relative_path('../../resources/moon.png')),
                         dark_image=Image.open(resolve_relative_path('../../resources/sun.png')), size=(40, 40))

# Set the default color theme and appearance mode
ctk.set_default_color_theme("blue")
ctk.set_appearance_mode("dark")


class SpyGexView(ctk.CTk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Set the geometry and properties of the main window
        self.geometry("930x550+130+100")
        self.resizable(False, False)
        self.title("SpyGex - Scraper")

        self.controller = None  # type: ignore

        # Initialize the main view and detail view
        self.init_main_view()
        self.init_detail_view()

        # Show the main view by default
        self.show_main_view()

        # User can change:
        # 1. Export format
        # 2. Copy options (to clipboard)
        # 3. Whether to delete previous entries when starting a new search

        self.options = {
            'export_format': ['csv', ['csv', 'json', 'xlsx']],
            'copy_to_clipboard': {'Match': True, 'Context': True, 'URL': True},
            'Delete_Previous_Entries': False,
        }

    def controller(self, controller):
        # Assign a controller to the view
        self.controller = controller

    def init_main_view(self):

        self.title_font = ctk.CTkFont('Helvetica', 14, 'bold')
        self.entry_font = ctk.CTkFont('Helvetica', 12, 'normal')
        self.combo_font = ctk.CTkFont('Helvetica', 12, 'normal')

        # Initialize the main view frame
        self.main_view_frame = ctk.CTkFrame(self)

    @staticmethod
    def center_text(text, fill_char, width):
        # Helper function to center text
        text_len = len(text)
        if text_len >= width:
            return text
        pad_len = int(1.35 * (width - text_len))
        # pad_left = pad_len // 2
        # pad_right = pad_len - pad_left
        # return f"{fill_char * pad_left}{text}{fill_char * pad_right}"
        return f"{text}{fill_char * pad_len}"

    def setup_main_view_layout(self):
        # Setup the main view layout
        image = Image.open(resolve_relative_path('../../resources/logo.png'))
        image = ctk.CTkImage(
            light_image=image, dark_image=image, size=(200, 200))
        self.image_label = ctk.CTkLabel(
            self.main_view_frame, image=image, text='')
        self.image_label.place(relx=0.5, rely=0.24, anchor=tk.CENTER)

        self.from_image_offset = 0.5

        # URL entry field
        self.url_entry = ctk.CTkEntry(self.main_view_frame,
                                      font=self.entry_font,
                                      placeholder_text="Enter the URL to scrap", width=500, height=40,
                                      )
        self.url_entry.place(
            relx=0.5, rely=self.from_image_offset, anchor=tk.CENTER)

        # Entry field for custom regex
        self.regex_entry = ctk.CTkEntry(
            self.main_view_frame, font=self.entry_font, placeholder_text="Enter your own custom REGEX", width=500, height=40,)
        self.regex_entry.place(
            relx=0.5, rely=self.from_image_offset + 0.1, anchor=tk.CENTER)

        # ComboBox for REGEX selection
        regex_options = list(
            self.controller.get_regex_patterns().keys()) + ["Custom REGEX"]

        self.regex_options = [SpyGexView.center_text(option, ' ', 100)
                              for option in regex_options]
        self.regex_combo = ctk.CTkComboBox(
            self.main_view_frame, values=self.regex_options, width=500, height=40, command=self.callback_regex_combo, font=self.combo_font, state="readonly")
        self.regex_combo.bind(
            '<Configure>', self.callback_regex_combo)

        self.regex_combo.place(
            relx=0.5, rely=self.from_image_offset + 0.2, anchor=tk.CENTER)
        self.regex_combo.set(self.regex_options[-1])

        # Search button
        self.search_button = ctk.CTkButton(
            width=100, height=40, master=self.main_view_frame, text="Scrap", command=self.start_search)
        self.search_button.place(
            relx=0.5, rely=self.from_image_offset + 0.4, anchor=tk.CENTER)

        self.option_button = ctk.CTkButton(master=self.main_view_frame, command=self.open_options,
                                           hover=False, width=20, height=20, corner_radius=5, image=option_icon, fg_color="transparent", text='')

        # Place option icon on the top left corner
        self.option_button.place(relx=0.05, rely=self.from_image_offset + 0.4,
                                 anchor='c')

        self.main_view_frame.pack(fill="both", expand=True)

    def change_theme(self):
        current_appearance_mode = ctk.get_appearance_mode()
        print(current_appearance_mode)
        if current_appearance_mode == "Dark":
            ctk.set_appearance_mode("light")
        else:
            ctk.set_appearance_mode("dark")

    def open_options(self):
        self.config_frame = ctk.CTkToplevel(self)
        self.config_frame.geometry('400x320')
        self.config_frame.title("SpyGex - Settings")
        self.config_frame.resizable(False, False)
        self.config_frame.grab_set()
        self.init_options_view()

    def init_options_view(self):
        self.theme_button = ctk.CTkButton(master=self.config_frame, command=self.change_theme,
                                          hover=False, width=20, height=20, corner_radius=5, image=moon_icon, fg_color="transparent", text='')

        self.mode_label = ctk.CTkLabel(
            text="Toggle dark/light mode", master=self.config_frame, font=self.entry_font)

        self.mode_label.place(
            relx=0.10, rely=(0.07 * 500) / 320, anchor='w')

        # Place option icon on the top left corner
        self.theme_button.place(relx=0.9, rely=(0.07 * 500) / 320,
                                anchor='e')

        separator = ttk.Separator(self.config_frame, orient='horizontal')
        separator.place(relx=0.5, rely=(0.16 * 500) / 320,
                        anchor=tk.CENTER, relwidth=0.8)

        self.export_label = ctk.CTkLabel(
            text="Export format", master=self.config_frame, font=self.entry_font)

        self.export_label.place(
            relx=0.1, rely=(0.24 * 500) / 320, anchor='w')

        self.format_combo = ctk.CTkComboBox(
            master=self.config_frame, values=self.options['export_format'][1], width=125, height=40, font=self.combo_font, state="readonly", command=self.config_export_format)

        self.format_combo.place(
            relx=0.9, rely=(0.24 * 500) / 320, anchor='e')
        self.format_combo.set(self.options['export_format'][0])

        separator = ttk.Separator(self.config_frame, orient='horizontal')
        separator.place(relx=0.5, rely=(0.32 * 500) / 320,
                        anchor=tk.CENTER, relwidth=0.8)

        self.copy_label = ctk.CTkLabel(
            master=self.config_frame, text="Copy options", font=self.entry_font)

        self.copy_label.place(relx=0.1, rely=(0.40 * 500) / 320, anchor='w')

        self.match_check_var = tk.BooleanVar(
            value=self.options['copy_to_clipboard']['Match'])
        self.match_check = ctk.CTkCheckBox(
            master=self.config_frame, text="Match", onvalue=True, offvalue=False, font=self.entry_font, variable=self.match_check_var, command=self.update_copy_to_clipboard)
        self.match_check.place(
            relx=0.62, rely=(0.40 * 500) / 320, anchor='e')

        self.context_check_var = tk.BooleanVar(
            value=self.options['copy_to_clipboard']['Context'])

        self.context_check = ctk.CTkCheckBox(
            master=self.config_frame, text="Context", onvalue=True, offvalue=False, variable=self.context_check_var, command=self.update_copy_to_clipboard)
        self.context_check.place(
            relx=0.795, rely=(0.40 * 500) / 320, anchor='e')

        self.url_check_var = tk.BooleanVar(
            value=self.options['copy_to_clipboard']['URL'])
        self.url_check = ctk.CTkCheckBox(
            master=self.config_frame, text="URL", onvalue=True, offvalue=False, font=self.entry_font, variable=self.url_check_var, command=self.update_copy_to_clipboard)
        self.url_check.place(relx=1.0, rely=(0.40 * 500) / 320, anchor='e')

        separator = ttk.Separator(self.config_frame, orient='horizontal')
        separator.place(relx=0.5, rely=(0.48 * 500) / 320,
                        anchor=tk.CENTER, relwidth=0.8)

        self.delete_prev = ctk.CTkLabel(
            master=self.config_frame, text="Delete previous entries", font=self.entry_font)
        self.delete_prev.place(
            relx=0.1, rely=(0.56 * 500) / 320, anchor='w')

        self.radio_bool = tk.BooleanVar(
            value=self.options['Delete_Previous_Entries'])

        ctk.CTkRadioButton(master=self.config_frame, text="Yes", value=True,
                           font=self.entry_font, command=self.update_delete_entries, variable=self.radio_bool).place(relx=0.85, rely=(0.56 * 500) / 320, anchor='e')

        ctk.CTkRadioButton(master=self.config_frame, text="No", value=False,
                           font=self.entry_font, command=self.update_delete_entries, variable=self.radio_bool).place(relx=1.03, rely=(0.56 * 500) / 320, anchor='e')

    def update_delete_entries(self, event=None):
        self.options['Delete_Previous_Entries'] = self.radio_bool.get()
        print(self.options['Delete_Previous_Entries'])

    def update_copy_to_clipboard(self, event=None):
        self.options['copy_to_clipboard']['Match'] = self.match_check_var.get()
        self.options['copy_to_clipboard']['Context'] = self.context_check_var.get()
        self.options['copy_to_clipboard']['URL'] = self.url_check_var.get()

        if not self.options['copy_to_clipboard']['Match'] and not self.options['copy_to_clipboard']['Context'] and not self.options['copy_to_clipboard']['URL']:
            self.match_check_var.set(True)
            self.options['copy_to_clipboard']['Match'] = True
        print(self.options['copy_to_clipboard'])

    def config_export_format(self, event=None):
        self.options['export_format'][0] = self.format_combo.get()
        print(self.options['export_format'][0])

    def init_detail_view(self):
        # Initialize the detail view frame
        self.detail_view_frame = ctk.CTkFrame(self)

        self.info_frame = ctk.CTkFrame(
            self.detail_view_frame, bg_color='transparent', fg_color="transparent")
        self.info_frame.place(relx=0.5, rely=0.02,
                              anchor='n', relwidth=0.98, relheight=0.15,)

        # Configure the scrollable frame
        self.scrollable_frame = ctk.CTkScrollableFrame(self.detail_view_frame)
        self.scrollable_frame.place(
            relwidth=0.98, relheight=0.61, anchor='n', relx=0.5, rely=0.26)

        # Frame for buttons
        button_frame = ctk.CTkFrame(
            self.detail_view_frame, bg_color='transparent', fg_color="transparent")
        button_frame.place(relx=0.5, rely=0.97, anchor='s',
                           relwidth=0.98, relheight=0.1)

        # "New Search" button
        new_search_button = ctk.CTkButton(
            button_frame, text="New scrap", command=self.new_search, font=self.entry_font)
        new_search_button.place(anchor='e', relx=0.97,
                                rely=0.6, relwidth=0.1, relheight=0.7)

        # "Export" button
        export_button = ctk.CTkButton(
            button_frame, text="Export", command=self.export_file, font=self.entry_font)
        export_button.place(anchor='e', relx=0.85, rely=0.6,
                            relwidth=0.1, relheight=0.7)

    # Update scrollable frame with search results

    def update_scrollable_frame(self, df, url, regex_to_use):
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
            ctk.CTkButton(row_frame, 20, 20, text="", image=copy_icon, fg_color="transparent", command=lambda row=row: self.copy_to_clipboard(
                row)).place(
                anchor='c', relx=0.95, rely=0.5)
        self.scrollable_frame.update_idletasks()

    def start_search(self):
        # Function to start the search process
        url = self.url_entry.get()
        regex_to_use = self.regex_entry.get()

        # Validate URL and regex input
        if not url.strip() or not regex_to_use.strip():
            messagebox.showerror(
                "Missing patterns", "Please enter a valid URL and a REGEX pattern.")
            return

        # In order to avoid blocking the main thread, we start a new thread
        # so the UI remains responsive

            # Create a progress bar
        self.progress_bar = ctk.CTkProgressBar(
            self.main_view_frame, width=500, height=5, mode='indeterminate', indeterminate_speed=1)

        self.progress_bar.place(
            relx=0.5, rely=0.5 + 0.30, anchor=tk.CENTER)
        # Start the progress bar
        self.progress_bar.start()

        new_thread = Thread(target=self.controller.start_search,
                            args=(url, regex_to_use), daemon=True)

        new_thread.start()

    def callback_regex_combo(self, event=None):
        # Callback for regex combo box selection
        selected_regex = self.regex_combo.get().strip(' ')
        regex_dict = self.controller.get_regex_patterns()
        # Update regex entry based on selection
        if selected_regex in regex_dict:
            self.regex_entry.delete(0, 'end')
            self.regex_entry.insert(0, regex_dict[selected_regex])
        elif (selected_regex == "Custom REGEX") and isinstance(event, str):
            self.regex_entry.delete(0, 'end')

    def show_main_view(self):
        # Switch to the main view
        self.detail_view_frame.pack_forget()

        self.main_view_frame.pack(fill="both", expand=True)

    def show_detail_view(self):
        # Switch to the detail view
        self.main_view_frame.pack_forget()
        self.detail_view_frame.pack(fill="both", expand=True)

    def run(self):
        # Setup the main view layout and start the application
        self.setup_main_view_layout()
        self.mainloop()

    def copy_to_clipboard(self, row):
        # Copy the selected row to clipboard based on user preferences
        text_to_copy = ''

        if self.options['copy_to_clipboard']['Match']:
            text_to_copy += 'Match:\n' + row['Match'] + '\n'

        if self.options['copy_to_clipboard']['Context']:
            text_to_copy += 'Context:\n' + str(row['Line']) + '\n'

        if self.options['copy_to_clipboard']['URL']:
            text_to_copy += 'URL:\n' + row['Url']

        # Copy URL to clipboard
        pyperclip.copy(text_to_copy)
        messagebox.showinfo("Information", "Sucessfully copied to clipboard.")

    def new_search(self):
        # Reset input fields and start a new search
        if self.options['Delete_Previous_Entries']:
            self.url_entry.delete(0, 'end')
            self.regex_entry.delete(0, 'end')
            self.regex_combo.set(self.regex_options[-1])

        # Destroy the progress bar if it exists
        self.progress_bar.destroy()

        # Clear displayed data in the detail view frame
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()

        for widget in self.info_frame.winfo_children():
            widget.destroy()

        # Reset the model for a new search
        self.controller.reset_model()

        # Logic to return to the main view and start a new bg_color
        self.show_main_view()

    def export_file(self):
        # Export data to a CSV file

        if self.options['export_format'][0] == 'csv':

            file_path = filedialog.asksaveasfilename(defaultextension='.csv',
                                                     filetypes=[
                                                         ("CSV files", '*.csv')],
                                                     title="Save As")

        elif self.options['export_format'][0] == 'json':

            file_path = filedialog.asksaveasfilename(defaultextension='.json',
                                                     filetypes=[
                                                         ("JSON files", '*.json')],
                                                     title="Save As")

        elif self.options['export_format'][0] == 'xlsx':

            file_path = filedialog.asksaveasfilename(defaultextension='.xlsx',
                                                     filetypes=[
                                                         ("Excel files", '*.xlsx')],
                                                     title="Save As")

        if file_path:  # type: ignore
            self.controller.export_file(file_path)
