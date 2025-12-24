"""
Domain models for Swish transaction data.

These dataclasses represent the structure of Swish CSV reports
according to the PRD specifications.
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional


@dataclass
class SwishMetadata:
    """
    Metadata section from Swish CSV report.
    
    Contains information about who created the report, when it was
    created, and the search parameters used.
    """
    
    created_by: str
    date: str
    search_criteria: str
    search_date_range: str
    swish_number: str
    result_count: int
    
    def get_date_range_display(self) -> str:
        """
        Extract and clean the date range for display purposes.
        
        Returns:
            str: Formatted date range string.
        """
        # Extract first part before comma (date range)
        if ',' in self.search_date_range:
            return self.search_date_range.split(',')[0].strip()
        return self.search_date_range.strip()


@dataclass
class SwishSummary:
    """
    Summary section from Swish CSV report.
    
    Contains aggregated information about transactions including
    market name, number of payments, and total amount.
    """
    
    market_name: str
    swish_number: str
    payment_count: int
    total_amount: str
    net_amount: Optional[str] = None
    
    def get_display_data(self) -> dict:
        """
        Get summary data formatted for display.
        
        Returns:
            dict: Dictionary with display-friendly field names.
        """
        return {
            'Antal Swish-betalningar': str(self.payment_count),
            'Totalt inbetalat belopp': self.total_amount
        }


@dataclass
class SwishTransaction:
    """
    Individual transaction from Swish CSV report.
    
    Represents a single payment transaction with all relevant details.
    """
    
    date: str
    time: str
    market_name: str
    swish_number: str
    name: str
    mobile_number: str
    amount: str
    message: Optional[str] = None
    reference: Optional[str] = None
    
    def to_list(self, columns: List[str]) -> List[str]:
        """
        Convert transaction to list format for specified columns.
        
        Parameters:
            columns (List[str]): Column names to include.
        
        Returns:
            List[str]: Transaction data in the order of columns.
        """
        mapping = {
            'DATUM': self.date,
            'TID': self.time,
            'MARKNADSNAMN': self.market_name,
            'SWISH NUMMER': self.swish_number,
            'NAMN': self.name,
            'MOBILNUMMER': self.mobile_number,
            'BELOPP': self.amount,
            'MEDDELANDE': self.message or '',
            'REFERENS': self.reference or ''
        }
        return [mapping.get(col, '') for col in columns]


@dataclass
class SwishReport:
    """
    Complete Swish report containing all sections.
    
    This is the top-level model that aggregates metadata,
    summary, and transaction data from a Swish CSV file.
    """
    
    metadata: SwishMetadata
    summary: SwishSummary
    transactions: List[SwishTransaction] = field(default_factory=list)
    
    @property
    def transaction_count(self) -> int:
        """Get the number of transactions in the report."""
        return len(self.transactions)
    
    @property
    def has_transactions(self) -> bool:
        """Check if the report contains any transactions."""
        return self.transaction_count > 0
    
    def get_preview_data(self) -> dict:
        """
        Get data for preview display before PDF generation.
        
        Returns:
            dict: Preview information including date range, count,
                  total amount, and market name.
        """
        return {
            'date_range': self.metadata.get_date_range_display(),
            'transaction_count': self.transaction_count,
            'total_amount': self.summary.total_amount,
            'market_name': self.summary.market_name
        }
