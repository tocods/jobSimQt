# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'hostinfo.ui'
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
from PySide6.QtWidgets import (QApplication, QDoubleSpinBox, QHBoxLayout, QHeaderView,
    QLabel, QLineEdit, QPushButton, QSizePolicy,
    QSpinBox, QTabWidget, QTableWidget, QTableWidgetItem,
    QVBoxLayout, QWidget)

class Ui_HostInfo(object):
    def setupUi(self, HostInfo):
        if not HostInfo.objectName():
            HostInfo.setObjectName(u"HostInfo")
        HostInfo.resize(1215, 671)
        HostInfo.setStyleSheet(u"")
        self.horizontalLayout_11 = QHBoxLayout(HostInfo)
        self.horizontalLayout_11.setObjectName(u"horizontalLayout_11")
        self.horizontalLayout_10 = QHBoxLayout()
        self.horizontalLayout_10.setObjectName(u"horizontalLayout_10")
        self.verticalLayout_7 = QVBoxLayout()
        self.verticalLayout_7.setObjectName(u"verticalLayout_7")
        self.horizontalLayout_9 = QHBoxLayout()
        self.horizontalLayout_9.setObjectName(u"horizontalLayout_9")
        self.label_13 = QLabel(HostInfo)
        self.label_13.setObjectName(u"label_13")

        self.horizontalLayout_9.addWidget(self.label_13)

        self.apply = QPushButton(HostInfo)
        self.apply.setObjectName(u"apply")

        self.horizontalLayout_9.addWidget(self.apply)

        self.horizontalLayout_9.setStretch(0, 10)
        self.horizontalLayout_9.setStretch(1, 1)

        self.verticalLayout_7.addLayout(self.horizontalLayout_9)

        self.verticalLayout_6 = QVBoxLayout()
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.horizontalLayout_7 = QHBoxLayout()
        self.horizontalLayout_7.setSpacing(20)
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.label_6 = QLabel(HostInfo)
        self.label_6.setObjectName(u"label_6")

        self.verticalLayout_2.addWidget(self.label_6)

        self.widget = QWidget(HostInfo)
        self.widget.setObjectName(u"widget")
        self.widget.setStyleSheet(u"border: 1px solid grey;\n"
"border-radius: 15px; ")
        self.horizontalLayout_12 = QHBoxLayout(self.widget)
        self.horizontalLayout_12.setObjectName(u"horizontalLayout_12")
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.label = QLabel(self.widget)
        self.label.setObjectName(u"label")
        self.label.setStyleSheet(u"border: none")

        self.horizontalLayout.addWidget(self.label)

        self.hostName = QLineEdit(self.widget)
        self.hostName.setObjectName(u"hostName")
        self.hostName.setStyleSheet(u"border: none")

        self.horizontalLayout.addWidget(self.hostName)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.label_2 = QLabel(self.widget)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setStyleSheet(u"border: none")

        self.horizontalLayout_2.addWidget(self.label_2)

        self.ram = QSpinBox(self.widget)
        self.ram.setObjectName(u"ram")
        self.ram.setStyleSheet(u"border: none")

        self.horizontalLayout_2.addWidget(self.ram)

        self.label_3 = QLabel(self.widget)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setStyleSheet(u"border: none")

        self.horizontalLayout_2.addWidget(self.label_3)


        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.label_4 = QLabel(self.widget)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setStyleSheet(u"border: none")

        self.horizontalLayout_3.addWidget(self.label_4)

        self.pcie = QDoubleSpinBox(self.widget)
        self.pcie.setObjectName(u"pcie")
        self.pcie.setStyleSheet(u"border: none")

        self.horizontalLayout_3.addWidget(self.pcie)

        self.label_5 = QLabel(self.widget)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setStyleSheet(u"border: none")

        self.horizontalLayout_3.addWidget(self.label_5)


        self.verticalLayout.addLayout(self.horizontalLayout_3)


        self.horizontalLayout_12.addLayout(self.verticalLayout)


        self.verticalLayout_2.addWidget(self.widget)

        self.verticalLayout_2.setStretch(0, 1)
        self.verticalLayout_2.setStretch(1, 20)

        self.horizontalLayout_7.addLayout(self.verticalLayout_2)

        self.verticalLayout_4 = QVBoxLayout()
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.label_7 = QLabel(HostInfo)
        self.label_7.setObjectName(u"label_7")

        self.verticalLayout_4.addWidget(self.label_7)

        self.widget_2 = QWidget(HostInfo)
        self.widget_2.setObjectName(u"widget_2")
        self.widget_2.setStyleSheet(u"border: 1px solid grey;\n"
"border-radius: 15px; ")
        self.horizontalLayout_13 = QHBoxLayout(self.widget_2)
        self.horizontalLayout_13.setObjectName(u"horizontalLayout_13")
        self.verticalLayout_3 = QVBoxLayout()
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.horizontalLayout_6 = QHBoxLayout()
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.label_8 = QLabel(self.widget_2)
        self.label_8.setObjectName(u"label_8")
        self.label_8.setStyleSheet(u"border: none\n"
"")

        self.horizontalLayout_6.addWidget(self.label_8)

        self.cpunum = QSpinBox(self.widget_2)
        self.cpunum.setObjectName(u"cpunum")
        self.cpunum.setStyleSheet(u"border:none")

        self.horizontalLayout_6.addWidget(self.cpunum)


        self.verticalLayout_3.addLayout(self.horizontalLayout_6)

        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.label_9 = QLabel(self.widget_2)
        self.label_9.setObjectName(u"label_9")
        self.label_9.setStyleSheet(u"border:  none")

        self.horizontalLayout_5.addWidget(self.label_9)

        self.corenum = QSpinBox(self.widget_2)
        self.corenum.setObjectName(u"corenum")
        self.corenum.setStyleSheet(u"border:none")

        self.horizontalLayout_5.addWidget(self.corenum)


        self.verticalLayout_3.addLayout(self.horizontalLayout_5)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.label_10 = QLabel(self.widget_2)
        self.label_10.setObjectName(u"label_10")
        self.label_10.setStyleSheet(u"border: none")

        self.horizontalLayout_4.addWidget(self.label_10)

        self.cpuflops = QLineEdit(self.widget_2)
        self.cpuflops.setObjectName(u"cpuflops")
        self.cpuflops.setStyleSheet(u"border: none")

        self.horizontalLayout_4.addWidget(self.cpuflops)


        self.verticalLayout_3.addLayout(self.horizontalLayout_4)


        self.horizontalLayout_13.addLayout(self.verticalLayout_3)


        self.verticalLayout_4.addWidget(self.widget_2)

        self.verticalLayout_4.setStretch(0, 1)
        self.verticalLayout_4.setStretch(1, 30)

        self.horizontalLayout_7.addLayout(self.verticalLayout_4)

        self.horizontalLayout_7.setStretch(0, 1)
        self.horizontalLayout_7.setStretch(1, 1)

        self.verticalLayout_6.addLayout(self.horizontalLayout_7)

        self.verticalLayout_5 = QVBoxLayout()
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.label_11 = QLabel(HostInfo)
        self.label_11.setObjectName(u"label_11")

        self.verticalLayout_5.addWidget(self.label_11)

        self.gputable = QTableWidget(HostInfo)
        self.gputable.setObjectName(u"gputable")

        self.verticalLayout_5.addWidget(self.gputable)

        self.horizontalLayout_8 = QHBoxLayout()
        self.horizontalLayout_8.setObjectName(u"horizontalLayout_8")
        self.label_12 = QLabel(HostInfo)
        self.label_12.setObjectName(u"label_12")

        self.horizontalLayout_8.addWidget(self.label_12)

        self.pushButton = QPushButton(HostInfo)
        self.pushButton.setObjectName(u"pushButton")
        self.pushButton.setStyleSheet(u"border: none\n"
"")
        icon = QIcon()
        icon.addFile(u"../img/\u52a0.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.pushButton.setIcon(icon)

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

        self.horizontalLayout_10.addLayout(self.verticalLayout_7)

        self.shows = QTabWidget(HostInfo)
        self.shows.setObjectName(u"shows")

        self.horizontalLayout_10.addWidget(self.shows)

        self.horizontalLayout_10.setStretch(0, 1)
        self.horizontalLayout_10.setStretch(1, 1)

        self.horizontalLayout_11.addLayout(self.horizontalLayout_10)


        self.retranslateUi(HostInfo)

        QMetaObject.connectSlotsByName(HostInfo)
    # setupUi

    def retranslateUi(self, HostInfo):
        HostInfo.setWindowTitle(QCoreApplication.translate("HostInfo", u"Form", None))
        self.label_13.setText("")
        self.apply.setText(QCoreApplication.translate("HostInfo", u"\u5e94\u7528", None))
        self.label_6.setText(QCoreApplication.translate("HostInfo", u"\u57fa\u672c\u4fe1\u606f", None))
        self.label.setText(QCoreApplication.translate("HostInfo", u"\u4e3b\u673a\u540d:", None))
        self.label_2.setText(QCoreApplication.translate("HostInfo", u"\u5185\u5b58:", None))
        self.label_3.setText(QCoreApplication.translate("HostInfo", u"GB", None))
        self.label_4.setText(QCoreApplication.translate("HostInfo", u"PCIe\u5e26\u5bbd:", None))
        self.label_5.setText(QCoreApplication.translate("HostInfo", u"GB/s", None))
        self.label_7.setText(QCoreApplication.translate("HostInfo", u"CPU\u4fe1\u606f", None))
        self.label_8.setText(QCoreApplication.translate("HostInfo", u"CPU\u6570:", None))
        self.label_9.setText(QCoreApplication.translate("HostInfo", u"CPU\u6838\u6570:", None))
        self.label_10.setText(QCoreApplication.translate("HostInfo", u"\u6838GFLOPS:", None))
        self.label_11.setText(QCoreApplication.translate("HostInfo", u"GPU\u4fe1\u606f", None))
        self.label_12.setText("")
        self.pushButton.setText("")
    # retranslateUi

