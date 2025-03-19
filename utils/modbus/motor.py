"""
Siemens Sinamics V20 motor control class.

This module provides a class for interfacing with Siemens Sinamics V20 
inverters via Modbus RTU protocol. It handles reading and writing parameters,
controlling the motor, and monitoring its status.
"""

import pymodbus
from typing import Dict, Any, List, Optional, Union, Tuple
from pymodbus.exceptions import ModbusException

from utils.logger import get_logger

logger = get_logger(__name__)

class SinamicV20:
    
    def __init__(self, client, slave_id):
        """
        Initialize the SinamicV20 controller.
        
        Args:
            client: ModbusSerialClient instance for communication
            slave_id: Slave ID of the inverter
        """
        logger.info(f'Initializing SinamicV20 with slave_id={slave_id}')
        
        # client connection
        self.client = client
        self.slave_id = slave_id
        self.ADDRESS_MIN = 40001
        self.ADDRESS_MAX = 40522
        
        # parameters
        # WDOG_TIME
        self.WDOG_TIME_ADDRESS = 40001
        self.WDOG_TIME_ACCESS = 'RW'
        self.WDOG_TIME_UNIT = 'ms'
        self.WDOG_TIME_SCALE = 1
        self.WDOG_TIME_MIN = 0
        self.WDOG_TIME_MAX = 65535
        self.WDOG_TIME_VALUE = 0
        
        # WDOG_ACTION
        self.WDOG_ACTION_ADDRESS = 40002
        self.WDOG_ACTION_ACCESS = 'RW'
        self.WDOG_ACTION_UNIT = '_'
        self.WDOG_ACTION_SCALE = 1
        self.WDOG_ACTION_MIN = None
        self.WDOG_ACTION_MAX = None
        self.WDOG_ACTION_VALUE = None
        
        # FREQ_REF
        self.FREQ_REF_ADDRESS = 40003
        self.FREQ_REF_ACCESS = 'RW'
        self.FREQ_REF_UNIT = '%'
        self.FREQ_REF_SCALE = 100
        self.FREQ_REF_MIN = 0.00
        self.FREQ_REF_MAX = 100.00
        self.FREQ_REF_VALUE = 0.0
        
        # RUN_ENABLE
        self.RUN_ENABLE_ADDRESS = 40004
        self.RUN_ENABLE_ACCESS = 'RW'
        self.RUN_ENABLE_UNIT = '_'
        self.RUN_ENABLE_SCALE = 1
        self.RUN_ENABLE_MIN = 0
        self.RUN_ENABLE_MAX = 1
        self.RUN_ENABLE_VALUE = 0
        
        # CMD_FWD_REV
        self.CMD_FWD_REV_ADDRESS = 40005
        self.CMD_FWD_REV_ACCESS = 'RW'
        self.CMD_FWD_REV_UNIT = '_'
        self.CMD_FWD_REV_SCALE = 1
        self.CMD_FWD_REV_MIN = 0
        self.CMD_FWD_REV_MAX = 1
        self.CMD_FWD_REV_VALUE = 0
        
        # CMD_START
        self.CMD_START_ADDRESS = 40006
        self.CMD_START_ACCESS = 'RW'
        self.CMD_START_UNIT = '_'
        self.CMD_START_SCALE = 1
        self.CMD_START_MIN = 0
        self.CMD_START_MAX = 1
        self.CMD_START_VALUE = 0
        
        # FAULT_ACK
        self.FAULT_ACK_ADDRESS = 40007
        self.FAULT_ACK_ACCESS = 'RW'
        self.FAULT_ACK_UNIT = '_'
        self.FAULT_ACK_SCALE = 1
        self.FAULT_ACK_MIN = 0
        self.FAULT_ACK_MAX = 1
        self.FAULT_ACK_VALUE = 0
        
        # PID_SETP_REF
        self.PID_SETP_REF_ADDRESS = 40008
        self.PID_SETP_REF_ACCESS = 'RW'
        self.PID_SETP_REF_UNIT = '%'
        self.PID_SETP_REF_SCALE = 100
        self.PID_SETP_REF_MIN = -200.0
        self.PID_SETP_REF_MAX = 200.0
        self.PID_SETP_REF_VALUE = 0.0
        
        # ENABLE_PID
        self.ENABLE_PID_ADDRESS = 40009
        self.ENABLE_PID_ACCESS = 'RW'
        self.ENABLE_PID_UNIT = '_'
        self.ENABLE_PID_SCALE = 1
        self.ENABLE_PID_MIN = 0
        self.ENABLE_PID_MAX = 1
        self.ENABLE_PID_VALUE = 0
        
        # CURRENT_LMT
        self.CURRENT_LMT_ADDRESS = 40010
        self.CURRENT_LMT_ACCESS = 'RW'
        self.CURRENT_LMT_UNIT = '%'
        self.CURRENT_LMT_SCALE = 10
        self.CURRENT_LMT_MIN = 10.0
        self.CURRENT_LMT_MAX = 400.0
        self.CURRENT_LMT_VALUE = 0.0
        
        # ACCEL_TIME
        self.ACCEL_TIME_ADDRESS = 40011
        self.ACCEL_TIME_ACCESS = 'RW'
        self.ACCEL_TIME_UNIT = 's'
        self.ACCEL_TIME_SCALE = 100
        self.ACCEL_TIME_MIN = 0.00
        self.ACCEL_TIME_MAX = 650.0
        self.ACCEL_TIME_VALUE = 0.0
        
        # DECEL_TIME
        self.DECEL_TIME_ADDRESS = 40012
        self.DECEL_TIME_ACCESS = 'RW'
        self.DECEL_TIME_UNIT = 's'
        self.DECEL_TIME_SCALE = 100
        self.DECEL_TIME_MIN = 0.00
        self.DECEL_TIME_MAX = 650.0
        self.DECEL_TIME_VALUE = 0.0
        
        # DIGITAL_OUT_1
        self.DIGITAL_OUT_1_ADDRESS = 40014
        self.DIGITAL_OUT_1_ACCESS = 'RW'
        self.DIGITAL_OUT_1_UNIT = '_'
        self.DIGITAL_OUT_1_SCALE = 1
        self.DIGITAL_OUT_1_MIN = True
        self.DIGITAL_OUT_1_MAX = False
        self.DIGITAL_OUT_1_VALUE = True
        
        # DIGITAL_OUT_2
        self.DIGITAL_OUT_2_ADDRESS = 40015
        self.DIGITAL_OUT_2_ACCESS = 'RW'
        self.DIGITAL_OUT_2_UNIT = '_'
        self.DIGITAL_OUT_2_SCALE = 1
        self.DIGITAL_OUT_2_MIN = True
        self.DIGITAL_OUT_2_MAX = False
        self.DIGITAL_OUT_2_VALUE = True
        
        # REF_FREQ
        self.REF_FREQ_ADDRESS = 40016
        self.REF_FREQ_ACCESS = 'RW'
        self.REF_FREQ_UNIT = 'Hz'
        self.REF_FREQ_SCALE = 100
        self.REF_FREQ_MIN = 1.00
        self.REF_FREQ_MAX = 550.0
        self.REF_FREQ_VALUE = 0.0
        
        # PID_UP_LMT
        self.PID_UP_LMT_ADDRESS = 40017
        self.PID_UP_LMT_ACCESS = 'RW'
        self.PID_UP_LMT_UNIT = '%'
        self.PID_UP_LMT_SCALE = 100
        self.PID_UP_LMT_MIN = -200.0
        self.PID_UP_LMT_MAX = 200.0
        self.PID_UP_LMT_VALUE = 0.0
        
        # PID_LO_LMT
        self.PID_LO_LMT_ADDRESS = 40018
        self.PID_LO_LMT_ACCESS = 'RW'
        self.PID_LO_LMT_UNIT = '%'
        self.PID_LO_LMT_SCALE = 100
        self.PID_LO_LMT_MIN = -200.0
        self.PID_LO_LMT_MAX = 200.0
        self.PID_LO_LMT_VALUE = 0.0
        
        # P_GAIN
        self.P_GAIN_ADDRESS = 40019
        self.P_GAIN_ACCESS = 'RW'
        self.P_GAIN_UNIT = '_'
        self.P_GAIN_SCALE = 1000
        self.P_GAIN_MIN = 0.0
        self.P_GAIN_MAX = 65.0
        self.P_GAIN_VALUE = 0.0
        
        # I_GAIN
        self.I_GAIN_ADDRESS = 40020
        self.I_GAIN_ACCESS = 'RW'
        self.I_GAIN_UNIT = 's'
        self.I_GAIN_SCALE = 1
        self.I_GAIN_MIN = 0
        self.I_GAIN_MAX = 60
        self.I_GAIN_VALUE = 0
        
        # D_GAIN
        self.D_GAIN_ADDRESS = 40021
        self.D_GAIN_ACCESS = 'RW'
        self.D_GAIN_UNIT = '_'
        self.D_GAIN_SCALE = 1
        self.D_GAIN_MIN = 0
        self.D_GAIN_MAX = 60
        self.D_GAIN_VALUE = 0
        
        # FEEDBK_GAIN
        self.FEEDBK_GAIN_ADDRESS = 40022
        self.FEEDBK_GAIN_ACCESS = 'RW'
        self.FEEDBK_GAIN_UNIT = '%'
        self.FEEDBK_GAIN_SCALE = 100
        self.FEEDBK_GAIN_MIN = 0.0
        self.FEEDBK_GAIN_MAX = 500.0
        self.FEEDBK_GAIN_VALUE = 0.0
        
        # LOW_PASS
        self.LOW_PASS_ADDRESS = 40023
        self.LOW_PASS_ACCESS = 'RW'
        self.LOW_PASS_UNIT = '_'
        self.LOW_PASS_SCALE = 100
        self.LOW_PASS_MIN = 0.0
        self.LOW_PASS_MAX = 60.0
        self.LOW_PASS_VALUE = 0.0
        
        # FREQ_OUTPUT
        self.FREQ_OUTPUT_ADDRESS = 40024
        self.FREQ_OUTPUT_ACCESS = 'R'
        self.FREQ_OUTPUT_UNIT = 'Hz'
        self.FREQ_OUTPUT_SCALE = 100
        self.FREQ_OUTPUT_MIN = -327.68
        self.FREQ_OUTPUT_MAX = 327.67
        self.FREQ_OUTPUT_VALUE = 0.0
        
        # SPEED
        self.SPEED_ADDRESS = 40025
        self.SPEED_ACCESS = 'R'
        self.SPEED_UNIT = 'RPM'
        self.SPEED_SCALE = 1
        self.SPEED_MIN = -16250
        self.SPEED_MAX = 16250
        self.SPEED_VALUE = 0.0
        
        # CURRENT
        self.CURRENT_ADDRESS = 40026
        self.CURRENT_ACCESS = 'R'
        self.CURRENT_UNIT = 'A'
        self.CURRENT_SCALE = 100
        self.CURRENT_MIN = 0.0
        self.CURRENT_MAX = 163.83
        self.CURRENT_VALUE = 0.0
        
        # TORQUE
        self.TORQUE_ADDRESS = 40027
        self.TORQUE_ACCESS = 'R'
        self.TORQUE_UNIT = 'Nm'
        self.TORQUE_SCALE = 100
        self.TORQUE_MIN = -325.0
        self.TORQUE_MAX = 325.0
        self.TORQUE_VALUE = 0.0
        
        # ACTUAL_PWR
        self.ACTUAL_PWR_ADDRESS = 40028
        self.ACTUAL_PWR_ACCESS = 'R'
        self.ACTUAL_PWR_UNIT = 'kW'
        self.ACTUAL_PWR_SCALE = 100
        self.ACTUAL_PWR_MIN = 0.0
        self.ACTUAL_PWR_MAX = 327.67
        self.ACTUAL_PWR_VALUE = 0.0
        
        # TOTAL_KWH
        self.TOTAL_KWH_ADDRESS = 40029
        self.TOTAL_KWH_ACCESS = 'R'
        self.TOTAL_KWH_UNIT = 'kWh'
        self.TOTAL_KWH_SCALE = 1
        self.TOTAL_KWH_MIN = 0
        self.TOTAL_KWH_MAX = 32767
        self.TOTAL_KWH_VALUE = 0.0
        
        # DC_BUS_VOLTS
        self.DC_BUS_VOLTS_ADDRESS = 40030
        self.DC_BUS_VOLTS_ACCESS = 'R'
        self.DC_BUS_VOLTS_UNIT = 'V'
        self.DC_BUS_VOLTS_SCALE = 1
        self.DC_BUS_VOLTS_MIN = 0
        self.DC_BUS_VOLTS_MAX = 32767
        self.DC_BUS_VOLTS_VALUE = 0.0
        
        # REFERENCE
        self.REFERENCE_ADDRESS = 40031
        self.REFERENCE_ACCESS = 'R'
        self.REFERENCE_UNIT = 'Hz'
        self.REFERENCE_SCALE = 100
        self.REFERENCE_MIN = -327.68
        self.REFERENCE_MAX = 327.67
        self.REFERENCE_VALUE = 0.0
        
        # RATED_PWR
        self.RATED_PWR_ADDRESS = 40032
        self.RATED_PWR_ACCESS = 'R'
        self.RATED_PWR_UNIT = 'kW'
        self.RATED_PWR_SCALE = 100
        self.RATED_PWR_MIN = 0.0
        self.RATED_PWR_MAX = 327.67
        self.RATED_PWR_VALUE = 0.0
        
        # OUTPUT_VOLTS
        self.OUTPUT_VOLTS_ADDRESS = 40033
        self.OUTPUT_VOLTS_ACCESS = 'R'
        self.OUTPUT_VOLTS_UNIT = 'V'
        self.OUTPUT_VOLTS_SCALE = 1
        self.OUTPUT_VOLTS_MIN = 0.0
        self.OUTPUT_VOLTS_MAX = 32767
        self.OUTPUT_VOLTS_VALUE = 0
        
        # FWD_REV
        self.FWD_REV_ADDRESS = 40034
        self.FWD_REV_ACCESS = 'R'
        self.FWD_REV_UNIT = '_'
        self.FWD_REV_SCALE = 1
        self.FWD_REV_MIN = 0 #'FWD'
        self.FWD_REV_MAX = 1 #'REV'
        self.FWD_REV_VALUE = 0
        
        # STOP_RUN
        self.STOP_RUN_ADDRESS = 40035
        self.STOP_RUN_ACCESS = 'R'
        self.STOP_RUN_UNIT = '_'
        self.STOP_RUN_SCALE = 1
        self.STOP_RUN_MIN = 0 #'STOP'
        self.STOP_RUN_MAX = 1 #'RUN'
        self.STOP_RUN_VALUE = 0
        
        # AT_MAX_FREQ
        self.AT_MAX_FREQ_ADDRESS = 40036
        self.AT_MAX_FREQ_ACCESS = 'R'
        self.AT_MAX_FREQ_UNIT = '_'
        self.AT_MAX_FREQ_SCALE = 1
        self.AT_MAX_FREQ_MIN = 0 #'MAX'
        self.AT_MAX_FREQ_MAX = 1 #'NO'
        self.AT_MAX_FREQ_VALUE = 0
        
        # CONTROL_MODE
        self.CONTROL_MODE_ADDRESS = 40037
        self.CONTROL_MODE_ACCESS = 'R'
        self.CONTROL_MODE_UNIT = '_'
        self.CONTROL_MODE_SCALE = 1
        self.CONTROL_MODE_MIN = 0 #'SERIAL'
        self.CONTROL_MODE_MAX = 1 #'LOCAL'
        self.CONTROL_MODE_VALUE = 0
        
        # ENABLED
        self.ENABLED_ADDRESS = 40038
        self.ENABLED_ACCESS = 'R'
        self.ENABLED_UNIT = '_'
        self.ENABLED_SCALE = 1
        self.ENABLED_MIN = 0 #'ON'
        self.ENABLED_MAX = 1 #'OFF'
        self.ENABLED_VALUE = 0
        
        # READY_TO_RUN
        self.READY_TO_RUN_ADDRESS = 40039
        self.READY_TO_RUN_ACCESS = 'R'
        self.READY_TO_RUN_UNIT = '_'
        self.READY_TO_RUN_SCALE = 1
        self.READY_TO_RUN_MIN = 0 #'READY'
        self.READY_TO_RUN_MAX = 1 #'OFF'
        self.READY_TO_RUN_VALUE = 0
        
        # ANALOG_IN_1
        self.ANALOG_IN_1_ADDRESS = 40040
        self.ANALOG_IN_1_ACCESS = 'R'
        self.ANALOG_IN_1_UNIT = '%'
        self.ANALOG_IN_1_SCALE = 100
        self.ANALOG_IN_1_MIN = -300
        self.ANALOG_IN_1_MAX = 300
        self.ANALOG_IN_1_VALUE = 0
        
        # ANALOG_IN_2
        self.ANALOG_IN_2_ADDRESS = 40041
        self.ANALOG_IN_2_ACCESS = 'R'
        self.ANALOG_IN_2_UNIT = '%'
        self.ANALOG_IN_2_SCALE = 100
        self.ANALOG_IN_2_MIN = -300
        self.ANALOG_IN_2_MAX = 300
        self.ANALOG_IN_2_VALUE = 0
        
        # ANALOG_OUT_1
        self.ANALOG_OUT_1_ADDRESS = 40042
        self.ANALOG_OUT_1_ACCESS = 'R'
        self.ANALOG_OUT_1_UNIT = '%'
        self.ANALOG_OUT_1_SCALE = 100
        self.ANALOG_OUT_1_MIN = -100
        self.ANALOG_OUT_1_MAX = 100
        self.ANALOG_OUT_1_VALUE = 0
        
        # FREQ_ACTUAL
        self.FREQ_ACTUAL_ADDRESS = 40044
        self.FREQ_ACTUAL_ACCESS = 'R'
        self.FREQ_ACTUAL_UNIT = '%'
        self.FREQ_ACTUAL_SCALE = 100
        self.FREQ_ACTUAL_MIN = -100
        self.FREQ_ACTUAL_MAX = 100
        self.FREQ_ACTUAL_VALUE = 0
        
        # PID_SETP_OUT
        self.PID_SETP_OUT_ADDRESS = 40045
        self.PID_SETP_OUT_ACCESS = 'R'
        self.PID_SETP_OUT_UNIT = '%'
        self.PID_SETP_OUT_SCALE = 100
        self.PID_SETP_OUT_MIN = -100
        self.PID_SETP_OUT_MAX = 100
        self.PID_SETP_OUT_VALUE = 0
        
        # PID_OUTPUT
        self.PID_OUTPUT_ADDRESS = 40046
        self.PID_OUTPUT_ACCESS = 'R'
        self.PID_OUTPUT_UNIT = '%'
        self.PID_OUTPUT_SCALE = 100
        self.PID_OUTPUT_MIN = -100
        self.PID_OUTPUT_MAX = 100
        self.PID_OUTPUT_VALUE = 0
        
        # PID_FEEDBACK
        self.PID_FEEDBACK_ADDRESS = 40047
        self.PID_FEEDBACK_ACCESS = 'R'
        self.PID_FEEDBACK_UNIT = '%'
        self.PID_FEEDBACK_SCALE = 100
        self.PID_FEEDBACK_MIN = -100
        self.PID_FEEDBACK_MAX = 100
        self.PID_FEEDBACK_VALUE = 0
        
        # DIGITAL_IN_1
        self.DIGITAL_IN_1_ADDRESS = 40048
        self.DIGITAL_IN_1_ACCESS = 'R'
        self.DIGITAL_IN_1_UNIT = '_'
        self.DIGITAL_IN_1_SCALE = 1
        self.DIGITAL_IN_1_MIN = 0 #HIGH
        self.DIGITAL_IN_1_MAX = 1 #LOW
        self.DIGITAL_IN_1_VALUE = 0
        
        # DIGITAL_IN_2
        self.DIGITAL_IN_2_ADDRESS = 40049
        self.DIGITAL_IN_2_ACCESS = 'R'
        self.DIGITAL_IN_2_UNIT = '_'
        self.DIGITAL_IN_2_SCALE = 1
        self.DIGITAL_IN_2_MIN = 0 #HIGH
        self.DIGITAL_IN_2_MAX = 1 #LOW
        self.DIGITAL_IN_2_VALUE = 0
        
        # DIGITAL_IN_3
        self.DIGITAL_IN_3_ADDRESS = 40050
        self.DIGITAL_IN_3_ACCESS = 'R'
        self.DIGITAL_IN_3_UNIT = '_'
        self.DIGITAL_IN_3_SCALE = 1
        self.DIGITAL_IN_3_MIN = 0 #HIGH
        self.DIGITAL_IN_3_MAX = 1 #LOW
        self.DIGITAL_IN_3_VALUE = 0
        
        # DIGITAL_IN_4
        self.DIGITAL_IN_4_ADDRESS = 40051
        self.DIGITAL_IN_4_ACCESS = 'R'
        self.DIGITAL_IN_4_UNIT = '_'
        self.DIGITAL_IN_4_SCALE = 1
        self.DIGITAL_IN_4_MIN = 0 #HIGH
        self.DIGITAL_IN_4_MAX = 1 #LOW
        self.DIGITAL_IN_4_VALUE = 0
        
        # FAULT
        self.FAULT_ADDRESS = 40054
        self.FAULT_ACCESS = 'R'
        self.FAULT_UNIT = '_'
        self.FAULT_SCALE = 1
        self.FAULT_MIN = 0 #FAULT
        self.FAULT_MAX = 1 #OFF
        self.FAULT_VALUE = 0
        
        # LAST_FAULT
        self.LAST_FAULT_ADDRESS = 40055
        self.LAST_FAULT_ACCESS = 'R'
        self.LAST_FAULT_UNIT = '_'
        self.LAST_FAULT_SCALE = 1
        self.LAST_FAULT_MIN = 0
        self.LAST_FAULT_MAX = 32767
        self.LAST_FAULT_VALUE = 0 
        
        # FAULT_1
        self.FAULT_1_ADDRESS = 40056
        self.FAULT_1_ACCESS = 'R'
        self.FAULT_1_UNIT = '_'
        self.FAULT_1_SCALE = 1
        self.FAULT_1_MIN = 0
        self.FAULT_1_MAX = 32767
        self.FAULT_1_VALUE = 0
        
        # FAULT_2
        self.FAULT_2_ADDRESS = 40057
        self.FAULT_2_ACCESS = 'R'
        self.FAULT_2_UNIT = '_'
        self.FAULT_2_SCALE = 1
        self.FAULT_2_MIN = 0
        self.FAULT_2_MAX = 32767
        self.FAULT_2_VALUE = 0
        
        # FAULT_3
        self.FAULT_3_ADDRESS = 40058
        self.FAULT_3_ACCESS = 'R'
        self.FAULT_3_UNIT = '_'
        self.FAULT_3_SCALE = 1
        self.FAULT_3_MIN = 0
        self.FAULT_3_MAX = 32767
        self.FAULT_3_VALUE = 0
        
        # WARNING
        self.WARNING_ADDRESS = 40059
        self.WARNING_ACCESS = 'R'
        self.WARNING_UNIT = '_'
        self.WARNING_SCALE = 1
        self.WARNING_MIN = 0 #WARN
        self.WARNING_MAX = 1 #OK
        self.WARNING_VALUE = 0
        
        # LAST_WARNING
        self.LAST_WARNING_ADDRESS = 40060
        self.LAST_WARNING_ACCESS = 'R'
        self.LAST_WARNING_UNIT = '_'
        self.LAST_WARNING_SCALE = 1
        self.LAST_WARNING_MIN = 0
        self.LAST_WARNING_MAX = 32767
        self.LAST_WARNING_VALUE = 0
        
        # INVERTER_VER
        self.INVERTER_VER_ADDRESS = 40061
        self.INVERTER_VER_ACCESS = 'R'
        self.INVERTER_VER_UNIT = '_'
        self.INVERTER_VER_SCALE = 100
        self.INVERTER_VER_MIN = 0
        self.INVERTER_VER_MAX = 327.67
        self.INVERTER_VER_VALUE = 0
        
        # DRIVE_MODEL
        self.DRIVE_MODEL_ADDRESS = 40062
        self.DRIVE_MODEL_ACCESS = 'R'
        self.DRIVE_MODEL_UNIT = '_'
        self.DRIVE_MODEL_SCALE = 1
        self.DRIVE_MODEL_MIN = 0
        self.DRIVE_MODEL_MAX = 32767
        self.DRIVE_MODEL_VALUE = 0
        
        # STW
        self.STW_ADDRESS = 40100
        self.STW_ACCESS = 'RW'
        self.STW_UNIT = '_'
        self.STW_SCALE = 1
        self.STW_MIN = None
        self.STW_MAX = None
        self.STW_VALUE = None
        
        # HSW
        self.HSW_ADDRESS = 40101
        self.HSW_ACCESS = 'RW'
        self.HSW_UNIT = '_'
        self.HSW_SCALE = 1
        self.HSW_MIN = None
        self.HSW_MAX = None
        self.HSW_VALUE = None
        
        # ZSW
        self.ZSW_ADDRESS = 40110
        self.ZSW_ACCESS = 'R'
        self.ZSW_UNIT = '_'
        self.ZSW_SCALE = 1
        self.ZSW_MIN = None
        self.ZSW_MAX = None
        self.ZSW_VALUE = None
        
        # HIW
        self.HIW_ADDRESS = 40111
        self.HIW_ACCESS = 'R'
        self.HIW_UNIT = '_'
        self.HIW_SCALE = 1
        self.HIW_MIN = None
        self.HIW_MAX = None
        self.HIW_VALUE = None
        
        # DIGITAL_OUT_1
        
        # DIGITAL_OUT_2
        
        # ANALOG_OUT_1
        
        # DIGITAL_IN_1
        
        # DIGITAL_IN_2
        
        # DIGITAL_IN_3
        
        # DIGITAL_IN_4
        
        # ANALOG_IN_1
        
        # ANALOG_IN_2
        
        # INVERTER_MODEL
        self.INVERTER_MODEL_ADDRESS = 40300
        self.INVERTER_MODEL_ACCESS = 'R'
        self.INVERTER_MODEL_UNIT = '_'
        self.INVERTER_MODEL_SCALE = 1
        self.INVERTER_MODEL_MIN = 0
        self.INVERTER_MODEL_MAX = 32767
        self.INVERTER_MODEL_VALUE = 0
        
        # INVERTER_VER
        self.INVERTER_VER_ADDRESS = 40301
        self.INVERTER_VER_ACCESS = 'R'
        self.INVERTER_VER_UNIT = '_'
        self.INVERTER_VER_SCALE = 100
        self.INVERTER_VER_MIN = 0
        self.INVERTER_VER_MAX = 327.67
        self.INVERTER_VER_VALUE = 0
        
        # RATED_PWR
        
        # CURRENT_LMT
        
        # ACCEL_TIME
        
        # DECEL_TIME
        
        # REF_FREQ
        
        
        # REFERENCE
        
        # SPEED
        
        # FREQ_OUTPUT
        
        # OUTPUT_VOLTS
        
        # DC_BUS_VOLTS
        
        # CURRENT
        
        # TORQUE
        
        # ACTUAL_PWR
        
        # TOTAL_KWH
        
        # HAND_AUTO
        self.HAND_AUTO_ADDRESS = 40349
        self.HAND_AUTO_ACCESS = 'R'
        self.HAND_AUTO_UNIT = '_'
        self.HAND_AUTO_SCALE = 1
        self.HAND_AUTO_MIN = 0 #HIGH
        self.HAND_AUTO_MAX = 1 #LOW
        self.HAND_AUTO_VALUE = 0
        
        # FAULT_1
        
        # FAULT_2
        
        # FAULT_3
        
        # FAULT_4
        self.FAULT_4_ADDRESS = 40403
        self.FAULT_4_ACCESS = 'R'
        self.FAULT_4_UNIT = '_'
        self.FAULT_4_SCALE = 1
        self.FAULT_4_MIN = 0
        self.FAULT_4_MAX = 32767
        self.FAULT_4_VALUE = 0
        
        # FAULT_5
        self.FAULT_5_ADDRESS = 40404
        self.FAULT_5_ACCESS = 'R'
        self.FAULT_5_UNIT = '_'
        self.FAULT_5_SCALE = 1
        self.FAULT_5_MIN = 0
        self.FAULT_5_MAX = 32767
        self.FAULT_5_VALUE = 0
        
        # FAULT_6
        self.FAULT_6_ADDRESS = 40405
        self.FAULT_6_ACCESS = 'R'
        self.FAULT_6_UNIT = '_'
        self.FAULT_6_SCALE = 1
        self.FAULT_6_MIN = 0
        self.FAULT_6_MAX = 32767
        self.FAULT_6_VALUE = 0
        
        # FAULT_7
        self.FAULT_7_ADDRESS = 40406
        self.FAULT_7_ACCESS = 'R'
        self.FAULT_7_UNIT = '_'
        self.FAULT_7_SCALE = 1
        self.FAULT_7_MIN = 0
        self.FAULT_7_MAX = 32767
        self.FAULT_7_VALUE = 0
        
        # FAULT_8
        self.FAULT_8_ADDRESS = 40407
        self.FAULT_8_ACCESS = 'R'
        self.FAULT_8_UNIT = '_'
        self.FAULT_8_SCALE = 1
        self.FAULT_8_MIN = 0
        self.FAULT_8_MAX = 32767
        self.FAULT_8_VALUE = 0
        
        # WARNING
        
        # PRM_ERROR_CODE
        self.PRM_ERROR_CODE_ADDRESS = 40499
        self.PRM_ERROR_CODE_ACCESS = 'R'
        self.PRM_ERROR_CODE_UNIT = '_'
        self.PRM_ERROR_CODE_SCALE = 1
        self.PRM_ERROR_CODE_MIN = 0
        self.PRM_ERROR_CODE_MAX = 254
        self.PRM_ERROR_CODE_VALUE = 0
        
        # ENABLE_PID
        
        # PID_SETP_REF
        
        # LOW_PASS
        
        # FEEDBK_GAIN
        
        # P_GAIN
        
        # I_GAIN
        
        
        # D_GAIN
        
        # PID_UP_LMT
        
        # PID_LO_LMT
        
        # PID_SETP_OUT
        
        # PI_FEEDBACK
        self.PI_FEEDBACK_ADDRESS = 40521
        self.PI_FEEDBACK_ACCESS = 'R'
        self.PI_FEEDBACK_UNIT = '%'
        self.PI_FEEDBACK_SCALE = 100
        self.PI_FEEDBACK_MIN = -100
        self.PI_FEEDBACK_MAX = 100
        self.PI_FEEDBACK_VALUE = 0
        # PID_OUTPUT
        
        # address_to_hex
        self.address_to_hex = {
            40001:0x00,
            40002:0x01,
            40003:0x02,
            40004:0x03,
            40005:0x04,
            40006:0x05,
            40007:0x06,
            40008:0x07,
            40009:0x08,
            40010:0x09,
            40011:0x0a,
            40012:0x0b,
            40014:0x0d,
            40015:0x0e,
            40016:0x0f,
            40017:0x10,
            40018:0x11,
            40019:0x12,
            40020:0x13,
            40021:0x14,
            40022:0x15,
            40023:0x15,
            40024:0x17,
            40025:0x18,
            40026:0x19,
            40027:0x1a,
            40028:0x1b,
            40029:0x1c,
            40030:0x1d,
            40031:0x1e,
            40032:0x1f,
            40033:0x20,
            40034:0x21,
            40035:0x22,
            40036:0x23,
            40037:0x24,
            40038:0x25,
            40039:0x26,
            40040:0x27,
            40041:0x28,
            40042:0x29,
            40044:0x2b,
            40045:0x2c,
            40046:0x2d,
            40047:0x2e,
            40048:0x2f,
            40049:0x30,
            40050:0x31,
            40051:0x32,
            40054:0x35,
            40055:0x36,
            40056:0x37,
            40057:0x38,
            40058:0x39,
            40059:0x3a,
            40060:0x3b,
            40061:0x3c,
            40062:0x3d,
            40100:0x63,
            40101:0x64,
            40110:0x6d,
            40111:0x6e,
            40300:0x12b,
            40301:0x12c,
            40349:0x15c,
            40403:0x192,
            40404:0x193,
            40405:0x194,
            40406:0x195,
            40407:0x196,
            40499:0x1f2,
            40521:0x208
        }
        
        # address_to_name
        self.address_to_name = {
            40001:'WDOG_TIME',
            40002:'WDOG_ACTION',
            40003:'FREQ_REF',
            40004:'RUN_ENABLE',
            40005:'CMD_FWD_REV',
            40006:'CMD_START',
            40007:'FAULT_ACK',
            40008:'PID_SETP_REF',
            40009:'ENABLE_PID',
            40010:'CURRENT_LMT',
            40011:'ACCEL_TIME',
            40012:'DECEL_TIME',
            40014:'DIGITAL_OUT_1',
            40015:'DIGITAL_OUT_2',
            40016:'REF_FREQ',
            40017:'PID_UP_LMT',
            40018:'PID_LO_LMT',
            40019:'P_GAIN',
            40020:'I_GAIN',
            40021:'D_GAIN',
            40022:'FEEDBK_GAIN',
            40023:'LOW_PASS',
            40024:'FREQ_OUTPUT',
            40025:'SPEED',
            40026:'CURRENT',
            40027:'TORQUE',
            40028:'ACTUAL_PWR',
            40029:'TOTAL_KWH',
            40030:'DC_BUS_VOLTS',
            40031:'REFERENCE',
            40032:'RATED_PWR',
            40033:'OUTPUT_VOLTS',
            40034:'FWD_REV',
            40035:'STOP_RUN',
            40036:'AT_MAX_FREQ',
            40037:'CONTROL_MODE',
            40038:'ENABLED',
            40039:'READY_TO_RUN',
            40040:'ANALOG_IN_1',
            40041:'ANALOG_IN_2',
            40042:'ANALOG_OUT_1',
            40044:'FREQ_ACTUAL',
            40045:'PID_SETP_OUT',
            40046:'PID_OUTPUT',
            40047:'PID_FEEDBACK',
            40048:'DIGITAL_IN_1',
            40049:'DIGITAL_IN_2',
            40050:'DIGITAL_IN_3',
            40051:'DIGITAL_IN_4',
            40054:'FAULT',
            40055:'LAST_FAULT',
            40056:'FAULT_1',
            40057:'FAULT_2',
            40058:'FAULT_3',
            40059:'WARNING',
            40060:'LAST_WARNING',
            40061:'INVERTER_VER',
            40062:'DRIVE_MODEL',
            40100:'STW',
            40101:'HSW',
            40110:'ZSW',
            40111:'HIW',
            40300:'INVERTER_MODEL',
            40301:'INVERTER_VER',
            40349:'HAND_AUTO',
            40403:'FAULT_4',
            40404:'FAULT_5',
            40405:'FAULT_6',
            40406:'FAULT_7',
            40407:'FAULT_8',
            40499:'PRM_ERROR_CODE',
            40521:'PI_FEEDBACK'
        }
        
        # name_to_address
        self.name_to_address = {self.address_to_name[k]:k for k in self.address_to_name.keys()}
        
        self.ADDRESS_LENGTH = len(self.address_to_name.keys())
        self.ADDRESS_LIST = list(self.address_to_name.keys())
        self.MAX_LENGTH_OF_ADDRESS = 125
        
        # address_to_param
        self.address_to_param = {
            40001:{'NAME':'WDOG_TIME','ACCESS':self.WDOG_TIME_ACCESS,'UNIT':self.WDOG_TIME_UNIT,'SCALE':self.WDOG_TIME_SCALE,'MIN':self.WDOG_TIME_MIN,'MAX':self.WDOG_TIME_MAX,'VALUE':self.WDOG_TIME_VALUE},
            
            40002:{'NAME':'WDOG_ACTION','ACCESS':self.WDOG_ACTION_ACCESS,'UNIT':self.WDOG_ACTION_UNIT,'SCALE':self.WDOG_ACTION_SCALE,'MIN':self.WDOG_ACTION_MIN,'MAX':self.WDOG_ACTION_MAX,'VALUE':self.WDOG_ACTION_VALUE},
            
            40003:{'NAME':'FREQ_REF','ACCESS':self.FREQ_REF_ACCESS,'UNIT':self.FREQ_REF_UNIT,'SCALE':self.FREQ_REF_SCALE,'MIN':self.FREQ_REF_MIN,'MAX':self.FREQ_REF_MAX,'VALUE':self.FREQ_REF_VALUE},
            
            40004:{'NAME':'RUN_ENABLE','ACCESS':self.RUN_ENABLE_ACCESS,'UNIT':self.RUN_ENABLE_UNIT,'SCALE':self.RUN_ENABLE_SCALE,'MIN':self.RUN_ENABLE_MIN,'MAX':self.RUN_ENABLE_MAX,'VALUE':self.RUN_ENABLE_VALUE},
            
            40005:{'NAME':'CMD_FWD_REV','ACCESS':self.CMD_FWD_REV_ACCESS,'UNIT':self.CMD_FWD_REV_UNIT,'SCALE':self.CMD_FWD_REV_SCALE,'MIN':self.CMD_FWD_REV_MIN,'MAX':self.CMD_FWD_REV_MAX,'VALUE':self.CMD_FWD_REV_VALUE},
            
            40006:{'NAME':'CMD_START','ACCESS':self.CMD_START_ACCESS,'UNIT':self.CMD_START_UNIT,'SCALE':self.CMD_START_SCALE,'MIN':self.CMD_START_MIN,'MAX':self.CMD_START_MAX,'VALUE':self.CMD_START_VALUE},
            
            40007:{'NAME':'FAULT_ACK','ACCESS':self.FAULT_ACK_ACCESS,'UNIT':self.FAULT_ACK_UNIT,'SCALE':self.FAULT_ACK_SCALE,'MIN':self.FAULT_ACK_MIN,'MAX':self.FAULT_ACK_MAX,'VALUE':self.FAULT_ACK_VALUE},
            
            40008:{'NAME':'PID_SETP_REF','ACCESS':self.PID_SETP_REF_ACCESS,'UNIT':self.PID_SETP_REF_UNIT,'SCALE':self.PID_SETP_REF_SCALE,'MIN':self.PID_SETP_REF_MIN,'MAX':self.PID_SETP_REF_MAX,'VALUE':self.PID_SETP_REF_VALUE},
            
            40009:{'NAME':'ENABLE_PID','ACCESS':self.ENABLE_PID_ACCESS,'UNIT':self.ENABLE_PID_UNIT,'SCALE':self.ENABLE_PID_SCALE,'MIN':self.ENABLE_PID_MIN,'MAX':self.ENABLE_PID_MAX,'VALUE':self.ENABLE_PID_VALUE},
            
            40010:{'NAME':'CURRENT_LMT','ACCESS':self.CURRENT_LMT_ACCESS,'UNIT':self.CURRENT_LMT_UNIT,'SCALE':self.CURRENT_LMT_SCALE,'MIN':self.CURRENT_LMT_MIN,'MAX':self.CURRENT_LMT_MAX,'VALUE':self.CURRENT_LMT_VALUE},
            
            40011:{'NAME':'ACCEL_TIME','ACCESS':self.ACCEL_TIME_ACCESS,'UNIT':self.ACCEL_TIME_UNIT,'SCALE':self.ACCEL_TIME_SCALE,'MIN':self.ACCEL_TIME_MIN,'MAX':self.ACCEL_TIME_MAX,'VALUE':self.ACCEL_TIME_VALUE},
            
            40012:{'NAME':'DECEL_TIME','ACCESS':self.DECEL_TIME_ACCESS,'UNIT':self.DECEL_TIME_UNIT,'SCALE':self.DECEL_TIME_SCALE,'MIN':self.DECEL_TIME_MIN,'MAX':self.DECEL_TIME_MAX,'VALUE':self.DECEL_TIME_VALUE},
            
            40014:{'NAME':'DIGITAL_OUT_1','ACCESS':self.DIGITAL_OUT_1_ACCESS,'UNIT':self.DIGITAL_OUT_1_UNIT,'SCALE':self.DIGITAL_OUT_1_SCALE,'MIN':self.DIGITAL_OUT_1_MIN,'MAX':self.DIGITAL_OUT_1_MAX,'VALUE':self.DIGITAL_OUT_1_VALUE},
            
            40015:{'NAME':'DIGITAL_OUT_2','ACCESS':self.DIGITAL_OUT_2_ACCESS,'UNIT':self.DIGITAL_OUT_2_UNIT,'SCALE':self.DIGITAL_OUT_2_SCALE,'MIN':self.DIGITAL_OUT_2_MIN,'MAX':self.DIGITAL_OUT_2_MAX,'VALUE':self.DIGITAL_OUT_2_VALUE},
            
            40016:{'NAME':'REF_FREQ','ACCESS':self.REF_FREQ_ACCESS,'UNIT':self.REF_FREQ_UNIT,'SCALE':self.REF_FREQ_SCALE,'MIN':self.REF_FREQ_MIN,'MAX':self.REF_FREQ_MAX,'VALUE':self.REF_FREQ_VALUE},
            
            40017:{'NAME':'PID_UP_LMT','ACCESS':self.PID_UP_LMT_ACCESS,'UNIT':self.PID_UP_LMT_UNIT,'SCALE':self.PID_UP_LMT_SCALE,'MIN':self.PID_UP_LMT_MIN,'MAX':self.PID_UP_LMT_MAX,'VALUE':self.PID_UP_LMT_VALUE},
            
            40018:{'NAME':'PID_LO_LMT','ACCESS':self.PID_LO_LMT_ACCESS,'UNIT':self.PID_LO_LMT_UNIT,'SCALE':self.PID_LO_LMT_SCALE,'MIN':self.PID_LO_LMT_MIN,'MAX':self.PID_LO_LMT_MAX,'VALUE':self.PID_LO_LMT_VALUE},
            
            40019:{'NAME':'P_GAIN','ACCESS':self.P_GAIN_ACCESS,'UNIT':self.P_GAIN_UNIT,'SCALE':self.P_GAIN_SCALE,'MIN':self.P_GAIN_MIN,'MAX':self.P_GAIN_MAX,'VALUE':self.P_GAIN_VALUE},
            
            40020:{'NAME':'I_GAIN','ACCESS':self.I_GAIN_ACCESS,'UNIT':self.I_GAIN_UNIT,'SCALE':self.I_GAIN_SCALE,'MIN':self.I_GAIN_MIN,'MAX':self.I_GAIN_MAX,'VALUE':self.I_GAIN_VALUE},
            
            40021:{'NAME':'D_GAIN','ACCESS':self.D_GAIN_ACCESS,'UNIT':self.D_GAIN_UNIT,'SCALE':self.D_GAIN_SCALE,'MIN':self.D_GAIN_MIN,'MAX':self.D_GAIN_MAX,'VALUE':self.D_GAIN_VALUE},
            
            40022:{'NAME':'FEEDBK_GAIN','ACCESS':self.FEEDBK_GAIN_ACCESS,'UNIT':self.FEEDBK_GAIN_UNIT,'SCALE':self.FEEDBK_GAIN_SCALE,'MIN':self.FEEDBK_GAIN_MIN,'MAX':self.FEEDBK_GAIN_MAX,'VALUE':self.FEEDBK_GAIN_VALUE},
            
            40023:{'NAME':'LOW_PASS','ACCESS':self.LOW_PASS_ACCESS,'UNIT':self.LOW_PASS_UNIT,'SCALE':self.LOW_PASS_SCALE,'MIN':self.LOW_PASS_MIN,'MAX':self.LOW_PASS_MAX,'VALUE':self.LOW_PASS_VALUE},
            
            40024:{'NAME':'FREQ_OUTPUT','ACCESS':self.FREQ_OUTPUT_ACCESS,'UNIT':self.FREQ_OUTPUT_UNIT,'SCALE':self.FREQ_OUTPUT_SCALE,'MIN':self.FREQ_OUTPUT_MIN,'MAX':self.FREQ_OUTPUT_MAX,'VALUE':self.FREQ_OUTPUT_VALUE},
            
            40025:{'NAME':'SPEED','ACCESS':self.SPEED_ACCESS,'UNIT':self.SPEED_UNIT,'SCALE':self.SPEED_SCALE,'MIN':self.SPEED_MIN,'MAX':self.SPEED_MAX,'VALUE':self.SPEED_VALUE},
            
            40026:{'NAME':'CURRENT','ACCESS':self.CURRENT_ACCESS,'UNIT':self.CURRENT_UNIT,'SCALE':self.CURRENT_SCALE,'MIN':self.CURRENT_MIN,'MAX':self.CURRENT_MAX,'VALUE':self.CURRENT_VALUE},
            
            40027:{'NAME':'TORQUE','ACCESS':self.TORQUE_ACCESS,'UNIT':self.TORQUE_UNIT,'SCALE':self.TORQUE_SCALE,'MIN':self.TORQUE_MIN,'MAX':self.TORQUE_MAX,'VALUE':self.TORQUE_VALUE},
            
            40028:{'NAME':'ACTUAL_PWR','ACCESS':self.ACTUAL_PWR_ACCESS,'UNIT':self.ACTUAL_PWR_UNIT,'SCALE':self.ACTUAL_PWR_SCALE,'MIN':self.ACTUAL_PWR_MIN,'MAX':self.ACTUAL_PWR_MAX,'VALUE':self.ACTUAL_PWR_VALUE},
            
            40029:{'NAME':'TOTAL_KWH','ACCESS':self.TOTAL_KWH_ACCESS,'UNIT':self.TOTAL_KWH_UNIT,'SCALE':self.TOTAL_KWH_SCALE,'MIN':self.TOTAL_KWH_MIN,'MAX':self.TOTAL_KWH_MAX,'VALUE':self.TOTAL_KWH_VALUE},
            
            40030:{'NAME':'DC_BUS_VOLTS','ACCESS':self.DC_BUS_VOLTS_ACCESS,'UNIT':self.DC_BUS_VOLTS_UNIT,'SCALE':self.DC_BUS_VOLTS_SCALE,'MIN':self.DC_BUS_VOLTS_MIN,'MAX':self.DC_BUS_VOLTS_MAX,'VALUE':self.DC_BUS_VOLTS_VALUE},
            
            40031:{'NAME':'REFERENCE','ACCESS':self.REFERENCE_ACCESS,'UNIT':self.REFERENCE_UNIT,'SCALE':self.REFERENCE_SCALE,'MIN':self.REFERENCE_MIN,'MAX':self.REFERENCE_MAX,'VALUE':self.REFERENCE_VALUE},
            
            40032:{'NAME':'RATED_PWR','ACCESS':self.RATED_PWR_ACCESS,'UNIT':self.RATED_PWR_UNIT,'SCALE':self.RATED_PWR_SCALE,'MIN':self.RATED_PWR_MIN,'MAX':self.RATED_PWR_MAX,'VALUE':self.RATED_PWR_VALUE},
            
            40033:{'NAME':'OUTPUT_VOLTS','ACCESS':self.OUTPUT_VOLTS_ACCESS,'UNIT':self.OUTPUT_VOLTS_UNIT,'SCALE':self.OUTPUT_VOLTS_SCALE,'MIN':self.OUTPUT_VOLTS_MIN,'MAX':self.OUTPUT_VOLTS_MAX,'VALUE':self.OUTPUT_VOLTS_VALUE},
            
            40034:{'NAME':'FWD_REV','ACCESS':self.FWD_REV_ACCESS,'UNIT':self.FWD_REV_UNIT,'SCALE':self.FWD_REV_SCALE,'MIN':self.FWD_REV_MIN,'MAX':self.FWD_REV_MAX,'VALUE':self.FWD_REV_VALUE},
            
            40035:{'NAME':'STOP_RUN','ACCESS':self.STOP_RUN_ACCESS,'UNIT':self.STOP_RUN_UNIT,'SCALE':self.STOP_RUN_SCALE,'MIN':self.STOP_RUN_MIN,'MAX':self.STOP_RUN_MAX,'VALUE':self.STOP_RUN_VALUE},
            
            40036:{'NAME':'AT_MAX_FREQ','ACCESS':self.AT_MAX_FREQ_ACCESS,'UNIT':self.AT_MAX_FREQ_UNIT,'SCALE':self.AT_MAX_FREQ_SCALE,'MIN':self.AT_MAX_FREQ_MIN,'MAX':self.AT_MAX_FREQ_MAX,'VALUE':self.AT_MAX_FREQ_VALUE},
            
            40037:{'NAME':'CONTROL_MODE','ACCESS':self.CONTROL_MODE_ACCESS,'UNIT':self.CONTROL_MODE_UNIT,'SCALE':self.CONTROL_MODE_SCALE,'MIN':self.CONTROL_MODE_MIN,'MAX':self.CONTROL_MODE_MAX,'VALUE':self.CONTROL_MODE_VALUE},
            
            40038:{'NAME':'ENABLED','ACCESS':self.ENABLED_ACCESS,'UNIT':self.ENABLED_UNIT,'SCALE':self.ENABLED_SCALE,'MIN':self.ENABLED_MIN,'MAX':self.ENABLED_MAX,'VALUE':self.ENABLED_VALUE},
            
            40039:{'NAME':'READY_TO_RUN','ACCESS':self.READY_TO_RUN_ACCESS,'UNIT':self.READY_TO_RUN_UNIT,'SCALE':self.READY_TO_RUN_SCALE,'MIN':self.READY_TO_RUN_MIN,'MAX':self.READY_TO_RUN_MAX,'VALUE':self.READY_TO_RUN_VALUE},
            
            40040:{'NAME':'ANALOG_IN_1','ACCESS':self.ANALOG_IN_1_ACCESS,'UNIT':self.ANALOG_IN_1_UNIT,'SCALE':self.ANALOG_IN_1_SCALE,'MIN':self.ANALOG_IN_1_MIN,'MAX':self.ANALOG_IN_1_MAX,'VALUE':self.ANALOG_IN_1_VALUE},
            
            40041:{'NAME':'ANALOG_IN_2','ACCESS':self.ANALOG_IN_2_ACCESS,'UNIT':self.ANALOG_IN_2_UNIT,'SCALE':self.ANALOG_IN_2_SCALE,'MIN':self.ANALOG_IN_2_MIN,'MAX':self.ANALOG_IN_2_MAX,'VALUE':self.ANALOG_IN_2_VALUE},
            
            40042:{'NAME':'ANALOG_OUT_1','ACCESS':self.ANALOG_OUT_1_ACCESS,'UNIT':self.ANALOG_OUT_1_UNIT,'SCALE':self.ANALOG_OUT_1_SCALE,'MIN':self.ANALOG_OUT_1_MIN,'MAX':self.ANALOG_OUT_1_MAX,'VALUE':self.ANALOG_OUT_1_VALUE},
            
            40044:{'NAME':'FREQ_ACTUAL','ACCESS':self.FREQ_ACTUAL_ACCESS,'UNIT':self.FREQ_ACTUAL_UNIT,'SCALE':self.FREQ_ACTUAL_SCALE,'MIN':self.FREQ_ACTUAL_MIN,'MAX':self.FREQ_ACTUAL_MAX,'VALUE':self.FREQ_ACTUAL_VALUE},
            
            40045:{'NAME':'PID_SETP_OUT','ACCESS':self.PID_SETP_OUT_ACCESS,'UNIT':self.PID_SETP_OUT_UNIT,'SCALE':self.PID_SETP_OUT_SCALE,'MIN':self.PID_SETP_OUT_MIN,'MAX':self.PID_SETP_OUT_MAX,'VALUE':self.PID_SETP_OUT_VALUE},
            
            40046:{'NAME':'PID_OUTPUT','ACCESS':self.PID_OUTPUT_ACCESS,'UNIT':self.PID_OUTPUT_UNIT,'SCALE':self.PID_OUTPUT_SCALE,'MIN':self.PID_OUTPUT_MIN,'MAX':self.PID_OUTPUT_MAX,'VALUE':self.PID_OUTPUT_VALUE},
            
            40047:{'NAME':'PID_FEEDBACK','ACCESS':self.PID_FEEDBACK_ACCESS,'UNIT':self.PID_FEEDBACK_UNIT,'SCALE':self.PID_FEEDBACK_SCALE,'MIN':self.PID_FEEDBACK_MIN,'MAX':self.PID_FEEDBACK_MAX,'VALUE':self.PID_FEEDBACK_VALUE},
            
            40048:{'NAME':'DIGITAL_IN_1','ACCESS':self.DIGITAL_IN_1_ACCESS,'UNIT':self.DIGITAL_IN_1_UNIT,'SCALE':self.DIGITAL_IN_1_SCALE,'MIN':self.DIGITAL_IN_1_MIN,'MAX':self.DIGITAL_IN_1_MAX,'VALUE':self.DIGITAL_IN_1_VALUE},
            
            40049:{'NAME':'DIGITAL_IN_2','ACCESS':self.DIGITAL_IN_2_ACCESS,'UNIT':self.DIGITAL_IN_2_UNIT,'SCALE':self.DIGITAL_IN_2_SCALE,'MIN':self.DIGITAL_IN_2_MIN,'MAX':self.DIGITAL_IN_2_MAX,'VALUE':self.DIGITAL_IN_2_VALUE},
            
            40050:{'NAME':'DIGITAL_IN_3','ACCESS':self.DIGITAL_IN_3_ACCESS,'UNIT':self.DIGITAL_IN_3_UNIT,'SCALE':self.DIGITAL_IN_3_SCALE,'MIN':self.DIGITAL_IN_3_MIN,'MAX':self.DIGITAL_IN_3_MAX,'VALUE':self.DIGITAL_IN_3_VALUE},
            
            40051:{'NAME':'DIGITAL_IN_4','ACCESS':self.DIGITAL_IN_4_ACCESS,'UNIT':self.DIGITAL_IN_4_UNIT,'SCALE':self.DIGITAL_IN_4_SCALE,'MIN':self.DIGITAL_IN_4_MIN,'MAX':self.DIGITAL_IN_4_MAX,'VALUE':self.DIGITAL_IN_4_VALUE},
            
            40054:{'NAME':'FAULT','ACCESS':self.FAULT_ACCESS,'UNIT':self.FAULT_UNIT,'SCALE':self.FAULT_SCALE,'MIN':self.FAULT_MIN,'MAX':self.FAULT_MAX,'VALUE':self.FAULT_VALUE},
            
            40055:{'NAME':'LAST_FAULT','ACCESS':self.LAST_FAULT_ACCESS,'UNIT':self.LAST_FAULT_UNIT,'SCALE':self.LAST_FAULT_SCALE,'MIN':self.LAST_FAULT_MIN,'MAX':self.LAST_FAULT_MAX,'VALUE':self.LAST_FAULT_VALUE},
            
            40056:{'NAME':'FAULT_1','ACCESS':self.FAULT_1_ACCESS,'UNIT':self.FAULT_1_UNIT,'SCALE':self.FAULT_1_SCALE,'MIN':self.FAULT_1_MIN,'MAX':self.FAULT_1_MAX,'VALUE':self.FAULT_1_VALUE},
            
            40057:{'NAME':'FAULT_2','ACCESS':self.FAULT_2_ACCESS,'UNIT':self.FAULT_2_UNIT,'SCALE':self.FAULT_2_SCALE,'MIN':self.FAULT_2_MIN,'MAX':self.FAULT_2_MAX,'VALUE':self.FAULT_2_VALUE},
            
            40058:{'NAME':'FAULT_3','ACCESS':self.FAULT_3_ACCESS,'UNIT':self.FAULT_3_UNIT,'SCALE':self.FAULT_3_SCALE,'MIN':self.FAULT_3_MIN,'MAX':self.FAULT_3_MAX,'VALUE':self.FAULT_3_VALUE},
            
            40059:{'NAME':'WARNING','ACCESS':self.WARNING_ACCESS,'UNIT':self.WARNING_UNIT,'SCALE':self.WARNING_SCALE,'MIN':self.WARNING_MIN,'MAX':self.WARNING_MAX,'VALUE':self.WARNING_VALUE},
            
            40060:{'NAME':'LAST_WARNING','ACCESS':self.LAST_WARNING_ACCESS,'UNIT':self.LAST_WARNING_UNIT,'SCALE':self.LAST_WARNING_SCALE,'MIN':self.LAST_WARNING_MIN,'MAX':self.LAST_WARNING_MAX,'VALUE':self.LAST_WARNING_VALUE},
            
            40061:{'NAME':'INVERTER_VER','ACCESS':self.INVERTER_VER_ACCESS,'UNIT':self.INVERTER_VER_UNIT,'SCALE':self.INVERTER_VER_SCALE,'MIN':self.INVERTER_VER_MIN,'MAX':self.INVERTER_VER_MAX,'VALUE':self.INVERTER_VER_VALUE},
            
            40062:{'NAME':'DRIVE_MODEL','ACCESS':self.DRIVE_MODEL_ACCESS,'UNIT':self.DRIVE_MODEL_UNIT,'SCALE':self.DRIVE_MODEL_SCALE,'MIN':self.DRIVE_MODEL_MIN,'MAX':self.DRIVE_MODEL_MAX,'VALUE':self.DRIVE_MODEL_VALUE},
            
            40100:{'NAME':'STW','ACCESS':self.STW_ACCESS,'UNIT':self.STW_UNIT,'SCALE':self.STW_SCALE,'MIN':self.STW_MIN,'MAX':self.STW_MAX,'VALUE':self.STW_VALUE},
            
            40101:{'NAME':'HSW','ACCESS':self.HSW_ACCESS,'UNIT':self.HSW_UNIT,'SCALE':self.HSW_SCALE,'MIN':self.HSW_MIN,'MAX':self.HSW_MAX,'VALUE':self.HSW_VALUE},
            
            40110:{'NAME':'ZSW','ACCESS':self.ZSW_ACCESS,'UNIT':self.ZSW_UNIT,'SCALE':self.ZSW_SCALE,'MIN':self.ZSW_MIN,'MAX':self.ZSW_MAX,'VALUE':self.ZSW_VALUE},
            
            40111:{'NAME':'HIW','ACCESS':self.HIW_ACCESS,'UNIT':self.HIW_UNIT,'SCALE':self.HIW_SCALE,'MIN':self.HIW_MIN,'MAX':self.HIW_MAX,'VALUE':self.HIW_VALUE},
            
            40300:{'NAME':'INVERTER_MODEL','ACCESS':self.INVERTER_MODEL_ACCESS,'UNIT':self.INVERTER_MODEL_UNIT,'SCALE':self.INVERTER_MODEL_SCALE,'MIN':self.INVERTER_MODEL_MIN,'MAX':self.INVERTER_MODEL_MAX,'VALUE':self.INVERTER_MODEL_VALUE},
            
            40301:{'NAME':'INVERTER_VER','ACCESS':self.INVERTER_VER_ACCESS,'UNIT':self.INVERTER_VER_UNIT,'SCALE':self.INVERTER_VER_SCALE,'MIN':self.INVERTER_VER_MIN,'MAX':self.INVERTER_VER_MAX,'VALUE':self.INVERTER_VER_VALUE},
            
            40349:{'NAME':'HAND_AUTO','ACCESS':self.HAND_AUTO_ACCESS,'UNIT':self.HAND_AUTO_UNIT,'SCALE':self.HAND_AUTO_SCALE,'MIN':self.HAND_AUTO_MIN,'MAX':self.HAND_AUTO_MAX,'VALUE':self.HAND_AUTO_VALUE},
            
            40403:{'NAME':'FAULT_4','ACCESS':self.FAULT_4_ACCESS,'UNIT':self.FAULT_4_UNIT,'SCALE':self.FAULT_4_SCALE,'MIN':self.FAULT_4_MIN,'MAX':self.FAULT_4_MAX,'VALUE':self.FAULT_4_VALUE},
            
            40404:{'NAME':'FAULT_5','ACCESS':self.FAULT_5_ACCESS,'UNIT':self.FAULT_5_UNIT,'SCALE':self.FAULT_5_SCALE,'MIN':self.FAULT_5_MIN,'MAX':self.FAULT_5_MAX,'VALUE':self.FAULT_5_VALUE},
            
            40405:{'NAME':'FAULT_6','ACCESS':self.FAULT_6_ACCESS,'UNIT':self.FAULT_6_UNIT,'SCALE':self.FAULT_6_SCALE,'MIN':self.FAULT_6_MIN,'MAX':self.FAULT_6_MAX,'VALUE':self.FAULT_6_VALUE},
            
            40406:{'NAME':'FAULT_7','ACCESS':self.FAULT_7_ACCESS,'UNIT':self.FAULT_7_UNIT,'SCALE':self.FAULT_7_SCALE,'MIN':self.FAULT_7_MIN,'MAX':self.FAULT_7_MAX,'VALUE':self.FAULT_7_VALUE},
            
            40407:{'NAME':'FAULT_8','ACCESS':self.FAULT_8_ACCESS,'UNIT':self.FAULT_8_UNIT,'SCALE':self.FAULT_8_SCALE,'MIN':self.FAULT_8_MIN,'MAX':self.FAULT_8_MAX,'VALUE':self.FAULT_8_VALUE},
            
            40499:{'NAME':'PRM_ERROR_CODE','ACCESS':self.PRM_ERROR_CODE_ACCESS,'UNIT':self.PRM_ERROR_CODE_UNIT,'SCALE':self.PRM_ERROR_CODE_SCALE,'MIN':self.PRM_ERROR_CODE_MIN,'MAX':self.PRM_ERROR_CODE_MAX,'VALUE':self.PRM_ERROR_CODE_VALUE},
            
            40521:{'NAME':'PI_FEEDBACK','ACCESS':self.PI_FEEDBACK_ACCESS,'UNIT':self.PI_FEEDBACK_UNIT,'SCALE':self.PI_FEEDBACK_SCALE,'MIN':self.PI_FEEDBACK_MIN,'MAX':self.PI_FEEDBACK_MAX,'VALUE':self.PI_FEEDBACK_VALUE}
        }
        
        print('[SinamicV20] End __init__')
    
    def read_raw_single_address(self, address: int) -> Optional[int]:
        """
        Read a single register value from the specified address.
        
        Args:
            address: Modbus register address to read
            
        Returns:
            The register value, or None if an error occurred
        """
        try:
            # Convert address from 4XXXX to 0-based addressing
            actual_address = address - 40001
            
            # Read the register
            result = self.client.read_holding_registers(
                address=actual_address,
                count=1,
                slave=self.slave_id
            )
            
            # Check for errors
            if result.isError():
                logger.error(f"Error reading address {address}: {result}")
                return None
                
            logger.debug(f"Read value {result.registers[0]} from address {address}")
            return result.registers[0]
            
        except ModbusException as e:
            logger.exception(f"Modbus exception reading address {address}: {e}")
            return None
        except Exception as e:
            logger.exception(f"Error reading address {address}: {e}")
            return None
    
    def read_raw_multi_address(self, addresses: List[int]) -> List[Optional[int]]:
        """
        Read multiple register values from the specified addresses.
        
        Args:
            addresses: List of Modbus register addresses to read
            
        Returns:
            List of register values, with None for any addresses that couldn't be read
        """
        values = []
        
        for address in addresses:
            try:
                value = self.read_raw_single_address(address)
                values.append(value)
            except Exception as e:
                logger.exception(f"Error reading address {address}: {e}")
                values.append(None)
        
        logger.debug(f"Read {len(values)} values from multiple addresses")
        return values
    
    def read_raw_all_address(self) -> List[Optional[int]]:
        """
        Read all register values defined in the ADDRESS_LIST.
        
        Returns:
            List of register values, with None for any addresses that couldn't be read
        """
        try:
            values = []
            
            for address in self.ADDRESS_LIST:
                value = self.read_raw_single_address(address)
                values.append(value)
                
            logger.debug(f"Read {len(values)} values from all addresses")
            return values
            
        except Exception as e:
            logger.exception(f"Error reading all addresses: {e}")
            return [None] * len(self.ADDRESS_LIST)
    
    def read_raw_all_address_convert_dict(self) -> Dict[str, Any]:
        """
        Read all register values and convert to a dictionary with parameter names as keys.
        
        Returns:
            Dictionary of parameter values with parameter names as keys
        """
        try:
            values_dict = {}
            raw_values = self.read_raw_all_address()
            
            for i, address in enumerate(self.ADDRESS_LIST):
                if i < len(raw_values):
                    param_name = self.address_to_param[address]['NAME']
                    values_dict[param_name] = raw_values[i]
                    
            logger.debug(f"Read {len(values_dict)} parameter values into dictionary")
            return values_dict
            
        except Exception as e:
            logger.exception(f"Error converting register values to dictionary: {e}")
            return {}
