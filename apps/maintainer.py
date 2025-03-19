#!/usr/bin/env python3
"""
Maintenance Monitor Application

This application monitors the motor performance by reading data from the database,
evaluating the current state, and providing warnings when parameters are outside
of normal operating ranges.

Usage:
    python -m apps.maintainer [--config CONFIG_FILE]
"""

import os
import sys
import time
import argparse
import sqlite3
import numpy as np
from typing import Dict, Any, Optional, Tuple, List
from pathlib import Path
from joblib import load

from utils.logger import get_logger
from utils.config import config
from utils.database.operations import execute_query

logger = get_logger(__name__)

# Speed classifications
SPEED_RANGES = {
    "stopped": (0, 0.1),  # Essentially zero
    "slow": (0.1, 7),     # Slow speed range
    "normal": (7, 13),    # Normal operating range
    "high": (13, float('inf'))  # High speed range
}

# Default configuration
DEFAULT_CONFIG = {
    "database": {
        "path": "data/inverter.db",
        "table_name": "sinamicv20",
        "row_id": 0
    },
    "maintainer": {
        "interval": 2.0,
        "model_path": "models/model.joblib",
        "rpm_conversion_factor": 8.10/242,
        "speed_field_index": 24
    }
}


def parse_args():
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(description='Monitor motor performance and maintenance')
    parser.add_argument('--config', type=str, help='Path to configuration file')
    parser.add_argument('--interval', type=float, help='Monitoring interval in seconds')
    parser.add_argument('--db-path', type=str, help='Database file path')
    parser.add_argument('--model-path', type=str, help='Path to ML model file')
    parser.add_argument('--verbose', '-v', action='store_true', help='Enable verbose output')
    return parser.parse_args()


def connect_to_database(db_path: str) -> sqlite3.Connection:
    """
    Connect to the SQLite database.
    
    Args:
        db_path: Path to the database file
        
    Returns:
        Database connection object
        
    Raises:
        FileNotFoundError: If the database file doesn't exist
        sqlite3.Error: If connection fails
    """
    if not os.path.exists(db_path):
        logger.error(f"Database file not found: {db_path}")
        raise FileNotFoundError(f"Database file not found: {db_path}")
        
    try:
        conn = sqlite3.connect(db_path)
        logger.info(f"Connected to database at {db_path}")
        return conn
    except sqlite3.Error as e:
        logger.exception(f"Error connecting to database: {e}")
        raise


def load_ml_model(model_path: str) -> Any:
    """
    Load the machine learning model.
    
    Args:
        model_path: Path to the saved model file
        
    Returns:
        Loaded model object
        
    Raises:
        FileNotFoundError: If the model file doesn't exist
    """
    if not os.path.exists(model_path):
        logger.error(f"Model file not found: {model_path}")
        raise FileNotFoundError(f"Model file not found: {model_path}")
        
    try:
        model = load(model_path)
        logger.info(f"Loaded model from {model_path}")
        return model
    except Exception as e:
        logger.exception(f"Error loading model: {e}")
        raise


def get_motor_data(conn: sqlite3.Connection, table_name: str, row_id: int) -> Tuple[Optional[List[Any]], Optional[str]]:
    """
    Get motor data from the database.
    
    Args:
        conn: Database connection
        table_name: Name of the table
        row_id: ID of the row to fetch
        
    Returns:
        Tuple containing (data row, error message if any)
    """
    try:
        query = f"SELECT * FROM {table_name} WHERE ID = {row_id}"
        result = execute_query(conn, query)
        
        if not result or not result[0]:
            return None, "No data found in database"
            
        return result[0], None
        
    except Exception as e:
        logger.exception(f"Error fetching motor data: {e}")
        return None, str(e)


def analyze_speed(speed: float) -> Tuple[str, str]:
    """
    Analyze the motor speed and determine status and message.
    
    Args:
        speed: Current motor speed
        
    Returns:
        Tuple of (status, message)
    """
    if speed <= SPEED_RANGES["stopped"][1]:
        return "stopped", f"SPEED = {speed:.2f} => MOTOR STOPPED"
        
    elif speed <= SPEED_RANGES["slow"][1]:
        return "slow", f"SPEED = {speed:.2f} => WARNING SLOW SPEED!"
        
    elif speed <= SPEED_RANGES["normal"][1]:
        return "normal", f"SPEED = {speed:.2f} => NORMAL SPEED"
        
    else:
        return "high", f"SPEED = {speed:.2f} => WARNING HIGH SPEED!"


def main():
    """Main application entry point."""
    try:
        # Parse command-line arguments
        args = parse_args()
        
        # Configure logging
        if args.verbose:
            import logging
            logging.getLogger().setLevel(logging.DEBUG)
        
        # Load config file if specified
        if args.config:
            config.load_from_file(args.config)
            
        # Set up configuration with fallbacks
        for section, items in DEFAULT_CONFIG.items():
            if section not in config:
                config[section] = {}
            for key, value in items.items():
                if key not in config[section]:
                    config[section][key] = value
        
        # Get configuration values
        db_path = args.db_path or config['database']['path']
        table_name = config['database']['table_name']
        row_id = config['database']['row_id']
        
        interval = args.interval or config['maintainer']['interval']
        model_path = args.model_path or config['maintainer']['model_path']
        rpm_conversion = config['maintainer']['rpm_conversion_factor']
        speed_index = config['maintainer']['speed_field_index']
        
        # Ensure model directory exists
        model_dir = os.path.dirname(model_path)
        if model_dir and not os.path.exists(model_dir):
            os.makedirs(model_dir)
            logger.info(f"Created directory for model: {model_dir}")
        
        # Connect to database
        conn = connect_to_database(db_path)
        
        # Load ML model if it exists, otherwise proceed without it
        model = None
        try:
            model = load_ml_model(model_path)
        except FileNotFoundError:
            logger.warning(f"Model file not found at {model_path}, continuing without ML predictions")
        
        logger.info(f"Starting maintenance monitor with interval={interval}s")
        
        # Main monitoring loop
        try:
            while True:
                start_time = time.time()
                
                # Get motor data
                data, error = get_motor_data(conn, table_name, row_id)
                
                if error:
                    logger.error(f"Error getting motor data: {error}")
                    time.sleep(interval)
                    continue
                
                # Extract and analyze speed
                raw_speed_value = data[speed_index] if data and len(data) > speed_index else 0
                speed = raw_speed_value * rpm_conversion
                
                # Analyze speed
                status, message = analyze_speed(speed)
                
                # Log status message
                if status in ["slow", "high"]:
                    logger.warning(message)
                else:
                    logger.info(message)
                    
                # Add ML prediction if model is available
                if model is not None and data:
                    try:
                        # Remove ID column for prediction
                        features = np.array(data[1:])
                        prediction = model.predict([features])[0]
                        logger.info(f"ML model prediction: {prediction}")
                    except Exception as e:
                        logger.exception(f"Error in ML prediction: {e}")
                
                # Calculate sleep time to maintain interval
                elapsed = time.time() - start_time
                sleep_time = max(0, interval - elapsed)
                
                if sleep_time > 0:
                    time.sleep(sleep_time)
                    
        except KeyboardInterrupt:
            logger.info("Maintenance monitor stopped by user")
            
        finally:
            # Clean up resources
            conn.close()
            logger.info("Database connection closed")
            
        return 0
        
    except Exception as e:
        logger.exception(f"Error in maintainer application: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
