from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtCore import QThread, pyqtSignal
from datn_gui import Ui_MainWindow
from robot_mqtt import *
import sys
import os
import json
import shutil
import time


class WorkerThread(QThread):
    progress = pyqtSignal(int)

    def __init__(self):
        super().__init__()
        self._running = True  # cờ điều khiển

    def run(self):
        count = 0
        while self._running :
            time.sleep(0.5)
            count+=0.5
            self.progress.emit(count)

    def stop(self):
        self._running = False

##This is how we create parallel task in qt5
class gui_handling(Ui_MainWindow):
    def __init__(self):
        self.main_window=QtWidgets.QMainWindow()
        self.setupUi(self.main_window)

        self.noteTextBrowser.setPlainText("The coordinate of every shelves are defined following sub shelf" \
        " 1. User should define sub shelf 2 coordinate the same as sub shelf 1")

        ### mqtt worker
        self.mqtt_worker = None
        ### mqttt
        self.gui_mqtt=Robot_MQTT_Position()
        self.portSpinBox.setValue(1883)
        self.BrokerLineEdit.setText("broker.emqx.io")
        self.GUITopicLineEdit.setText("GUI")
        self.robotTopicLineEdit.setText("Robot")
        self.mqttConnectPushButton.clicked.connect(self.mqttStartButtonHandle)
        self.stopMqttPushButton.clicked.connect(self.mqttStopButtonHandle)
        self.sendSettingPushButton.clicked.connect(self.mqttSendSettingButtonHandle)
        self.stopMqttPushButton.setEnabled(False)
        self.sendSettingPushButton.setEnabled(False)
        self.worker = WorkerThread()


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
        self.textBrowser.setText(str)


##  mqtt
    def mqttStartButtonHandle(self):
        broker=self.BrokerLineEdit.text()
        port=self.portSpinBox.value()
        topic=self.GUITopicLineEdit.text()
        self.gui_mqtt.set_up_broker(broker,port,topic)
        self.gui_mqtt.start_mqtt()
        msg=QMessageBox()
        msg.setWindowTitle("MQTT warning")
        msg.setText("MQTT has been connected\nBegin waiting for data")
        msg.setIcon(QMessageBox.Information)

       
        self.mqttConnectPushButton.setEnabled(False)
        self.sendSettingPushButton.setEnabled(True)
        self.stopMqttPushButton.setEnabled(True)
        self.BrokerLineEdit.setReadOnly(True)
        self.GUITopicLineEdit.setReadOnly(True)
        self.start_thread()
        x=msg.exec_()
           
       
    def mqttStopButtonHandle(self):
        self.gui_mqtt.stop_mqtt()
        self.gui_mqtt.disconnect()
        msg=QMessageBox()
        msg.setWindowTitle("MQTT warning")
        msg.setText("MQTT has been disconnected\nStopping receiving data")
        msg.setIcon(QMessageBox.Information)

        x=msg.exec_()

        self.mqttConnectPushButton.setEnabled(True)
        self.sendSettingPushButton.setEnabled(False)
        self.stopMqttPushButton.setEnabled(False)
        self.BrokerLineEdit.setReadOnly(False)
        self.GUITopicLineEdit.setReadOnly(False)
        self.stop_thread()
    

    def mqttSendSettingButtonHandle(self):
        message=''
        for root, dirs, files in os.walk(self.path):
            for file in files:
                if file.endswith(".json"):
                    full_path = os.path.join(root, file)
                    with open(full_path,"r") as readfile:
                        data = json.load(readfile)
                        message=message+f'{data}/'
        rbtext=self.robotTopicLineEdit.text()
        message=message+f'{rbtext}'
        self.gui_mqtt.publish(self.gui_mqtt.topic,message)
        msg=QMessageBox()
        msg.setWindowTitle("MQTT warning")
        msg.setText("MQTT has sent the setting")
        msg.setIcon(QMessageBox.Warning)

        x=msg.exec_()

    def start_thread(self):
        if not self.worker.isRunning():
            self.worker = WorkerThread()  # tạo mới nếu đã stop trước đó
            self.worker.progress.connect(self.waitingDataThread)
            self.worker.start()
        else:
            msg=QMessageBox()
            msg.setWindowTitle("MQTT warning")
            msg.setText("MQTT has already connected")
            msg.setIcon(QMessageBox.Warning)

            x=msg.exec_()

    def stop_thread(self):
        if self.worker.isRunning():
            self.worker.stop()
        else:
            msg=QMessageBox()
            msg.setWindowTitle("MQTT warning")
            msg.setText("MQTT has already stopped")
            msg.setIcon(QMessageBox.Warning)

            x=msg.exec_()

    def waitingDataThread(self):
        if self.gui_mqtt.message==None:
            self.debug("")
            pass
        else:
            message=self.gui_mqtt.get_message()
            self.debug(message)
            

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
        subshelf=self.subShelfIdSpinBox.value()
        state=False
        for root, dirs, files in os.walk(self.path):
            for file in files:
                if file.endswith(".json"):
                    file_name=file.split('.')
                    if file_name[0]==f"shelf{shelf}_{subshelf}":
                        msg=QMessageBox()
                        msg.setWindowTitle("Add shelf warning")
                        msg.setText(f"shelf {shelf}_{subshelf} has already exist so new data will be written on old data")
                        msg.setIcon(QMessageBox.Warning)
                        x=msg.exec_()
                        state=True
                        break
                    else:
                        continue
            if state==False:
                msg=QMessageBox()
                msg.setWindowTitle("Add shelf warning")
                msg.setText(f"shelf {shelf}_{subshelf} will be added right now")
                msg.setIcon(QMessageBox.Information)
                x=msg.exec_()   

                    
        if shelf not in self.shelf_existed:
            self.shelf_existed.add(shelf)
            self.shelfComboBox.addItem(f"Shelf {shelf}")
       
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

        with open(file,"r") as readfile:
            data=str(json.load(readfile))
            self.debug(data)


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
    

    
    