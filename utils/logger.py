"""
Logging utilities for ModCon.

This module provides functions for setting up and using loggers
throughout the application.
"""

import logging
import sys
from typing import Optional
from pathlib import Path


def get_logger(name: str, level: int = logging.INFO, log_file: Optional[str] = None) -> logging.Logger:
    """
    Get a configured logger instance.
    
    Args:
        name: Name of the logger.
        level: Logging level.
        log_file: Optional path to a log file.
        
    Returns:
        A configured logger instance.
    """
    logger = logging.getLogger(name)
    logger.setLevel(level)
    
    # Create formatters
    console_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    
    # Add console handler if not already present
    has_console_handler = any(isinstance(h, logging.StreamHandler) and h.stream == sys.stdout 
                             for h in logger.handlers)
    if not has_console_handler:
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(console_formatter)
        logger.addHandler(console_handler)
    
    # Add file handler if requested and not already present
    if log_file:
        log_path = Path(log_file)
        log_path.parent.mkdir(parents=True, exist_ok=True)
        
        has_file_handler = any(isinstance(h, logging.FileHandler) and h.baseFilename == str(log_path.absolute()) 
                              for h in logger.handlers)
        
        if not has_file_handler:
            file_handler = logging.FileHandler(log_file)
            file_handler.setFormatter(file_formatter)
            logger.addHandler(file_handler)
    
    return logger
