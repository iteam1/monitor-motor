"""
File I/O utilities for ModCon.

This module provides functions for reading and writing data to/from
various file formats, including CSV, JSON, and others.
"""

import os
import csv
import json
from typing import List, Dict, Any, Optional, Union
from pathlib import Path

from utils.logger import get_logger
from utils.config import config

logger = get_logger(__name__)


def write_csv(
    data: List[Any],
    filepath: Optional[str] = None,
    headers: Optional[List[str]] = None,
    append: bool = True
) -> bool:
    """
    Write data to a CSV file.
    
    Args:
        data: List of data items to write as a row, or list of lists for multiple rows
        filepath: Path to the output file, or None to use default from config
        headers: Column headers to include at the top of a new file
        append: Whether to append to an existing file or overwrite it
    
    Returns:
        True if successful, False otherwise
    """
    try:
        # Get default filepath from config if not provided
        if filepath is None:
            data_config = config.get('data', {})
            filepath = data_config.get('default_csv_path', 'assets/data/output.csv')
        
        # Make sure the directory exists
        directory = os.path.dirname(filepath)
        if directory and not os.path.exists(directory):
            os.makedirs(directory)
            logger.info(f"Created directory: {directory}")
        
        # Determine if we need to write headers
        file_exists = os.path.exists(filepath)
        write_headers = headers is not None and (not file_exists or not append)
        
        # Open file in appropriate mode
        mode = 'a' if append and file_exists else 'w'
        
        with open(filepath, mode, newline='') as f:
            writer = csv.writer(f)
            
            # Write headers if needed
            if write_headers:
                writer.writerow(headers)
                logger.debug(f"Wrote headers to {filepath}")
            
            # Write data - handle both single row and multiple rows
            if data and isinstance(data[0], list):
                # Multiple rows
                writer.writerows(data)
                logger.debug(f"Wrote {len(data)} rows to {filepath}")
            else:
                # Single row
                writer.writerow(data)
                logger.debug(f"Wrote 1 row to {filepath}")
                
        logger.info(f"Successfully wrote data to {filepath}")
        return True
        
    except Exception as e:
        logger.exception(f"Error writing CSV data to {filepath}: {e}")
        return False


def read_csv(
    filepath: str,
    as_dict: bool = False,
    encoding: str = 'utf-8'
) -> List[Any]:
    """
    Read data from a CSV file.
    
    Args:
        filepath: Path to the CSV file
        as_dict: Whether to return data as list of dictionaries (True) or list of lists (False)
        encoding: File encoding
    
    Returns:
        List of rows, where each row is either a list or dictionary depending on as_dict
    """
    try:
        data = []
        
        with open(filepath, 'r', newline='', encoding=encoding) as f:
            if as_dict:
                reader = csv.DictReader(f)
                data = [dict(row) for row in reader]
                logger.debug(f"Read {len(data)} dictionary rows from {filepath}")
            else:
                reader = csv.reader(f)
                data = [row for row in reader]
                logger.debug(f"Read {len(data)} rows from {filepath}")
        
        logger.info(f"Successfully read {len(data)} rows from {filepath}")
        return data
        
    except Exception as e:
        logger.exception(f"Error reading CSV data from {filepath}: {e}")
        return []


def write_json(
    data: Union[Dict[str, Any], List[Any]],
    filepath: str,
    pretty: bool = True
) -> bool:
    """
    Write data to a JSON file.
    
    Args:
        data: Data to write (dictionary or list)
        filepath: Path to the output file
        pretty: Whether to pretty-print the JSON with indentation
    
    Returns:
        True if successful, False otherwise
    """
    try:
        # Make sure the directory exists
        directory = os.path.dirname(filepath)
        if directory and not os.path.exists(directory):
            os.makedirs(directory)
            logger.info(f"Created directory: {directory}")
        
        with open(filepath, 'w', encoding='utf-8') as f:
            if pretty:
                json.dump(data, f, indent=4)
            else:
                json.dump(data, f)
                
        logger.info(f"Successfully wrote JSON data to {filepath}")
        return True
        
    except Exception as e:
        logger.exception(f"Error writing JSON data to {filepath}: {e}")
        return False


def read_json(
    filepath: str
) -> Union[Dict[str, Any], List[Any], None]:
    """
    Read data from a JSON file.
    
    Args:
        filepath: Path to the JSON file
    
    Returns:
        The parsed JSON data (dictionary or list), or None if there was an error
    """
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
                
        logger.info(f"Successfully read JSON data from {filepath}")
        return data
        
    except Exception as e:
        logger.exception(f"Error reading JSON data from {filepath}: {e}")
        return None


# Example usage
if __name__ == "__main__":
    # Example CSV writing
    test_data = [
        ["id", "name", "value"],
        [1, "item1", 10.5],
        [2, "item2", 20.7],
        [3, "item3", 30.2]
    ]
    
    write_csv(test_data[1:], "example.csv", headers=test_data[0], append=False)
    
    # Example CSV reading
    read_data = read_csv("example.csv", as_dict=True)
    print("CSV Data:", read_data)
    
    # Example JSON writing
    json_data = {
        "settings": {
            "interval": 1000,
            "enabled": True
        },
        "items": [
            {"id": 1, "name": "item1"},
            {"id": 2, "name": "item2"}
        ]
    }
    
    write_json(json_data, "example.json")
    
    # Example JSON reading
    read_json_data = read_json("example.json")
    print("JSON Data:", read_json_data)
