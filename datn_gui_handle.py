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
import ast
import yaml


class WorkerThread(QThread):
    progress = pyqtSignal(int)

    def __init__(self):
        super().__init__()
        self._running = True  # cờ điều khiển

    def run(self):
        count = 0
        while self._running :
            time.sleep(0.1)
            count+=0.1
            self.progress.emit(count)

    def stop(self):
        self._running = False

##This is how we create parallel task in qt5
class gui_handling(Ui_MainWindow):
    def __init__(self):
        self.main_window=QtWidgets.QMainWindow()
        self.setupUi(self.main_window)

        self.noteTextBrowser.setPlainText("1. The coordinate of every shelves are defined following sub shelf 1. " \
        "User should define sub shelf 2 coordinate the same as sub shelf 1\n\n" \
        "2. The coordinate values always follow the rule that \"From\" values are smaller than \"To\" values\n\n" \
        "3. With theta values, keep following the the rule but make sure the range is smaller than pi or else the logic of " \
        "algorithm might have a problem. If between theta range there is pi, keep assign the values following the rule, the " \
        "algorithm will handle the pi overfloating problem\n\n" \
        "4. Robot will return a theta value in range (-pi,pi)")

        ### mqtt worker
        self.mqtt_worker = None
        ### mqttt
        self.gui_mqtt=Robot_MQTT_Position()
        self.guiToYoloMqtt=Robot_MQTT_Position()
        self.portSpinBox.setValue(1883)
        self.BrokerLineEdit.setText("broker.emqx.io")
        self.GUITopicLineEdit.setText("GUI")
        self.robotTopicLineEdit.setText("Yolo")
        self.mqttConnectPushButton.clicked.connect(self.mqttStartButtonHandle)
        self.stopMqttPushButton.clicked.connect(self.mqttStopButtonHandle)
        self.sendSettingPushButton.clicked.connect(self.mqttSendSettingButtonHandle)
        self.stopMqttPushButton.setEnabled(False)
        self.sendSettingPushButton.setEnabled(False)
        self.worker = WorkerThread()
        self.read_worker=WorkerThread()

        #path

        self.path = './shelves_info'
        self.status_path='./shelves_status'
        self.temp_path='./shelves_logic'

        
        if not os.path.exists(self.path):
            os.mkdir(self.path)
        if not os.path.exists(self.status_path):
            os.mkdir(self.status_path)
        else:
            shutil.rmtree(self.status_path)
            os.mkdir(self.status_path)

        #shelf
        self.addproductcheck=0
        with open('data.yaml', 'r') as file:
            data_yaml = yaml.safe_load(file)
        self.class_names = data_yaml['names']
        self.productComboBox.addItems(self.class_names)
        self.addProductPushButton.clicked.connect(self.addProductButtonHandle) 
        self.deleteProductPushButton.clicked.connect(self.deleteProductButtonHandle)      
        self.resetShelfPushButton.clicked.connect(self.resetShelfButtonHandle)
        self.addSubShelfPushButton.clicked.connect(self.addSubShelfButtonHandle)
        self.deleteSubShelfPushButton.clicked.connect(self.deleteSubShelfButtonHandle)
        self.loadSubShelfPushButton.clicked.connect(self.loadSubShelfButtonHandle)


        #watch shelf
        self.shelf_existed={0}
        self.watching_shelf=0
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
        self.fixShelfPushButton.clicked.connect(self.fixShelfButtonHandle)
        self.subShelfLineEdit.setReadOnly(True)
        self.subShelfLineEdit_2.setReadOnly(True)
        self.xFromDoubleSpinBox.setReadOnly(True)
        self.yFromDoubleSpinBox.setReadOnly(True)
        self.thetaFromDoubleSpinBox.setReadOnly(True)
        self.xToDoubleSpinBox.setReadOnly(True)
        self.yToDoubleSpinBox.setReadOnly(True)
        self.thetaToDoubleSpinBox.setReadOnly(True)
        self.fixShelfPushButton.setEnabled(False)
        self.wrongObjectTextBrowser.setPlainText("Sub shelf 1: No object\nSub shelf 2: No object")
        self.SOOSObjectTextBrowser.setPlainText("Sub shelf 1: No object\nSub shelf 2: No object")
        self.OOSStatusTextBrowser.setPlainText("Sub shelf 1: No OOS\nSub shelf 2: No OOS")
        self.shelfComboBoxHandle()

    def show(self):
        self.main_window.show()


    def debug(self,str=""):
        self.debugTextBrowser.setPlainText(str)


