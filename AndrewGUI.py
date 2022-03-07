# from vimba import *
import sys
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QWidget
from PyQt5 import uic

qtcreator_file  = "C:\\Users\\Andrew\\Documents\\PhDSantiago\\VimbaCameraGUI\\GUI_vimbaCamera.ui" # Enter file here.
# Ui_MainWindow, QtBaseClass = uic.loadUiType(qtcreator_file)


'''From the example below'''

app = QApplication(sys.argv)

window = QWidget()
window.setWindowTitle('PyQt5 App')
window.setGeometry(100, 100, 280, 80)
window.move(60, 15)
helloMsg = QLabel('<h1>Hello World!</h1>', parent=window)
helloMsg.move(60, 15)

window.show()

sys.exit(app.exec_())


'''This is an outline of code for the QT designer. Just have to put the file path below to the ui.'''

# import sys
# from PyQt5 import QtWidgets, uic

# qtcreator_file  = "C:\\Users\\Andrew\\Documents\\PhDSantiago\\VimbaCameraGUI\\GUI_vimbaCamera.ui" # Enter file here.
# Ui_MainWindow, QtBaseClass = uic.loadUiType(qtcreator_file)


# class MyApp(QtWidgets.QMainWindow, Ui_MainWindow):
#     def __init__(self):
#         QtWidgets.QMainWindow.__init__(self)
#         Ui_MainWindow.__init__(self)
#         self.setupUi(self)

# if __name__ == "__main__":
#     app = QtWidgets.QApplication(sys.argv)
#     window = MyWindow()
#     window.show()
#     sys.exit(app.exec_())