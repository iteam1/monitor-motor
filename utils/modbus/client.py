"""
Modbus client utilities.

This module provides functions for creating and managing Modbus RTU clients
for communication with industrial devices.
"""

import logging
from typing import Optional, Dict, Any
from pymodbus.client import ModbusSerialClient
from pymodbus.exceptions import ModbusException

from utils.config import config
from utils.logger import get_logger

logger = get_logger(__name__)


def create_modbus_client(
    method: Optional[str] = None,
    port: Optional[str] = None,
    stopbits: Optional[int] = None,
    bytesize: Optional[int] = None,
    parity: Optional[str] = None,
    baudrate: Optional[int] = None,
    timeout: Optional[float] = None,
    unit: Optional[int] = None
) -> ModbusSerialClient:
    """
    Create a Modbus RTU client with the specified parameters.
    
    If any parameter is None, it will use the value from the configuration.
    
    Args:
        method: Modbus method ('rtu' or 'ascii')
        port: Serial port
        stopbits: Number of stop bits
        bytesize: Number of data bits
        parity: Parity ('N' for none, 'E' for even, 'O' for odd)
        baudrate: Baud rate
        timeout: Timeout in seconds
        unit: Unit ID
        
    Returns:
        A configured ModbusSerialClient instance
    """
    # Use configuration values if parameters not provided
    modbus_config = config.get('modbus', {})
    
    method = method or modbus_config.get('method', 'rtu')
    port = port or modbus_config.get('port', '/dev/ttyUSB0')
    stopbits = stopbits or modbus_config.get('stopbits', 1)
    bytesize = bytesize or modbus_config.get('bytesize', 8)
    parity = parity or modbus_config.get('parity', 'N')
    baudrate = baudrate or modbus_config.get('baudrate', 9600)
    timeout = timeout or modbus_config.get('timeout', 3.0)
    unit = unit or 1  # Default unit ID if not explicitly in config
    
    logger.info(f"Creating Modbus client for port {port} with method {method}")
    
    client = ModbusSerialClient(
        method=method,
        port=port,
        stopbits=stopbits,
        bytesize=bytesize,
        parity=parity,
        baudrate=baudrate,
        timeout=timeout,
        unit=unit
    )
    
    return client


def connect_client(client: ModbusSerialClient) -> bool:
    """
    Connect to a Modbus RTU client.
    
    Args:
        client: The ModbusSerialClient to connect
        
    Returns:
        True if connection successful, False otherwise
    """
    try:
        connected = client.connect()
        if connected:
            logger.info("Successfully connected to Modbus device")
        else:
            logger.error("Failed to connect to Modbus device")
        return connected
    except Exception as e:
        logger.exception("Error connecting to Modbus device")
        return False


def close_client(client: ModbusSerialClient) -> None:
    """
    Close the connection to a Modbus RTU client.
    
    Args:
        client: The ModbusSerialClient to disconnect
    """
    try:
        client.close()
        logger.info("Disconnected from Modbus device")
    except Exception as e:
        logger.exception("Error disconnecting from Modbus device")
