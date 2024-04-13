'''
sudo chmod a+rw /dev/ttyUSB0
python utils/connect_client.py

'''
import serial
import pymodbus
from pymodbus.client import ModbusSerialClient
print('Import Successfully!')

# Initialize
my_port = '/dev/ttyUSB0'
my_method = 'rtu'

client = ModbusSerialClient(method = my_method,
 port = my_port,
 stopbits = 1,
  bytesize = 8,
   parity = 'N',
    baudrate= 9600
    )

# Connect to serial modbus server
connection_status = client.connect()
print('connection_status',connection_status)

# Read holding register start from 40001=0x00
result = client.read_holding_registers(address=0x00,count=100,slave=2)
print(result)
print(result.registers)

#Closes the underlying socket connection
client.close()