"""
Main controller for the application.

Coordinates UI events with service layer operations.
Handles user interactions without implementing business logic.
"""

import logging
import os
from typing import Optional
from datetime import datetime
from tkinter import filedialog
from models.swish_data import SwishReport
from services.csv_parser import CSVParserService
from services.validator import ValidationService
from services.pdf_generator import PDFGeneratorService
from storage.file_handler import FileHandler
from ui.main_window import MainWindow


logger = logging.getLogger(__name__)


class MainController:
    """
    Main application controller.
    
    Coordinates between UI and service layer.
    Translates user actions into service calls.
    """
    
    def __init__(self, main_window: MainWindow):
        """
        Initialize the controller.
        
        Parameters:
            main_window (MainWindow): The main application window.
        """
        self.main_window = main_window
        
        # Initialize services
        self.csv_parser = CSVParserService()
        self.validator = ValidationService()
        self.pdf_generator = PDFGeneratorService()
        self.file_handler = FileHandler()
        
        # State
        self.current_file_path: Optional[str] = None
        self.current_report: Optional[SwishReport] = None
        self.pdf_settings = {
            'page_size': 'A4',
            'orientation': 'Portrait',
            'font_size': 7
        }
        
        # Connect callbacks
        self._setup_callbacks()
        
        logger.info("Controller initialized")
    
    def _setup_callbacks(self) -> None:
        """Connect UI callbacks to controller methods."""
        self.main_window.on_file_selected = self.handle_file_selected
        self.main_window.on_generate_pdf = self.handle_generate_pdf
        self.main_window.on_settings_changed = self.handle_settings_changed
        
        # Set initial settings
        self.main_window.set_settings(self.pdf_settings)
    
    def handle_file_selected(self, file_path: str) -> None:
        """
        Handle file selection.
        
        Parameters:
            file_path (str): Path to the selected file.
        """
        logger.info(f"File selected: {file_path}")
        self._load_file(file_path)
    
    def _load_file(self, file_path: str) -> None:
        """
        Load and validate CSV file.
        
        Parameters:
            file_path (str): Path to the file to load.
        """
        # Validate file path
        is_valid, error_message = self.validator.validate_file_path(file_path)
        if not is_valid:
            self.main_window.show_error("Ogiltig fil", error_message)
            return
        
        # Validate file content
        is_valid, error_message = self.validator.validate_file_content(file_path)
        if not is_valid:
            self.main_window.show_error("Ogiltigt filinnehåll", error_message)
            return
        
        # Parse file
        try:
            self.current_report = self.csv_parser.parse_file(file_path)
            self.current_file_path = file_path
            
            # Update preview
            self.main_window.show_preview(self.current_report)
            
            filename = os.path.basename(file_path)
            logger.info(f"File successfully loaded: {filename}")
            
        except Exception as e:
            logger.error(f"Error parsing file: {str(e)}")
            self.main_window.show_error(
                "Fel vid inläsning",
                f"Kunde inte läsa CSV-filen:\n{str(e)}"
            )
            self.main_window.show_empty_state()
            self.current_report = None
            self.current_file_path = None
    
    def handle_generate_pdf(self) -> None:
        """Generate PDF from current report."""
        if not self.current_report:
            self.main_window.show_error(
                "Ingen fil",
                "Vänligen ladda en CSV-fil först"
            )
            return
        
        # Generate default filename using date from report SÖK field
        report_date = None
        try:
            # Extract date from search_date_range (SÖK field)
            if self.current_report.metadata.search_date_range:
                # Split by comma first to get just the date range part
                date_range_part = self.current_report.metadata.search_date_range.split(',')[0].strip()
                # Take the first date (before the dash)
                if ' - ' in date_range_part:
                    start_date_str = date_range_part.split(' - ')[0].strip()
                    # Parse the datetime and extract just the date part
                    # Format: "2025-06-12 00:00:00"
                    date_only = start_date_str.split()[0]
                    report_date = datetime.strptime(date_only, '%Y-%m-%d')
        except (ValueError, IndexError, AttributeError) as e:
            # If parsing fails, log and use None (will default to today)
            logger.warning(f"Could not parse date from SÖK field: {e}")
            pass
        
        default_filename = self.file_handler.generate_filename(
            'Swish',
            '.pdf',
            report_date
        )
        
        # Ask user where to save
        output_path = filedialog.asksaveasfilename(
            defaultextension=".pdf",
            initialfile=default_filename,
            filetypes=[("PDF filer", "*.pdf"), ("Alla filer", "*.*")],
            title="Spara PDF som"
        )
        
        if not output_path:
            logger.info("PDF save cancelled by user")
            # Restore focus to main window
            self.main_window.root.focus_force()
            return
        
        try:
            # Configure PDF generator with current settings
            self.pdf_generator.set_page_format(
                self.pdf_settings['page_size'],
                self.pdf_settings['orientation']
            )
            self.pdf_generator.set_font_size(self.pdf_settings['font_size'])
            
            # Generate PDF
            self.pdf_generator.generate_pdf(
                self.current_report,
                output_path
            )
            
            logger.info(f"PDF generated successfully: {output_path}")
            
            # Restore focus before showing success
            self.main_window.root.focus_force()
            self.main_window.show_success(
                "PDF skapad",
                f"PDF-filen har sparats:\n{output_path}"
            )
            
        except Exception as e:
            logger.error(f"Error generating PDF: {str(e)}")
            self.main_window.root.focus_force()
            self.main_window.show_error(
                "Fel vid PDF-skapande",
                f"Kunde inte skapa PDF:\n{str(e)}"
            )
    
    def handle_settings_changed(self, settings: dict) -> None:
        """
        Handle settings change from sidebar.
        
        Parameters:
            settings (dict): Updated settings dictionary.
        """
        self.pdf_settings = settings
        logger.info(f"Settings updated: {self.pdf_settings}")
