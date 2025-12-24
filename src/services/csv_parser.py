"""
CSV parsing service for Swish transaction files.

This service handles the parsing of Swish CSV files into structured
data models, following the three-section format specified in the PRD.
"""

import csv
import logging
from typing import List, Tuple, Optional
from models.swish_data import (
    SwishMetadata,
    SwishSummary,
    SwishTransaction,
    SwishReport
)


logger = logging.getLogger(__name__)


class CSVParserService:
    """
    Service for parsing Swish CSV files.
    
    Handles the parsing of CSV files following the expected Swish format
    with three logical sections: metadata, summary, and transactions.
    """
    
    def __init__(self):
        """Initialize the CSV parser service."""
        self.encoding = 'utf-8'
        self.delimiter = ';'
    
    def parse_file(self, file_path: str) -> SwishReport:
        """
        Parse a Swish CSV file into a SwishReport object.
        
        Parameters:
            file_path (str): Path to the CSV file to parse.
        
        Returns:
            SwishReport: Parsed report containing metadata, summary,
                         and transactions.
        
        Raises:
            ValueError: If file cannot be parsed or format is invalid.
            FileNotFoundError: If file does not exist.
        """
        logger.info(f"Starting to parse CSV file: {file_path}")
        
        try:
            with open(file_path, 'r', encoding=self.encoding) as file:
                lines = [
                    line.strip()
                    for line in file
                    if line.strip()
                ]
            
            metadata_lines, summary_lines, transaction_lines = (
                self._split_sections(lines)
            )
            
            metadata = self._parse_metadata(metadata_lines)
            summary = self._parse_summary(summary_lines)
            transactions = self._parse_transactions(transaction_lines)
            
            report = SwishReport(
                metadata=metadata,
                summary=summary,
                transactions=transactions
            )
            
            logger.info(
                f"Successfully parsed CSV with {len(transactions)} "
                f"transactions"
            )
            return report
            
        except FileNotFoundError:
            logger.error(f"File not found: {file_path}")
            raise
        except Exception as e:
            logger.error(f"Error parsing CSV file: {str(e)}")
            raise ValueError(f"Failed to parse CSV file: {str(e)}")
    
    def _split_sections(
        self,
        lines: List[str]
    ) -> Tuple[List[str], List[str], List[str]]:
        """
        Split CSV lines into three logical sections.
        
        Parameters:
            lines (List[str]): All lines from the CSV file.
        
        Returns:
            Tuple containing metadata, summary, and transaction line lists.
        """
        metadata_lines = []
        summary_lines = []
        transaction_lines = []
        current_section = "metadata"
        
        for line in lines:
            # Remove quotes and clean
            clean_line = line.replace('"', '').strip()
            
            if not clean_line:
                continue
            
            # Detect section transitions
            if current_section == "metadata":
                if clean_line.startswith("MARKNADSNAMN"):
                    # This is the summary header
                    summary_lines.append(clean_line)
                    current_section = "summary"
                else:
                    metadata_lines.append(clean_line)
            
            elif current_section == "summary":
                if clean_line.startswith("DATUM"):
                    # This is the transaction header
                    transaction_lines.append(clean_line)
                    current_section = "transactions"
                else:
                    summary_lines.append(clean_line)
            
            elif current_section == "transactions":
                transaction_lines.append(clean_line)
        
        return metadata_lines, summary_lines, transaction_lines
    
    def _parse_metadata(self, lines: List[str]) -> SwishMetadata:
        """
        Parse metadata section.
        
        Parameters:
            lines (List[str]): Metadata section lines.
        
        Returns:
            SwishMetadata: Parsed metadata object.
        """
        metadata_dict = {}
        
        for line in lines:
            if ';' in line:
                parts = line.split(';', 1)
                key = parts[0].strip().rstrip(':')
                value = parts[1].strip() if len(parts) > 1 else ''
                metadata_dict[key] = value
        
        return SwishMetadata(
            created_by=metadata_dict.get('Skapad av', ''),
            date=metadata_dict.get('Datum', ''),
            search_criteria=metadata_dict.get('Sökbegrepp', ''),
            search_date_range=metadata_dict.get('Sök', ''),
            swish_number=metadata_dict.get('Swish-nummer', ''),
            result_count=int(metadata_dict.get('Antal resultat', 0))
        )
    
    def _parse_summary(self, lines: List[str]) -> SwishSummary:
        """
        Parse summary section.
        
        Parameters:
            lines (List[str]): Summary section lines (header + data).
        
        Returns:
            SwishSummary: Parsed summary object.
        """
        if not lines or len(lines) < 2:
            raise ValueError("Invalid summary section")
        
        header = lines[0].split(self.delimiter)
        # Skip "Total" row, use first market row
        data_line = next(
            (line for line in lines[1:] if not line.startswith('Total')),
            lines[1]
        )
        data = data_line.split(self.delimiter)
        
        # Create mapping
        summary_dict = {
            header[i].strip(): data[i].strip()
            for i in range(min(len(header), len(data)))
        }
        
        return SwishSummary(
            market_name=summary_dict.get('MARKNADSNAMN', ''),
            swish_number=summary_dict.get('SWISH NUMMER', ''),
            payment_count=int(
                summary_dict.get('ANTAL SWISH-BETALNINGAR', 0)
            ),
            total_amount=summary_dict.get('TOTALT INBETALAT BELOPP', ''),
            net_amount=summary_dict.get('NETTO', None)
        )
    
    def _parse_transactions(
        self,
        lines: List[str]
    ) -> List[SwishTransaction]:
        """
        Parse transaction section.
        
        Parameters:
            lines (List[str]): Transaction section lines (header + data).
        
        Returns:
            List[SwishTransaction]: List of parsed transaction objects.
        """
        if not lines:
            return []
        
        header = lines[0].split(self.delimiter)
        transactions = []
        
        for line in lines[1:]:
            data = line.split(self.delimiter)
            
            # Create mapping
            trans_dict = {
                header[i].strip(): data[i].strip()
                for i in range(min(len(header), len(data)))
            }
            
            transaction = SwishTransaction(
                date=trans_dict.get('DATUM', ''),
                time=trans_dict.get('TID', ''),
                market_name=trans_dict.get('MARKNADSNAMN', ''),
                swish_number=trans_dict.get('SWISH NUMMER', ''),
                name=trans_dict.get('NAMN', ''),
                mobile_number=trans_dict.get('MOBILNUMMER', ''),
                amount=trans_dict.get('BELOPP', ''),
                message=trans_dict.get('MEDDELANDE', None),
                reference=trans_dict.get('REFERENS', None)
            )
            transactions.append(transaction)
        
        return transactions
