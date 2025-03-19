"""
Configuration settings for ModCon.

This module provides functions for loading and managing configuration
settings from environment variables and configuration files.
"""

import os
import json
from typing import Dict, Any
from pathlib import Path

# Default configuration values
DEFAULT_CONFIG = {
    'modbus': {
        'port': '/dev/ttyUSB0',
        'method': 'rtu',
        'stopbits': 1,
        'bytesize': 8,
        'parity': 'N',
        'baudrate': 9600,
        'slave_id': 2,
        'timeout': 3.0
    },
    'database': {
        'path': 'data/inverter.db',
        'table_name': 'sinamicv20',
        'default_id': 0
    },
    'data_collection': {
        'n_samples': 100,
        'csv_file': 'data/data.csv',
        'sleep_time': 2
    },
    'visualization': {
        'update_interval': 50,
        'n_points': 100,
        'line_color': (255, 0, 0)
    }
}

# Global configuration object
config: Dict[str, Any] = {}


def load_config(config_file: str = None) -> Dict[str, Any]:
    """
    Load configuration from a file and/or environment variables.
    
    Args:
        config_file: Path to the configuration JSON file.
        
    Returns:
        The loaded configuration dictionary.
    """
    global config
    
    # Start with default configuration
    config = DEFAULT_CONFIG.copy()
    
    # Load from config file if specified
    if config_file and Path(config_file).exists():
        try:
            with open(config_file, 'r') as f:
                file_config = json.load(f)
                _update_nested_dict(config, file_config)
        except (json.JSONDecodeError, IOError) as e:
            print(f"Error loading configuration file: {e}")
    
    # Override with environment variables
    # Environment variables should be in the format MODCON_SECTION_KEY
    for env_name, env_value in os.environ.items():
        if env_name.startswith('MODCON_'):
            parts = env_name.lower().split('_')
            if len(parts) >= 3:
                section = parts[1]
                key = '_'.join(parts[2:])
                
                if section in config and key in config[section]:
                    # Convert to the appropriate type
                    original_value = config[section][key]
                    if isinstance(original_value, int):
                        config[section][key] = int(env_value)
                    elif isinstance(original_value, float):
                        config[section][key] = float(env_value)
                    elif isinstance(original_value, bool):
                        config[section][key] = env_value.lower() in ('true', 'yes', '1')
                    else:
                        config[section][key] = env_value
    
    return config


def _update_nested_dict(base_dict: Dict[str, Any], update_dict: Dict[str, Any]) -> None:
    """
    Update a nested dictionary recursively.
    
    Args:
        base_dict: Base dictionary to update.
        update_dict: Dictionary with updates to apply.
    """
    for key, value in update_dict.items():
        if key in base_dict and isinstance(base_dict[key], dict) and isinstance(value, dict):
            _update_nested_dict(base_dict[key], value)
        else:
            base_dict[key] = value


# Initialize configuration on module import
load_config()
