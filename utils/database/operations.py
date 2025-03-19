"""
Database operations for ModCon.

This module provides functions for common database operations,
such as creating tables and generating SQL queries.
"""

import sqlite3
import logging
from typing import Dict, Any, Union, List, Optional
from pathlib import Path

from utils.logger import get_logger
from utils.config import config

logger = get_logger(__name__)


def create_database(db_path: Optional[str] = None, table_name: Optional[str] = None) -> None:
    """
    Create the database and tables needed for the ModCon application.
    
    Args:
        db_path: Path to the SQLite database file
        table_name: Name of the table to create
    """
    db_config = config.get('database', {})
    db_path = db_path or db_config.get('path', 'data/inverter.db')
    table_name = table_name or db_config.get('table_name', 'sinamicv20')
    
    # Ensure directory exists
    Path(db_path).parent.mkdir(parents=True, exist_ok=True)
    
    logger.info(f"Creating database at {db_path} with table {table_name}")
    
    try:
        conn = sqlite3.connect(db_path)
        c = conn.cursor()
        
        # Create the table with all the parameters for the Sinamics V20 inverter
        c.execute(f"""
            CREATE TABLE IF NOT EXISTS {table_name} (
                ID INT PRIMARY KEY,
                WDOG_TIME INT,
                WDOG_ACTION INT,
                FREQ_REF INT,
                RUN_ENABLE INT,
                CMD_FWD_REV INT,
                CMD_START INT,
                FAULT_ACK INT,
                PID_SETP_REF INT,
                ENABLE_PID INT,
                CURRENT_LMT INT,
                ACCEL_TIME INT,
                DECEL_TIME INT,
                DIGITAL_OUT_1 INT,
                DIGITAL_OUT_2 INT,
                REF_FREQ INT,
                PID_UP_LMT INT,
                PID_LO_LMT INT,
                P_GAIN INT,
                I_GAIN INT,
                D_GAIN INT,
                FEEDBK_GAIN INT,
                LOW_PASS INT,
                FREQ_OUTPUT INT,
                SPEED INT,
                CURRENT INT,
                TORQUE INT,
                ACTUAL_PWR INT,
                TOTAL_KWH INT,
                DC_BUS_VOLTS INT,
                REFERENCE INT,
                RATED_PWR INT,
                OUTPUT_VOLTS INT,
                FWD_REV INT,
                STOP_RUN INT,
                AT_MAX_FREQ INT,
                CONTROL_MODE INT,
                ENABLED INT,
                READY_TO_RUN INT,
                ANALOG_IN_1 INT,
                ANALOG_IN_2 INT,
                ANALOG_OUT_1 INT,
                FREQ_ACTUAL INT,
                PID_SETP_OUT INT,
                PID_OUTPUT INT,
                PID_FEEDBACK INT,
                DIGITAL_IN_1 INT,
                DIGITAL_IN_2 INT,
                DIGITAL_IN_3 INT,
                DIGITAL_IN_4 INT,
                FAULT INT,
                LAST_FAULT INT,
                FAULT_1 INT,
                FAULT_2 INT,
                FAULT_3 INT,
                WARNING INT,
                LAST_WARNING INT,
                INVERTER_VER INT,
                DRIVE_MODEL INT,
                STW INT,
                HSW INT,
                ZSW INT,
                HIW INT,
                INVERTER_MODEL INT,
                HAND_AUTO INT,
                FAULT_4 INT,
                FAULT_5 INT,
                FAULT_6 INT,
                FAULT_7 INT,
                FAULT_8 FLOAT,
                PRM_ERROR_CODE INT,
                PI_FEEDBACK INT
            )
        """)
        
        # Check if we need to insert the initial row
        c.execute(f"SELECT COUNT(*) FROM {table_name} WHERE ID = 0")
        count = c.fetchone()[0]
        
        if count == 0:
            # Insert initial values
            c.execute(f"""
                INSERT INTO {table_name} (
                    ID, WDOG_TIME, WDOG_ACTION, FREQ_REF, RUN_ENABLE, CMD_FWD_REV, CMD_START,
                    FAULT_ACK, PID_SETP_REF, ENABLE_PID, CURRENT_LMT, ACCEL_TIME, DECEL_TIME,
                    DIGITAL_OUT_1, DIGITAL_OUT_2, REF_FREQ, PID_UP_LMT, PID_LO_LMT, P_GAIN,
                    I_GAIN, D_GAIN, FEEDBK_GAIN, LOW_PASS, FREQ_OUTPUT, SPEED, CURRENT,
                    TORQUE, ACTUAL_PWR, TOTAL_KWH, DC_BUS_VOLTS, REFERENCE, RATED_PWR,
                    OUTPUT_VOLTS, FWD_REV, STOP_RUN, AT_MAX_FREQ, CONTROL_MODE, ENABLED,
                    READY_TO_RUN, ANALOG_IN_1, ANALOG_IN_2, ANALOG_OUT_1, FREQ_ACTUAL,
                    PID_SETP_OUT, PID_OUTPUT, PID_FEEDBACK, DIGITAL_IN_1, DIGITAL_IN_2,
                    DIGITAL_IN_3, DIGITAL_IN_4, FAULT, LAST_FAULT, FAULT_1, FAULT_2, FAULT_3,
                    WARNING, LAST_WARNING, INVERTER_VER, DRIVE_MODEL, STW, HSW, ZSW, HIW,
                    INVERTER_MODEL, HAND_AUTO, FAULT_4, FAULT_5, FAULT_6, FAULT_7, FAULT_8,
                    PRM_ERROR_CODE, PI_FEEDBACK
                )
                VALUES (
                    0, 0, 0, 0, 0, 0, 0, 999, 0, 1186, 1000, 1000, 1, 0, 1500, 10000, 0, 3000,
                    0, 0, 10000, 10000, 0, 0, 0, 0, 0, 17, 315, 7, 55, 0, 1, 0, 0, 1, 1, 0, 0,
                    21, 0, 0, 999, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 394, 6307, 0, 0, 60209,
                    0, 6307, 394, 1, 0, 0, 0, 0, 0.0, 255, 12
                )
            """)
        
        conn.commit()
        logger.info("Database created successfully")
        
    except sqlite3.Error as e:
        logger.exception(f"Error creating database: {e}")
        raise
    finally:
        if 'conn' in locals():
            conn.close()


