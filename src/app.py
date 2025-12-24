import sys
import logging
import customtkinter as ctk
from tkinterdnd2 import TkinterDnD

# Import core configuration
from core.config import Config
from core.logging_config import setup_logging

# Import UI and controller
from ui.main_window import MainWindow
from controllers.main_controller import MainController


def main() -> int:
    """
    Main application entry point.
    
    Initializes logging, creates UI, and starts the application.
    
    Returns:
        int: Exit code (0 for success, 1 for error).
    """
    try:
        # Setup logging first (no print statements allowed per PRD)
        setup_logging()
        logger = logging.getLogger(__name__)
        logger.info("Application starting")
        
        # Configure CustomTkinter appearance
        ctk.set_appearance_mode(Config.APPEARANCE_MODE)
        # Note: Not using set_default_color_theme() - we use custom theme from ui.theme
        
        # Create root window with drag-and-drop support
        root = TkinterDnD.Tk()
        
        # Create main window
        main_window = MainWindow(root)
        
        # Create controller to coordinate UI and services
        controller = MainController(main_window)
        
        logger.info("Application initialized successfully")
        
        # Start main loop
        main_window.run()
        
        logger.info("Application shutting down normally")
        return 0
        
    except Exception as e:
        # Log any startup errors
        if 'logger' in locals():
            logger.critical(f"Fatal error during startup: {str(e)}", exc_info=True)
        else:
            # Fallback if logging not yet configured
            print(f"FATAL ERROR: {str(e)}")
        
        return 1


if __name__ == "__main__":
    sys.exit(main())