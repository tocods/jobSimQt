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

class Ui_Result(object):
    def setupUi(self, Result):
        if not Result.objectName():
            Result.setObjectName(u"Result")
        Result.resize(906, 685)
        self.horizontalLayout_2 = QHBoxLayout(Result)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.jobTabs = QTabWidget(Result)
        self.jobTabs.setObjectName(u"jobTabs")

        self.verticalLayout.addWidget(self.jobTabs)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.verticalLayout_5 = QVBoxLayout()
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.label = QLabel(Result)
        self.label.setObjectName(u"label")

        self.verticalLayout_5.addWidget(self.label)

        self.jobshow1 = QTextEdit(Result)
        self.jobshow1.setObjectName(u"jobshow1")
        self.jobshow1.setStyleSheet(u"background-color: transparent; \n"
"")
        self.jobshow1.setReadOnly(True)

        self.verticalLayout_5.addWidget(self.jobshow1)


        self.horizontalLayout_4.addLayout(self.verticalLayout_5)

        self.verticalLayout_8 = QVBoxLayout()
        self.verticalLayout_8.setObjectName(u"verticalLayout_8")
        self.label_2 = QLabel(Result)
        self.label_2.setObjectName(u"label_2")

        self.verticalLayout_8.addWidget(self.label_2)

        self.jobShow3 = QTextEdit(Result)
        self.jobShow3.setObjectName(u"jobShow3")
        self.jobShow3.setStyleSheet(u"background-color: transparent; \n"
"")

        self.verticalLayout_8.addWidget(self.jobShow3)


        self.horizontalLayout_4.addLayout(self.verticalLayout_8)

        self.verticalLayout_6 = QVBoxLayout()
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.label_3 = QLabel(Result)
        self.label_3.setObjectName(u"label_3")

        self.verticalLayout_6.addWidget(self.label_3)

        self.jobshow2 = QTextEdit(Result)
        self.jobshow2.setObjectName(u"jobshow2")
        self.jobshow2.setStyleSheet(u"background-color: transparent; ")

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
        self.showHost = QTabWidget(Result)
        self.showHost.setObjectName(u"showHost")

        self.horizontalLayout.addWidget(self.showHost)


        self.verticalLayout_3.addLayout(self.horizontalLayout)

        self.verticalLayout_3.setStretch(0, 1)

        self.verticalLayout_4.addLayout(self.verticalLayout_3)

        self.hostTabs = QTabWidget(Result)
        self.hostTabs.setObjectName(u"hostTabs")

        self.verticalLayout_4.addWidget(self.hostTabs)

        self.verticalLayout_4.setStretch(0, 2)
        self.verticalLayout_4.setStretch(1, 1)

        self.horizontalLayout_3.addLayout(self.verticalLayout_4)

        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.faultTabs = QTabWidget(Result)
        self.faultTabs.setObjectName(u"faultTabs")

        self.verticalLayout_2.addWidget(self.faultTabs)

        self.verticalLayout_7 = QVBoxLayout()
        self.verticalLayout_7.setObjectName(u"verticalLayout_7")
        self.label_4 = QLabel(Result)
        self.label_4.setObjectName(u"label_4")

        self.verticalLayout_7.addWidget(self.label_4)

        self.faultResult = QTextEdit(Result)
        self.faultResult.setObjectName(u"faultResult")
        self.faultResult.setStyleSheet(u"background: transparent;")

        self.verticalLayout_7.addWidget(self.faultResult)


        self.verticalLayout_2.addLayout(self.verticalLayout_7)

        self.verticalLayout_2.setStretch(0, 5)
        self.verticalLayout_2.setStretch(1, 1)

        self.horizontalLayout_3.addLayout(self.verticalLayout_2)

        self.horizontalLayout_3.setStretch(0, 1)
        self.horizontalLayout_3.setStretch(1, 1)
        self.horizontalLayout_3.setStretch(2, 1)

        self.horizontalLayout_2.addLayout(self.horizontalLayout_3)


        self.retranslateUi(Result)

        self.jobTabs.setCurrentIndex(-1)
        self.faultTabs.setCurrentIndex(-1)


        QMetaObject.connectSlotsByName(Result)
    # setupUi

    def retranslateUi(self, Result):
        Result.setWindowTitle(QCoreApplication.translate("Result", u"Form", None))
        self.label.setText(QCoreApplication.translate("Result", u"\u5e73\u5747\u8fd0\u884c", None))
        self.label_2.setText(QCoreApplication.translate("Result", u"\u7b97\u529b\u5229\u7528\u7387", None))
        self.label_3.setText(QCoreApplication.translate("Result", u"\u541e\u5410", None))
        self.label_4.setText(QCoreApplication.translate("Result", u"\u4f59\u5ea6\u53ef\u9760\u6027", None))
    # retranslateUi

