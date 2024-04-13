'''
sudo chmod a+rw /dev/ttyUSB0
python utils/cont_reading.py

'''
import time
import datetime
import serial
import pymodbus
from pymodbus.client import ModbusSerialClient
print('Import Successfully!')

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

    if connection_status:
        while True:
            # Get current timestamp
            current_datetime = datetime.datetime.now()
            print("timestamp:", current_datetime.timestamp())
            
            try:
                # Read holding register start from 40001=0x00
                result = client.read_holding_registers(address = ADDRESS_START,count = COUNT,slave = 2)
                print(result)
                print(result.registers)
            except Exception as e:
                print('Error',e)
            
            time.sleep(SLEEP_TIME)

        #Closes the underlying socket connection
        client.close()
        exit(0)
        
    else:
        exit(-1)