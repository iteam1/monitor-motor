'''
sudo chmod a+rw /dev/ttyUSB0
python3 collector.py
'''
import sqlite3
from utils.motor import SinamicV20
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

ID = 0
TABLE_NAME  = 'sinamicv20'

def generate_update_query_by_id(table_name, data_dict, id):
    query = f"UPDATE {table_name} SET "
    updates = []
    for key, value in data_dict.items():
        if isinstance(value, str):
            updates.append(f"{key} = '{value}'")
        else:
            updates.append(f"{key} = {value}")
    query += ", ".join(updates)
    query += f" WHERE ID = {id}"
    query += ";"
    return query


if __name__ == "__main__":
    
    client = ModbusSerialClient(method = METHOD,
                                port = PORT,
                                stopbits = STOPBITS,
                                bytesize = BYTESIZE,
                                parity = PARITY,
                                baudrate= BAUDRATE,
                                unit=1)
    
    inverter = SinamicV20(client=client,slave_id=2)
    
    conn = sqlite3.connect('data/inverter.db')
    
    c = conn.cursor()
    
    while True:

        # get inverter values
        dict_of_values = inverter.read_raw_all_address_convert_dict()
        
        update_query = generate_update_query_by_id(TABLE_NAME, dict_of_values, ID)
        
        c.execute(update_query)
        
        print(update_query)
    
    conn.commit()

    conn.close()