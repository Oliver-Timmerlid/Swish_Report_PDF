"""
PDF generation service for Swish reports.

Handles the creation of PDF documents from parsed Swish data,
with proper formatting and layout according to PRD specifications.
"""

import logging
from typing import List, Optional
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import (
    SimpleDocTemplate,
    Table,
    TableStyle,
    Paragraph,
    Spacer
)
from models.swish_data import SwishReport


logger = logging.getLogger(__name__)


class PDFGeneratorService:
    """
    Service for generating PDF reports from Swish data.
    
    Creates formatted PDF documents with summary overview and
    transaction details, following the layout specified in the PRD.
    """
    
    # Default columns to display in transactions table
    DEFAULT_TRANSACTION_COLUMNS = [
        'DATUM',
        'TID',
        'MARKNADSNAMN',
        'SWISH NUMMER',
        'NAMN',
        'MOBILNUMMER',
        'BELOPP'
    ]
    
    def __init__(self):
        """Initialize the PDF generator service."""
        self.page_size = A4
        self.orientation = 'portrait'
        self.font_size = 7
        # Table width = page width - left margin - right margin
        # A4 width = 595 points, with 40pt margins on each side
        self.table_width = 515
    
    def set_page_format(
        self,
        page_size: str = 'A4',
        orientation: str = 'portrait'
    ) -> None:
        """
        Configure PDF page format settings.
        
        Parameters:
            page_size (str): Page size ('A4' or 'Letter').
            orientation (str): Page orientation ('portrait' or 'landscape').
        """
        if page_size.upper() == 'A4':
            self.page_size = A4
        elif page_size.upper() == 'LETTER':
            self.page_size = letter
        
        self.orientation = orientation.lower()
        logger.info(f"PDF format set to {page_size} {orientation}")
    
    def set_font_size(self, size: int) -> None:
        """
        Set the font size for PDF content.
        
        Parameters:
            size (int): Font size in points.
        """
        self.font_size = size
        logger.info(f"PDF font size set to {size}")
    
    def generate_pdf(
        self,
        report: SwishReport,
        output_path: str,
        columns: Optional[List[str]] = None
    ) -> None:
        """
        Generate a PDF document from a Swish report.
        
        Parameters:
            report (SwishReport): The parsed Swish report data.
            output_path (str): Path where the PDF should be saved.
            columns (Optional[List[str]]): Transaction columns to include.
                                           If None, uses default columns.
        
        Raises:
            ValueError: If report is invalid or has no transactions.
        """
        if not report.has_transactions:
            raise ValueError("Cannot generate PDF: report has no transactions")
        
        logger.info(f"Generating PDF: {output_path}")
        
        if columns is None:
            columns = self.DEFAULT_TRANSACTION_COLUMNS
        
        # Create document
        doc = SimpleDocTemplate(
            output_path, 
            pagesize=self.page_size,
            leftMargin=40,
            rightMargin=40,
            topMargin=50,
            bottomMargin=50
        )
        elements = []
        styles = getSampleStyleSheet()
        
        # Add summary section
        elements.extend(
            self._create_summary_section(report, styles)
        )
        
        # Add transactions section
        elements.extend(
            self._create_transactions_section(report, columns, styles)
        )
        
        # Build PDF
        doc.build(elements)
        logger.info(f"PDF generated successfully: {output_path}")
    
    def _create_summary_section(
        self,
        report: SwishReport,
        styles
    ) -> List:
        """
        Create the summary (overview) section of the PDF.
        
        Parameters:
            report (SwishReport): The report data.
            styles: ReportLab styles.
        
        Returns:
            List: List of ReportLab flowables for summary section.
        """
        elements = []
        
        # Section title
        title_style = styles["Heading3"]
        title_style.leftIndent = 0
        elements.append(Paragraph("Översikt", title_style))
        elements.append(Spacer(1, 6))
        
        # Prepare data
        date_range = report.metadata.get_date_range_display()
        summary_data = report.summary.get_display_data()
        
        # Create table
        header = ['SÖKDATUM', 'ANTAL SWISH-BETALNINGAR', 'TOTALT INBETALAT BELOPP']
        data_row = [
            date_range,
            summary_data['Antal Swish-betalningar'],
            summary_data['Totalt inbetalat belopp']
        ]
        
        table_data = [header, data_row]
        
        # Calculate column widths
        num_cols = len(header)
        col_widths = [self.table_width / num_cols] * num_cols
        
        # Create and style table
        table = Table(table_data, colWidths=col_widths)
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ('FONTSIZE', (0, 0), (-1, -1), self.font_size),
            ('ALIGN', (0, 0), (-1, 0), 'LEFT'),      # Header
            ('ALIGN', (0, 1), (-2, -1), 'LEFT'),     # All but last column
            ('ALIGN', (-1, 1), (-1, -1), 'RIGHT'),   # Last column (amount)
        ]))
        
        elements.append(table)
        elements.append(Spacer(1, 20))
        
        return elements
    
    def _create_transactions_section(
        self,
        report: SwishReport,
        columns: List[str],
        styles
    ) -> List:
        """
        Create the transactions table section of the PDF.
        
        Parameters:
            report (SwishReport): The report data.
            columns (List[str]): Columns to include in table.
            styles: ReportLab styles.
        
        Returns:
            List: List of ReportLab flowables for transactions section.
        """
        elements = []
        
        # Section title
        title_style = styles["Heading3"]
        title_style.leftIndent = 0
        elements.append(Paragraph("Transaktioner", title_style))
        elements.append(Spacer(1, 6))
        
        # Prepare table data
        table_data = [columns]  # Header row
        
        for transaction in report.transactions:
            row = transaction.to_list(columns)
            table_data.append(row)
        
        # Calculate dynamic column widths
        max_lengths = [
            max(len(str(row[i])) for row in table_data)
            for i in range(len(columns))
        ]
        total_length = sum(max_lengths)
        
        col_widths = [
            (self.table_width * (length / total_length))
            for length in max_lengths
        ]
        
        # Create and style table
        table = Table(table_data, colWidths=col_widths, repeatRows=1)
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
            ('FONTSIZE', (0, 0), (-1, -1), self.font_size),
            ('ALIGN', (0, 0), (-1, 0), 'LEFT'),      # Header row
            ('ALIGN', (0, 1), (-2, -1), 'LEFT'),     # All columns except last
            ('ALIGN', (-1, 1), (-1, -1), 'RIGHT'),   # Right-align BELOPP
        ]))
        
        elements.append(table)
        
        return elements
