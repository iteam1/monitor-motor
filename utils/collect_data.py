'''
sudo chmod a+rw /dev/ttyUSB0
python3 utils/collect_data.py
'''
import sys
import time
from motor import SinamicV20
from pymodbus.client import ModbusSerialClient

print('Import successfully!')

# Initialize
PORT = '/dev/ttyUSB0'
METHOD = 'rtu'
STOPBITS = 1
BYTESIZE = 8
PARITY = 'N'
BAUDRATE = 9600
SLAVE_ID = 2
N_SAMPLES = 100

if __name__ == "__main__":
    
    client = ModbusSerialClient(method = METHOD,
                                    port = PORT,
                                    stopbits = STOPBITS,
                                    bytesize = BYTESIZE,
                                    parity = PARITY,
                                    baudrate= BAUDRATE,
                                    unit=1)
    
    inverter = SinamicV20(client=client,slave_id=2)
    
    while True:
        
        list_of_values = inverter.read_raw_all_address()
        
        print(list_of_values)