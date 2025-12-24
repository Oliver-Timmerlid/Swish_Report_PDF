"""
Logging configuration for the application.

Sets up structured logging according to PRD requirements.
"""

import logging
import os
from typing import Optional
from .config import Config


def setup_logging(
    level: Optional[str] = None,
    log_file: Optional[str] = None
) -> None:
    """
    Configure application logging.
    
    Sets up logging to both file and console according to PRD specs.
    No print statements should be used in the application.
    
    Parameters:
        level (Optional[str]): Log level (DEBUG, INFO, WARNING, ERROR, CRITICAL).
                               If None, uses Config.LOG_LEVEL.
        log_file (Optional[str]): Path to log file. If None, uses Config path.
    """
    if level is None:
        level = Config.LOG_LEVEL
    
    if log_file is None:
        log_file = Config.get_log_file_path()
    
    # Ensure log directory exists
    log_dir = os.path.dirname(log_file)
    if log_dir:
        os.makedirs(log_dir, exist_ok=True)
    
    # Create formatter
    formatter = logging.Formatter(
        Config.LOG_FORMAT,
        datefmt=Config.LOG_DATE_FORMAT
    )
    
    # Configure root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(level)
    
    # Remove existing handlers
    root_logger.handlers.clear()
    
    # File handler
    file_handler = logging.FileHandler(log_file, encoding='utf-8')
    file_handler.setLevel(level)
    file_handler.setFormatter(formatter)
    root_logger.addHandler(file_handler)
    
    # Console handler (for development)
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.WARNING)  # Only warnings+ to console
    console_handler.setFormatter(formatter)
    root_logger.addHandler(console_handler)
    
    # Log startup
    logging.info("=" * 60)
    logging.info(f"{Config.APP_NAME} v{Config.APP_VERSION}")
    logging.info(f"Logging initialized - Level: {level}")
    logging.info(f"Log file: {log_file}")
    logging.info("=" * 60)


def get_logger(name: str) -> logging.Logger:
    """
    Get a logger instance for a module.
    
    Parameters:
        name (str): Module name (use __name__).
    
    Returns:
        logging.Logger: Logger instance.
    """
    return logging.getLogger(name)
