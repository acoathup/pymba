# -*- coding: utf-8 -*-
"""
Created on Thu Nov 25 15:55:37 2021

@author: Adrián Bembibre
"""

import serial, time, os
import serial.tools.list_ports
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtGui import QIcon

from flip_servo_ui import *
from connection_popup_ui import *


class MyPopup(QtWidgets.QDialog, Ui_Dialog):
    
    COMPort = QtCore.pyqtSignal(str,str)
    noCOM = QtCore.pyqtSignal()
    
    def __init__(self, *args, **kwargs):
        QtWidgets.QDialog.__init__(self, *args, **kwargs)
        self.setupUi(self)
        self.setModal(True)
        self.buttonBox.accepted.connect(self.buttonOK)
        
        self.buttonBox.rejected.connect(self.buttonCancel)
        self.getCOM()
        
        self.autoClosed = False
        self.port = None
        
    
    def closeEvent(self, event):
        if not self.autoClosed:
            self.noCOM.emit()
    
    
    def buttonOK(self):
        port = self.comboBox.currentText().split()
        # print(port)
        self.COMPort.emit(port[0], port[2])
        self.autoClosed = True
        # self.close()
    
    
    def buttonCancel(self):
        self.noCOM.emit()
    
    
    def getCOM(self):
        portsListed = []
        ports = serial.tools.list_ports.comports()
        for port in sorted(ports):
            portsListed.append(str(port))
        self.comboBox.addItems(portsListed)



