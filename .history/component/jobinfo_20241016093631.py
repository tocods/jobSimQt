# Form implementation generated from reading ui file 'jobinfo.ui'
#
# Created by: PyQt6 UI code generator 6.7.1
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from qdarktheme.qtpy import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(732, 699)
        self.widget = QtWidgets.QWidget(parent=Form)
        self.widget.setGeometry(QtCore.QRect(140, 30, 501, 531))
        self.widget.setObjectName("widget")
        self.verticalLayout_7 = QtWidgets.QVBoxLayout(self.widget)
        self.verticalLayout_7.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_7.setObjectName("verticalLayout_7")
        self.horizontalLayout_9 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_9.setObjectName("horizontalLayout_9")
        self.label_13 = QtWidgets.QLabel(parent=self.widget)
        self.label_13.setText("")
        self.label_13.setObjectName("label_13")
        self.horizontalLayout_9.addWidget(self.label_13)
        self.apply = QtWidgets.QPushButton(parent=self.widget)
        self.apply.setObjectName("apply")
        self.horizontalLayout_9.addWidget(self.apply)
        self.horizontalLayout_9.setStretch(0, 10)
        self.horizontalLayout_9.setStretch(1, 1)
        self.verticalLayout_7.addLayout(self.horizontalLayout_9)
        self.verticalLayout_6 = QtWidgets.QVBoxLayout()
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.horizontalLayout_7 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_7.setSpacing(20)
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.label_6 = QtWidgets.QLabel(parent=self.widget)
        self.label_6.setObjectName("label_6")
        self.verticalLayout_2.addWidget(self.label_6)
        self.widget1 = QtWidgets.QWidget(parent=self.widget)
        self.widget1.setStyleSheet("border: 1px solid grey;\n"
"border-radius: 15px; ")
        self.widget1.setObjectName("widget1")
        self.layoutWidget_2 = QtWidgets.QWidget(parent=self.widget1)
        self.layoutWidget_2.setGeometry(QtCore.QRect(10, 10, 201, 161))
        self.layoutWidget_2.setObjectName("layoutWidget_2")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.layoutWidget_2)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QtWidgets.QLabel(parent=self.layoutWidget_2)
        self.label.setStyleSheet("border: none")
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.jobName = QtWidgets.QLineEdit(parent=self.layoutWidget_2)
        self.jobName.setStyleSheet("border: none")
        self.jobName.setObjectName("jobName")
        self.horizontalLayout.addWidget(self.jobName)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label_2 = QtWidgets.QLabel(parent=self.layoutWidget_2)
        self.label_2.setStyleSheet("border: none")
        self.label_2.setObjectName("label_2")
        self.horizontalLayout_2.addWidget(self.label_2)
        self.ram = QtWidgets.QSpinBox(parent=self.layoutWidget_2)
        self.ram.setStyleSheet("border: none")
        self.ram.setObjectName("ram")
        self.horizontalLayout_2.addWidget(self.ram)
        self.label_3 = QtWidgets.QLabel(parent=self.layoutWidget_2)
        self.label_3.setStyleSheet("border: none")
        self.label_3.setObjectName("label_3")
        self.horizontalLayout_2.addWidget(self.label_3)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.label_4 = QtWidgets.QLabel(parent=self.layoutWidget_2)
        self.label_4.setStyleSheet("border: none")
        self.label_4.setObjectName("label_4")
        self.horizontalLayout_3.addWidget(self.label_4)
        self.period = QtWidgets.QLineEdit(parent=self.layoutWidget_2)
        self.period.setObjectName("period")
        self.horizontalLayout_3.addWidget(self.period)
        self.label_5 = QtWidgets.QLabel(parent=self.layoutWidget_2)
        self.label_5.setStyleSheet("border: none")
        self.label_5.setObjectName("label_5")
        self.horizontalLayout_3.addWidget(self.label_5)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.verticalLayout_2.addWidget(self.widget1)
        self.verticalLayout_2.setStretch(0, 1)
        self.verticalLayout_2.setStretch(1, 20)
        self.horizontalLayout_7.addLayout(self.verticalLayout_2)
        self.verticalLayout_4 = QtWidgets.QVBoxLayout()
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.label_7 = QtWidgets.QLabel(parent=self.widget)
        self.label_7.setObjectName("label_7")
        self.verticalLayout_4.addWidget(self.label_7)
        self.widget_2 = QtWidgets.QWidget(parent=self.widget)
        self.widget_2.setStyleSheet("border: 1px solid grey;\n"
"border-radius: 15px; ")
        self.widget_2.setObjectName("widget_2")
        self.layoutWidget_3 = QtWidgets.QWidget(parent=self.widget_2)
        self.layoutWidget_3.setGeometry(QtCore.QRect(20, 10, 201, 191))
        self.layoutWidget_3.setObjectName("layoutWidget_3")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.layoutWidget_3)
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.label_9 = QtWidgets.QLabel(parent=self.layoutWidget_3)
        self.label_9.setStyleSheet("border:  none")
        self.label_9.setObjectName("label_9")
        self.horizontalLayout_5.addWidget(self.label_9)
        self.corenum = QtWidgets.QSpinBox(parent=self.layoutWidget_3)
        self.corenum.setStyleSheet("border:none")
        self.corenum.setObjectName("corenum")
        self.horizontalLayout_5.addWidget(self.corenum)
        self.verticalLayout_3.addLayout(self.horizontalLayout_5)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.label_10 = QtWidgets.QLabel(parent=self.layoutWidget_3)
        self.label_10.setStyleSheet("border: none")
        self.label_10.setObjectName("label_10")
        self.horizontalLayout_4.addWidget(self.label_10)
        self.cpuflops = QtWidgets.QLineEdit(parent=self.layoutWidget_3)
        self.cpuflops.setStyleSheet("border: none")
        self.cpuflops.setObjectName("cpuflops")
        self.horizontalLayout_4.addWidget(self.cpuflops)
        self.verticalLayout_3.addLayout(self.horizontalLayout_4)
        self.verticalLayout_4.addWidget(self.widget_2)
        self.verticalLayout_4.setStretch(0, 1)
        self.verticalLayout_4.setStretch(1, 30)
        self.horizontalLayout_7.addLayout(self.verticalLayout_4)
        self.horizontalLayout_7.setStretch(0, 1)
        self.horizontalLayout_7.setStretch(1, 1)
        self.verticalLayout_6.addLayout(self.horizontalLayout_7)
        self.verticalLayout_5 = QtWidgets.QVBoxLayout()
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.label_11 = QtWidgets.QLabel(parent=self.widget)
        self.label_11.setObjectName("label_11")
        self.verticalLayout_5.addWidget(self.label_11)
        self.gputable = QtWidgets.QTableView(parent=self.widget)
        self.gputable.setObjectName("gputable")
        self.verticalLayout_5.addWidget(self.gputable)
        self.horizontalLayout_8 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_8.setObjectName("horizontalLayout_8")
        self.label_12 = QtWidgets.QLabel(parent=self.widget)
        self.label_12.setText("")
        self.label_12.setObjectName("label_12")
        self.horizontalLayout_8.addWidget(self.label_12)
        self.pushButton = QtWidgets.QPushButton(parent=self.widget)
        self.pushButton.setStyleSheet("border: none\n"
"")
        self.pushButton.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("../img/加.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.pushButton.setIcon(icon)
        self.pushButton.setObjectName("pushButton")
        self.horizontalLayout_8.addWidget(self.pushButton)
        self.horizontalLayout_8.setStretch(0, 10)
        self.horizontalLayout_8.setStretch(1, 1)
        self.verticalLayout_5.addLayout(self.horizontalLayout_8)
        self.verticalLayout_6.addLayout(self.verticalLayout_5)
        self.verticalLayout_6.setStretch(0, 1)
        self.verticalLayout_6.setStretch(1, 1)
        self.verticalLayout_7.addLayout(self.verticalLayout_6)
        self.verticalLayout_7.setStretch(0, 1)
        self.verticalLayout_7.setStretch(1, 20)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.apply.setText(_translate("Form", "应用"))
        self.label_6.setText(_translate("Form", "基本信息"))
        self.label.setText(_translate("Form", "任务名:"))
        self.label_2.setText(_translate("Form", "需求内存:"))
        self.label_3.setText(_translate("Form", "GB"))
        self.label_4.setText(_translate("Form", "周期:"))
        self.label_5.setText(_translate("Form", "s"))
        self.label_7.setText(_translate("Form", "CPU需求"))
        self.label_9.setText(_translate("Form", "需求核数:"))
        self.label_10.setText(_translate("Form", "FLOP:"))
        self.label_11.setText(_translate("Form", "GPU需求"))
