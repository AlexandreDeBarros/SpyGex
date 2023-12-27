import os
import tkinter as tk
from tkinter import filedialog
import customtkinter as ctk
from tkinter import messagebox
import pyperclip
from PIL import Image, ImageTk, ImageDraw

# Set the default color theme and appearance mode
ctk.set_default_color_theme("blue")
ctk.set_appearance_mode("dark")

class SpyGexView(ctk.CTk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Set the geometry and properties of the main window
        self.geometry("930x550+130+100")
        self.resizable(False, False)
        self.title("SpyGex - Scrapper")

        self.controller = None

        # Initialize the main view and detail view
        self.init_main_view()
        self.init_detail_view()

        # Show the main view by default
        self.show_main_view()
    
    def controller(self, controller):
        # Assign a controller to the view
        self.controller = controller

    def init_main_view(self):
        # Initialize the main view frame
        self.main_view_frame = ctk.CTkFrame(self)

    def setup_main_view_layout(self):
        # Configure the logo
        # Update the path with the actual location
        # logo_path = os.path.join(os.path.dirname(__file__), '..\\..\\resources\\logo.jpg')
        # logo_img = Image.open(logo_path)
        # logo_img = logo_img.resize((250, 250), Image.LANCZOS)
        # mask = Image.new("L", (250, 250), 0)
        # draw = ImageDraw.Draw(mask)
        # draw.ellipse((0, 0, 250, 250), fill=255)
        # logo_pil_img = Image.open(logo_path)
        # logo_pil_img = logo_pil_img.resize((250, 250), Image.LANCZOS)
        # circular_img = Image.new("RGBA", (250, 250))
        # circular_img.paste(logo_pil_img, mask=mask)
        # circular_photo = ImageTk.PhotoImage(logo_img)
        # label = ctk.CTkLabel(self, image=circular_photo, fg_color="transparent", text="")
        # label.place(relx=0.5, rely=0.25, anchor=ctk.CENTER)

        # URL entry field
        self.url_entry = ctk.CTkEntry(self.main_view_frame, placeholder_text="Enter the URL to scrap", width=300, height=40)
        self.url_entry.place(relx=0.5, rely=0.3, anchor=tk.CENTER)

        # Entry field for custom regex
        self.regex_entry = ctk.CTkEntry(self.main_view_frame, placeholder_text="Enter Custom REGEX", width=300, height=40)
        self.regex_entry.place(relx=0.5, rely=0.45, anchor=tk.CENTER)

        # ComboBox for REGEX selection
        regex_options = list(self.controller.get_regex_patterns().keys()) + ["Custom REGEX"]
        self.regex_combo = ctk.CTkComboBox(self.main_view_frame, values=regex_options, width=300, height=40, command=self.callback_regex_combo)
        self.regex_combo.place(relx=0.5, rely=0.6, anchor=tk.CENTER)
        self.regex_combo.set("Custom REGEX")

        # Search button
        self.search_button = ctk.CTkButton(self.main_view_frame, text="Scrap", command=self.start_search)
        self.search_button.place(relx=0.5, rely=0.75, anchor=tk.CENTER)

        self.main_view_frame.pack(fill="both", expand=True)

    def init_detail_view(self):
        # Initialize the detail view frame
        self.detail_view_frame = ctk.CTkFrame(self)
        
        # Configure the scrollable frame 
        self.scrollable_frame = ctk.CTkScrollableFrame(self.detail_view_frame)
        self.scrollable_frame.pack(padx=10, pady=10, fill="both", expand=True)

        # Frame for buttons
        button_frame = ctk.CTkFrame(self.detail_view_frame)
        button_frame.pack(padx=10, pady=10, fill="x")

        # "New Search" button
        new_search_button = ctk.CTkButton(button_frame, text="New Search", command=self.new_search)
        new_search_button.pack(side="left", padx=10, fill="x", expand=True)

        # "Export" button
        export_button = ctk.CTkButton(button_frame, text="Export", command=self.export_csv)
        export_button.pack(side="left", padx=10, fill="x", expand=True)

    # Update scrollable frame with search results
    def update_scrollable_frame(self, df, url, regex_to_use):

        # Create frame and labels for domain name and regex
        info_frame = ctk.CTkFrame(self)
        info_frame.pack(fill='x', padx=10, pady=5)
        ctk.CTkLabel(info_frame, text=f"Domain Name : {url}").pack(side='left', padx=5)
        ctk.CTkLabel(info_frame, text=f"Regex : {regex_to_use}").pack(side='left', padx=5)

        # Create and add column headers
        header_frame = ctk.CTkFrame(self.scrollable_frame)
        header_frame.pack(fill='x', padx=10, pady=2)
        ctk.CTkLabel(header_frame, text="Match").pack(side='left', fill='x', expand=True)
        ctk.CTkLabel(header_frame, text="Line").pack(side='left', fill='x', expand=True)
        ctk.CTkLabel(header_frame, text="URL").pack(side='left', fill='x', expand=True)

        # Add new data
        for index, row in df.iterrows():
            row_frame = ctk.CTkFrame(self.scrollable_frame)
            row_frame.pack(fill='x', padx=10, pady=2)
            ctk.CTkLabel(row_frame, text=row['Match']).pack(side='left', fill='x', expand=True)
            ctk.CTkLabel(row_frame, text=str(row['Line'])).pack(side='left', fill='x', expand=True)
            ctk.CTkLabel(row_frame, text=row['Url']).pack(side='left', fill='x', expand=True)
            ctk.CTkButton(row_frame, text='Copy', command=lambda url=row['Url']: self.copy_to_clipboard(url)).pack(side='left', padx=10)
        self.scrollable_frame.update_idletasks()
    
    def start_search(self):
        # Function to start the search process
        url = self.url_entry.get()
        regex_to_use = self.regex_entry.get()
        
        # Validate URL and regex input
        if not url.strip() or not regex_to_use.strip():
            messagebox.showerror("Error", "Please enter a URL and a regex pattern.")
            return

        # Start the search with provided URL and regex
        self.controller.start_search(url, regex_to_use)

    def callback_regex_combo(self, event=None):
        # Callback for regex combo box selection
        selected_regex = self.regex_combo.get()
        regex_dict = self.controller.get_regex_patterns()
        # Update regex entry based on selection
        if selected_regex in regex_dict:
            self.regex_entry.delete(0, 'end')
            self.regex_entry.insert(0, regex_dict[selected_regex])
        elif selected_regex == "Custom REGEX":
            self.regex_entry.delete(0, 'end')
        else:
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

    def copy_to_clipboard(self, url):
        # Copy URL to clipboard
        pyperclip.copy(url)
        messagebox.showinfo("Info", "URL copied to clipboard!")

    def new_search(self):
        # Reset input fields and start a new search
        self.url_entry.delete(0, 'end')
        self.regex_entry.delete(0, 'end')
        self.regex_combo.set("Custom REGEX")

        # Clear displayed data in the scrollable frame
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()

        # Clear displayed data in the detail view frame
        for widget in self.detail_view_frame.winfo_children():
            widget.destroy()
        
        # Reset the model for a new search
        self.controller.reset_model()

        # Logic to return to the main view and start a new search
        self.show_main_view()

    def export_csv(self):
        # Export data to a CSV file

        file_path = filedialog.asksaveasfilename(defaultextension='.csv',
                                                 filetypes=[("CSV files", '*.csv')],
                                                 title="Save As")
        if file_path:
            self.controller.export_csv(file_path)
