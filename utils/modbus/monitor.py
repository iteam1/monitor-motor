"""
Modbus monitoring utilities.

This module provides classes and functions for continuously monitoring
Modbus devices and processing the read values.
"""

import time
import datetime
from typing import Optional, List, Callable, Any
from pymodbus.client import ModbusSerialClient
from pymodbus.exceptions import ModbusException

from utils.logger import get_logger
from utils.config import config
from utils.modbus.client import create_modbus_client, connect_client, close_client

logger = get_logger(__name__)


class ModbusMonitor:
    """
    Class for continuously monitoring a Modbus device.
    """
    
    def __init__(
        self,
        client: Optional[ModbusSerialClient] = None,
        **client_kwargs
    ):
        """
        Initialize the ModbusMonitor.
        
        Args:
            client: An existing ModbusSerialClient instance, or None to create a new one
            **client_kwargs: Arguments to pass to create_modbus_client if client is None
        """
        # Get configuration
        modbus_config = config.get('modbus', {})
        self.slave_id = client_kwargs.pop('slave_id', modbus_config.get('slave_id', 2))
        self.sleep_time = modbus_config.get('sleep_time', 2)
        
        # Create or use provided client
        if client is None:
            self.client = create_modbus_client(**client_kwargs)
            self.owns_client = True
        else:
            self.client = client
            self.owns_client = False
            
        # Default register settings
        self.address_start = 0x00  # Start at register 40001
        self.count = 125  # Read 125 registers
        
        logger.info(f"ModbusMonitor initialized with slave_id={self.slave_id}")
        
    def __enter__(self):
        """
        Context manager entry point.
        """
        self.connect()
        return self
        
    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        Context manager exit point.
        """
        if self.owns_client:
            close_client(self.client)
            
    def connect(self) -> bool:
        """
        Connect to the Modbus device.
        
        Returns:
            True if connection successful, False otherwise
        """
        return connect_client(self.client)
        
    def read_registers(self) -> List[int]:
        """
        Read holding registers from the device.
        
        Returns:
            List of register values, or empty list on error
        """
        try:
            result = self.client.read_holding_registers(
                address=self.address_start,
                count=self.count,
                slave=self.slave_id
            )
            
            if result.isError():
                logger.error(f"Error reading registers: {result}")
                return []
                
            return result.registers
            
        except ModbusException as e:
            logger.exception(f"Modbus exception reading registers: {e}")
            return []
        except Exception as e:
            logger.exception(f"Exception reading registers: {e}")
            return []
            
    def monitor_continuous(
        self,
        callback: Optional[Callable[[List[int], float], Any]] = None,
        max_iterations: Optional[int] = None,
        sleep_time: Optional[float] = None
    ) -> None:
        """
        Continuously monitor the device and process readings.
        
        Args:
            callback: Function to call with each set of readings
            max_iterations: Maximum number of iterations, or None for infinite
            sleep_time: Time to sleep between readings, or None to use default
        """
        if not connect_client(self.client):
            logger.error("Failed to connect to Modbus device, aborting monitoring")
            return
            
        sleep_time = sleep_time if sleep_time is not None else self.sleep_time
        iterations = 0
        
        try:
            logger.info(f"Starting continuous monitoring with sleep_time={sleep_time}")
            
            while max_iterations is None or iterations < max_iterations:
                # Get current timestamp
                current_datetime = datetime.datetime.now()
                timestamp = current_datetime.timestamp()
                
                # Read registers
                registers = self.read_registers()
                
                if registers:
                    logger.info(f"Read {len(registers)} registers at {timestamp}")
                    
                    # Call callback function if provided
                    if callback is not None:
                        callback(registers, timestamp)
                else:
                    logger.warning("No registers read")
                    
                iterations += 1
                time.sleep(sleep_time)
                
        except KeyboardInterrupt:
            logger.info("Monitoring stopped by user")
        except Exception as e:
            logger.exception(f"Error in continuous monitoring: {e}")
        finally:
            if self.owns_client:
                close_client(self.client)
                
    def simple_monitor(self, max_iterations: Optional[int] = None) -> None:
        """
        Simple monitoring that just prints register values.
        
        Args:
            max_iterations: Maximum number of iterations, or None for infinite
        """
        def print_callback(registers, timestamp):
            logger.info(f"Timestamp: {timestamp}")
            logger.info(f"Registers: {registers}")
            
        self.monitor_continuous(callback=print_callback, max_iterations=max_iterations)
