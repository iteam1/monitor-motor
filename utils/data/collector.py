"""
Data collection utilities for ModCon.

This module provides functions for collecting data from Modbus devices
and saving it to CSV files or databases.
"""

import csv
import time
from datetime import datetime
from typing import List, Dict, Any, Optional
from pathlib import Path

from utils.logger import get_logger
from utils.config import config
from utils.modbus.motor import SinamicV20

logger = get_logger(__name__)


class DataCollector:
    """Class for collecting and storing data from a Modbus device."""
    
    def __init__(
        self, 
        inverter: SinamicV20, 
        csv_file: Optional[str] = None,
        append: bool = True
    ):
        """
        Initialize the DataCollector.
        
        Args:
            inverter: The SinamicV20 inverter instance
            csv_file: Path to the CSV file to write data to
            append: Whether to append to an existing file or create a new one
        """
        self.inverter = inverter
        self.count = 0
        
        # Get configuration
        data_config = config.get('data_collection', {})
        self.csv_file = csv_file or data_config.get('csv_file', 'data/data.csv')
        
        # Ensure directory exists
        Path(self.csv_file).parent.mkdir(parents=True, exist_ok=True)
        
        # Create or append to CSV file
        if not append or not Path(self.csv_file).exists():
            self._write_header()
            
        logger.info(f"DataCollector initialized, writing to {self.csv_file}")
        
    def _write_header(self) -> None:
        """Write the CSV header with parameter names."""
        try:
            headers = list(self.inverter.name_to_address.keys())
            self._write_csv(headers)
            logger.info(f"Wrote header to {self.csv_file}")
        except Exception as e:
            logger.exception(f"Error writing CSV header: {e}")
            
    def _write_csv(self, data: List[Any]) -> None:
        """
        Write a row of data to the CSV file.
        
        Args:
            data: List of values to write
        """
        try:
            with open(self.csv_file, 'a', newline='') as outfile:
                writer = csv.writer(outfile)
                writer.writerow(data)
        except Exception as e:
            logger.exception(f"Error writing to CSV: {e}")
                
    def collect_data_point(self) -> List[Any]:
        """
        Collect a single data point from the inverter.
        
        Returns:
            List of collected values
        """
        try:
            # Get current timestamp
            current_time = datetime.now()
            timestamp = current_time.timestamp()
            
            # Get inverter values
            list_of_values = self.inverter.read_raw_all_address()
            
            # Log collection
            logger.info(f"Collected data point {self.count}: {len(list_of_values)} values at {timestamp}")
            
            # Write to CSV
            self._write_csv(list_of_values)
            
            self.count += 1
            return list_of_values
            
        except Exception as e:
            logger.exception(f"Error collecting data: {e}")
            return []
            
    def collect_data_continuously(self, interval: float = 1.0, max_points: Optional[int] = None) -> None:
        """
        Continuously collect data at specified intervals.
        
        Args:
            interval: Time between data points in seconds
            max_points: Maximum number of points to collect, or None for unlimited
        """
        logger.info(f"Starting continuous data collection with interval {interval}s")
        points_collected = 0
        
        try:
            while max_points is None or points_collected < max_points:
                self.collect_data_point()
                points_collected += 1
                
                if max_points is not None:
                    logger.info(f"Collected {points_collected}/{max_points} data points")
                    
                time.sleep(interval)
                
        except KeyboardInterrupt:
            logger.info("Data collection stopped by user")
        except Exception as e:
            logger.exception(f"Error in continuous data collection: {e}")
        finally:
            logger.info(f"Data collection finished, collected {points_collected} points")
