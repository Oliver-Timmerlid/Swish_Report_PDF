"""
Footer component with action buttons.

UI component only - no business logic.
"""

import logging
from typing import Optional, Callable
import customtkinter as ctk
from tkinter import filedialog
from ui.theme import ACCENT_ACTION, ACCENT_ACTION_HOVER, ACCENT_PRIMARY, ACCENT_PRIMARY_HOVER


logger = logging.getLogger(__name__)


class FooterComponent(ctk.CTkFrame):
    """Bottom action bar with load and generate buttons."""
    
    def __init__(self, parent):
        """
        Initialize the footer component.
        
        Parameters:
            parent: Parent widget.
        """
        super().__init__(parent, fg_color="transparent", height=80)
        self.pack_propagate(False)
        
        # Callbacks
        self.on_file_selected: Optional[Callable[[str], None]] = None
        self.on_generate_pdf: Optional[Callable[[], None]] = None
        
        self._build_ui()
    
    def _build_ui(self) -> None:
        """Build footer UI."""
        action_content = ctk.CTkFrame(self, fg_color="transparent")
        action_content.pack(expand=True)
        
        button_container = ctk.CTkFrame(action_content, fg_color="transparent")
        button_container.pack(pady=(0, 20))
        
        self.load_file_button = ctk.CTkButton(
            button_container,
            text="Ladda fil",
            command=self._on_load_click,
            width=160,
            height=42,
            font=ctk.CTkFont(size=14, weight="bold"),
            fg_color=ACCENT_ACTION,
            hover_color=ACCENT_ACTION_HOVER,
            corner_radius=6
        )
        self.load_file_button.pack(side='left', padx=8)
        
        self.pdf_button = ctk.CTkButton(
            button_container,
            text="Skapa PDF",
            command=lambda: self.on_generate_pdf() if self.on_generate_pdf else None,
            state='disabled',
            width=160,
            height=42,
            font=ctk.CTkFont(size=14, weight="bold"),
            fg_color=ACCENT_PRIMARY,
            hover_color=ACCENT_PRIMARY_HOVER,
            corner_radius=6
        )
        self.pdf_button.pack(side='left', padx=8)
    
    def _on_load_click(self) -> None:
        """Handle load file button click."""
        file_path = filedialog.askopenfilename(
            title="Välj CSV-fil",
            filetypes=[("CSV filer", "*.csv"), ("Alla filer", "*.*")]
        )
        
        if file_path and self.on_file_selected:
            self.on_file_selected(file_path)
    
    def enable_pdf_button(self) -> None:
        """Enable the PDF generation button."""
        self.pdf_button.configure(state='normal')
    
    def disable_pdf_button(self) -> None:
        """Disable the PDF generation button."""
        self.pdf_button.configure(state='disabled')
