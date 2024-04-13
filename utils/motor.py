import time
import datetime
import serial
import pymodbus
from pymodbus.client import ModbusSerialClient

class SinamicV20:
    def __init__(self, client):
        # client connection
        self.client = client
        
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
        self.DIGITAL_OUT_1_ADDRESS = 40200
        self.DIGITAL_OUT_1_ACCESS = 'RW'
        self.DIGITAL_OUT_1_UNIT = '_'
        self.DIGITAL_OUT_1_SCALE = 1
        self.DIGITAL_OUT_1_MIN = 0 #HIGH
        self.DIGITAL_OUT_1_MAX = 1 #LOW
        self.DIGITAL_OUT_1_VALUE = 0
        # DIGITAL_OUT_2
        self.DIGITAL_OUT_2_ADDRESS = 40201
        self.DIGITAL_OUT_2_ACCESS = 'RW'
        self.DIGITAL_OUT_2_UNIT = '_'
        self.DIGITAL_OUT_2_SCALE = 1
        self.DIGITAL_OUT_2_MIN = 0 #HIGH
        self.DIGITAL_OUT_2_MAX = 1 #LOW
        self.DIGITAL_OUT_2_VALUE = 0
        # ANALOG_OUT_1
        self.ANALOG_OUT_1_ADDRESS = 40220
        self.ANALOG_OUT_1_ACCESS = 'R'
        self.ANALOG_OUT_1_UNIT = '%'
        self.ANALOG_OUT_1_SCALE = 100
        self.ANALOG_OUT_1_MIN = -100.0 #HIGH
        self.ANALOG_OUT_1_MAX = 100.0 #LOW
        self.ANALOG_OUT_1_VALUE = 0
        # DIGITAL_IN_1_2
        self.DIGITAL_IN_1_2_ADDRESS = 40240
        self.DIGITAL_IN_1_2_ACCESS = 'R'
        self.DIGITAL_IN_1_2_UNIT = '_'
        self.DIGITAL_IN_1_2_SCALE = 1
        self.DIGITAL_IN_1_2_MIN = 0 #HIGH
        self.DIGITAL_IN_1_2_MAX = 1 #LOW
        self.DIGITAL_IN_1_2_VALUE = 0
        # DIGITAL_IN_2_2
        self.DIGITAL_IN_2_2_ADDRESS = 40241
        self.DIGITAL_IN_2_2_ACCESS = 'R'
        self.DIGITAL_IN_2_2_UNIT = '_'
        self.DIGITAL_IN_2_2_SCALE = 1
        self.DIGITAL_IN_2_2_MIN = 0 #HIGH
        self.DIGITAL_IN_2_2_MAX = 1 #LOW
        self.DIGITAL_IN_2_2_VALUE = 0
        # DIGITAL_IN_3_2
        self.DIGITAL_IN_3_2_ADDRESS = 40242
        self.DIGITAL_IN_3_2_ACCESS = 'R'
        self.DIGITAL_IN_3_2_UNIT = '_'
        self.DIGITAL_IN_3_2_SCALE = 1
        self.DIGITAL_IN_3_2_MIN = 0 #HIGH
        self.DIGITAL_IN_3_2_MAX = 1 #LOW
        self.DIGITAL_IN_3_2_VALUE = 0
        # DIGITAL_IN_4_2
        self.DIGITAL_IN_4_2_ADDRESS = 40243
        self.DIGITAL_IN_4_2_ACCESS = 'R'
        self.DIGITAL_IN_4_2_UNIT = '_'
        self.DIGITAL_IN_4_2_SCALE = 1
        self.DIGITAL_IN_4_2_MIN = 0 #HIGH
        self.DIGITAL_IN_4_2_MAX = 1 #LOW
        self.DIGITAL_IN_4_2_VALUE = 0
        # ANALOG_IN_1_2
        self.ANALOG_IN_1_2_ADDRESS = 40260
        self.ANALOG_IN_1_2_ACCESS = 'R'
        self.ANALOG_IN_1_2_UNIT = '%'
        self.ANALOG_IN_1_2_SCALE = 100
        self.ANALOG_IN_1_2_MIN = -300
        self.ANALOG_IN_1_2_MAX = 300
        self.ANALOG_IN_1_2_VALUE = 0
        # ANALOG_IN_2_2
        self.ANALOG_IN_2_2_ADDRESS = 40261
        self.ANALOG_IN_2_2_ACCESS = 'R'
        self.ANALOG_IN_2_2_UNIT = '%'
        self.ANALOG_IN_2_2_SCALE = 100
        self.ANALOG_IN_2_2_MIN = -300
        self.ANALOG_IN_2_2_MAX = 300
        self.ANALOG_IN_2_2_VALUE = 0
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
        # FAULT_1
        # FAULT_2
        # FAULT_3
        # FAULT_4
        # FAULT_5
        # FAULT_6
        # FAULT_7
        # FAULT_8
        # WARNING
        # PRM_ERROR_CODE
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
        # PID_OUTPUT
        
        # dict_of_address
        
    def read_single_address(self,addr):
        list_of_values = []
        return list_of_values
    
    def read_multi_address(self,addr):
        list_of_values = []
        return list_of_values
    
    def read_all_address(self,addr):
        list_of_values = []
        return list_of_values
