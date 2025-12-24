"""
Main application window.

Composes UI components and handles window-level functionality.
UI only - no business logic.
"""

import logging
from typing import Optional, Callable
import customtkinter as ctk
from tkinterdnd2 import TkinterDnD
from tkinter import messagebox
from core.config import Config
from ui.theme import BG_APP
from ui.components.header_component import HeaderComponent
from ui.components.preview_component import PreviewComponent
from ui.components.settings_component import SettingsComponent
from ui.components.footer_component import FooterComponent


logger = logging.getLogger(__name__)


class MainWindow:
    """
    Main application window that composes UI components.
    
    Handles window setup, drag-and-drop, and component coordination.
    """
    
    def __init__(self, root: TkinterDnD.Tk):
        """
        Initialize the main window.
        
        Parameters:
            root (TkinterDnD.Tk): Root window with DnD support.
        """
        self.root = root
        self.root.title(Config.APP_NAME)
        self.root.geometry(f"{Config.WINDOW_WIDTH}x{Config.WINDOW_HEIGHT}")
        self.root.minsize(Config.WINDOW_MIN_WIDTH, Config.WINDOW_MIN_HEIGHT)
        self.root.resizable(True, True)
        self.root.configure(bg=BG_APP)
        
        # Callbacks
        self.on_file_selected: Optional[Callable[[str], None]] = None
        self.on_generate_pdf: Optional[Callable[[], None]] = None
        self.on_settings_changed: Optional[Callable[[dict], None]] = None
        
        # Components
        self.header: Optional[HeaderComponent] = None
        self.preview: Optional[PreviewComponent] = None
        self.settings: Optional[SettingsComponent] = None
        self.footer: Optional[FooterComponent] = None
        
        self._setup_drag_and_drop()
        self._build_ui()
    
    def _setup_drag_and_drop(self) -> None:
        """Setup drag and drop functionality for entire window."""
        try:
            self.root.drop_target_register('DND_Files')
            self.root.dnd_bind('<<Drop>>', self._on_drop)
            logger.debug("Drag and drop configured")
        except Exception as e:
            logger.warning(f"Could not setup drag and drop: {e}")
    
    def _on_drop(self, event) -> None:
        """Handle file drop event."""
        try:
            file_path = event.data.strip('{}')
            logger.debug(f"File dropped: {file_path}")
            if self.on_file_selected:
                self.on_file_selected(file_path)
        except Exception as e:
            logger.error(f"Error handling drop: {e}")
    
    def _build_ui(self) -> None:
        """Compose UI from components."""
        # Main container
        container = ctk.CTkFrame(self.root, fg_color=BG_APP)
        container.pack(fill='both', expand=True)
        
        # Header
        self.header = HeaderComponent(container)
        self.header.pack(fill='x', padx=0, pady=0)
        
        # Main content area (two columns)
        content = ctk.CTkFrame(container, fg_color="transparent")
        content.pack(fill='both', expand=True, padx=15, pady=10)
        
        # Left column: Preview
        self.preview = PreviewComponent(content)
        self.preview.pack(side='left', fill='both', expand=True, padx=(5, 10))
        
        # Right column: Settings sidebar
        self.settings = SettingsComponent(content)
        self.settings.pack(side='right', fill='y', padx=(0, 5))
        
        # Footer with action buttons
        self.footer = FooterComponent(container)
        self.footer.pack(fill='x', padx=0, pady=0)
        
        # Connect component callbacks
        self._connect_callbacks()
    
    def _connect_callbacks(self) -> None:
        """Connect component callbacks to main window handlers."""
        # Footer callbacks
        self.footer.on_file_selected = lambda path: (
            self.on_file_selected(path) if self.on_file_selected else None
        )
        self.footer.on_generate_pdf = lambda: (
            self.on_generate_pdf() if self.on_generate_pdf else None
        )
        
        # Settings callback
        self.settings.on_settings_changed = lambda settings: (
            self.on_settings_changed(settings) if self.on_settings_changed else None
        )
    
    def set_settings(self, settings: dict) -> None:
        """
        Update settings controls with values.
        
        Parameters:
            settings (dict): Settings dictionary.
        """
        self.settings.set_settings(settings)
    
    def show_preview(self, report) -> None:
        """
        Display report preview.
        
        Parameters:
            report: SwishReport instance to preview.
        """
        self.preview.show_preview(report)
        self.footer.enable_pdf_button()
    
    def show_empty_state(self) -> None:
        """Show empty state in preview."""
        self.preview.show_empty_state()
        self.footer.disable_pdf_button()
    
    def show_error(self, title: str, message: str) -> None:
        """Show error message dialog."""
        messagebox.showerror(title, message)
        logger.error(f"{title}: {message}")
    
    def show_success(self, title: str, message: str) -> None:
        """Show success message dialog."""
        messagebox.showinfo(title, message)
        logger.info(f"{title}: {message}")
    
    def run(self) -> None:
        """Start the application main loop."""
        self.root.mainloop()
