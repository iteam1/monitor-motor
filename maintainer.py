'''
sudo chmod a+rw /dev/ttyUSB0
python3 maintainer.py
'''
import time
import numpy as np
import sqlite3
from joblib import load

print('Import successfully!')

# Init
ID = 0
TABLE_NAME  = 'sinamicv20'
DATABASE_PATH = 'data/inverter.db'
SLEEPING_TIME = 2
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

    
    while True:
        
        query = """SELECT * FROM sinamicv20 WHERE ID = 0"""
        c.execute(query)
        
        x = c.fetchone()
        #print(x)
        # x_drop_index = x[1:]
        # print(len(x_drop_index),SPEED_DICT[int(model.predict([np.array(x_drop_index)]))])
        
        speed = x[24] * 8.10/242
        
        if speed != 0:
            if speed < 7:
                print('SPEE =',speed,'=> WARNING SLOW SPEED!')
            elif speed > 13:
                print('SPEED =',speed,'=> WARNING HIGH SPEED!')
            else:
                print('SPEED =',speed,'=> NORMAL SPEED')
        else:
            print('SPEED =',speed,'=> MOTOR STOPPED')
            
        conn.commit()
        time.sleep(SLEEPING_TIME)
        