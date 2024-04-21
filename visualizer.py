'''
sudo chmod a+rw /dev/ttyUSB0
python3 visualizer.py
'''
import sys
import sqlite3
import pyqtgraph as pg
from utils.motor import SinamicV20
from PyQt5 import QtWidgets, QtCore
from pyqtgraph import PlotWidget, plot
from pymodbus.client import ModbusSerialClient

print('Import successfully!')

ID = 0
TABLE_NAME  = 'sinamicv20'
DATABASE_PATH = 'data/inverter.db'
N_SAMPLES = 100

class MainWindow(QtWidgets.QMainWindow):
    
    def __init__(self, *args, **kwargs):
        
        super(MainWindow, self).__init__(*args, **kwargs)

        # Connect to database
        self.conn = sqlite3.connect(DATABASE_PATH)
        self.c = self.conn.cursor()

        self.graphWidget = pg.PlotWidget()
        self.setCentralWidget(self.graphWidget)
        
        # time-series data
        self.x = list(range(N_SAMPLES)) # 100 time points
        self.y = [0]*N_SAMPLES  # 100 data points
        
        # setup widget
        self.graphWidget.setBackground('black')
        pen = pg.mkPen(color=(255,0,0))
        self.data_line = self.graphWidget.plot(self.x, self.y, pen=pen)
        
        # setup timer
        self.timer = QtCore.QTimer()
        self.timer.setInterval(50)
        self.timer.timeout.connect(self.update_plot_data)
        self.timer.start()
        
    def update_plot_data(self):
        
        # query = """SELECT * FROM sinamicv20 WHERE ID = 0"""
        query = """SELECT SPEED FROM sinamicv20 WHERE ID = 0"""
        
        self.c.execute(query)
        self.conn.commit()
        
        y_new =  self.c.fetchone()[0]
        
        if isinstance(y_new, (int, float)):
            # Add data
            self.x = self.x[1:] # Remove the first x element
            self.x.append(self.x[-1]+1) # Add new value 1 higher than the last
            
            self.y = self.y[1:] # Remove the first y element
            
            self.y.append(y_new)  # Add a new random value.
            
            # Update dataset
            self.data_line.setData(self.x, self.y) # Update the data
        else:
            pass
        
if __name__ == "__main__":
    
    app = QtWidgets.QApplication(sys.argv)
    w = MainWindow()
    w.show()
    sys.exit(app.exec_())