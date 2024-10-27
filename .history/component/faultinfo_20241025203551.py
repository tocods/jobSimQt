# Form implementation generated from reading ui file 'faultinfo.ui'
#
# Created by: PyQt6 UI code generator 6.7.1
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from qdarktheme.qtpy import QtCore, QtGui, QtWidgets
from PySide6.QtCharts import QChart,QChartView,QLineSeries,QDateTimeAxis,QValueAxis
from PySide6.QtGui import QPainter
from PySide6.QtCore import QDateTime,Qt

class Ui_FaultInfo(object):
    def setupUi(self, FaultInfo):
        FaultInfo.setObjectName("FaultInfo")
        FaultInfo.resize(985, 784)
        self.widget = QtWidgets.QWidget(parent=FaultInfo)
        self.widget.setGeometry(QtCore.QRect(100, 70, 881, 538))
        self.widget.setObjectName("widget")
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout(self.widget)
        self.horizontalLayout_6.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.listWidget = QtWidgets.QListWidget(parent=self.widget)
        self.listWidget.setObjectName("listWidget")
        self.verticalLayout_2.addWidget(self.listWidget)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QtWidgets.QLabel(parent=self.widget)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.name = QtWidgets.QLineEdit(parent=self.widget)
        self.name.setObjectName("name")
        self.horizontalLayout.addWidget(self.name)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label_2 = QtWidgets.QLabel(parent=self.widget)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout_2.addWidget(self.label_2)
        self.aim = QtWidgets.QComboBox(parent=self.widget)
        self.aim.setObjectName("aim")
        self.horizontalLayout_2.addWidget(self.aim)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.label_3 = QtWidgets.QLabel(parent=self.widget)
        self.label_3.setObjectName("label_3")
        self.horizontalLayout_3.addWidget(self.label_3)
        self.type = QtWidgets.QComboBox(parent=self.widget)
        self.type.setObjectName("type")
        self.type.addItem("")
        self.type.addItem("")
        self.type.addItem("")
        self.type.addItem("")
        self.horizontalLayout_3.addWidget(self.type)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.label_4 = QtWidgets.QLabel(parent=self.widget)
        self.label_4.setObjectName("label_4")
        self.horizontalLayout_4.addWidget(self.label_4)
        self.time1 = QtWidgets.QLineEdit(parent=self.widget)
        self.time1.setObjectName("time1")
        self.horizontalLayout_4.addWidget(self.time1)
        self.label_6 = QtWidgets.QLabel(parent=self.widget)
        self.label_6.setObjectName("label_6")
        self.horizontalLayout_4.addWidget(self.label_6)
        self.verticalLayout.addLayout(self.horizontalLayout_4)
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.label_5 = QtWidgets.QLabel(parent=self.widget)
        self.label_5.setObjectName("label_5")
        self.horizontalLayout_5.addWidget(self.label_5)
        self.time2 = QtWidgets.QLineEdit(parent=self.widget)
        self.time2.setObjectName("time2")
        self.horizontalLayout_5.addWidget(self.time2)
        self.label_7 = QtWidgets.QLabel(parent=self.widget)
        self.label_7.setObjectName("label_7")
        self.horizontalLayout_5.addWidget(self.label_7)
        self.verticalLayout.addLayout(self.horizontalLayout_5)
        self.verticalLayout_2.addLayout(self.verticalLayout)
        self.horizontalLayout_7 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")
        self.label_9 = QtWidgets.QLabel(parent=self.widget)
        self.label_9.setText("")
        self.label_9.setObjectName("label_9")
        self.horizontalLayout_7.addWidget(self.label_9)
        self.apply = QtWidgets.QPushButton(parent=self.widget)
        self.apply.setObjectName("apply")
        self.horizontalLayout_7.addWidget(self.apply)
        self.horizontalLayout_7.setStretch(0, 2)
        self.horizontalLayout_7.setStretch(1, 1)
        self.verticalLayout_2.addLayout(self.horizontalLayout_7)
        self.listWidget_2 = QtWidgets.QListWidget(parent=self.widget)
        self.listWidget_2.setObjectName("listWidget_2")
        self.verticalLayout_2.addWidget(self.listWidget_2)
        self.verticalLayout_2.setStretch(0, 1)
        self.verticalLayout_2.setStretch(1, 2)
        self.verticalLayout_2.setStretch(3, 1)
        self.horizontalLayout_6.addLayout(self.verticalLayout_2)
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.label_8 = QtWidgets.QLabel(parent=self.widget)
        self.label_8.setObjectName("label_8")
        self.verticalLayout_3.addWidget(self.label_8)
        self.chat=QChart()
        self.chat.setAnimationOptions(QChart.AllAnimations) # 设置移动动画
        self.show = QChartView(parent=self.widget, chart=self.chat)
        self.show.setObjectName("show")
        self.show2 = QChartView(parent=self.widget)
        self.show2.setObjectName("show2")
        self.verticalLayout_3.addWidget(self.show)
        self.verticalLayout_3.addWidget(self.show2)
        self.verticalLayout_3.setStretch(0, 1)
        self.verticalLayout_3.setStretch(1, 20)
        self.horizontalLayout_6.addLayout(self.verticalLayout_3)
        self.horizontalLayout_6.setStretch(0, 1)
        self.horizontalLayout_6.setStretch(1, 3)
        
        self.retranslateUi(FaultInfo)
        QtCore.QMetaObject.connectSlotsByName(FaultInfo)

    def retranslateUi(self, FaultInfo):
        _translate = QtCore.QCoreApplication.translate
        FaultInfo.setWindowTitle(_translate("FaultInfo", "Form"))
        self.label.setText(_translate("FaultInfo", "故障模型名:"))
        self.label_2.setText(_translate("FaultInfo", "注入对象:"))
        self.label_3.setText(_translate("FaultInfo", "分布类型:"))
        self.type.setItemText(0, _translate("FaultInfo", "正态分布"))
        self.type.setItemText(1, _translate("FaultInfo", "韦伯分布"))
        self.type.setItemText(2, _translate("FaultInfo", "对数正态分布"))
        self.type.setItemText(3, _translate("FaultInfo", "伽马分布"))
        self.label_4.setText(_translate("FaultInfo", "平均无故障时间:"))
        self.label_6.setText(_translate("FaultInfo", "秒"))
        self.label_5.setText(_translate("FaultInfo", "平均故障修复时间:"))
        self.label_7.setText(_translate("FaultInfo", "秒"))
        self.apply.setText(_translate("FaultInfo", "应用"))
        self.label_8.setText(_translate("FaultInfo", "分布图像"))
