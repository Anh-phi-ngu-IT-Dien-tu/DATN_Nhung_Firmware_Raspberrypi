from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox
from datn_gui import Ui_MainWindow
from robot_mqtt import *
import sys
import os
import json
import shutil


##This is how we create parallel task in qt5
class gui_handling(Ui_MainWindow):
    def __init__(self):
        self.main_window=QtWidgets.QMainWindow()
        self.setupUi(self.main_window)


        ### mqtt worker
        self.mqtt_worker = None
        ### mqttt
        self.gui_mqtt=Robot_MQTT_Position()
        self.portSpinBox.setValue(1883)
        self.BrokerLineEdit.setText("broker.emqx.io")
        self.GUITopicLineEdit.setText("GUI")
        self.mqttConnectPushButton.clicked.connect(self.mqttStartButtonHandle)
        self.stopMqttPushButton.clicked.connect(self.mqttStopButtonHandle)
        self.sendSettingPushButton.clicked.connect(self.mqttSendSettingButtonHandle)
        self.stopMqttPushButton.setEnabled(False)
        self.sendSettingPushButton.setEnabled(False)

        #shelf

        self.path = './shelves_info'

        
        if not os.path.exists(self.path):
            os.mkdir(self.path)
        self.addproductcheck=0

        

        self.productComboBox.addItems(['247', 'Chinsu', 'ChocoPie', 'D.Thanh', 'Heineken', 'Oreo', 'Pepsi-xanh', 'Redbull', 'Revive-chanh', 'Simply', 'TH true Milk', 'Tea Plus', 'Vinamilk', 'coca', 'coca-chai', 'custas', 'fanta-cam', 'khongdo', 'number1', 'sprite-lon', 'sting', 'vinhhao'])
        self.addProductPushButton.clicked.connect(self.addProductButtonHandle) 
        self.subShelfProductLineEdit.setReadOnly(True) 
        self.deleteProductPushButton.clicked.connect(self.deleteProductButtonHandle)      
        self.resetShelfPushButton.clicked.connect(self.resetShelfButtonHandle)
        self.addSubShelfPushButton.clicked.connect(self.addSubShelfButtonHandle)
       


        #watch shelf
        self.shelf_existed={0}
        for root, dirs, files in os.walk(self.path):
            for file in files:
                if file.endswith(".json"):
                    full_path = os.path.join(root, file)
                    with open(full_path,"r") as readfile:
                        data = json.load(readfile)
                        shelf_num=data['Shelf']
                        if shelf_num not in self.shelf_existed:
                            self.shelf_existed.add(shelf_num)
                            self.shelfComboBox.addItem(f"Shelf {shelf_num}")

        self.shelfComboBox.currentIndexChanged.connect(self.shelfComboBoxHandle)
        self.subShelfLineEdit.setReadOnly(True)
        self.subShelfLineEdit_2.setReadOnly(True)
        self.xFromDoubleSpinBox.setReadOnly(True)
        self.yFromDoubleSpinBox.setReadOnly(True)
        self.thetaFromDoubleSpinBox.setReadOnly(True)
        self.xToDoubleSpinBox.setReadOnly(True)
        self.yToDoubleSpinBox.setReadOnly(True)
        self.thetaToDoubleSpinBox.setReadOnly(True)


    def show(self):
        self.main_window.show()


    def debug(self,str=""):
        self.textBrowser.setPlainText(str)


##  mqtt
    def mqttStartButtonHandle(self):
        broker=self.BrokerLineEdit.text()
        port=self.portSpinBox.value()
        topic=self.GUITopicLineEdit.text()
        self.gui_mqtt.set_up_broker(broker,port,topic)
        self.gui_mqtt.start_mqtt()
        msg=QMessageBox()
        msg.setWindowTitle("MQTT warning")
        msg.setText("MQTT has been connected")
        msg.setIcon(QMessageBox.Information)

        x=msg.exec_()
        self.mqttConnectPushButton.setEnabled(False)
        self.sendSettingPushButton.setEnabled(True)
        self.stopMqttPushButton.setEnabled(True)
        self.BrokerLineEdit.setReadOnly(True)
        self.GUITopicLineEdit.setReadOnly(True)
           
       
    def mqttStopButtonHandle(self):
        self.gui_mqtt.stop_mqtt()
        self.gui_mqtt.disconnect()
        msg=QMessageBox()
        msg.setWindowTitle("MQTT warning")
        msg.setText("MQTT has been disconnected")
        msg.setIcon(QMessageBox.Information)

        x=msg.exec_()

        self.mqttConnectPushButton.setEnabled(True)
        self.sendSettingPushButton.setEnabled(False)
        self.stopMqttPushButton.setEnabled(False)
        self.BrokerLineEdit.setReadOnly(False)
        self.GUITopicLineEdit.setReadOnly(False)
    

    def mqttSendSettingButtonHandle(self):
        message=''
        for root, dirs, files in os.walk(self.path):
            for file in files:
                if file.endswith(".json"):
                    full_path = os.path.join(root, file)
                    with open(full_path,"r") as readfile:
                        data = json.load(readfile)
                        message=message+f'{data}/'
                        
        self.gui_mqtt.publish(self.gui_mqtt.topic,message)
        msg=QMessageBox()
        msg.setWindowTitle("MQTT warning")
        msg.setText("MQTT has sent the setting")
        msg.setIcon(QMessageBox.Warning)

        x=msg.exec_()
        


