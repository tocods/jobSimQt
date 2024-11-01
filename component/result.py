# Form implementation generated from reading ui file 'result.ui'
#
# Created by: PyQt6 UI code generator 6.7.1
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from qdarktheme.qtpy import QtCore, QtGui, QtWidgets
from PySide6.QtCharts import QChart,QChartView,QLineSeries,QDateTimeAxis,QValueAxis
from PySide6.QtGui import QPainter
from PySide6.QtCore import QDateTime,Qt

class Ui_Result(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(906, 685)
        self.layoutWidget = QtWidgets.QWidget(parent=Form)
        self.layoutWidget.setGeometry(QtCore.QRect(160, 110, 614, 265))
        self.layoutWidget.setObjectName("layoutWidget")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.layoutWidget)
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.jobTabs = QtWidgets.QTabWidget(parent=self.layoutWidget)
        self.jobTabs.setObjectName("jobTabs")
        self.verticalLayout.addWidget(self.jobTabs)
        self.jobResult = QtWidgets.QWidget(parent=self.layoutWidget)
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout(self.jobResult)
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.jobResultAnalysis = QChartView(parent=self.jobResult)
        self.jobResultAnalysis.setObjectName("jobResultAnalysis")
        self.jobResultAnalysis2 = QChartView(parent=self.jobResult)
        self.jobResultAnalysis2.setObjectName("jobResultAnalysis2")
        self.jobResultAnalysis3 = QChartView(parent=self.jobResult)
        self.jobResultAnalysis3.setObjectName("jobResultAnalysis3")
        self.horizontalLayout_5.addWidget(self.jobResultAnalysis2)
        self.horizontalLayout_5.addWidget(self.jobResultAnalysis)
        self.horizontalLayout_5.addWidget(self.jobResultAnalysis3)
        self.horizontalLayout_5.setStretch(0, 1)
        self.horizontalLayout_5.setStretch(1, 1)
        self.horizontalLayout_5.setStretch(2, 1)
        self.label = QtWidgets.QLabel(parent=self.jobResult)
        self.label.setGeometry(QtCore.QRect(0, 0, 121, 16))
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.jobResult)
        self.verticalLayout.setStretch(0, 3)
        self.verticalLayout.setStretch(1, 1)
        self.horizontalLayout_3.addLayout(self.verticalLayout)
        self.verticalLayout_4 = QtWidgets.QVBoxLayout()
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.showCPU = QChartView(parent=self.layoutWidget)
        self.showCPU.setObjectName("showCPU")
        self.horizontalLayout.addWidget(self.showCPU)
        self.showRam = QChartView(parent=self.layoutWidget)
        self.showRam.setObjectName("showCPU_2")
        self.horizontalLayout.addWidget(self.showRam)
        self.horizontalLayout.setStretch(0, 1)
        self.horizontalLayout.setStretch(1, 1)
        self.verticalLayout_3.addLayout(self.horizontalLayout)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.showGPU = QChartView(parent=self.layoutWidget)
        self.showGPU.setObjectName("showGPU")
        self.horizontalLayout_2.addWidget(self.showGPU)
        self.show = QChartView(parent=self.layoutWidget)
        self.show.setObjectName("show")
        self.horizontalLayout_2.addWidget(self.show)
        self.horizontalLayout_2.setStretch(0, 1)
        self.horizontalLayout_2.setStretch(1, 1)
        self.verticalLayout_3.addLayout(self.horizontalLayout_2)
        self.verticalLayout_3.setStretch(0, 1)
        self.verticalLayout_3.setStretch(1, 1)
        self.verticalLayout_4.addLayout(self.verticalLayout_3)
        self.hostTabs = QtWidgets.QTabWidget(parent=self.layoutWidget)
        self.hostTabs.setObjectName("hostTabs")
        self.verticalLayout_4.addWidget(self.hostTabs)
        self.verticalLayout_4.setStretch(0, 2)
        self.verticalLayout_4.setStretch(1, 1)
        self.horizontalLayout_3.addLayout(self.verticalLayout_4)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.faultTabs = QtWidgets.QTabWidget(parent=self.layoutWidget)
        self.faultTabs.setObjectName("faultTabs")
        self.verticalLayout_2.addWidget(self.faultTabs)
        self.faultResult = QtWidgets.QWidget(parent=self.layoutWidget)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout(self.faultResult)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.faultResultAnalysis = QChartView(parent=self.faultResult)
        self.faultResultAnalysis.setObjectName("faultResultAnalysis")
        self.faultResultAnalysis2 = QChartView(parent=self.faultResult)
        self.faultResultAnalysis2.setObjectName("faultResultAnalysis2")
        self.horizontalLayout_4.addWidget(self.faultResultAnalysis)
        self.horizontalLayout_4.addWidget(self.faultResultAnalysis2)
        self.horizontalLayout_4.setStretch(0, 1)
        self.horizontalLayout_4.setStretch(1, 1)
        self.label_2 = QtWidgets.QLabel(parent=self.faultResult)
        self.label_2.setGeometry(QtCore.QRect(0, 0, 111, 16))
        self.label_2.setObjectName("label_2")
        self.verticalLayout_2.addWidget(self.faultResult)
        self.verticalLayout_2.setStretch(0, 3)
        self.verticalLayout_2.setStretch(1, 1)
        self.horizontalLayout_3.addLayout(self.verticalLayout_2)
        self.horizontalLayout_3.setStretch(0, 1)
        self.horizontalLayout_3.setStretch(1, 1)
        self.horizontalLayout_3.setStretch(2, 1)

        self.retranslateUi(Form)
        self.jobTabs.setCurrentIndex(-1)
        self.faultTabs.setCurrentIndex(-1)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.label.setText(_translate("Form", "任务运行结果分析"))
        self.label_2.setText(_translate("Form", "错误注入结果分析"))
