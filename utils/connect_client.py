'''
sudo chmod a+rw /dev/ttyUSB0
'''
import serial
import pymodbus
from pymodbus.client import ModbusSerialClient
print('Import Successfully!')

# Initialize
my_port = '/dev/ttyUSB0'
my_method = 'rtu'

client = ModbusSerialClient(method = "rtu",
 port="/dev/ttyUSB0",
 stopbits = 1,
  bytesize = 8,
   parity = 'N',
    baudrate= 9600
    )

# Connect to serial modbus server
connection_status = client.connect()
print('connection_status',connection_status)


result = client.read_holding_registers(address=40001,count=2,unit=1)
print(result)

#Closes the underlying socket connection
client.close()
