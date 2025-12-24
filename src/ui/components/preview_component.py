"""
Preview component for displaying report data.

UI component only - no business logic.
"""

import logging
import customtkinter as ctk
from ui.theme import (
    BG_APP, BG_PANEL, BG_CARD, TEXT_PRIMARY, TEXT_SECONDARY, 
    TEXT_MUTED, ACCENT_PRIMARY
)


logger = logging.getLogger(__name__)


class PreviewComponent(ctk.CTkFrame):
    """Preview area for displaying loaded report data."""
    
    def __init__(self, parent):
        """
        Initialize the preview component.
        
        Parameters:
            parent: Parent widget.
        """
        super().__init__(parent, fg_color=BG_PANEL, corner_radius=12)
        
        self.current_report = None
        
        self._build_ui()
    
    def _build_ui(self) -> None:
        """Build preview UI."""
        # Header
        preview_header = ctk.CTkFrame(self, fg_color="transparent")
        preview_header.pack(fill='x', padx=20, pady=(15, 10))
        
        preview_title = ctk.CTkLabel(
            preview_header,
            text="Förhandsgranskning",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color=TEXT_PRIMARY
        )
        preview_title.pack(side='left')
        
        # Scrollable content area
        self.preview_scroll = ctk.CTkScrollableFrame(
            self,
            fg_color="transparent"
        )
        self.preview_scroll.pack(fill='both', expand=True, padx=20, pady=(0, 15))
        
        # Initial empty state
        self.show_empty_state()
    
    def show_preview(self, report) -> None:
        """
        Update preview with report data.
        
        Parameters:
            report: SwishReport instance to preview.
        """
        self.current_report = report
        
        # Clear existing content
        for widget in self.preview_scroll.winfo_children():
            widget.destroy()
        
        preview_data = report.get_preview_data()
        
        # Summary section
        summary_frame = ctk.CTkFrame(self.preview_scroll, fg_color=BG_CARD, corner_radius=10)
        summary_frame.pack(fill='x', pady=(0, 15))
        
        summary_title = ctk.CTkLabel(
            summary_frame,
            text="Översikt",
            font=ctk.CTkFont(size=15, weight="bold"),
            text_color=TEXT_PRIMARY
        )
        summary_title.pack(pady=(15, 10), padx=15, anchor='w')
        
        self._add_info_row(summary_frame, "Marknadsnamn:", preview_data['market_name'])
        self._add_info_row(summary_frame, "Datumintervall:", preview_data['date_range'])
        self._add_info_row(summary_frame, "Antal transaktioner:", str(preview_data['transaction_count']))
        self._add_info_row(summary_frame, "Totalbelopp:", preview_data['total_amount'])
        
        # Transaction table
        if report.transactions:
            trans_frame = ctk.CTkFrame(self.preview_scroll, fg_color=BG_CARD, corner_radius=10)
            trans_frame.pack(fill='both', expand=True, pady=(0, 10))
            
            trans_title = ctk.CTkLabel(
                trans_frame,
                text=f"Transaktioner ({len(report.transactions)} st)",
                font=ctk.CTkFont(size=14, weight="bold"),
                text_color=TEXT_PRIMARY
            )
            trans_title.pack(pady=(12, 8), padx=15, anchor='w')
            
            # Table container
            table_container = ctk.CTkFrame(trans_frame, fg_color="transparent")
            table_container.pack(fill='both', expand=True, padx=15, pady=(0, 15))
            
            # Table header
            header_row = ctk.CTkFrame(table_container, fg_color="#0f0f10", corner_radius=6)
            header_row.pack(fill='x', pady=(0, 4))
            
            headers = [
                ("Datum", 90, 'w'),
                ("Tid", 70, 'w'),
                ("Namn", 210, 'w'),
                ("Telefon", 120, 'w'),
                ("Belopp", 110, 'e')
            ]
            
            for header_text, width, align in headers:
                header_label = ctk.CTkLabel(
                    header_row,
                    text=header_text,
                    font=ctk.CTkFont(size=13, weight="bold"),
                    text_color="#94a3b8",
                    anchor=align,
                    width=width
                )
                header_label.pack(side='left', padx=8, pady=10)
            
            # Table rows
            for i, trans in enumerate(report.transactions):
                row_color = "#1a1a1d" if i % 2 == 0 else "#15151a"
                row_frame = ctk.CTkFrame(table_container, fg_color=row_color, corner_radius=4)
                row_frame.pack(fill='x', pady=1)
                
                # Date
                date_cell = ctk.CTkLabel(
                    row_frame,
                    text=trans.date,
                    font=ctk.CTkFont(size=12),
                    text_color=TEXT_PRIMARY,
                    anchor='w',
                    width=90
                )
                date_cell.pack(side='left', padx=8, pady=8)
                
                # Time
                time_cell = ctk.CTkLabel(
                    row_frame,
                    text=trans.time,
                    font=ctk.CTkFont(size=12),
                    text_color=TEXT_PRIMARY,
                    anchor='w',
                    width=70
                )
                time_cell.pack(side='left', padx=8, pady=8)
                
                # Name
                name_cell = ctk.CTkLabel(
                    row_frame,
                    text=trans.name[:28] + "..." if len(trans.name) > 28 else trans.name,
                    font=ctk.CTkFont(size=12),
                    text_color=TEXT_PRIMARY,
                    anchor='w',
                    width=210
                )
                name_cell.pack(side='left', padx=8, pady=8)
                
                # Phone
                phone_cell = ctk.CTkLabel(
                    row_frame,
                    text=trans.mobile_number,
                    font=ctk.CTkFont(size=12),
                    text_color=TEXT_SECONDARY,
                    anchor='w',
                    width=120
                )
                phone_cell.pack(side='left', padx=8, pady=8)
                
                # Amount
                amount_cell = ctk.CTkLabel(
                    row_frame,
                    text=f"{trans.amount} kr",
                    font=ctk.CTkFont(size=13, weight="bold"),
                    text_color=ACCENT_PRIMARY,
                    anchor='e',
                    width=110
                )
                amount_cell.pack(side='left', padx=8, pady=8)
    
    def show_empty_state(self) -> None:
        """Show empty state when no file is loaded."""
        # Clear existing content
        for widget in self.preview_scroll.winfo_children():
            widget.destroy()
        
        empty_container = ctk.CTkFrame(self.preview_scroll, fg_color="transparent")
        empty_container.pack(expand=True, pady=100)
        
        empty_label = ctk.CTkLabel(
            empty_container,
            text="Ingen fil vald",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color=TEXT_PRIMARY
        )
        empty_label.pack(pady=(0, 8))
        
        sub_label = ctk.CTkLabel(
            empty_container,
            text="Ladda eller dra in en CSV-fil för att förhandsgranska",
            font=ctk.CTkFont(size=12),
            text_color=TEXT_MUTED
        )
        sub_label.pack()
        
        self.current_report = None
    
    def _add_info_row(self, parent, label: str, value: str) -> None:
        """
        Add an information row to the summary.
        
        Parameters:
            parent: Parent widget.
            label (str): Label text.
            value (str): Value text.
        """
        row_frame = ctk.CTkFrame(parent, fg_color="transparent")
        row_frame.pack(fill='x', padx=15, pady=6)
        
        label_widget = ctk.CTkLabel(
            row_frame,
            text=label,
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color=TEXT_SECONDARY,
            anchor='w'
        )
        label_widget.pack(side='left', padx=(0, 10))
        
        value_widget = ctk.CTkLabel(
            row_frame,
            text=value,
            font=ctk.CTkFont(size=12),
            text_color=TEXT_PRIMARY,
            anchor='w'
        )
        value_widget.pack(side='left', fill='x', expand=True)