class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, *args, **kwargs):
        QtWidgets.QMainWindow.__init__(self, *args, **kwargs)
        self.setupUi(self)
        self.setWindowTitle("Micro Servo Controller")
        # self.setWindowIcon(QIcon("D:/Archivos/Universidade/Doctorado/Arduino/flip_servo_motor/icono/sin-fondo/icono-multi-SF.ico"))
        self.setWindowIcon(QIcon("resources\\icono-multi.ico"))
        self.pushButton_Manual.clicked.connect(self.pushManual)
        self.pushButton_Shutter.clicked.connect(self.pushShutter)
        self.pushButton_In.clicked.connect(self.pushIn)
        self.pushButton_Out.clicked.connect(self.pushOut)
        self.pushButton_Go.clicked.connect(self.pushGo)
        self.pushButton_SetIn.clicked.connect(self.pushSetIn)
        self.pushButton_SetOut.clicked.connect(self.pushSetOut)
        self.pushButton_Params.clicked.connect(self.pushParams)
        self.pushButton_OnOff.clicked.connect(self.pushOnOff)
        self.radioButton_All.toggled.connect(self.selectedMotor)
        self.pushButton_Clear.clicked.connect(self.pushClear)
        self.checkBox_Motor0.toggled.connect(self.selectedMotor)
        self.checkBox_Motor1.toggled.connect(self.selectedMotor)
        self.checkBox_Motor2.toggled.connect(self.selectedMotor)
        self.checkBox_Motor3.toggled.connect(self.selectedMotor)
        self.checkBox_Motor4.toggled.connect(self.selectedMotor)
        # self.pushButton_UpdateLabel.clicked.connect(self.changeLabel)
        self.pushButton_SaveSettings.clicked.connect(self.saveSettings)
        self.action_Enabled.triggered.connect(self.verboseEnabled)
        self.action_Disabled.triggered.connect(self.verboseDisabled)
        
        self.lineEdit_Motor0.editingFinished.connect(self.saveSettings)
        self.lineEdit_Motor1.editingFinished.connect(self.saveSettings)
        self.lineEdit_Motor2.editingFinished.connect(self.saveSettings)
        self.lineEdit_Motor3.editingFinished.connect(self.saveSettings)
        self.lineEdit_Motor4.editingFinished.connect(self.saveSettings)
        
        
        self.widget.setEnabled(False)
        self.pushButton_OnOff.setText("connected")
        
        self.connected = False
        
        self.selectedAllVar = False
        self.selectedMotor0 = False
        self.selectedMotor1 = False
        self.selectedMotor2 = False
        self.selectedMotor3 = False
        self.selectedMotor4 = False
        self.selectedArray = [self.selectedMotor0,self.selectedMotor1,self.selectedMotor2,self.selectedMotor3,self.selectedMotor4]
        self.shutter = False
        self.pushButton_Manual.setCheckable(True)
        self.pushButton_Shutter.setCheckable(True)
        self.pushButton_Manual.setChecked(True)
        self.pushButton_Shutter.setChecked(False)
        
        self.COM = "Puerto no seleccionado\n"
        
        self.mypopup = MyPopup()
        self.mypopup.show()
        self.mypopup.setWindowTitle("Connection Dialog")
        
        self.mypopup.COMPort.connect(self.accepted)
        self.mypopup.noCOM.connect(self.rejectedOrClosed)
        self.initialisation()
        
    
    @pyqtSlot(str,str)  # No entiendo cómo funciona esto
    def accepted(self, COM, device):
        if (device == 'Arduino'): # Para prevenir que se conecte a otro COM porque al no responer 'P' peta al abrir en self.initialisation porque el archivo de ajustes estaría vacío
            self.COM = COM
        # print(self.COM)
        self.pushOnOff()
        
        
    def rejectedOrClosed(self):
        self.plainTextEdit.appendPlainText("No se ha seleccionado puerto COM.\nReiniciar programa para conectar")
        
    
    def closeEvent(self, event):
        if self.connected:
            self.saveSettings()
            self.disconnect()
        
        
    def connect(self):
        try:
            self.arduino = serial.Serial(self.COM, 9600)
            self.plainTextEdit.appendPlainText("Conectado al puerto " + self.COM)
            time.sleep(2)
            self.connected = True
        except Exception as e:
            self.plainTextEdit.appendPlainText("Puerto COM seleccionado incorrecto.\nReinicie el programa para seleccionar el correcto.\n")
    
    
    def disconnect(self):
        if self.connected:
            self.arduino.close()
            self.connected = False
                
        
    def showText(self, params = False):
        if self.action_Enabled.isChecked() or params:   # De momento lo quito porque por problema de timpos no mueve dos motores seguidos sin este sleep
            time.sleep(2)
            while self.arduino.inWaiting():
                rawString = self.arduino.readline()
                string = rawString.decode()
                # self.plainTextEdit.appendPlainText(string)
                self.plainTextEdit.appendPlainText(string[:-2]) # Borra los enter extra que manda el arduino
    
    
    def pushOnOff(self):
        if self.connected:
        # if self.pushButton_OnOff.isChecked():
            self.disconnect()
            self.widget.setEnabled(False)
            self.pushButton_OnOff.setText("connected")
        else:
            self.connect()
            self.widget.setEnabled(True)
            self.initialisation()
            self.pushButton_OnOff.setText("CONNECTED")
        
        
    def initialisation(self):
        if os.path.exists("settingsServoMotors.txt"):
            settings = open("settingsServoMotors.txt", "r")
            params = settings.readlines()
            if (len(params) > 5):
                # self.checkBox_Motor0.setText(str(params[0][:-1]))
                # self.checkBox_Motor1.setText(str(params[1][:-1]))
                # self.checkBox_Motor2.setText(str(params[2][:-1]))
                # self.checkBox_Motor3.setText(str(params[3][:-1]))
                # self.checkBox_Motor4.setText(str(params[4][:-1]))
                self.lineEdit_Motor0.setText(str(params[0][:-1]))
                self.lineEdit_Motor1.setText(str(params[1][:-1]))
                self.lineEdit_Motor2.setText(str(params[2][:-1]))
                self.lineEdit_Motor3.setText(str(params[3][:-1]))
                self.lineEdit_Motor4.setText(str(params[4][:-1]))
            else:
                self.plainTextEdit.appendPlainText("¡ATENCIÓN! Nombre de motores por defecto.\n")
            settings.close()
        else:
            self.plainTextEdit.appendPlainText("¡ATENCIÓN! Nombre de motores por defecto.\n")
        
        
    def pushManual(self):
        if self.connected:
            self.arduino.write(b'M0 0 1 2 3 4\n') # Realmente si es M0 no harían falta los demás pero para que no dé error el arduino que me da pereza cambiarlo ahora que funciona
            self.shutter = False
            self.pushButton_Manual.setChecked(True)
            self.pushButton_Shutter.setChecked(False)
            if self.action_Enabled.isChecked():
                self.plainTextEdit.appendPlainText(self.arduino.readline().decode()[:-2])
        else:
            self.plainTextEdit.appendPlainText("Arduino desconectado")
    
    def pushShutter(self):
        if self.connected:
            if self.radioButton_All.isChecked():
                self.arduino.write(b'M1 0 1 2 3 4\n')
            else:
                nums = self.readNum()
                self.arduino.write(bytes('M1'+' '+str(nums[0])+' '+str(nums[1])+' '+str(nums[2])+' '+str(nums[3])+' '+str(nums[4]) + '\n','utf-8'))
            self.shutter = True
            self.pushButton_Manual.setChecked(False)
            self.pushButton_Shutter.setChecked(True)
            if self.action_Enabled.isChecked():
                self.plainTextEdit.appendPlainText(self.arduino.readline().decode()[:-2])
        else:
            self.plainTextEdit.appendPlainText("Arduino desconectado")
    
    
    def selectedMotor(self):
        if self.radioButton_All.isChecked():
            self.selectedAllVar = True
            self.selectedMotor0 = False
            self.selectedMotor1 = False
            self.selectedMotor2 = False
            self.selectedMotor3 = False
            self.selectedMotor4 = False
        else:
            self.selectedAllVar = False
            self.selectedMotor0 = self.checkBox_Motor0.isChecked()
            self.selectedMotor1 = self.checkBox_Motor1.isChecked()
            self.selectedMotor2 = self.checkBox_Motor2.isChecked()
            self.selectedMotor3 = self.checkBox_Motor3.isChecked()
            self.selectedMotor4 = self.checkBox_Motor4.isChecked()
        self.selectedArray = [self.selectedMotor0,self.selectedMotor1,self.selectedMotor2,self.selectedMotor3,self.selectedMotor4]
        if self.shutter:
            self.pushShutter()
    
    def readNum(self):
        m = 0
        nums = []
        for motor in self.selectedArray:
            if motor:
                nums.append(m)
            else:
                nums.append(999)
            m = m+1
        # self.plainTextEdit.appendPlainText("Selecciona motor")
        return nums
    
    
    # def changeLabel(self):
    #     if self.selectedMotor0:
    #         self.checkBox_Motor0.setText(self.lineEdit_MotorLabel.text())
    #     if self.selectedMotor1:
    #         self.checkBox_Motor1.setText(self.lineEdit_MotorLabel.text())
    #     if self.selectedMotor2:
    #         self.checkBox_Motor2.setText(self.lineEdit_MotorLabel.text())
    #     if self.selectedMotor3:
    #         self.checkBox_Motor3.setText(self.lineEdit_MotorLabel.text())
    #     if self.selectedMotor4:
    #         self.checkBox_Motor4.setText(self.lineEdit_MotorLabel.text())
    #     self.saveSettings()
            
        
    def saveSettings(self):
        settings = open(r"settingsServoMotors.txt", "w+")
        # label0 = str(self.checkBox_Motor0.text())+"\n"    # Motor 0
        # label1 = str(self.checkBox_Motor1.text())+"\n"    # Motor 1
        # label2 = str(self.checkBox_Motor2.text())+"\n"    # Motor 2
        # label3 = str(self.checkBox_Motor3.text())+"\n"    # Motor 3
        # label4 = str(self.checkBox_Motor4.text())+"\n"    # Motor 4
        label0 = str(self.lineEdit_Motor0.text())+"\n"    # Motor 0
        label1 = str(self.lineEdit_Motor1.text())+"\n"    # Motor 1
        label2 = str(self.lineEdit_Motor2.text())+"\n"    # Motor 2
        label3 = str(self.lineEdit_Motor3.text())+"\n"    # Motor 3
        label4 = str(self.lineEdit_Motor4.text())+"\n"    # Motor 4
        sep = "-----------------\n"
        S = [label0,label1,label2,label3,label4,sep]
        settings.writelines(S)
        if self.connected:
            self.arduino.write(b'P\n')
            time.sleep(0.5)
            while self.arduino.inWaiting():
                rawString = self.arduino.readline()
                settings.write(rawString.decode())
        else:
            self.plainTextEdit.appendPlainText("Arduino desconectado")
        settings.close()
                
    
    def pushIn(self):
        if self.connected:
            if self.selectedAllVar:
                self.arduino.write(b'I A\n')
                self.showText()
            else:
                nums = self.readNum()
                for num in nums:
                    if num == 999:
                        continue
                    self.arduino.write(bytes('I '+str(num) + '\n','utf-8'))
                    self.arduino.flush()
                    self.showText()
        else:
            self.plainTextEdit.appendPlainText("Arduino desconectado")
    
    
    def pushOut(self):
        if self.connected:
            if self.selectedAllVar:
                self.arduino.write(b'O A\n')
                self.showText()
            else:
                nums = self.readNum()
                for num in nums:
                    if num == 999:
                        continue
                    self.arduino.write(bytes('O '+str(num) + '\n','utf-8'))
                    self.arduino.flush()
                    self.showText()
        else:
            self.plainTextEdit.appendPlainText("Arduino desconectado")
    
    
    def readPosGo(self):
        posValue = str(self.lineEdit_PosGo.text())
        return posValue
    
    
    def pushGo(self):
        if self.connected:
            if self.selectedAllVar:
                self.arduino.write(bytes('G A ' + self.readPosGo() + '\n','utf-8'))
                self.showText()
            else:
                nums = self.readNum()
                for num in nums:
                    if num == 999:
                        continue
                    self.arduino.write(bytes('G ' + str(num) + ' ' + self.readPosGo() + '\n','utf-8'))
                    self.showText()
        else:
            self.plainTextEdit.appendPlainText("Arduino desconectado")
    
    
    def readPosSet(self):
        posValue = str(self.lineEdit_PosSet.text())
        return posValue
    
    
    def pushSetIn(self):
        if self.connected:
            if self.selectedAllVar:
                self.arduino.write(bytes('S A I=' + self.readPosSet() + '\n','utf-8'))
                self.showText()
            else:
                nums = self.readNum()
                for num in nums:
                    if num == 999:
                        continue
                    self.arduino.write(bytes('S ' + str(num) + ' I=' + self.readPosSet() + '\n','utf-8'))
                    self.showText()
        else:
            self.plainTextEdit.appendPlainText("Arduino desconectado")
    
    
    def pushSetOut(self):
        if self.connected:
            if self.selectedAllVar:
                self.arduino.write(bytes('S A O=' + self.readPosSet() + '\n','utf-8'))
                self.showText()
            else:
                nums = self.readNum()
                for num in nums:
                    if num == 999:
                        continue
                    self.arduino.write(bytes('S ' + str(num) + ' O=' + self.readPosSet() + '\n','utf-8'))
                    self.showText()
        else:
            self.plainTextEdit.appendPlainText("Arduino desconectado")
    
    
    def pushParams(self):
        if self.connected:
            self.arduino.write(b'P\n')
            self.showText(params = True)
        else:
            self.plainTextEdit.appendPlainText("Arduino desconectado")
            
        
    def pushClear(self):
        self.plainTextEdit.clear()
        
        
    def verboseDisabled(self):
        if self.connected:
            self.action_Enabled.setChecked(False)
            self.arduino.write(b'V 0\n')
        else:
            self.action_Disabled.setChecked(False)
            self.plainTextEdit.appendPlainText("Arduino desconectado")
            
    
    def verboseEnabled(self):
        if self.connected:
            self.action_Disabled.setChecked(False)
            self.arduino.write(b'V 1\n')
        else:
            self.action_Enabled.setChecked(False)
            self.plainTextEdit.appendPlainText("Arduino desconectado")
    
    
if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    window = MainWindow()
    window.show()
    app.exec_()
        