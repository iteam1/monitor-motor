'''
sudo chmod a+rw /dev/ttyUSB0
python3 utils/visualize_app.py
'''
import sys
import time
import datetime
import pyqtgraph as pg
from motor import SinamicV20
from random import randint
from PyQt5 import QtWidgets, QtCore
from pyqtgraph import PlotWidget, plot
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

# Establish connection
client = ModbusSerialClient(method = METHOD,
                            port = PORT,
                            stopbits = STOPBITS,
                            bytesize = BYTESIZE,
                            parity = PARITY,
                            baudrate= BAUDRATE)

# Connect to serial modbus server
connection_status = client.connect()
print('connection_status',connection_status)

# instantiate
inverter = SinamicV20(client=client,slave_id=2)

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, *args, **kwargs):
        
        super(MainWindow, self).__init__(*args, **kwargs)
        
        self.graphWidget = pg.PlotWidget()
        self.setCentralWidget(self.graphWidget)
        
        # time-series data
        self.x = list(range(N_SAMPLES)) # 100 time points
        self.y = [randint(0,100) for _ in range(N_SAMPLES)]  # 100 data points
        
        # setup widget
        self.graphWidget.setBackground('b')
        pen = pg.mkPen(color=(255,0,0))
        self.data_line = self.graphWidget.plot(self.x, self.y, pen=pen)
        
        # setup timer
        self.timer = QtCore.QTimer()
        self.timer.setInterval(50)
        self.timer.timeout.connect(self.update_plot_data)
        self.timer.start()
        
    def update_plot_data(self):
        
        # Add data
        self.x = self.x[1:] # Remove the first x element
        self.x.append(self.x[-1]+1) # Add new value 1 higher than the last
        
        self.y = self.y[1:] # Remove the first y element
        self.y.append(randint(0,100))  # Add a new random value.
        
        # Update dataset
        self.data_line.setData(self.x, self.y) # Update the data
        
if __name__ == "__main__":
    
    app = QtWidgets.QApplication(sys.argv)
    w = MainWindow()
    w.show()
    sys.exit(app.exec_())