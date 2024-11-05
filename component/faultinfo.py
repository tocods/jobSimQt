# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'faultinfo.ui'
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
from PySide6.QtWidgets import (QApplication, QComboBox, QHBoxLayout, QLabel,
    QLineEdit, QListWidget, QListWidgetItem, QPushButton,
    QSizePolicy, QTabWidget, QVBoxLayout, QWidget)

class Ui_FaultInfo(object):
    def setupUi(self, FaultInfo):
        if not FaultInfo.objectName():
            FaultInfo.setObjectName(u"FaultInfo")
        FaultInfo.resize(985, 784)
        self.horizontalLayout_8 = QHBoxLayout(FaultInfo)
        self.horizontalLayout_8.setObjectName(u"horizontalLayout_8")
        self.horizontalLayout_6 = QHBoxLayout()
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.listWidget = QListWidget(FaultInfo)
        self.listWidget.setObjectName(u"listWidget")

        self.verticalLayout_2.addWidget(self.listWidget)

        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.label = QLabel(FaultInfo)
        self.label.setObjectName(u"label")

        self.horizontalLayout.addWidget(self.label)

        self.name = QLineEdit(FaultInfo)
        self.name.setObjectName(u"name")

        self.horizontalLayout.addWidget(self.name)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.label_2 = QLabel(FaultInfo)
        self.label_2.setObjectName(u"label_2")

        self.horizontalLayout_2.addWidget(self.label_2)

        self.aim = QComboBox(FaultInfo)
        self.aim.setObjectName(u"aim")

        self.horizontalLayout_2.addWidget(self.aim)


        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.label_3 = QLabel(FaultInfo)
        self.label_3.setObjectName(u"label_3")

        self.horizontalLayout_3.addWidget(self.label_3)

        self.type = QComboBox(FaultInfo)
        self.type.addItem("")
        self.type.addItem("")
        self.type.addItem("")
        self.type.addItem("")
        self.type.setObjectName(u"type")

        self.horizontalLayout_3.addWidget(self.type)


        self.verticalLayout.addLayout(self.horizontalLayout_3)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.label_4 = QLabel(FaultInfo)
        self.label_4.setObjectName(u"label_4")

        self.horizontalLayout_4.addWidget(self.label_4)

        self.time1 = QLineEdit(FaultInfo)
        self.time1.setObjectName(u"time1")

        self.horizontalLayout_4.addWidget(self.time1)

        self.label_6 = QLabel(FaultInfo)
        self.label_6.setObjectName(u"label_6")

        self.horizontalLayout_4.addWidget(self.label_6)


        self.verticalLayout.addLayout(self.horizontalLayout_4)

        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.label_5 = QLabel(FaultInfo)
        self.label_5.setObjectName(u"label_5")

        self.horizontalLayout_5.addWidget(self.label_5)

        self.time2 = QLineEdit(FaultInfo)
        self.time2.setObjectName(u"time2")

        self.horizontalLayout_5.addWidget(self.time2)

        self.label_7 = QLabel(FaultInfo)
        self.label_7.setObjectName(u"label_7")

        self.horizontalLayout_5.addWidget(self.label_7)


        self.verticalLayout.addLayout(self.horizontalLayout_5)


        self.verticalLayout_2.addLayout(self.verticalLayout)

        self.horizontalLayout_7 = QHBoxLayout()
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.label_9 = QLabel(FaultInfo)
        self.label_9.setObjectName(u"label_9")

        self.horizontalLayout_7.addWidget(self.label_9)

        self.apply = QPushButton(FaultInfo)
        self.apply.setObjectName(u"apply")

        self.horizontalLayout_7.addWidget(self.apply)

        self.horizontalLayout_7.setStretch(0, 2)
        self.horizontalLayout_7.setStretch(1, 1)

        self.verticalLayout_2.addLayout(self.horizontalLayout_7)

        self.listWidget_2 = QListWidget(FaultInfo)
        self.listWidget_2.setObjectName(u"listWidget_2")

        self.verticalLayout_2.addWidget(self.listWidget_2)

        self.verticalLayout_2.setStretch(0, 1)
        self.verticalLayout_2.setStretch(1, 2)
        self.verticalLayout_2.setStretch(3, 1)

        self.horizontalLayout_6.addLayout(self.verticalLayout_2)

        self.verticalLayout_3 = QVBoxLayout()
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.shows = QTabWidget(FaultInfo)
        self.shows.setObjectName(u"shows")

        self.verticalLayout_3.addWidget(self.shows)


        self.horizontalLayout_6.addLayout(self.verticalLayout_3)

        self.horizontalLayout_6.setStretch(0, 1)
        self.horizontalLayout_6.setStretch(1, 2)

        self.horizontalLayout_8.addLayout(self.horizontalLayout_6)


        self.retranslateUi(FaultInfo)

        QMetaObject.connectSlotsByName(FaultInfo)
    # setupUi

    def retranslateUi(self, FaultInfo):
        FaultInfo.setWindowTitle(QCoreApplication.translate("FaultInfo", u"Form", None))
        self.label.setText(QCoreApplication.translate("FaultInfo", u"\u6545\u969c\u6a21\u578b\u540d:", None))
        self.label_2.setText(QCoreApplication.translate("FaultInfo", u"\u6ce8\u5165\u5bf9\u8c61:", None))
        self.label_3.setText(QCoreApplication.translate("FaultInfo", u"\u5206\u5e03\u7c7b\u578b:", None))
        self.type.setItemText(0, QCoreApplication.translate("FaultInfo", u"\u6b63\u6001\u5206\u5e03", None))
        self.type.setItemText(1, QCoreApplication.translate("FaultInfo", u"\u97e6\u4f2f\u5206\u5e03", None))
        self.type.setItemText(2, QCoreApplication.translate("FaultInfo", u"\u5bf9\u6570\u6b63\u6001\u5206\u5e03", None))
        self.type.setItemText(3, QCoreApplication.translate("FaultInfo", u"\u4f3d\u9a6c\u5206\u5e03", None))

        self.label_4.setText(QCoreApplication.translate("FaultInfo", u"\u5e73\u5747\u65e0\u6545\u969c\u65f6\u95f4:", None))
        self.label_6.setText(QCoreApplication.translate("FaultInfo", u"\u79d2", None))
        self.label_5.setText(QCoreApplication.translate("FaultInfo", u"\u5e73\u5747\u6545\u969c\u4fee\u590d\u65f6\u95f4:", None))
        self.label_7.setText(QCoreApplication.translate("FaultInfo", u"\u79d2", None))
        self.label_9.setText("")
        self.apply.setText(QCoreApplication.translate("FaultInfo", u"\u5e94\u7528", None))
    # retranslateUi