#shelf 

    def addProductButtonHandle(self):
        product=self.productComboBox.currentText()
        if self.addproductcheck==0:
            text=product
        else:
            text=f",{product}"
        self.subShelfProductLineEdit.insert(text)
        self.productComboBox.removeItem(self.productComboBox.currentIndex())
        self.addproductcheck+=1
        pass            
    
    def deleteProductButtonHandle(self):
        self.subShelfProductLineEdit.selectAll()
        self.subShelfProductLineEdit.del_()
        self.addproductcheck=0
        self.productComboBox.clear()
        self.productComboBox.addItems(['247', 'Chinsu', 'ChocoPie', 'D.Thanh', 'Heineken', 'Oreo', 'Pepsi-xanh', 'Redbull', 'Revive-chanh', 'Simply', 'TH true Milk', 'Tea Plus', 'Vinamilk', 'coca', 'coca-chai', 'custas', 'fanta-cam', 'khongdo', 'number1', 'sprite-lon', 'sting', 'vinhhao'])

    def resetShelfButtonHandle(self):
        shutil.rmtree(self.path) 
        os.mkdir(self.path)
        self.shelfComboBox.clear()

    def addSubShelfButtonHandle(self):
        shelf=self.shelfIdSpinBox.value()
        if shelf not in self.shelf_existed:
            self.shelf_existed.add(shelf)
            self.shelfComboBox.addItem(f"Shelf {shelf}")
        subshelf=self.subShelfIdSpinBox.value()
        file=f"{self.path}/shelf{shelf}_{subshelf}.json"
        text=self.subShelfProductLineEdit.text()
        product=text.split(',')
        below=[self.xBelowDoubleSpinBox.value(),self.yBelowDoubleSpinBox.value(),self.thetaBelowDoubleSpinBox.value()]
        above=[self.xAboveDoubleSpinBox.value(),self.yAboveDoubleSpinBox.value(),self.thetaAboveDoubleSpinBox.value()]
        data={
            "Shelf":shelf,
            "Sub shelf":subshelf,
            "Product":product,
            "From":below,
            "To":above
        }
        with open(file,"w") as outfile:
            json.dump(data,outfile,indent=4)


#watch shelf
    def shelfComboBoxHandle(self):
        self.subShelfLineEdit_2.setText("")
        self.subShelfLineEdit.setText("")
        shelf_text=self.shelfComboBox.currentText()
        if shelf_text=="":
            return
        shelf_text_temp=shelf_text.split(' ')
        shelf_num_in_box=int(shelf_text_temp[1])
        for root, dirs, files in os.walk(self.path):
            for file in files:
                if file.endswith(".json"):
                    full_path = os.path.join(root, file)
                    with open(full_path,"r") as readfile:
                        data = json.load(readfile)
                        shelf_num=data['Shelf']
                        if shelf_num==shelf_num_in_box:
                            if data['Sub shelf']==1:
                                for text in data['Product']:    
                                    self.subShelfLineEdit.insert(f"{text},")
                            elif data['Sub shelf']==2:
                                for text in data['Product']:    
                                    self.subShelfLineEdit_2.insert(f"{text},")

                            coor_from=data["From"]
                            coor_to=data["To"]

                            self.xFromDoubleSpinBox.setValue(coor_from[0])
                            self.yFromDoubleSpinBox.setValue(coor_from[1])
                            self.thetaFromDoubleSpinBox.setValue(coor_from[2])

                            self.xToDoubleSpinBox.setValue(coor_to[0])
                            self.yToDoubleSpinBox.setValue(coor_to[1])
                            self.thetaToDoubleSpinBox.setValue(coor_to[2])


                        else:
                            continue
                        

        

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    ui=gui_handling()
    ui.show()
    sys.exit(app.exec_())
    

    
    