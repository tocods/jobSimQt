# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'managermaster.ui'
##
## Created by: Qt User Interface Compiler version 6.8.0
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
from PySide6.QtWidgets import (QApplication, QGraphicsView, QHBoxLayout, QHeaderView,
    QLabel, QPushButton, QSizePolicy, QTableWidget,
    QTableWidgetItem, QTreeWidget, QTreeWidgetItem, QVBoxLayout,
    QWidget, QTabWidget)
from MasterView import MasterView

class Ui_ManagerMaster(object):
    def setupUi(self, ManagerMaster):
        if not ManagerMaster.objectName():
            ManagerMaster.setObjectName(u"ManagerMaster")
        ManagerMaster.resize(1013, 765)
        self.horizontalLayout_2 = QHBoxLayout(ManagerMaster)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.treeWidget = QTreeWidget(ManagerMaster)
        self.treeWidget.setObjectName(u"treeWidget")

        self.verticalLayout_2.addWidget(self.treeWidget)


        #self.verticalLayout_2.addWidget(self.pushButton)


        self.horizontalLayout.addLayout(self.verticalLayout_2)

        self.graphicsView = MasterView(ManagerMaster)
        self.graphicsView.setObjectName(u"graphicsView")

        self.horizontalLayout.addWidget(self.graphicsView)

        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.label = QLabel(ManagerMaster)
        self.label.setObjectName(u"label")

        self.verticalLayout.addWidget(self.label)

        self.tableWidget = QTabWidget(ManagerMaster)
        self.tableWidget.setObjectName(u"tableWidget")

        self.verticalLayout.addWidget(self.tableWidget)

        self.label_2 = QLabel(ManagerMaster)
        self.label_2.setObjectName(u"label_2")

        self.verticalLayout.addWidget(self.label_2)

        self.tableWidget_2 = QTableWidget(ManagerMaster)
        self.tableWidget_2.setObjectName(u"tableWidget_2")

        self.verticalLayout.addWidget(self.tableWidget_2)


        self.horizontalLayout.addLayout(self.verticalLayout)

        self.horizontalLayout.setStretch(0, 1)
        self.horizontalLayout.setStretch(1, 5)
        self.horizontalLayout.setStretch(2, 3)

        self.horizontalLayout_2.addLayout(self.horizontalLayout)


        self.retranslateUi(ManagerMaster)

        QMetaObject.connectSlotsByName(ManagerMaster)
    # setupUi

    def retranslateUi(self, ManagerMaster):
        ManagerMaster.setWindowTitle(QCoreApplication.translate("ManagerMaster", u"\u7cfb\u7edf\u7ba1\u7406\u8f6f\u4ef6(\u4e3b)", None))
        #self.pushButton.setText(QCoreApplication.translate("ManagerMaster", u"\u5f00\u59cb", None))
        self.label.setText(QCoreApplication.translate("ManagerMaster", u"\u4e8b\u52a1\u8bb0\u5f55", None))
        self.label_2.setText(QCoreApplication.translate("ManagerMaster", u"\u91cd\u6784\u8bb0\u5f55", None))
    # retranslateUi

