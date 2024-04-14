'''
sudo chmod a+rw /dev/ttyUSB0
python3 utils/test_motor.py
'''
import time
import datetime
from pymodbus.client import ModbusSerialClient
from motor import SinamicV20

print('Import Successfully')

# Initialize
PORT = '/dev/ttyUSB0'
METHOD = 'rtu'
STOPBITS = 1
BYTESIZE = 8
PARITY = 'N'
BAUDRATE = 9600

SLEEP_TIME = 2
SLAVE_ID = 2 
ADDRESS_START = 0x00
COUNT = 125

if __name__ == "__main__":
    
    # Establish connection
    client = ModbusSerialClient(method = METHOD,
    port = PORT,
    stopbits = STOPBITS,
    bytesize = BYTESIZE,
    parity = PARITY,
        baudrate= BAUDRATE
        )

    # Connect to serial modbus server
    connection_status = client.connect()
    print('connection_status',connection_status)
    
    # instantiate
    inverter = SinamicV20(client=client,slave_id=2)
    
    #print(inverter.name_to_address)
    
    #print(inverter.ADDRESS_LENGTH)
    
    inverter.read_single_address(40001)
    inverter.read_single_address(40002)
    inverter.read_single_address(40003)
    
    