import customtkinter as ctk

class DigitSpinbox(ctk.CTkFrame):
    def __init__(self, *args, width=100, height=32, step_size=1, command=None, **kwargs):
        super().__init__(*args, width=width, height=height, **kwargs)

        self.step_size = step_size
        self.command = command

        self.configure(fg_color=("gray78", "gray28"))

        self.grid_columnconfigure((0, 2), weight=0)
        self.grid_columnconfigure(1, weight=1)

        self.subtract_button = ctk.CTkButton(self, text="-", width=height-6, height=height-6,
                                             command=self.subtract_button_callback)
        self.subtract_button.grid(row=0, column=0, padx=(3, 0), pady=3)

        self.label = ctk.CTkLabel(self, width=width-(2*height), height=height-6, anchor="center")
        self.label.grid(row=0, column=1, padx=3, pady=3, sticky="ew")
        self.set(1)

        self.add_button = ctk.CTkButton(self, text="+", width=height-6, height=height-6,
                                        command=self.add_button_callback)
        self.add_button.grid(row=0, column=2, padx=(0, 3), pady=3)

    def add_button_callback(self):
        try:
            current_value = int(self.label.cget("text"))
            new_value = current_value + self.step_size
            self.set(new_value)
        except ValueError:
            return
        
        if self.command is not None:
            self.command()

    def subtract_button_callback(self):
        try:
            current_value = int(self.label.cget("text"))
            new_value = max(current_value - self.step_size, 1)
            self.set(new_value)
        except ValueError:
            return
        
        if self.command is not None:
            self.command()

    def get(self) -> int:
        try:
            return max(int(self.label.cget("text")), 1)  
        except ValueError:
            return 1  

    def set(self, value: int):
        self.label.configure(text=str(max(int(value), 1)))  
