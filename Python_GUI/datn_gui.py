# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'DATN_GUI.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1400, 815)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.ShelfPropertiesGroupBox = QtWidgets.QGroupBox(self.centralwidget)
        self.ShelfPropertiesGroupBox.setGeometry(QtCore.QRect(0, 160, 801, 291))
        font = QtGui.QFont()
        font.setPointSize(9)
        self.ShelfPropertiesGroupBox.setFont(font)
        self.ShelfPropertiesGroupBox.setObjectName("ShelfPropertiesGroupBox")
        self.subShelfProductLineEdit = QtWidgets.QLineEdit(self.ShelfPropertiesGroupBox)
        self.subShelfProductLineEdit.setGeometry(QtCore.QRect(130, 70, 661, 22))
        self.subShelfProductLineEdit.setText("")
        self.subShelfProductLineEdit.setObjectName("subShelfProductLineEdit")
        self.subShelfPositionDefineGroupBox = QtWidgets.QGroupBox(self.ShelfPropertiesGroupBox)
        self.subShelfPositionDefineGroupBox.setGeometry(QtCore.QRect(0, 100, 791, 81))
        self.subShelfPositionDefineGroupBox.setObjectName("subShelfPositionDefineGroupBox")
        self.label_4 = QtWidgets.QLabel(self.subShelfPositionDefineGroupBox)
        self.label_4.setGeometry(QtCore.QRect(20, 50, 81, 16))
        self.label_4.setObjectName("label_4")
        self.xBelowDoubleSpinBox = QtWidgets.QDoubleSpinBox(self.subShelfPositionDefineGroupBox)
        self.xBelowDoubleSpinBox.setGeometry(QtCore.QRect(110, 50, 91, 22))
        self.xBelowDoubleSpinBox.setMinimum(-5000.0)
        self.xBelowDoubleSpinBox.setMaximum(5000.0)
        self.xBelowDoubleSpinBox.setObjectName("xBelowDoubleSpinBox")
        self.label_5 = QtWidgets.QLabel(self.subShelfPositionDefineGroupBox)
        self.label_5.setGeometry(QtCore.QRect(110, 20, 91, 21))
        self.label_5.setAlignment(QtCore.Qt.AlignCenter)
        self.label_5.setObjectName("label_5")
        self.label_6 = QtWidgets.QLabel(self.subShelfPositionDefineGroupBox)
        self.label_6.setGeometry(QtCore.QRect(210, 20, 91, 21))
        self.label_6.setAlignment(QtCore.Qt.AlignCenter)
        self.label_6.setObjectName("label_6")
        self.yBelowDoubleSpinBox = QtWidgets.QDoubleSpinBox(self.subShelfPositionDefineGroupBox)
        self.yBelowDoubleSpinBox.setGeometry(QtCore.QRect(210, 50, 91, 22))
        self.yBelowDoubleSpinBox.setMinimum(-5000.0)
        self.yBelowDoubleSpinBox.setMaximum(5000.0)
        self.yBelowDoubleSpinBox.setObjectName("yBelowDoubleSpinBox")
        self.label_7 = QtWidgets.QLabel(self.subShelfPositionDefineGroupBox)
        self.label_7.setGeometry(QtCore.QRect(310, 20, 91, 21))
        self.label_7.setAlignment(QtCore.Qt.AlignCenter)
        self.label_7.setObjectName("label_7")
        self.thetaBelowDoubleSpinBox = QtWidgets.QDoubleSpinBox(self.subShelfPositionDefineGroupBox)
        self.thetaBelowDoubleSpinBox.setGeometry(QtCore.QRect(310, 50, 91, 22))
        self.thetaBelowDoubleSpinBox.setMinimum(-5000.0)
        self.thetaBelowDoubleSpinBox.setMaximum(5000.0)
        self.thetaBelowDoubleSpinBox.setObjectName("thetaBelowDoubleSpinBox")
        self.label_8 = QtWidgets.QLabel(self.subShelfPositionDefineGroupBox)
        self.label_8.setGeometry(QtCore.QRect(420, 50, 51, 16))
        self.label_8.setObjectName("label_8")
        self.yAboveDoubleSpinBox = QtWidgets.QDoubleSpinBox(self.subShelfPositionDefineGroupBox)
        self.yAboveDoubleSpinBox.setGeometry(QtCore.QRect(560, 50, 91, 22))
        self.yAboveDoubleSpinBox.setMinimum(-5000.0)
        self.yAboveDoubleSpinBox.setMaximum(5000.0)
        self.yAboveDoubleSpinBox.setObjectName("yAboveDoubleSpinBox")
        self.label_9 = QtWidgets.QLabel(self.subShelfPositionDefineGroupBox)
        self.label_9.setGeometry(QtCore.QRect(460, 20, 91, 21))
        self.label_9.setAlignment(QtCore.Qt.AlignCenter)
        self.label_9.setObjectName("label_9")
        self.label_10 = QtWidgets.QLabel(self.subShelfPositionDefineGroupBox)
        self.label_10.setGeometry(QtCore.QRect(660, 20, 91, 21))
        self.label_10.setAlignment(QtCore.Qt.AlignCenter)
        self.label_10.setObjectName("label_10")
        self.xAboveDoubleSpinBox = QtWidgets.QDoubleSpinBox(self.subShelfPositionDefineGroupBox)
        self.xAboveDoubleSpinBox.setGeometry(QtCore.QRect(460, 50, 91, 22))
        self.xAboveDoubleSpinBox.setMinimum(-5000.0)
        self.xAboveDoubleSpinBox.setMaximum(5000.0)
        self.xAboveDoubleSpinBox.setObjectName("xAboveDoubleSpinBox")
        self.label_11 = QtWidgets.QLabel(self.subShelfPositionDefineGroupBox)
        self.label_11.setGeometry(QtCore.QRect(560, 20, 91, 21))
        self.label_11.setAlignment(QtCore.Qt.AlignCenter)
        self.label_11.setObjectName("label_11")
        self.thetaAboveDoubleSpinBox = QtWidgets.QDoubleSpinBox(self.subShelfPositionDefineGroupBox)
        self.thetaAboveDoubleSpinBox.setGeometry(QtCore.QRect(660, 50, 91, 22))
        self.thetaAboveDoubleSpinBox.setMinimum(-5000.0)
        self.thetaAboveDoubleSpinBox.setMaximum(5000.0)
        self.thetaAboveDoubleSpinBox.setObjectName("thetaAboveDoubleSpinBox")
        self.label_12 = QtWidgets.QLabel(self.ShelfPropertiesGroupBox)
        self.label_12.setGeometry(QtCore.QRect(10, 200, 51, 16))
        self.label_12.setObjectName("label_12")
        self.shelfIdSpinBox = QtWidgets.QSpinBox(self.ShelfPropertiesGroupBox)
        self.shelfIdSpinBox.setGeometry(QtCore.QRect(90, 200, 71, 22))
        self.shelfIdSpinBox.setMinimum(1)
        self.shelfIdSpinBox.setMaximum(4)
        self.shelfIdSpinBox.setObjectName("shelfIdSpinBox")
        self.subShelfIdSpinBox = QtWidgets.QSpinBox(self.ShelfPropertiesGroupBox)
        self.subShelfIdSpinBox.setGeometry(QtCore.QRect(340, 200, 71, 22))
        self.subShelfIdSpinBox.setMinimum(1)
        self.subShelfIdSpinBox.setMaximum(2)
        self.subShelfIdSpinBox.setObjectName("subShelfIdSpinBox")
        self.label_13 = QtWidgets.QLabel(self.ShelfPropertiesGroupBox)
        self.label_13.setGeometry(QtCore.QRect(230, 200, 91, 20))
        self.label_13.setObjectName("label_13")
        self.label_14 = QtWidgets.QLabel(self.ShelfPropertiesGroupBox)
        self.label_14.setGeometry(QtCore.QRect(10, 70, 121, 16))
        self.label_14.setObjectName("label_14")
        self.addSubShelfPushButton = QtWidgets.QPushButton(self.ShelfPropertiesGroupBox)
        self.addSubShelfPushButton.setGeometry(QtCore.QRect(220, 250, 121, 28))
        self.addSubShelfPushButton.setObjectName("addSubShelfPushButton")
        self.resetShelfPushButton = QtWidgets.QPushButton(self.ShelfPropertiesGroupBox)
        self.resetShelfPushButton.setGeometry(QtCore.QRect(70, 250, 111, 28))
        self.resetShelfPushButton.setObjectName("resetShelfPushButton")
        self.productComboBox = QtWidgets.QComboBox(self.ShelfPropertiesGroupBox)
        self.productComboBox.setGeometry(QtCore.QRect(10, 30, 231, 22))
        self.productComboBox.setObjectName("productComboBox")
        self.addProductPushButton = QtWidgets.QPushButton(self.ShelfPropertiesGroupBox)
        self.addProductPushButton.setGeometry(QtCore.QRect(280, 30, 93, 28))
        self.addProductPushButton.setObjectName("addProductPushButton")
        self.deleteProductPushButton = QtWidgets.QPushButton(self.ShelfPropertiesGroupBox)
        self.deleteProductPushButton.setGeometry(QtCore.QRect(450, 30, 121, 28))
        self.deleteProductPushButton.setObjectName("deleteProductPushButton")
        self.deleteSubShelfPushButton = QtWidgets.QPushButton(self.ShelfPropertiesGroupBox)
        self.deleteSubShelfPushButton.setGeometry(QtCore.QRect(390, 250, 121, 28))
        self.deleteSubShelfPushButton.setObjectName("deleteSubShelfPushButton")
        self.loadSubShelfPushButton = QtWidgets.QPushButton(self.ShelfPropertiesGroupBox)
        self.loadSubShelfPushButton.setGeometry(QtCore.QRect(560, 250, 121, 28))
        self.loadSubShelfPushButton.setObjectName("loadSubShelfPushButton")
        self.DebugGroupBox = QtWidgets.QGroupBox(self.centralwidget)
        self.DebugGroupBox.setGeometry(QtCore.QRect(0, 450, 801, 181))
        font = QtGui.QFont()
        font.setPointSize(9)
        self.DebugGroupBox.setFont(font)
        self.DebugGroupBox.setObjectName("DebugGroupBox")
        self.debugTextBrowser = QtWidgets.QTextBrowser(self.DebugGroupBox)
        self.debugTextBrowser.setGeometry(QtCore.QRect(10, 30, 781, 141))
        self.debugTextBrowser.setTabStopWidth(150)
        self.debugTextBrowser.setObjectName("debugTextBrowser")
        self.mqttGroupBox = QtWidgets.QGroupBox(self.centralwidget)
        self.mqttGroupBox.setGeometry(QtCore.QRect(0, 20, 791, 131))
        font = QtGui.QFont()
        font.setPointSize(9)
        self.mqttGroupBox.setFont(font)
        self.mqttGroupBox.setObjectName("mqttGroupBox")
        self.label_16 = QtWidgets.QLabel(self.mqttGroupBox)
        self.label_16.setGeometry(QtCore.QRect(30, 30, 55, 16))
        self.label_16.setObjectName("label_16")
        self.BrokerLineEdit = QtWidgets.QLineEdit(self.mqttGroupBox)
        self.BrokerLineEdit.setGeometry(QtCore.QRect(90, 30, 221, 22))
        self.BrokerLineEdit.setObjectName("BrokerLineEdit")
        self.label_17 = QtWidgets.QLabel(self.mqttGroupBox)
        self.label_17.setGeometry(QtCore.QRect(340, 30, 55, 16))
        self.label_17.setObjectName("label_17")
        self.portSpinBox = QtWidgets.QSpinBox(self.mqttGroupBox)
        self.portSpinBox.setGeometry(QtCore.QRect(410, 30, 111, 22))
        self.portSpinBox.setMaximum(3000)
        self.portSpinBox.setObjectName("portSpinBox")
        self.mqttConnectPushButton = QtWidgets.QPushButton(self.mqttGroupBox)
        self.mqttConnectPushButton.setGeometry(QtCore.QRect(550, 30, 93, 28))
        self.mqttConnectPushButton.setObjectName("mqttConnectPushButton")
        self.stopMqttPushButton = QtWidgets.QPushButton(self.mqttGroupBox)
        self.stopMqttPushButton.setGeometry(QtCore.QRect(670, 30, 93, 28))
        self.stopMqttPushButton.setObjectName("stopMqttPushButton")
        self.label_2 = QtWidgets.QLabel(self.mqttGroupBox)
        self.label_2.setGeometry(QtCore.QRect(30, 90, 81, 16))
        self.label_2.setObjectName("label_2")
        self.GUITopicLineEdit = QtWidgets.QLineEdit(self.mqttGroupBox)
        self.GUITopicLineEdit.setGeometry(QtCore.QRect(120, 90, 131, 22))
        self.GUITopicLineEdit.setObjectName("GUITopicLineEdit")
        self.sendSettingPushButton = QtWidgets.QPushButton(self.mqttGroupBox)
        self.sendSettingPushButton.setGeometry(QtCore.QRect(670, 90, 93, 28))
        self.sendSettingPushButton.setObjectName("sendSettingPushButton")
        self.label = QtWidgets.QLabel(self.mqttGroupBox)
        self.label.setGeometry(QtCore.QRect(300, 90, 91, 16))
        self.label.setObjectName("label")
        self.robotTopicLineEdit = QtWidgets.QLineEdit(self.mqttGroupBox)
        self.robotTopicLineEdit.setGeometry(QtCore.QRect(410, 90, 151, 22))
        self.robotTopicLineEdit.setObjectName("robotTopicLineEdit")
        self.watchShelfgroupBox = QtWidgets.QGroupBox(self.centralwidget)
        self.watchShelfgroupBox.setGeometry(QtCore.QRect(810, 50, 581, 711))
        font = QtGui.QFont()
        font.setPointSize(9)
        self.watchShelfgroupBox.setFont(font)
        self.watchShelfgroupBox.setObjectName("watchShelfgroupBox")
        self.shelfComboBox = QtWidgets.QComboBox(self.watchShelfgroupBox)
        self.shelfComboBox.setGeometry(QtCore.QRect(20, 30, 171, 22))
        self.shelfComboBox.setMaxVisibleItems(11)
        self.shelfComboBox.setObjectName("shelfComboBox")
        self.subShelfLineEdit = QtWidgets.QLineEdit(self.watchShelfgroupBox)
        self.subShelfLineEdit.setGeometry(QtCore.QRect(20, 70, 441, 22))
        self.subShelfLineEdit.setObjectName("subShelfLineEdit")
        self.label_18 = QtWidgets.QLabel(self.watchShelfgroupBox)
        self.label_18.setGeometry(QtCore.QRect(490, 70, 81, 16))
        self.label_18.setObjectName("label_18")
        self.subShelfLineEdit_2 = QtWidgets.QLineEdit(self.watchShelfgroupBox)
        self.subShelfLineEdit_2.setGeometry(QtCore.QRect(20, 110, 441, 22))
        self.subShelfLineEdit_2.setObjectName("subShelfLineEdit_2")
        self.label_19 = QtWidgets.QLabel(self.watchShelfgroupBox)
        self.label_19.setGeometry(QtCore.QRect(490, 110, 81, 16))
        self.label_19.setObjectName("label_19")
        self.ShelfPositionGroupBox = QtWidgets.QGroupBox(self.watchShelfgroupBox)
        self.ShelfPositionGroupBox.setGeometry(QtCore.QRect(20, 150, 551, 151))
        self.ShelfPositionGroupBox.setObjectName("ShelfPositionGroupBox")
        self.label_21 = QtWidgets.QLabel(self.ShelfPositionGroupBox)
        self.label_21.setGeometry(QtCore.QRect(20, 50, 81, 16))
        self.label_21.setObjectName("label_21")
        self.xFromDoubleSpinBox = QtWidgets.QDoubleSpinBox(self.ShelfPositionGroupBox)
        self.xFromDoubleSpinBox.setGeometry(QtCore.QRect(110, 50, 91, 22))
        self.xFromDoubleSpinBox.setMinimum(-5000.0)
        self.xFromDoubleSpinBox.setMaximum(5000.0)
        self.xFromDoubleSpinBox.setObjectName("xFromDoubleSpinBox")
        self.label_22 = QtWidgets.QLabel(self.ShelfPositionGroupBox)
        self.label_22.setGeometry(QtCore.QRect(110, 20, 91, 21))
        self.label_22.setAlignment(QtCore.Qt.AlignCenter)
        self.label_22.setObjectName("label_22")
        self.label_23 = QtWidgets.QLabel(self.ShelfPositionGroupBox)
        self.label_23.setGeometry(QtCore.QRect(210, 20, 91, 21))
        self.label_23.setAlignment(QtCore.Qt.AlignCenter)
        self.label_23.setObjectName("label_23")
        self.yFromDoubleSpinBox = QtWidgets.QDoubleSpinBox(self.ShelfPositionGroupBox)
        self.yFromDoubleSpinBox.setGeometry(QtCore.QRect(210, 50, 91, 22))
        self.yFromDoubleSpinBox.setMinimum(-5000.0)
        self.yFromDoubleSpinBox.setMaximum(5000.0)
        self.yFromDoubleSpinBox.setObjectName("yFromDoubleSpinBox")
        self.label_24 = QtWidgets.QLabel(self.ShelfPositionGroupBox)
        self.label_24.setGeometry(QtCore.QRect(310, 20, 91, 21))
        self.label_24.setAlignment(QtCore.Qt.AlignCenter)
        self.label_24.setObjectName("label_24")
        self.thetaFromDoubleSpinBox = QtWidgets.QDoubleSpinBox(self.ShelfPositionGroupBox)
        self.thetaFromDoubleSpinBox.setGeometry(QtCore.QRect(310, 50, 91, 22))
        self.thetaFromDoubleSpinBox.setMinimum(-5000.0)
        self.thetaFromDoubleSpinBox.setMaximum(5000.0)
        self.thetaFromDoubleSpinBox.setObjectName("thetaFromDoubleSpinBox")
        self.label_25 = QtWidgets.QLabel(self.ShelfPositionGroupBox)
        self.label_25.setGeometry(QtCore.QRect(20, 100, 81, 16))
        self.label_25.setObjectName("label_25")
        self.xToDoubleSpinBox = QtWidgets.QDoubleSpinBox(self.ShelfPositionGroupBox)
        self.xToDoubleSpinBox.setGeometry(QtCore.QRect(110, 100, 91, 22))
        self.xToDoubleSpinBox.setMinimum(-5000.0)
        self.xToDoubleSpinBox.setMaximum(5000.0)
        self.xToDoubleSpinBox.setObjectName("xToDoubleSpinBox")
        self.yToDoubleSpinBox = QtWidgets.QDoubleSpinBox(self.ShelfPositionGroupBox)
        self.yToDoubleSpinBox.setGeometry(QtCore.QRect(210, 100, 91, 22))
        self.yToDoubleSpinBox.setMinimum(-5000.0)
        self.yToDoubleSpinBox.setMaximum(5000.0)
        self.yToDoubleSpinBox.setObjectName("yToDoubleSpinBox")
        self.thetaToDoubleSpinBox = QtWidgets.QDoubleSpinBox(self.ShelfPositionGroupBox)
        self.thetaToDoubleSpinBox.setGeometry(QtCore.QRect(310, 100, 91, 22))
        self.thetaToDoubleSpinBox.setMinimum(-5000.0)
        self.thetaToDoubleSpinBox.setMaximum(5000.0)
        self.thetaToDoubleSpinBox.setObjectName("thetaToDoubleSpinBox")
        self.shelfStatusGroupBox = QtWidgets.QGroupBox(self.watchShelfgroupBox)
        self.shelfStatusGroupBox.setGeometry(QtCore.QRect(20, 300, 561, 391))
        self.shelfStatusGroupBox.setObjectName("shelfStatusGroupBox")
        self.label_3 = QtWidgets.QLabel(self.shelfStatusGroupBox)
        self.label_3.setGeometry(QtCore.QRect(10, 60, 101, 16))
        self.label_3.setObjectName("label_3")
        self.label_15 = QtWidgets.QLabel(self.shelfStatusGroupBox)
        self.label_15.setGeometry(QtCore.QRect(10, 180, 101, 16))
        self.label_15.setObjectName("label_15")
        self.label_20 = QtWidgets.QLabel(self.shelfStatusGroupBox)
        self.label_20.setGeometry(QtCore.QRect(10, 270, 101, 16))
        self.label_20.setObjectName("label_20")
        self.fixShelfPushButton = QtWidgets.QPushButton(self.shelfStatusGroupBox)
        self.fixShelfPushButton.setGeometry(QtCore.QRect(210, 350, 151, 28))
        self.fixShelfPushButton.setCheckable(False)
        self.fixShelfPushButton.setObjectName("fixShelfPushButton")
        self.wrongObjectTextBrowser = QtWidgets.QTextBrowser(self.shelfStatusGroupBox)
        self.wrongObjectTextBrowser.setGeometry(QtCore.QRect(110, 40, 421, 71))
        self.wrongObjectTextBrowser.setObjectName("wrongObjectTextBrowser")
        self.SOOSObjectTextBrowser = QtWidgets.QTextBrowser(self.shelfStatusGroupBox)
        self.SOOSObjectTextBrowser.setGeometry(QtCore.QRect(110, 150, 421, 71))
        self.SOOSObjectTextBrowser.setObjectName("SOOSObjectTextBrowser")
        self.OOSStatusTextBrowser = QtWidgets.QTextBrowser(self.shelfStatusGroupBox)
        self.OOSStatusTextBrowser.setGeometry(QtCore.QRect(110, 250, 421, 71))
        self.OOSStatusTextBrowser.setObjectName("OOSStatusTextBrowser")
        self.noteGroupBox = QtWidgets.QGroupBox(self.centralwidget)
        self.noteGroupBox.setGeometry(QtCore.QRect(0, 630, 801, 151))
        font = QtGui.QFont()
        font.setPointSize(9)
        self.noteGroupBox.setFont(font)
        self.noteGroupBox.setObjectName("noteGroupBox")
        self.noteTextBrowser = QtWidgets.QTextBrowser(self.noteGroupBox)
        self.noteTextBrowser.setGeometry(QtCore.QRect(10, 20, 781, 111))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.noteTextBrowser.setFont(font)
        self.noteTextBrowser.setObjectName("noteTextBrowser")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1400, 26))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "DATN-GUI"))
        self.ShelfPropertiesGroupBox.setTitle(_translate("MainWindow", "Shelf properties"))
        self.subShelfPositionDefineGroupBox.setTitle(_translate("MainWindow", "Sub shelf position"))
        self.label_4.setText(_translate("MainWindow", "From "))
        self.label_5.setText(_translate("MainWindow", "x"))
        self.label_6.setText(_translate("MainWindow", "y"))
        self.label_7.setText(_translate("MainWindow", "theta"))
        self.label_8.setText(_translate("MainWindow", "To"))
        self.label_9.setText(_translate("MainWindow", "x"))
        self.label_10.setText(_translate("MainWindow", "theta"))
        self.label_11.setText(_translate("MainWindow", "y"))
        self.label_12.setText(_translate("MainWindow", "Shelf id"))
        self.label_13.setText(_translate("MainWindow", "Sub shelf id"))
        self.label_14.setText(_translate("MainWindow", "Sub shelf product"))
        self.addSubShelfPushButton.setText(_translate("MainWindow", "Add sub shelf"))
        self.resetShelfPushButton.setText(_translate("MainWindow", "Reset shelf"))
        self.addProductPushButton.setText(_translate("MainWindow", "Add product"))
        self.deleteProductPushButton.setText(_translate("MainWindow", "Delete product"))
        self.deleteSubShelfPushButton.setText(_translate("MainWindow", "Delete sub shelf"))
        self.loadSubShelfPushButton.setText(_translate("MainWindow", "Load sub shelf"))
        self.DebugGroupBox.setTitle(_translate("MainWindow", "Debug"))
        self.mqttGroupBox.setTitle(_translate("MainWindow", "MQTT properties"))
        self.label_16.setText(_translate("MainWindow", "Broker"))
        self.label_17.setText(_translate("MainWindow", "Port"))
        self.mqttConnectPushButton.setText(_translate("MainWindow", "Connect"))
        self.stopMqttPushButton.setText(_translate("MainWindow", "Stop connect"))
        self.label_2.setText(_translate("MainWindow", "GUI Topic"))
        self.sendSettingPushButton.setText(_translate("MainWindow", "Send setting"))
        self.label.setText(_translate("MainWindow", "Robot Topic"))
        self.watchShelfgroupBox.setTitle(_translate("MainWindow", "Watch shelf"))
        self.label_18.setText(_translate("MainWindow", "Sub shelf 1"))
        self.label_19.setText(_translate("MainWindow", "Sub shelf 2"))
        self.ShelfPositionGroupBox.setTitle(_translate("MainWindow", "Shelf current position"))
        self.label_21.setText(_translate("MainWindow", "From "))
        self.label_22.setText(_translate("MainWindow", "x"))
        self.label_23.setText(_translate("MainWindow", "y"))
        self.label_24.setText(_translate("MainWindow", "theta"))
        self.label_25.setText(_translate("MainWindow", "To"))
        self.shelfStatusGroupBox.setTitle(_translate("MainWindow", "Shelf status"))
        self.label_3.setText(_translate("MainWindow", "Wrong object"))
        self.label_15.setText(_translate("MainWindow", "SOOS object"))
        self.label_20.setText(_translate("MainWindow", "OOS status"))
        self.fixShelfPushButton.setText(_translate("MainWindow", "Fixed shelf"))
        self.noteGroupBox.setTitle(_translate("MainWindow", "Note"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
