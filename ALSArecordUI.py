import sys
import os
import time
import subprocess
import shlex
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLineEdit, QVBoxLayout, QVBoxLayout, QFormLayout, QProgressBar, QLabel
from PyQt5.QtCore import QThread, pyqtSignal

inputTime = 0
pitch = ""
setupComple = 0
setValComple = False
MsetValinit = False
class RunThread(QThread):
    set_max = pyqtSignal(int)
    update = pyqtSignal(int)
    Mset_max = pyqtSignal(int)
    Mupdate = pyqtSignal(int)

    def __init__(self):
        QThread.__init__(self)

    def __del__(self):
        self.wait()

    def run(self):
        self.set_max.emit(100)

        for index in range(1, 101):
            self.update.emit(index)
            time.sleep(0.01)
  
        
class MainWindow(QWidget):
    def __init__(self):
        super(self.__class__, self).__init__()
        self.setupUi()
        self._run_thread = RunThread()
        self._run_thread.set_max.connect(self.Set_Max)
        self._run_thread.update.connect(self.Set_Value)
        self._run_thread.set_max.connect(self.MSet_Max)
        self._run_thread.update.connect(self.MSet_Value)
        self.show()


    def setupUi(self):
        self.setWindowTitle("SoundChangeApp")
        self.label = QLabel()
        self.label.setText("Please enter the time(sec) you want to record.")
        self.button_input = QPushButton()
        self.button_input.setText("Input")
        self.button_setup = QPushButton()
        self.button_setup.setText("Setup")
        self.button_start = QPushButton()
        self.button_start.setText("Start")
        self.button_high = QPushButton()
        self.button_high.setText("Change pitch to High")
        self.button_low = QPushButton()
        self.button_low.setText("Change pitch to Low")
        self.button_reverse = QPushButton()
        self.button_reverse.setText("Reverse the sound")
        self.setupProgress_bar = QProgressBar()
        self.startProgress_bar = QProgressBar()
        self.line_input = QLineEdit()
        self.line_setup = QLineEdit()

        form_layout = QFormLayout()
        form_layout.addRow(self.button_input, self.line_input)
        form_layout.addRow(self.button_setup,self.setupProgress_bar)
        form_layout.addRow(self.button_high, self.button_low)
        form_layout.addRow(self.button_start,self.startProgress_bar)
        form_layout.addRow(self.button_reverse)

        h_layout = QVBoxLayout()
        h_layout.addWidget(self.label)
        h_layout.addLayout(form_layout)
 
        self.setLayout(h_layout) # must set the layout beyond to execute show
        self.button_input.clicked.connect(self.input)
        self.button_setup.clicked.connect(self.start)
        self.button_start.clicked.connect(self.start)
        self.button_high.clicked.connect(self.highClick)
        self.button_low.clicked.connect(self.lowClick)
        self.button_reverse.clicked.connect(self.revClick)

    def start(self):
        global inputTime
        self._run_thread.start()
        if setupComple == 0:
           subprocess.call('./ALSAsetup.sh')
        if setupComple == 2:
           os.chmod("record.sh", 0o777)
           subprocess.call(shlex.split('./record.sh '+ inputTime + ' ' + pitch))
   
    def input(self):
        global inputTime
        inputTime = self.line_input.text()
        #self.line_input.setText("hello")
        print(inputTime)

    def highClick(self):
        global pitch
        pitch = "high"
        print(pitch)

    def lowClick(self):
        global pitch
        pitch = "low"
        print(pitch)

    def revClick(self):
        global pitch
        pitch = "reverse"
        print(pitch)
  
    #def stop(self):
     #   self.line.setText("stop")
      #  self._run_thread.terminate()

    def Set_Max(self, data):
        global setupComple, setValComple, MsetValinit 
        if setupComple == 0:	
           self.setupProgress_bar.setMaximum(data)
           setupComple = 1

    def MSet_Max(self, data):
        global setupComple
        if setupComple == 2:
           self.startProgress_bar.setMaximum(data)
           MsetValinit = True
        print(data)
        if data == 100 and setupComple == 2:        
           setupComple = 3
        print(setupComple)

    def Set_Value(self, data): 
        global setupComple
        if setupComple == 1:        
           self.setupProgress_bar.setValue(data)

        if data == 100 and setupComple == 1:
           data = 0
           setupComple = 2
           #print("setSuccess")

    def MSet_Value(self, data):
        global setupComple
        if setupComple == 3:
           self.startProgress_bar.setValue(data)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    MainWindow = MainWindow()
    sys.exit(app.exec_())

