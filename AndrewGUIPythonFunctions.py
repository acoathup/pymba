# from PyQt5.QtCore import pyqtSlot
# from PyQt5.QtGui import QIcon

from GUI_vimbaCamera import *

class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, *args, **kwargs):
        QtWidgets.QMainWindow.__init__(self, *args, **kwargs)
        self.setupUi(self)
        self.setWindowTitle("Laser Position Verification")
        self.horizontalSlider.valueChanged.connect(self.exposure)
        self.horizontalSlider_2.valueChanged.connect(self.gain)
    

    def gain(self):
        #this is a function to modify the gain in the video stream
        return None

    def exposure(self):
        #this is a function to modify the exposure in the video stream
        return None

    
    









if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    window = MainWindow()
    window.show()
    app.exec_()