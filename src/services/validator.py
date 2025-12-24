"""
Validation service for Swish CSV files.

Validates CSV files against expected format and business rules
before processing them into PDF.
"""

import logging
import os
from typing import List, Tuple, Optional


logger = logging.getLogger(__name__)


class ValidationService:
    """
    Service for validating Swish CSV files.
    
    Ensures that CSV files meet the expected format and contain
    all required sections and data before processing.
    """
    
    # Expected headers for validation
    REQUIRED_METADATA_FIELDS = [
        'Skapad av',
        'Datum',
        'Swish-nummer'
    ]
    
    SUMMARY_HEADER_START = 'MARKNADSNAMN'
    TRANSACTION_HEADER_START = 'DATUM'
    
    REQUIRED_TRANSACTION_COLUMNS = [
        'DATUM',
        'TID',
        'MARKNADSNAMN',
        'SWISH NUMMER',
        'NAMN',
        'MOBILNUMMER',
        'BELOPP'
    ]
    
    def validate_file_path(self, file_path: str) -> Tuple[bool, Optional[str]]:
        """
        Validate that the file exists and has correct extension.
        
        Parameters:
            file_path (str): Path to the file to validate.
        
        Returns:
            Tuple[bool, Optional[str]]: (is_valid, error_message).
                                         error_message is None if valid.
        """
        if not file_path:
            return False, "Ingen fil vald"
        
        if not os.path.exists(file_path):
            logger.error(f"File does not exist: {file_path}")
            return False, "Filen kunde inte hittas"
        
        if not file_path.lower().endswith('.csv'):
            logger.error(f"Invalid file extension: {file_path}")
            return False, "Endast CSV-filer accepteras"
        
        return True, None
    
    def validate_file_content(
        self,
        file_path: str
    ) -> Tuple[bool, Optional[str]]:
        """
        Validate the content structure of a CSV file.
        
        Parameters:
            file_path (str): Path to the CSV file.
        
        Returns:
            Tuple[bool, Optional[str]]: (is_valid, error_message).
                                         error_message is None if valid.
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()
            
            # Check if file is empty
            if not content.strip():
                return False, "CSV-filen är tom"
            
            lines = [line.strip() for line in content.split('\n') if line.strip()]
            
            # Validate sections exist
            has_summary_header = any(
                self.SUMMARY_HEADER_START in line
                for line in lines
            )
            has_transaction_header = any(
                self.TRANSACTION_HEADER_START in line.split(';')[0]
                for line in lines
            )
            
            if not has_summary_header:
                logger.error("Missing summary header in CSV")
                return (
                    False,
                    "CSV-filen saknar sammanfattningsdel (MARKNADSNAMN)"
                )
            
            if not has_transaction_header:
                logger.error("Missing transaction header in CSV")
                return (
                    False,
                    "CSV-filen saknar transaktionsdel (DATUM)"
                )
            
            # Check for at least one transaction
            transaction_start_idx = None
            for i, line in enumerate(lines):
                if self.TRANSACTION_HEADER_START in line.split(';')[0]:
                    transaction_start_idx = i
                    break
            
            if transaction_start_idx is None or (
                transaction_start_idx >= len(lines) - 1
            ):
                logger.error("No transactions found in CSV")
                return False, "CSV-filen innehåller inga transaktioner"
            
            logger.info("File content validation passed")
            return True, None
            
        except UnicodeDecodeError:
            logger.error("File encoding error")
            return False, "Felaktig filkodning. Kontrollera att filen är UTF-8"
        except Exception as e:
            logger.error(f"Error validating file content: {str(e)}")
            return False, f"Kunde inte validera fil: {str(e)}"
    
    def validate_required_columns(
        self,
        header: List[str]
    ) -> Tuple[bool, Optional[str]]:
        """
        Validate that all required columns are present in header.
        
        Parameters:
            header (List[str]): Column headers from CSV.
        
        Returns:
            Tuple[bool, Optional[str]]: (is_valid, error_message).
                                         error_message is None if valid.
        """
        missing_columns = [
            col for col in self.REQUIRED_TRANSACTION_COLUMNS
            if col not in header
        ]
        
        if missing_columns:
            logger.error(f"Missing required columns: {missing_columns}")
            return (
                False,
                f"CSV saknar obligatoriska kolumner: {', '.join(missing_columns)}"
            )
        
        return True, None
    
    def validate_complete(
        self,
        file_path: str
    ) -> Tuple[bool, Optional[str]]:
        """
        Perform complete validation of a CSV file.
        
        This is a convenience method that runs all validation checks.
        
        Parameters:
            file_path (str): Path to the CSV file.
        
        Returns:
            Tuple[bool, Optional[str]]: (is_valid, error_message).
                                         error_message is None if valid.
        """
        # Validate file path
        is_valid, error = self.validate_file_path(file_path)
        if not is_valid:
            return is_valid, error
        
        # Validate file content
        is_valid, error = self.validate_file_content(file_path)
        if not is_valid:
            return is_valid, error
        
        logger.info(f"Complete validation passed for: {file_path}")
        return True, None
