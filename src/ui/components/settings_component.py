"""
Settings sidebar component.

UI component only - no business logic.
"""

import logging
from typing import Optional, Callable
import customtkinter as ctk
from ui.theme import (
    BG_PANEL, BG_INPUT, TEXT_PRIMARY, TEXT_SECONDARY,
    ACCENT_PRIMARY, ACCENT_PRIMARY_HOVER
)


logger = logging.getLogger(__name__)


class SettingsComponent(ctk.CTkFrame):
    """Settings sidebar with PDF configuration options."""
    
    def __init__(self, parent):
        """
        Initialize the settings component.
        
        Parameters:
            parent: Parent widget.
        """
        super().__init__(parent, fg_color=BG_PANEL, corner_radius=12, width=280)
        self.pack_propagate(False)
        
        # Callback
        self.on_settings_changed: Optional[Callable[[dict], None]] = None
        
        self._build_ui()
    
    def _build_ui(self) -> None:
        """Build settings UI."""
        settings_title = ctk.CTkLabel(
            self,
            text="Inställningar",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color=TEXT_PRIMARY
        )
        settings_title.pack(pady=(20, 15), padx=15)
        
        # Page Size
        page_size_label = ctk.CTkLabel(
            self,
            text="Sidformat:",
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color=TEXT_SECONDARY,
            anchor='w'
        )
        page_size_label.pack(pady=(10, 5), padx=15, anchor='w')
        
        self.page_size_var = ctk.StringVar(value="A4")
        self.page_size_menu = ctk.CTkOptionMenu(
            self,
            variable=self.page_size_var,
            values=["A4", "Letter"],
            command=self._on_settings_change,
            width=250,
            fg_color=BG_INPUT,
            button_color="#374151",
            button_hover_color="#4b5563"
        )
        self.page_size_menu.pack(pady=(0, 15), padx=15)
        
        # Section separator
        ctk.CTkFrame(self, height=1, fg_color="#1e293b").pack(fill="x", padx=15, pady=10)
        
        # Orientation
        orientation_label = ctk.CTkLabel(
            self,
            text="Orientering:",
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color=TEXT_SECONDARY,
            anchor='w'
        )
        orientation_label.pack(pady=(10, 5), padx=15, anchor='w')
        
        self.orientation_var = ctk.StringVar(value="Portrait")
        self.orientation_menu = ctk.CTkOptionMenu(
            self,
            variable=self.orientation_var,
            values=["Portrait", "Landscape"],
            command=self._on_settings_change,
            width=250,
            fg_color=BG_INPUT,
            button_color="#374151",
            button_hover_color="#4b5563"
        )
        self.orientation_menu.pack(pady=(0, 15), padx=15)
        
        # Section separator
        ctk.CTkFrame(self, height=1, fg_color="#1e293b").pack(fill="x", padx=15, pady=10)
        
        # Font Size
        font_size_label = ctk.CTkLabel(
            self,
            text="Textstorlek:",
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color=TEXT_SECONDARY,
            anchor='w'
        )
        font_size_label.pack(pady=(10, 5), padx=15, anchor='w')
        
        self.font_size_var = ctk.IntVar(value=7)
        self.font_size_slider = ctk.CTkSlider(
            self,
            from_=6,
            to=12,
            number_of_steps=6,
            variable=self.font_size_var,
            command=self._on_font_size_change,
            width=250,
            fg_color=BG_INPUT,
            progress_color=ACCENT_PRIMARY,
            button_color=ACCENT_PRIMARY,
            button_hover_color=ACCENT_PRIMARY_HOVER
        )
        self.font_size_slider.pack(pady=(0, 5), padx=15)
        
        self.font_size_display = ctk.CTkLabel(
            self,
            text="7 pt",
            font=ctk.CTkFont(size=11),
            text_color=TEXT_PRIMARY
        )
        self.font_size_display.pack(pady=(0, 15), padx=15)
    
    def _on_settings_change(self, value=None) -> None:
        """Handle settings change."""
        if self.on_settings_changed:
            settings = {
                'page_size': self.page_size_var.get(),
                'orientation': self.orientation_var.get(),
                'font_size': self.font_size_var.get()
            }
            self.on_settings_changed(settings)
    
    def _on_font_size_change(self, value) -> None:
        """Handle font size slider change."""
        size = int(value)
        self.font_size_display.configure(text=f"{size} pt")
        self._on_settings_change()
    
    def set_settings(self, settings: dict) -> None:
        """
        Update settings controls with values.
        
        Parameters:
            settings (dict): Settings dictionary.
        """
        self.page_size_var.set(settings.get('page_size', 'A4'))
        self.orientation_var.set(settings.get('orientation', 'Portrait'))
        font_size = settings.get('font_size', 7)
        self.font_size_var.set(font_size)
        self.font_size_display.configure(text=f"{font_size} pt")
