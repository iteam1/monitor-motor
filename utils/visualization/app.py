"""
Visualization application for Modbus data.

This module provides a standalone application for real-time visualization
of Modbus data from Siemens Sinamics V20 inverters.

Usage:
    python -m utils.visualization.app
"""

import sys
from typing import Optional, Any

from PyQt5 import QtWidgets
import pyqtgraph as pg

from utils.logger import get_logger
from utils.config import config
from utils.modbus.client import create_modbus_client, connect_client, close_client
from utils.modbus.motor import SinamicV20
from utils.visualization.realtime_plot import RealtimePlot

logger = get_logger(__name__)


class ModbusVisualizationApp(QtWidgets.QMainWindow):
    """
    Main application window for Modbus data visualization.
    
    This class creates a window with a real-time plot that
    displays data from a Modbus device.
    """
    
    def __init__(
        self, 
        port: Optional[str] = None,
        method: Optional[str] = None,
        baudrate: Optional[int] = None,
        slave_id: Optional[int] = None,
        address: Optional[int] = None,
        n_samples: Optional[int] = None,
        title: Optional[str] = None,
        y_label: Optional[str] = None,
        update_interval: Optional[int] = None
    ):
        """
        Initialize the visualization application.
        
        Args:
            port: Modbus serial port
            method: Modbus method ('rtu' or 'ascii')
            baudrate: Serial baudrate
            slave_id: Modbus slave ID
            address: Modbus register address to monitor
            n_samples: Number of data points to display
            title: Window title
            y_label: Y-axis label
            update_interval: Update interval in milliseconds
        """
        super(ModbusVisualizationApp, self).__init__()
        
        # Load configuration
        modbus_config = config.get('modbus', {})
        vis_config = config.get('visualization', {})
        
        # Set parameters, prioritizing constructor arguments over config
        self.port = port or modbus_config.get('port', '/dev/ttyUSB0')
        self.method = method or modbus_config.get('method', 'rtu')
        self.baudrate = baudrate or modbus_config.get('baudrate', 9600)
        self.slave_id = slave_id or modbus_config.get('slave_id', 2)
        self.address = address or vis_config.get('address', 40025)  # Default to frequency
        
        self.n_samples = n_samples or vis_config.get('n_samples', 100)
        self.title = title or vis_config.get('title', 'Modbus Data Visualization')
        self.y_label = y_label or vis_config.get('y_label', 'Value')
        self.update_interval = update_interval or vis_config.get('update_interval', 50)
        
        # Initialize UI and connections
        self._init_modbus_connection()
        self._init_ui()
        
        logger.info(f"Initialized ModbusVisualizationApp with address={self.address}")
    
    def _init_modbus_connection(self) -> None:
        """Initialize the Modbus connection."""
        try:
            # Create and connect Modbus client
            self.client = create_modbus_client(
                method=self.method,
                port=self.port,
                baudrate=self.baudrate
            )
            
            if not connect_client(self.client):
                logger.error("Failed to connect to Modbus device")
                raise ConnectionError("Failed to connect to Modbus device")
                
            # Create inverter instance
            self.inverter = SinamicV20(client=self.client, slave_id=self.slave_id)
            logger.info(f"Connected to Modbus device on {self.port}")
            
        except Exception as e:
            logger.exception(f"Error initializing Modbus connection: {e}")
            raise
    
    def _init_ui(self) -> None:
        """Initialize the user interface."""
        try:
            # Set window properties
            self.setWindowTitle(self.title)
            self.resize(800, 600)
            
            # Create the plot
            self.plot = RealtimePlot(
                n_points=self.n_samples,
                update_interval_ms=self.update_interval,
                background_color='k',  # black background
                line_color=(255, 0, 0),  # red line
                title=self.title,
                y_label=self.y_label,
                x_label="Time (samples)"
            )
            
            # Set the plot as central widget
            self.setCentralWidget(self.plot.create_widget())
            
            # Start the plot updates
            self.plot.start_timer(update_callback=self._get_modbus_data)
            
            logger.info("UI initialization complete")
            
        except Exception as e:
            logger.exception(f"Error initializing UI: {e}")
            raise
    
    def _get_modbus_data(self) -> float:
        """
        Get data from the Modbus device.
        
        Returns:
            The value read from the Modbus register, or 0 if there was an error
        """
        try:
            value = self.inverter.read_raw_single_address(self.address)
            
            if value is None:
                logger.warning(f"Failed to read address {self.address}")
                return 0.0
                
            return float(value)
            
        except Exception as e:
            logger.exception(f"Error reading Modbus data: {e}")
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
                
            # Close Modbus connection
            if hasattr(self, 'client'):
                close_client(self.client)
                logger.info("Closed Modbus connection")
                
        except Exception as e:
            logger.exception(f"Error during shutdown: {e}")
            
        # Accept the close event
        event.accept()
        logger.info("Application closed")


def run_app():
    """Run the visualization application."""
    try:
        app = QtWidgets.QApplication(sys.argv)
        window = ModbusVisualizationApp()
        window.show()
        return app.exec_()
    except Exception as e:
        logger.exception(f"Error running application: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(run_app())
