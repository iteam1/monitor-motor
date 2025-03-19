#!/usr/bin/env python3
"""
Test script for the SinamicV20 motor controller.

This script tests basic functionality of the SinamicV20 class,
including connection and reading of various registers.

Usage:
    python -m tests.modbus.test_motor
"""

import time
import argparse
import logging
from typing import List, Optional, Dict, Any

from pymodbus.client import ModbusSerialClient

from utils.logger import get_logger
from utils.config import config
from utils.modbus.client import create_modbus_client, connect_client, close_client
from utils.modbus.motor import SinamicV20

logger = get_logger(__name__)


def parse_args():
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(description='Test SinamicV20 motor controller')
    
    parser.add_argument('--port', type=str, 
                       help='Serial port (e.g. /dev/ttyUSB0)')
    parser.add_argument('--method', type=str, choices=['rtu', 'ascii'], 
                       help='Modbus method')
    parser.add_argument('--baudrate', type=int, 
                       help='Baud rate')
    parser.add_argument('--slave-id', type=int, 
                       help='Slave ID')
    parser.add_argument('--sleep', type=float, default=1.0,
                       help='Sleep time between operations')
    parser.add_argument('--verbose', '-v', action='store_true',
                       help='Enable verbose output')
    
    return parser.parse_args()


def test_single_address(inverter: SinamicV20, address: int) -> None:
    """
    Test reading a single address from the inverter.
    
    Args:
        inverter: SinamicV20 instance
        address: Address to read
    """
    try:
        result = inverter.read_raw_single_address(address)
        param_name = inverter.address_to_param[address]['NAME']
        param_unit = inverter.address_to_param[address]['UNIT']
        
        logger.info(f"Address: {address}, Name: {param_name}, Value: {result} {param_unit}")
    except Exception as e:
        logger.exception(f"Error reading address {address}: {e}")


def test_multi_address(inverter: SinamicV20, addresses: List[int]) -> None:
    """
    Test reading multiple addresses from the inverter.
    
    Args:
        inverter: SinamicV20 instance
        addresses: List of addresses to read
    """
    try:
        results = inverter.read_raw_multi_address(addresses)
        
        for i, address in enumerate(addresses):
            param_name = inverter.address_to_param[address]['NAME']
            param_unit = inverter.address_to_param[address]['UNIT']
            
            logger.info(f"Address: {address}, Name: {param_name}, Value: {results[i]} {param_unit}")
            
    except Exception as e:
        logger.exception(f"Error reading addresses {addresses}: {e}")


def test_all_addresses(inverter: SinamicV20) -> None:
    """
    Test reading all addresses from the inverter.
    
    Args:
        inverter: SinamicV20 instance
    """
    try:
        results = inverter.read_raw_all_address()
        
        for i, address in enumerate(inverter.ADDRESS_LIST):
            param_name = inverter.address_to_param[address]['NAME']
            param_unit = inverter.address_to_param[address]['UNIT']
            
            logger.info(f"Address: {address}, Name: {param_name}, Value: {results[i]} {param_unit}")
            
    except Exception as e:
        logger.exception(f"Error reading all addresses: {e}")


def test_to_dict(inverter: SinamicV20) -> None:
    """
    Test converting readings to a dictionary.
    
    Args:
        inverter: SinamicV20 instance
    """
    try:
        results = inverter.read_raw_all_address_convert_dict()
        
        for name, value in results.items():
            logger.info(f"Name: {name}, Value: {value}")
            
    except Exception as e:
        logger.exception(f"Error converting readings to dictionary: {e}")


def main():
    """Run the motor controller tests."""
    args = parse_args()
    
    # Configure logging
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    
    # Load configuration
    modbus_config = config.get('modbus', {})
    
    # Use command-line args if provided, otherwise use config
    port = args.port or modbus_config.get('port', '/dev/ttyUSB0')
    method = args.method or modbus_config.get('method', 'rtu')
    baudrate = args.baudrate or modbus_config.get('baudrate', 9600)
    slave_id = args.slave_id or modbus_config.get('slave_id', 2)
    
    logger.info(f"Testing SinamicV20 on port {port} with method {method}, baudrate {baudrate}, slave_id {slave_id}")
    
    # Create client
    client = create_modbus_client(
        method=method,
        port=port,
        baudrate=baudrate
    )
    
    # Connect to client
    if not connect_client(client):
        logger.error("Failed to connect to client")
        return 1
        
    try:
        # Create inverter instance
        inverter = SinamicV20(client=client, slave_id=slave_id)
        
        # Test single address reading
        logger.info("\n--- TEST READING SINGLE ADDRESS ---")
        test_addresses = [40023, 40521, 40028]  # Example addresses to test
        
        for addr in test_addresses:
            test_single_address(inverter, addr)
            time.sleep(args.sleep)
        
        # Test multi-address reading
        logger.info("\n--- TEST READING MULTIPLE ADDRESSES ---")
        test_multi_address(inverter, test_addresses)
        time.sleep(args.sleep)
        
        # Test all address reading
        logger.info("\n--- TEST READING ALL ADDRESSES ---")
        test_all_addresses(inverter)
        time.sleep(args.sleep)
        
        # Test dictionary conversion
        logger.info("\n--- TEST CONVERTING TO DICTIONARY ---")
        test_to_dict(inverter)
        
        logger.info("\nAll tests completed successfully")
        return 0
        
    except Exception as e:
        logger.exception(f"Test failed: {e}")
        return 1
    finally:
        # Close client connection
        close_client(client)


if __name__ == "__main__":
    exit(main())
