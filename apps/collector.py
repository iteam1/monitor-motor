#!/usr/bin/env python3
"""
Modbus Data Collector Application

This application connects to a Siemens Sinamics V20 inverter via Modbus,
collects data at regular intervals, and stores it in a SQLite database.

Usage:
    python -m apps.collector [--config CONFIG_FILE]
"""

import os
import sys
import time
import argparse
import sqlite3
from typing import Dict, Any, Optional

from utils.logger import get_logger
from utils.config import config
from utils.modbus.client import create_modbus_client, connect_client, close_client
from utils.modbus.motor import SinamicV20
from utils.database.operations import create_database_if_not_exists, generate_update_query

logger = get_logger(__name__)


def parse_args():
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(description='Collect data from Modbus device')
    parser.add_argument('--config', type=str, help='Path to configuration file')
    parser.add_argument('--interval', type=float, help='Data collection interval in seconds')
    parser.add_argument('--port', type=str, help='Modbus serial port')
    parser.add_argument('--db-path', type=str, help='Database file path')
    parser.add_argument('--verbose', '-v', action='store_true', help='Enable verbose output')
    return parser.parse_args()


def init_database(db_path: str, table_name: str) -> sqlite3.Connection:
    """
    Initialize the database connection and create table if needed.
    
    Args:
        db_path: Path to the SQLite database file
        table_name: Name of the table to use
        
    Returns:
        Database connection object
    """
    try:
        # Create directory if it doesn't exist
        db_dir = os.path.dirname(db_path)
        if db_dir and not os.path.exists(db_dir):
            os.makedirs(db_dir)
            logger.info(f"Created directory for database: {db_dir}")
        
        # Connect to database
        conn = sqlite3.connect(db_path)
        
        # Create table if it doesn't exist
        create_database_if_not_exists(conn, table_name)
        
        logger.info(f"Database initialized at {db_path}")
        return conn
        
    except Exception as e:
        logger.exception(f"Error initializing database: {e}")
        raise


def collect_and_store_data(
    inverter: SinamicV20,
    conn: sqlite3.Connection,
    table_name: str,
    row_id: int = 0
) -> bool:
    """
    Collect data from the inverter and store it in the database.
    
    Args:
        inverter: SinamicV20 instance
        conn: Database connection
        table_name: Table name to update
        row_id: ID of the row to update
        
    Returns:
        True if successful, False otherwise
    """
    try:
        # Get data from inverter
        data = inverter.read_raw_all_address_convert_dict()
        
        if not data:
            logger.warning("No data received from inverter")
            return False
            
        # Generate update query
        update_query = generate_update_query(table_name, data, row_id)
        
        # Execute query
        cursor = conn.cursor()
        cursor.execute(update_query)
        conn.commit()
        
        logger.debug(f"Data collected and stored with {len(data)} parameters")
        return True
        
    except Exception as e:
        logger.exception(f"Error collecting and storing data: {e}")
        return False


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
            
        # Get configuration
        modbus_config = config.get('modbus', {})
        database_config = config.get('database', {})
        collector_config = config.get('collector', {})
        
        # Use command-line args if provided, otherwise use config
        port = args.port or modbus_config.get('port', '/dev/ttyUSB0')
        method = modbus_config.get('method', 'rtu')
        baudrate = modbus_config.get('baudrate', 9600)
        slave_id = modbus_config.get('slave_id', 2)
        
        db_path = args.db_path or database_config.get('path', 'data/inverter.db')
        table_name = database_config.get('table_name', 'sinamicv20')
        row_id = database_config.get('row_id', 0)
        
        interval = args.interval or collector_config.get('interval', 1.0)
        
        logger.info(f"Starting data collector with interval={interval}s, port={port}")
        
        # Create and connect to Modbus client
        client = create_modbus_client(
            method=method,
            port=port,
            baudrate=baudrate
        )
        
        if not connect_client(client):
            logger.error("Failed to connect to Modbus client")
            return 1
            
        # Create inverter instance
        inverter = SinamicV20(client=client, slave_id=slave_id)
        
        # Initialize database
        conn = init_database(db_path, table_name)
        
        # Main collection loop
        try:
            logger.info("Starting data collection loop")
            
            while True:
                start_time = time.time()
                
                # Collect and store data
                success = collect_and_store_data(inverter, conn, table_name, row_id)
                
                if success:
                    logger.info("Data collection cycle completed successfully")
                else:
                    logger.warning("Data collection cycle completed with errors")
                
                # Calculate sleep time to maintain interval
                elapsed = time.time() - start_time
                sleep_time = max(0, interval - elapsed)
                
                if sleep_time > 0:
                    time.sleep(sleep_time)
                    
        except KeyboardInterrupt:
            logger.info("Data collection stopped by user")
            
        finally:
            # Clean up resources
            conn.close()
            close_client(client)
            logger.info("Resources cleaned up")
            
        return 0
        
    except Exception as e:
        logger.exception(f"Error in collector application: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
