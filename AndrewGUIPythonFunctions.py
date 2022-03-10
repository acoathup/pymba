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
        self.pushButton.clicked.connect(self.centreOfMass)
        self.pushButton_2.clicked.connect(self.calculateWidth)
        #not sure if I need to put an additional line here for the video feed

    def gain(self):
        #this is a function to modify the gain in the video stream
        return None

    def exposure(self):
        #this is a function to modify the exposure in the video stream
        return None

    def centreOfMass(self):
        #this is a function to calculate the centre of mass of the laser spot in pixels
        return None
    
    def calculateWidth(self):
        #this is a function to calculate the 1/e2 width of the laser cross-section
        return None
    

    









if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    window = MainWindow()
    window.show()
    app.exec_()