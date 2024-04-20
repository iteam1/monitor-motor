'''
sudo chmod a+rw /dev/ttyUSB0
python3 utils/collect_data.py
'''
import csv
from datetime import datetime
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
CSV_FILE = 'data.csv'

def write_csv(data):
    with open(CSV_FILE, 'a') as outfile:
        writer = csv.writer(outfile)
        writer.writerow(data)
        
if __name__ == "__main__":
    
    client = ModbusSerialClient(method = METHOD,
                                    port = PORT,
                                    stopbits = STOPBITS,
                                    bytesize = BYTESIZE,
                                    parity = PARITY,
                                    baudrate= BAUDRATE,
                                    unit=1)
    
    inverter = SinamicV20(client=client,slave_id=2)
    
    # write header
    headers = list(inverter.name_to_address.keys())
    write_csv(headers)
    
    while True:
        
        # get current timestamp
        current_time = datetime.now()
        timestamp = current_time.timestamp()

        # get inverter values
        list_of_values = inverter.read_raw_all_address()
        print(timestamp,len(list_of_values))
 
        # append to csv file
        write_csv(list_of_values)