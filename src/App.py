import tkinter as tk
from tkinter import ttk
from model import SpyGexModel
from controller import SpyGexController
from view import SpyGexView

class App(tk.Tk):
    def __init__(self):
        super().__init__()

        # create the model
        model = SpyGexModel.SpyGexModel()

        # create the view
        view = SpyGexView.SpyGexView()
        
        # simulation
        model.regex = "(?:(?:31(\/|-|\.)(?:0?[13578]|1[02]))\1|(?:(?:29|30)(\/|-|\.)(?:0?[13-9]|1[0-2])\2))(?:(?:1[6-9]|[2-9]\d)?\d{2})$|^(?:29(\/|-|\.)0?2\3(?:(?:(?:1[6-9]|[2-9]\d)?(?:0[48]|[2468][048]|[13579][26])|(?:(?:16|[2468][048]|[3579][26])00))))$|^(?:0?[1-9]|1\d|2[0-8])(\/|-|\.)(?:(?:0?[1-9])|(?:1[0-2]))\4(?:(?:1[6-9]|[2-9]\d)?\d{2})|(?:(?:1[6-9]|[2-9]\d)?\d{2})(\/|-|\.)(?:0?[13578]|1[02])(\/|-|\.)31|(?:0?[13-9]|1[0-2])(\/|-|\.)(29|30)$|^(?:(?:(?:1[6-9]|[2-9]\d)?(?:0[48]|[2468][048]|[13579][26])|(?:(?:16|[2468][048]|[3579][26])00)))(\/|-|\.)0?2(\/|-|\.)29$|^(?:(?:1[6-9]|[2-9]\d)?\d{2})(\/|-|\.)(?:(?:0?[1-9])|(?:1[0-2]))(\/|-|\.)(?:0?[1-9]|1\d|2[0-8])$"
        model.url = "https://realpython.github.io/fake-jobs/"

        # create a controller
        controller = SpyGexController.SpyGexController(model, view)
        controller.research()


if __name__ == '__main__':
    app = App()
    app.mainloop()