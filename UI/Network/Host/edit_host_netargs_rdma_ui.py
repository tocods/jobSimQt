# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'd:\jobSimQt\UI\Network\Host\edit_host_netargs_rdma.ui'
#
# Created by: PyQt5 UI code generator 5.15.11
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from qdarktheme.qtpy import QtCore, QtGui, QtWidgets


class Ui_Rdma(object):
    def setupUi(self, Rdma):
        Rdma.setObjectName("Rdma")
        Rdma.resize(833, 489)
        self.verticalLayoutWidget = QtWidgets.QWidget(Rdma)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(10, 10, 811, 471))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.tableWidget_netargs = QtWidgets.QTableWidget(self.verticalLayoutWidget)
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
        self.verticalLayout.addWidget(self.tableWidget_netargs)
        self.applyButton = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.applyButton.setAutoDefault(False)
        self.applyButton.setObjectName("applyButton")
        self.verticalLayout.addWidget(self.applyButton)

        self.retranslateUi(Rdma)
        QtCore.QMetaObject.connectSlotsByName(Rdma)

    def retranslateUi(self, Rdma):
        _translate = QtCore.QCoreApplication.translate
        Rdma.setWindowTitle(_translate("Rdma", "Dialog"))
        item = self.tableWidget_netargs.verticalHeaderItem(0)
        item.setText(_translate("Rdma", "名称"))
        item = self.tableWidget_netargs.verticalHeaderItem(1)
        item.setText(_translate("Rdma", "app数量"))
        item = self.tableWidget_netargs.verticalHeaderItem(2)
        item.setText(_translate("Rdma", "app参数"))
        item = self.tableWidget_netargs.verticalHeaderItem(3)
        item.setText(_translate("Rdma", "IP"))
        item = self.tableWidget_netargs.verticalHeaderItem(4)
        item.setText(_translate("Rdma", "MAC"))
        item = self.tableWidget_netargs.horizontalHeaderItem(0)
        item.setText(_translate("Rdma", "值"))
        __sortingEnabled = self.tableWidget_netargs.isSortingEnabled()
        self.tableWidget_netargs.setSortingEnabled(False)
        self.tableWidget_netargs.setSortingEnabled(__sortingEnabled)
        self.applyButton.setText(_translate("Rdma", "应用"))