def generate_update_query_by_id(
    table_name: str, 
    data_dict: Dict[str, Any], 
    id_value: int
) -> str:
    """
    Generate an SQL UPDATE query for the specified table and data.
    
    Args:
        table_name: Name of the table to update
        data_dict: Dictionary of column names and values to update
        id_value: ID value to identify the row to update
        
    Returns:
        SQL UPDATE query string
    """
    query = f"UPDATE {table_name} SET "
    updates = []
    
    for key, value in data_dict.items():
        if isinstance(value, str):
            updates.append(f"{key} = '{value}'")
        else:
            updates.append(f"{key} = {value}")
            
    query += ", ".join(updates)
    query += f" WHERE ID = {id_value}"
    query += ";"
    
    return query


def execute_query(
    query: str, 
    db_path: Optional[str] = None,
    fetch_one: bool = False,
    fetch_all: bool = False
) -> Optional[Union[List[Any], Any]]:
    """
    Execute an SQL query on the database.
    
    Args:
        query: SQL query to execute
        db_path: Path to the SQLite database
        fetch_one: Whether to fetch one result
        fetch_all: Whether to fetch all results
        
    Returns:
        Query results if fetch_one or fetch_all is True, otherwise None
    """
    db_config = config.get('database', {})
    db_path = db_path or db_config.get('path', 'data/inverter.db')
    
    result = None
    
    try:
        conn = sqlite3.connect(db_path)
        c = conn.cursor()
        
        c.execute(query)
        
        if fetch_one:
            result = c.fetchone()
        elif fetch_all:
            result = c.fetchall()
            
        conn.commit()
        
    except sqlite3.Error as e:
        logger.exception(f"Error executing query: {e}")
        raise
    finally:
        if 'conn' in locals():
            conn.close()
            
    return result
