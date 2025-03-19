"""
Real-time plotting utilities for ModCon.

This module provides classes for creating real-time plots
using PyQt5 and pyqtgraph.
"""

from typing import List, Optional, Tuple, Callable, Any
from random import randint
import sys

from PyQt5 import QtWidgets, QtCore
import pyqtgraph as pg

from utils.logger import get_logger
from utils.config import config

logger = get_logger(__name__)


class RealtimePlot:
    """
    A utility class for creating real-time plots.
    
    This class provides a wrapper around pyqtgraph to make it easier
    to create and update real-time plots.
    """
    
    def __init__(
        self,
        n_points: int = 100,
        update_interval_ms: int = 50,
        background_color: str = 'w',
        line_color: Tuple[int, int, int] = (255, 0, 0),
        title: Optional[str] = None,
        x_label: Optional[str] = None,
        y_label: Optional[str] = None,
        y_range: Optional[Tuple[float, float]] = None
    ):
        """
        Initialize the real-time plot.
        
        Args:
            n_points: Number of data points to display
            update_interval_ms: Update interval in milliseconds
            background_color: Background color of the plot
            line_color: Color of the plot line as RGB tuple
            title: Plot title
            x_label: X-axis label
            y_label: Y-axis label
            y_range: Y-axis range as (min, max)
        """
        # Load configuration
        vis_config = config.get('visualization', {})
        self.n_points = n_points or vis_config.get('n_points', 100)
        self.update_interval = update_interval_ms or vis_config.get('update_interval', 50)
        
        # Initialize data
        self.x_data = list(range(self.n_points))
        self.y_data = [0] * self.n_points
        
        logger.info(f"Initialized RealtimePlot with {self.n_points} points and {self.update_interval}ms update interval")
        
        # Store parameters for later use when widget is created
        self.background_color = background_color
        self.line_color = line_color
        self.title = title
        self.x_label = x_label
        self.y_label = y_label
        self.y_range = y_range
        
        # These will be initialized when create_widget is called
        self.graph_widget = None
        self.data_line = None
        self.timer = None
        self.update_callback = None
    
    def create_widget(self, parent: Optional[QtWidgets.QWidget] = None) -> pg.PlotWidget:
        """
        Create and configure the plot widget.
        
        Args:
            parent: Parent widget, or None for no parent
            
        Returns:
            The created plot widget
        """
        # Create the plot widget
        self.graph_widget = pg.PlotWidget(parent=parent)
        
        # Configure widget appearance
        self.graph_widget.setBackground(self.background_color)
        
        # Set title and labels if provided
        if self.title:
            self.graph_widget.setTitle(self.title)
        if self.x_label:
            self.graph_widget.setLabel('bottom', self.x_label)
        if self.y_label:
            self.graph_widget.setLabel('left', self.y_label)
        if self.y_range:
            self.graph_widget.setYRange(self.y_range[0], self.y_range[1])
        
        # Create the plot line
        pen = pg.mkPen(color=self.line_color)
        self.data_line = self.graph_widget.plot(self.x_data, self.y_data, pen=pen)
        
        logger.info("Created plot widget")
        return self.graph_widget
    
    def start_timer(
        self, 
        update_callback: Optional[Callable[[], float]] = None,
        interval: Optional[int] = None
    ) -> None:
        """
        Start the update timer.
        
        Args:
            update_callback: Function to call for new data, should return a float
            interval: Update interval in milliseconds, or None to use default
        """
        if self.graph_widget is None:
            logger.error("Cannot start timer: widget not created yet")
            return
            
        if self.timer is not None:
            logger.warning("Timer already started")
            return
            
        self.update_callback = update_callback
        
        # Create and start the timer
        self.timer = QtCore.QTimer()
        self.timer.setInterval(interval or self.update_interval)
        self.timer.timeout.connect(self._update_plot_data)
        self.timer.start()
        
        logger.info(f"Started timer with interval {self.timer.interval()}ms")
    
    def stop_timer(self) -> None:
        """Stop the update timer."""
        if self.timer is not None:
            self.timer.stop()
            logger.info("Stopped timer")
    
    def _update_plot_data(self) -> None:
        """Update the plot data with a new value."""
        try:
            # Get new value from callback or generate random
            if self.update_callback is not None:
                new_value = self.update_callback()
            else:
                new_value = randint(0, 100)
            
            # Update data arrays
            self.x_data = self.x_data[1:]
            self.x_data.append(self.x_data[-1] + 1)
            
            self.y_data = self.y_data[1:]
            self.y_data.append(new_value)
            
            # Update plot
            self.data_line.setData(self.x_data, self.y_data)
            
        except Exception as e:
            logger.exception(f"Error updating plot: {e}")
    
    def set_data(self, x_data: List[float], y_data: List[float]) -> None:
        """
        Set the plot data directly.
        
        Args:
            x_data: X values
            y_data: Y values
        """
        if len(x_data) != len(y_data):
            logger.error(f"Data length mismatch: x={len(x_data)}, y={len(y_data)}")
            return
            
        self.x_data = list(x_data)
        self.y_data = list(y_data)
        
        if self.data_line is not None:
            self.data_line.setData(self.x_data, self.y_data)
            
        logger.debug(f"Set data with {len(x_data)} points")


class RealtimePlotWindow(QtWidgets.QMainWindow):
    """
    A window containing a real-time plot.
    
    This class creates a QMainWindow with a RealtimePlot as its central widget.
    """
    
    def __init__(
        self,
        *args,
        **kwargs
    ):
        """
        Initialize the real-time plot window.
        
        Args:
            *args: Arguments to pass to RealtimePlot
            **kwargs: Keyword arguments to pass to RealtimePlot
        """
        super(RealtimePlotWindow, self).__init__()
        
        # Create the plot
        self.plot = RealtimePlot(*args, **kwargs)
        
        # Setup the window
        self.setCentralWidget(self.plot.create_widget())
        
        logger.info("Created RealtimePlotWindow")
    
    def start_plotting(
        self, 
        update_callback: Optional[Callable[[], float]] = None,
        interval: Optional[int] = None
    ) -> None:
        """
        Start the real-time plot updates.
        
        Args:
            update_callback: Function to call for new data, should return a float
            interval: Update interval in milliseconds, or None to use default
        """
        self.plot.start_timer(update_callback, interval)
    
    def stop_plotting(self) -> None:
        """Stop the real-time plot updates."""
        self.plot.stop_timer()


def run_example():
    """Run a simple example of the RealtimePlotWindow."""
    app = QtWidgets.QApplication(sys.argv)
    
    # Create window with a random data generator
    window = RealtimePlotWindow(
        title="Real-time Data",
        x_label="Time (s)",
        y_label="Value",
        y_range=(0, 100)
    )
    
    # Start the random updates
    window.start_plotting()
    
    # Show the window
    window.show()
    
    # Run the application
    sys.exit(app.exec_())


if __name__ == "__main__":
    run_example()
