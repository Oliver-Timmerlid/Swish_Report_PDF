"""
File handler for storage operations.

Passive layer for file reading and writing without business logic.
"""

import logging
import os
from datetime import datetime
from typing import Optional


logger = logging.getLogger(__name__)


class FileHandler:
    """
    Handles file operations for the application.
    
    This is a passive storage layer that only deals with file I/O
    without implementing any business rules or validation.
    """
    
    @staticmethod
    def read_file(file_path: str, encoding: str = 'utf-8') -> str:
        """
        Read entire file content as string.
        
        Parameters:
            file_path (str): Path to the file.
            encoding (str): File encoding (default: 'utf-8').
        
        Returns:
            str: File content.
        
        Raises:
            FileNotFoundError: If file does not exist.
            IOError: If file cannot be read.
        """
        logger.debug(f"Reading file: {file_path}")
        
        try:
            with open(file_path, 'r', encoding=encoding) as file:
                content = file.read()
            logger.debug(f"Successfully read {len(content)} characters")
            return content
        except Exception as e:
            logger.error(f"Error reading file {file_path}: {str(e)}")
            raise
    
    @staticmethod
    def file_exists(file_path: str) -> bool:
        """
        Check if a file exists.
        
        Parameters:
            file_path (str): Path to check.
        
        Returns:
            bool: True if file exists, False otherwise.
        """
        return os.path.exists(file_path) and os.path.isfile(file_path)
    
    @staticmethod
    def get_file_extension(file_path: str) -> str:
        """
        Get the file extension from a path.
        
        Parameters:
            file_path (str): Path to the file.
        
        Returns:
            str: File extension including the dot (e.g., '.csv').
        """
        return os.path.splitext(file_path)[1]
    
    @staticmethod
    def generate_filename(
        base_name: str,
        extension: str,
        date: Optional[datetime] = None
    ) -> str:
        """
        Generate a filename with date.
        
        Parameters:
            base_name (str): Base name for the file (e.g., 'Swish').
            extension (str): File extension (e.g., '.pdf').
            date (Optional[datetime]): Date to include. If None, uses today.
        
        Returns:
            str: Generated filename (e.g., 'Swish_2025-12-24.pdf').
        """
        if date is None:
            date = datetime.now()
        
        date_str = date.strftime('%Y-%m-%d')
        
        if not extension.startswith('.'):
            extension = f'.{extension}'
        
        return f"{base_name}_{date_str}{extension}"
    
    @staticmethod
    def ensure_directory_exists(file_path: str) -> None:
        """
        Ensure that the directory for a file path exists.
        
        Parameters:
            file_path (str): Full file path.
        """
        directory = os.path.dirname(file_path)
        if directory and not os.path.exists(directory):
            os.makedirs(directory)
            logger.info(f"Created directory: {directory}")
