# Form implementation generated from reading ui file 'UI\Network\Host\edit_host_netargs_udp.ui'
#
# Created by: PyQt6 UI code generator 6.4.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from qdarktheme.qtpy import QtCore, QtGui, QtWidgets


class Ui_Udp(object):
    def setupUi(self, Udp):
        Udp.setObjectName("Udp")
        Udp.resize(833, 489)
        self.applyButton = QtWidgets.QPushButton(Udp)
        self.applyButton.setGeometry(QtCore.QRect(360, 420, 141, 41))
        self.applyButton.setAutoDefault(False)
        self.applyButton.setObjectName("applyButton")
        self.tableWidget_netargs = QtWidgets.QTableWidget(Udp)
        self.tableWidget_netargs.setGeometry(QtCore.QRect(40, 30, 751, 361))
        self.tableWidget_netargs.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.tableWidget_netargs.setStyleSheet("")
        self.tableWidget_netargs.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.tableWidget_netargs.setObjectName("tableWidget_netargs")
        self.tableWidget_netargs.setColumnCount(1)
        self.tableWidget_netargs.setRowCount(5)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_netargs.setVerticalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_netargs.setVerticalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_netargs.setVerticalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_netargs.setVerticalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_netargs.setVerticalHeaderItem(4, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_netargs.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        self.tableWidget_netargs.setItem(1, 0, item)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        self.tableWidget_netargs.setItem(2, 0, item)
        self.tableWidget_netargs.horizontalHeader().setCascadingSectionResizes(False)
        self.tableWidget_netargs.horizontalHeader().setDefaultSectionSize(300)
        self.tableWidget_netargs.horizontalHeader().setHighlightSections(True)
        self.tableWidget_netargs.horizontalHeader().setStretchLastSection(True)
        self.tableWidget_netargs.verticalHeader().setDefaultSectionSize(50)
        self.tableWidget_netargs.verticalHeader().setStretchLastSection(False)

        self.retranslateUi(Udp)
        QtCore.QMetaObject.connectSlotsByName(Udp)

    def retranslateUi(self, Udp):
        _translate = QtCore.QCoreApplication.translate
        Udp.setWindowTitle(_translate("Udp", "Dialog"))
        self.applyButton.setText(_translate("Udp", "应用"))
        item = self.tableWidget_netargs.verticalHeaderItem(0)
        item.setText(_translate("Udp", "名称"))
        item = self.tableWidget_netargs.verticalHeaderItem(1)
        item.setText(_translate("Udp", "app数量"))
        item = self.tableWidget_netargs.verticalHeaderItem(2)
        item.setText(_translate("Udp", "app参数"))
        item = self.tableWidget_netargs.verticalHeaderItem(3)
        item.setText(_translate("Udp", "IP"))
        item = self.tableWidget_netargs.verticalHeaderItem(4)
        item.setText(_translate("Udp", "MAC"))
        item = self.tableWidget_netargs.horizontalHeaderItem(0)
        item.setText(_translate("Udp", "值"))
        __sortingEnabled = self.tableWidget_netargs.isSortingEnabled()
        self.tableWidget_netargs.setSortingEnabled(False)
        self.tableWidget_netargs.setSortingEnabled(__sortingEnabled)
