# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'result.ui'
##
## Created by: Qt User Interface Compiler version 6.7.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QHBoxLayout, QLabel, QSizePolicy,
    QTabWidget, QTextEdit, QVBoxLayout, QWidget)
from PySide6.QtCharts import *
class Ui_Result(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(906, 685)
        self.layoutWidget = QWidget(Form)
        self.layoutWidget.setObjectName(u"layoutWidget")
        self.layoutWidget.setGeometry(QRect(160, 110, 614, 265))
        self.horizontalLayout_3 = QHBoxLayout(self.layoutWidget)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.jobTabs = QTabWidget(self.layoutWidget)
        self.jobTabs.setObjectName(u"jobTabs")

        self.verticalLayout.addWidget(self.jobTabs)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.verticalLayout_5 = QVBoxLayout()
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.label = QLabel(self.layoutWidget)
        self.label.setObjectName(u"label")

        self.verticalLayout_5.addWidget(self.label)

        self.jobshow1 = QTextEdit(self.layoutWidget)
        self.jobshow1.setObjectName(u"jobshow1")
        self.jobshow1.setStyleSheet(u"background-color: transparent; \n"
"border:0 px;")

        self.verticalLayout_5.addWidget(self.jobshow1)


        self.horizontalLayout_4.addLayout(self.verticalLayout_5)

        self.verticalLayout_6 = QVBoxLayout()
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.label_3 = QLabel(self.layoutWidget)
        self.label_3.setObjectName(u"label_3")

        self.verticalLayout_6.addWidget(self.label_3)

        self.jobshow2 = QTextEdit(self.layoutWidget)
        self.jobshow2.setObjectName(u"jobshow2")
        self.jobshow2.setStyleSheet(u"background-color: transparent; border:0px;")

        self.verticalLayout_6.addWidget(self.jobshow2)


        self.horizontalLayout_4.addLayout(self.verticalLayout_6)


        self.verticalLayout.addLayout(self.horizontalLayout_4)

        self.verticalLayout.setStretch(0, 5)
        self.verticalLayout.setStretch(1, 1)

        self.horizontalLayout_3.addLayout(self.verticalLayout)

        self.verticalLayout_4 = QVBoxLayout()
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.verticalLayout_3 = QVBoxLayout()
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.showHost = QTabWidget(self.layoutWidget)
        self.showHost.setObjectName(u"showHost")

        self.horizontalLayout.addWidget(self.showHost)


        self.verticalLayout_3.addLayout(self.horizontalLayout)

        self.verticalLayout_3.setStretch(0, 1)

        self.verticalLayout_4.addLayout(self.verticalLayout_3)

        self.hostTabs = QTabWidget(self.layoutWidget)
        self.hostTabs.setObjectName(u"hostTabs")

        self.verticalLayout_4.addWidget(self.hostTabs)

        self.verticalLayout_4.setStretch(0, 2)
        self.verticalLayout_4.setStretch(1, 1)

        self.horizontalLayout_3.addLayout(self.verticalLayout_4)

        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.faultTabs = QTabWidget(self.layoutWidget)
        self.faultTabs.setObjectName(u"faultTabs")

        self.verticalLayout_2.addWidget(self.faultTabs)

        self.faultResultAnalysis = QC(self.layoutWidget)
        self.faultResultAnalysis.setObjectName(u"faultResultAnalysis")
        self.label_2 = QLabel(self.faultResultAnalysis)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setGeometry(QRect(0, 0, 111, 16))

        self.verticalLayout_2.addWidget(self.faultResultAnalysis)

        self.verticalLayout_2.setStretch(0, 4)
        self.verticalLayout_2.setStretch(1, 1)

        self.horizontalLayout_3.addLayout(self.verticalLayout_2)

        self.horizontalLayout_3.setStretch(0, 1)
        self.horizontalLayout_3.setStretch(1, 1)
        self.horizontalLayout_3.setStretch(2, 1)

        self.retranslateUi(Form)

        self.jobTabs.setCurrentIndex(-1)
        self.faultTabs.setCurrentIndex(-1)


        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.label.setText(QCoreApplication.translate("Form", u"\u5e73\u5747\u8fd0\u884c", None))
        self.label_3.setText(QCoreApplication.translate("Form", u"\u541e\u5410", None))
        self.label_2.setText(QCoreApplication.translate("Form", u"\u9519\u8bef\u6ce8\u5165\u7ed3\u679c\u5206\u6790", None))
    # retranslateUi

