from model import spygex_model as sm
from controller import spygex_controller as sc
from view import spygex_view as sv

class App():
    def __init__(self):
        super().__init__()

        # Create the model
        model = sm.SpyGexModel()

        # Create the view
        view = sv.SpyGexView()

        # Create the controller
        controller = sc.SpyGexController(model, view)

        # Assign the controller to the view
        view.controller = controller

        # Start the user interface
        view.run()

# Entry point of the application
if __name__ == '__main__':
    app = App()