##  mqtt
    def mqttStartButtonHandle(self):
        broker=self.BrokerLineEdit.text()
        port=self.portSpinBox.value()
        topic=self.GUITopicLineEdit.text()
        self.gui_mqtt.set_up_broker(broker,port,topic)
        self.gui_mqtt.start_mqtt()
        yolo_topic=self.robotTopicLineEdit.text()
        self.guiToYoloMqtt.set_up_broker(broker,port,yolo_topic)
        self.guiToYoloMqtt.start_mqtt()
        msg=QMessageBox()
        msg.setWindowTitle("MQTT warning")
        msg.setText("MQTT has been connected\nBegin waiting for data")
        msg.setIcon(QMessageBox.Information)

        self.mqttConnectPushButton.setEnabled(False)
        self.sendSettingPushButton.setEnabled(True)
        self.stopMqttPushButton.setEnabled(True)
        self.BrokerLineEdit.setReadOnly(True)
        self.GUITopicLineEdit.setReadOnly(True)
        self.robotTopicLineEdit.setReadOnly(True)
        self.fixShelfPushButton.setEnabled(True)
        self.start_thread()
        x=msg.exec_()
           
       
    def mqttStopButtonHandle(self):
        self.gui_mqtt.stop_mqtt()
        self.gui_mqtt.disconnect()
        self.guiToYoloMqtt.stop_mqtt()
        self.guiToYoloMqtt.disconnect()
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
        self.robotTopicLineEdit.setReadOnly(False)
        self.fixShelfPushButton.setEnabled(True)
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
        if not self.worker.isRunning() and not self.read_worker.isRunning():
            self.worker = WorkerThread()  # tạo mới nếu đã stop trước đó
            self.worker.progress.connect(self.waitingDataThread)
            self.read_worker.progress.connect(self.reading_data_thread)
            self.worker.start()
            self.read_worker.start()


    def stop_thread(self):
        if self.worker.isRunning() and self.read_worker.isRunning():
            self.worker.stop()
            self.read_worker.stop()

    def waitingDataThread(self):
        if self.gui_mqtt.message==None:
            pass
        else:
            message=self.gui_mqtt.get_message()
            self.debug(message)
            spilt_message=message.split('\n')
            if spilt_message[0]=='stop':
                return
            for deal_message in spilt_message:
                try:
                    if deal_message.startswith("Shelf"):
                        temp_message=deal_message.split('/')
                        index_part=temp_message[0].replace("Shelf","")
                        index=index_part.split("_")
                        x=int(index[0])
                        y=int(index[1])
                        wrong_object_text=temp_message[1].replace("Wrong object :","")
                        soos_text=temp_message[2].replace("-- SOOS:","")
                        oos_text=temp_message[3].replace("-- OOS:","")
                        file=f"shelf{x}_{y}.txt"
                        full_status_file=f"{self.status_path}/{file}"
                        with open(full_status_file, "w", encoding="utf-8") as f:
                            f.write(wrong_object_text+'\n')
                            f.write(soos_text+'\n')
                            f.write(oos_text+'\n')
                except:
                    print("error in handling received frame")
                    return

            #read data 
            
    def reading_data_thread(self):
        wrong_message=''
        soos_message=''
        oos_message=''

        for i in range(1,3):
            wrong_message=wrong_message+f"\nSub shelf {i}: "
            soos_message=soos_message+f"\nSub shelf {i}: "
            oos_message=oos_message+f"\nSub shelf {i}: "
            file=f"shelf{self.watching_shelf}_{i}.txt"
            file_path=f"{self.status_path}/{file}"
            if not os.path.exists(file_path):
                print(f"shelf{self.watching_shelf}")
                print("file doesn't exist")
                wrong_message=wrong_message+"No object"
                soos_message=soos_message+"No object"
                oos_message=oos_message+"No OOS"
                continue
            with open(file_path, "r", encoding="utf-8") as f:
                lines = f.readlines()
            temp=[]
            for line in lines:                
                line=line.replace("{","")
                line=line.replace("}","")
                line=line.replace('[',"")
                line=line.replace(']',"")
                line=line.replace(' ','')
                line=line.replace('\'','')
                
                temp.append(line.strip())
                
            lines=temp
            wrong_object_result,soos_result,oos_result=lines
            if wrong_object_result!='':
                data=wrong_object_result.split(',')
                for temp in data: 
                    temp=temp.replace("object:","")
                    if temp!='':
                        wrong_message=wrong_message+temp+',' 
            else:
                wrong_message=wrong_message+"No object"
            if soos_result!='':
                data=soos_result.split(',')
                if data[-1]!=':0':
                    state=False
                    for temp in data[:-1]:
                        split_temp=temp.split(':')
                        if split_temp[1]=='1':
                            soos_message=soos_message+split_temp[0]+','
                            state=True
                    if state==False:
                        soos_message=soos_message+'SOOS exist but unknow object'
                else:
                    soos_message=soos_message+"No object"
            else:
                soos_message=soos_message+"No object"  
            if oos_result!='':
                data=oos_result.split(',')
                if data[-1]!=':0':

                    oos_message=oos_message+"OOS exist"
                else:
                    oos_message=oos_message+"No OOS"

            else:
                oos_message=oos_message+"No OOS"
            
        self.wrongObjectTextBrowser.setPlainText(wrong_message)
        self.SOOSObjectTextBrowser.setPlainText(soos_message)
        self.OOSStatusTextBrowser.setPlainText(oos_message)

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
        self.productComboBox.addItems(self.class_names)

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
    
    def deleteSubShelfButtonHandle(self):
        shelf=self.shelfIdSpinBox.value()
        subshelf=self.subShelfIdSpinBox.value()
        state=False
        for root, dirs, files in os.walk(self.path):
            for file in files:
                if file.endswith(".json"):
                    file_name=file.split('.')
                    if file_name[0]==f"shelf{shelf}_{subshelf}":
                        msg=QMessageBox()
                        msg.setWindowTitle("Delete shelf warning")
                        msg.setText(f"Deleting shelf {shelf}_{subshelf} ")
                        msg.setIcon(QMessageBox.Warning)
                        x=msg.exec_()
                        full_path=os.path.join(root,file)
                        os.remove(full_path)
                        state=True
                        break
                    else:
                        continue
            
            if state==False:
                msg=QMessageBox()
                msg.setWindowTitle("Deleting shelf warning")
                msg.setText(f"{shelf}_{subshelf} has already been deleted")
                msg.setIcon(QMessageBox.Information)
                x=msg.exec_() 

        num={0}
        for root, dirs, files in os.walk(self.path):
            for file in files:
                if file.endswith(".json"):
                    file_name=file.split('.')
                    t=int(file_name[0].replace("shelf","").split('_')[0])
                    num.add(t)
        
        temp={0}
        temp.remove(0)
        for j in self.shelf_existed:
            if j not in num:
                temp.add(j)
                self.shelfComboBox.removeItem(self.shelfComboBox.findText(f"Shelf {j}"))
        
        for k in temp:
            self.shelf_existed.remove(k)

            
    def loadSubShelfButtonHandle(self):
        shelf=self.shelfIdSpinBox.value()
        subshelf=self.subShelfIdSpinBox.value()
        state=False
        for root, dirs, files in os.walk(self.path):
            for file in files:
                if file.endswith(".json"):
                    file_name=file.split('.')
                    if file_name[0]==f"shelf{shelf}_{subshelf}":
                        msg=QMessageBox()
                        msg.setWindowTitle("Load shelf warning")
                        msg.setText(f"Loading shelf {shelf}_{subshelf} ")
                        msg.setIcon(QMessageBox.Information)
                        x=msg.exec_()
                        full_path=os.path.join(root,file)
                        with open(full_path,"r") as readfile:
                            data=json.load(readfile)
                        text_data=data['Product']
                        text=''
                        for t in text_data:
                            text=text+f",{t}"
                        text=text.replace(',','',1)
                        self.subShelfProductLineEdit.setText(text)
                        below=data['From']
                        above=data['To']
                        self.xBelowDoubleSpinBox.setValue(below[0])
                        self.yBelowDoubleSpinBox.setValue(below[1])
                        self.thetaBelowDoubleSpinBox.setValue(below[2])
                        self.xAboveDoubleSpinBox.setValue(above[0])
                        self.yAboveDoubleSpinBox.setValue(above[1])
                        self.thetaAboveDoubleSpinBox.setValue(above[2])
                        state=True
                        file=f"{self.path}/shelf{shelf}_{subshelf}.json"
                        with open(file,"r") as readfile:
                            data=str(json.load(readfile))
                            self.debug(data)

                        state=True
                        break
                    else:
                        continue
            
            if state==False:
                msg=QMessageBox()
                msg.setWindowTitle("Loading shelf warning")
                msg.setText(f"{shelf}_{subshelf} does not exist")
                msg.setIcon(QMessageBox.Information)
                x=msg.exec_() 

        


#watch shelf
    def shelfComboBoxHandle(self):
        self.subShelfLineEdit_2.setText("")
        self.subShelfLineEdit.setText("")
        shelf_text=self.shelfComboBox.currentText()
        if shelf_text=="":
            return
        shelf_text_temp=shelf_text.split(' ')
        shelf_num_in_box=int(shelf_text_temp[1])
        self.watching_shelf=shelf_num_in_box
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

                            if data['Sub shelf']==1:
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

    def fixShelfButtonHandle(self):
        send_message=f"Shelf{self.watching_shelf}"
        self.guiToYoloMqtt.publish(self.guiToYoloMqtt.topic,send_message)

    
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    ui=gui_handling()
    ui.show()
    sys.exit(app.exec_())
    

    
    