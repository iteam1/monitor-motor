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
    
    print('---TEST READ SINGLE ADDRESS---')
    
    addr = 40023
    res = inverter.read_raw_single_address(addr)
    print(f"address={addr} name={inverter.address_to_param[addr]['NAME']} res={res}")
    
    addr = 40521
    res = inverter.read_raw_single_address(addr)
    print(f"address={addr} name={inverter.address_to_param[addr]['NAME']} res={res}")
    
    addr = 40028
    res = inverter.read_raw_single_address(addr)
    print(f"address={addr} name={inverter.address_to_param[addr]['NAME']} res={res}")
    
    print('TEST READ MULTI ADDRESS')
    
    addrs = [40023, 40521, 40028]
    
    res = inverter.read_raw__multi_address(addrs)
    
    for i,addr in enumerate(addrs):
        print(f"address={addr} name={inverter.address_to_param[addr]['NAME']} res={res[i]}")
    
    print('---TEST READ ALL ADDRESS---')
    
    res = inverter.read_raw_all_address()
    
    for i,addr in enumerate(inverter.ADDRESS_LIST):
        print(f"address={addr} name={inverter.address_to_param[addr]['NAME']} res={res[i]}")