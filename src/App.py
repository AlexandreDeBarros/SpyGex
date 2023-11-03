import tkinter as tk
from tkinter import ttk
from model import SpyGexModel
from controller import SpyGexController
from view import SpyGexView

class App(tk.Tk):
    def __init__(self):
        super().__init__()

        model = SpyGexModel.SpyGexModel()
        view = SpyGexView.SpyGexView()

        # create a controller
        controller = SpyGexController.SpyGexController(model, view)
        controller.research()


if __name__ == '__main__':
    app = App()
    app.mainloop()