# MVC modules
from model import spygex_model as sm
from controller import spygex_controller as sc
from view import spygex_view as sv

class App():
    """
    Main application class that sets up the Model-View-Controller architecture.

    This class initializes the model, view, and controller, and starts the user interface.
    """

    def __init__(self):
        """Initialize the application by setting up the MVC components."""
        
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
    """
    The entry point of the application.

    When the script is run directly, it creates an instance of the App class,
    which in turn initializes and runs the application.
    """
