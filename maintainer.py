'''
sudo chmod a+rw /dev/ttyUSB0
python3 maintainer.py
'''
import time
import sqlite3
from joblib import load
from utils.motor import SinamicV20
from pymodbus.client import ModbusSerialClient

print('Import successfully!')

# Init
ID = 0
TABLE_NAME  = 'sinamicv20'
DATABASE_PATH = 'data/inverter.db'
SLEEPING_TIME = 1
SPEED_DICT = {0:'stopped',
              1:'low_speed',
              2:'normal_speed',
              3:'high_speed'}
if __name__ == "__main__":
    
    # Connect to database
    conn = sqlite3.connect(DATABASE_PATH)
    c = conn.cursor()
    
    # Load model
    model = load('notebooks/model.joblib') 

    query = """SELECT * FROM sinamicv20 WHERE ID = 0"""
    
    while True:
        
        c.execute(query)
        conn.commit()
        
        x = c.fetchone()
        x_drop_index = x[1:]
        
        print(len(x_drop_index),SPEED_DICT[int(model.predict([x_drop_index]))])
        
        time.sleep(SLEEPING_TIME)
        