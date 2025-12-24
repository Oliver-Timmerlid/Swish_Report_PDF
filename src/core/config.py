"""
Application configuration.

Central configuration for the Swish CSV to PDF Converter.
"""

import os
from typing import Final


class Config:
    """
    Application configuration constants.
    
    Contains all configuration values used throughout the application.
    """
    
    # Application metadata
    APP_NAME: Final[str] = "Swish CSV to PDF Converter"
    APP_VERSION: Final[str] = "1.0.0"
    
    # File settings
    SUPPORTED_EXTENSIONS: Final[list] = ['.csv']
    DEFAULT_ENCODING: Final[str] = 'utf-8'
    CSV_DELIMITER: Final[str] = ';'
    
    # PDF settings
    DEFAULT_PAGE_SIZE: Final[str] = 'A4'
    DEFAULT_ORIENTATION: Final[str] = 'Portrait'
    DEFAULT_FONT_SIZE: Final[int] = 7
    DEFAULT_TABLE_WIDTH: Final[int] = 600
    
    # UI settings
    WINDOW_WIDTH: Final[int] = 1100
    WINDOW_HEIGHT: Final[int] = 750
    WINDOW_MIN_WIDTH: Final[int] = 900
    WINDOW_MIN_HEIGHT: Final[int] = 600
    THEME: Final[str] = "blue"
    APPEARANCE_MODE: Final[str] = "dark"
    
    # Logging
    LOG_LEVEL: Final[str] = "INFO"
    LOG_FORMAT: Final[str] = (
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    LOG_DATE_FORMAT: Final[str] = '%Y-%m-%d %H:%M:%S'
    
    # Paths
    @staticmethod
    def get_log_directory() -> str:
        """
        Get the directory for log files.
        
        Returns:
            str: Path to log directory.
        """
        # Use current directory or user's home directory
        return os.path.join(os.getcwd(), 'logs')
    
    @staticmethod
    def get_log_file_path() -> str:
        """
        Get the full path to the log file.
        
        Returns:
            str: Path to log file.
        """
        log_dir = Config.get_log_directory()
        os.makedirs(log_dir, exist_ok=True)
        return os.path.join(log_dir, 'swish_converter.log')
