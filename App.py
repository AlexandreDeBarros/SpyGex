import tkinter as tk
from tkinter import ttk

class App(tk.Tk):
    def __init__(self):
        super().__init__()

        # create a model
        model = SpyGexModel()

        # create a controller
        controller = SpyGexController(model, view)


if __name__ == '__main__':
    app = App()
    app.mainloop()