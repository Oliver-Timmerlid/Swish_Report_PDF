"""
Header component with application title.

UI component only - no business logic.
"""

import customtkinter as ctk


class HeaderComponent(ctk.CTkFrame):
    """Top header bar with application title."""
    
    def __init__(self, parent):
        """
        Initialize the header component.
        
        Parameters:
            parent: Parent widget.
        """
        super().__init__(parent, fg_color="transparent", height=60)
        self.pack_propagate(False)
        
        self._build_ui()
    
    def _build_ui(self) -> None:
        """Build header UI."""
        title = ctk.CTkLabel(
            self,
            text="Swish CSV till PDF",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color="#60a5fa"
        )
        title.pack(side='left', padx=20, pady=15)
