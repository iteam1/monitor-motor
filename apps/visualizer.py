#!/usr/bin/env python3
"""
Database Visualization Application

This application visualizes motor speed data from the database using
a real-time plot with PyQtGraph.

Usage:
    python -m apps.visualizer [--config CONFIG_FILE]
"""

import os
import sys
import sqlite3
import argparse
from typing import List, Any, Optional, Tuple

import pyqtgraph as pg
from PyQt5 import QtWidgets, QtCore

from utils.logger import get_logger
from utils.config import config
from utils.database.operations import execute_query
from utils.visualization.realtime_plot import RealtimePlot

logger = get_logger(__name__)

# Default configuration
DEFAULT_CONFIG = {
    "database": {
        "path": "data/inverter.db",
        "table_name": "sinamicv20",
        "row_id": 0
    },
    "visualization": {
        "n_points": 100,
        "update_interval": 50,
        "rpm_conversion_factor": 8.10/242,
        "title": "Motor Speed Visualization",
        "y_label": "Speed (RPM)",
        "x_label": "Time (samples)",
        "y_range": [0, 20]
    }
}


def parse_args():
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(description='Visualize motor speed data from database')
    parser.add_argument('--config', type=str, help='Path to configuration file')
    parser.add_argument('--interval', type=int, help='Update interval in milliseconds')
    parser.add_argument('--db-path', type=str, help='Database file path')
    parser.add_argument('--points', type=int, help='Number of data points to display')
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


class DatabaseVisualizer(QtWidgets.QMainWindow):
    """
    Main window for visualizing database data.
    
    This class creates a window with a real-time plot that
    displays motor speed data from a SQLite database.
    """
    
    def __init__(
        self,
        db_path: str,
        table_name: str, 
        row_id: int,
        n_points: int = 100,
        update_interval: int = 50,
        rpm_conversion: float = 8.10/242,
        title: Optional[str] = None,
        y_label: Optional[str] = None,
        x_label: Optional[str] = None,
        y_range: Optional[Tuple[float, float]] = None
    ):
        """
        Initialize the database visualizer.
        
        Args:
            db_path: Path to the database file
            table_name: Name of the table to query
            row_id: ID of the row to fetch
            n_points: Number of data points to display
            update_interval: Update interval in milliseconds
            rpm_conversion: Conversion factor from raw speed to RPM
            title: Plot title
            y_label: Y-axis label
            x_label: X-axis label
            y_range: Y-axis range as (min, max)
        """
        super(DatabaseVisualizer, self).__init__()
        
        # Set window properties
        self.setWindowTitle(title or "Database Visualizer")
        self.resize(800, 600)
        
        # Store parameters
        self.db_path = db_path
        self.table_name = table_name
        self.row_id = row_id
        self.rpm_conversion = rpm_conversion
        
        # Initialize database connection
        try:
            self.conn = connect_to_database(db_path)
            self.cursor = self.conn.cursor()
        except Exception as e:
            logger.exception(f"Error initializing database connection: {e}")
            raise
        
        # Create plot
        self.plot = RealtimePlot(
            n_points=n_points,
            update_interval_ms=update_interval,
            background_color='k',  # black background
            line_color=(255, 0, 0),  # red line
            title=title,
            y_label=y_label,
            x_label=x_label,
            y_range=y_range
        )
        
        # Set up the central widget
        self.setCentralWidget(self.plot.create_widget())
        
        # Start the plot updates
        self.plot.start_timer(update_callback=self._get_speed_data)
        
        logger.info("Database visualizer initialized")
    
    def _get_speed_data(self) -> float:
        """
        Get speed data from the database.
        
        Returns:
            The current motor speed in RPM, or 0 if there was an error
        """
        try:
            query = f"SELECT SPEED FROM {self.table_name} WHERE ID = {self.row_id}"
            result = execute_query(self.conn, query)
            
            if not result or not result[0]:
                logger.warning("No data found in database")
                return 0.0
                
            # Extract and convert speed value
            raw_speed = result[0][0]
            speed = raw_speed * self.rpm_conversion
            
            logger.debug(f"Current speed: {speed:.2f} RPM")
            return speed
            
        except Exception as e:
            logger.exception(f"Error getting speed data: {e}")
            return 0.0
    
    def closeEvent(self, event: Any) -> None:
        """
        Handle window close event.
        
        Args:
            event: Close event
        """
        try:
            # Stop the timer
            if hasattr(self, 'plot') and self.plot.timer is not None:
                self.plot.stop_timer()
                
            # Close database connection
            if hasattr(self, 'conn'):
                self.conn.close()
                logger.info("Database connection closed")
                
        except Exception as e:
            logger.exception(f"Error during shutdown: {e}")
            
        # Accept the close event
        event.accept()
        logger.info("Application closed")


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
        
        n_points = args.points or config['visualization']['n_points']
        update_interval = args.interval or config['visualization']['update_interval']
        rpm_conversion = config['visualization']['rpm_conversion_factor']
        title = config['visualization']['title']
        y_label = config['visualization']['y_label']
        x_label = config['visualization']['x_label']
        y_range = config['visualization']['y_range']
        
        # Ensure database directory exists
        db_dir = os.path.dirname(db_path)
        if db_dir and not os.path.exists(db_dir):
            os.makedirs(db_dir)
            logger.info(f"Created directory for database: {db_dir}")
            
        logger.info("Starting database visualizer")
        
        # Create and run the application
        app = QtWidgets.QApplication(sys.argv)
        window = DatabaseVisualizer(
            db_path=db_path,
            table_name=table_name,
            row_id=row_id,
            n_points=n_points,
            update_interval=update_interval,
            rpm_conversion=rpm_conversion,
            title=title,
            y_label=y_label,
            x_label=x_label,
            y_range=y_range
        )
        window.show()
        
        return app.exec_()
        
    except Exception as e:
        logger.exception(f"Error in visualizer application: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
