# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'link_editor.ui'
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
from PySide6.QtWidgets import (QApplication, QHeaderView, QSizePolicy, QTableWidget,
    QTableWidgetItem, QVBoxLayout, QWidget)


class Ui_linkEdit(object):
    def setupUi(self, linkEdit):
        linkEdit.setObjectName("linkEdit")
        linkEdit.resize(750, 476)
        self.verticalLayout = QVBoxLayout(linkEdit)
        self.verticalLayout.setObjectName("verticalLayout")
        self.tableWidget_netargs = QTableWidget(linkEdit)
        self.tableWidget_netargs.setLayoutDirection(Qt.LeftToRight)
        self.tableWidget_netargs.setStyleSheet("")
        self.tableWidget_netargs.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.tableWidget_netargs.setObjectName("tableWidget_netargs")
        self.tableWidget_netargs.setColumnCount(1)
        self.tableWidget_netargs.setRowCount(7)
        item = QTableWidgetItem()
        self.tableWidget_netargs.setVerticalHeaderItem(0, item)
        item = QTableWidgetItem()
        self.tableWidget_netargs.setVerticalHeaderItem(1, item)
        item = QTableWidgetItem()
        self.tableWidget_netargs.setVerticalHeaderItem(2, item)
        item = QTableWidgetItem()
        self.tableWidget_netargs.setVerticalHeaderItem(3, item)
        item = QTableWidgetItem()
        self.tableWidget_netargs.setVerticalHeaderItem(4, item)
        item = QTableWidgetItem()
        self.tableWidget_netargs.setVerticalHeaderItem(5, item)
        item = QTableWidgetItem()
        self.tableWidget_netargs.setVerticalHeaderItem(6, item)
        item = QTableWidgetItem()
        self.tableWidget_netargs.setHorizontalHeaderItem(0, item)
        item = QTableWidgetItem()
        item.setTextAlignment(Qt.AlignCenter)
        self.tableWidget_netargs.setItem(1, 0, item)
        self.tableWidget_netargs.horizontalHeader().setCascadingSectionResizes(False)
        self.tableWidget_netargs.horizontalHeader().setDefaultSectionSize(300)
        self.tableWidget_netargs.horizontalHeader().setHighlightSections(True)
        self.tableWidget_netargs.horizontalHeader().setStretchLastSection(True)
        self.tableWidget_netargs.verticalHeader().setDefaultSectionSize(50)
        self.tableWidget_netargs.verticalHeader().setStretchLastSection(False)
        self.verticalLayout.addWidget(self.tableWidget_netargs)

        self.retranslateUi(linkEdit)
        QMetaObject.connectSlotsByName(linkEdit)

    def retranslateUi(self, linkEdit):
        _translate = QCoreApplication.translate
        linkEdit.setWindowTitle(_translate("linkEdit", "Form"))
        item = self.tableWidget_netargs.verticalHeaderItem(0)
        item.setText(_translate("linkEdit", "名称"))
        item = self.tableWidget_netargs.verticalHeaderItem(1)
        item.setText(_translate("linkEdit", "转发速率(Mbps)"))
        item = self.tableWidget_netargs.verticalHeaderItem(2)
        item.setText(_translate("linkEdit", "丢包率"))
        item = self.tableWidget_netargs.verticalHeaderItem(3)
        item.setText(_translate("linkEdit", "端点一"))
        item = self.tableWidget_netargs.verticalHeaderItem(4)
        item.setText(_translate("linkEdit", "端点一端口"))
        item = self.tableWidget_netargs.verticalHeaderItem(5)
        item.setText(_translate("linkEdit", "端点二"))
        item = self.tableWidget_netargs.verticalHeaderItem(6)
        item.setText(_translate("linkEdit", "端点二端口"))
        item = self.tableWidget_netargs.horizontalHeaderItem(0)
        item.setText(_translate("linkEdit", "值"))
        __sortingEnabled = self.tableWidget_netargs.isSortingEnabled()
        self.tableWidget_netargs.setSortingEnabled(False)
        self.tableWidget_netargs.setSortingEnabled(__sortingEnabled)
