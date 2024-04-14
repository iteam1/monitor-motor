'''
python3 utils/test_motor.py
'''
import time
import datetime
import serial
import pymodbus
from pymodbus.client import ModbusSerialClient
from motor import SinamicV20

print('Import Successfully')


if __name__ == "__main__":
    # instantiate
    inverter = SinamicV20(None)
    
    #print(inverter.name_to_address)
    
    #print(inverter.ADDRESS_LENGTH)
    
    print(inverter.address_to_param[40001])