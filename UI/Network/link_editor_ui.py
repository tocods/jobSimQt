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
    def setupUi(self, switchEdit):
        if not switchEdit.objectName():
            switchEdit.setObjectName(u"switchEdit")
        switchEdit.resize(1026, 664)
        self.verticalLayout_2 = QVBoxLayout(switchEdit)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.tableWidget_netargs = QTableWidget(switchEdit)
        if (self.tableWidget_netargs.columnCount() < 1):
            self.tableWidget_netargs.setColumnCount(1)
        __qtablewidgetitem = QTableWidgetItem()
        self.tableWidget_netargs.setHorizontalHeaderItem(0, __qtablewidgetitem)
        if (self.tableWidget_netargs.rowCount() < 2):
            self.tableWidget_netargs.setRowCount(2)
        __qtablewidgetitem1 = QTableWidgetItem()
        self.tableWidget_netargs.setVerticalHeaderItem(0, __qtablewidgetitem1)
        __qtablewidgetitem2 = QTableWidgetItem()
        self.tableWidget_netargs.setVerticalHeaderItem(1, __qtablewidgetitem2)
        __qtablewidgetitem3 = QTableWidgetItem()
        __qtablewidgetitem3.setTextAlignment(Qt.AlignCenter);
        self.tableWidget_netargs.setItem(1, 0, __qtablewidgetitem3)
        self.tableWidget_netargs.setObjectName(u"tableWidget_netargs")
        self.tableWidget_netargs.setLayoutDirection(Qt.LeftToRight)
        self.tableWidget_netargs.setStyleSheet(u"")
        self.tableWidget_netargs.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.tableWidget_netargs.horizontalHeader().setCascadingSectionResizes(False)
        self.tableWidget_netargs.horizontalHeader().setDefaultSectionSize(300)
        self.tableWidget_netargs.horizontalHeader().setHighlightSections(True)
        self.tableWidget_netargs.horizontalHeader().setStretchLastSection(True)
        self.tableWidget_netargs.verticalHeader().setDefaultSectionSize(50)
        self.tableWidget_netargs.verticalHeader().setStretchLastSection(False)

        self.verticalLayout_2.addWidget(self.tableWidget_netargs)


        self.retranslateUi(switchEdit)

        QMetaObject.connectSlotsByName(switchEdit)
    # setupUi

    def retranslateUi(self, switchEdit):
        switchEdit.setWindowTitle(QCoreApplication.translate("switchEdit", u"Form", None))
        ___qtablewidgetitem = self.tableWidget_netargs.horizontalHeaderItem(0)
        ___qtablewidgetitem.setText(QCoreApplication.translate("switchEdit", u"\u503c", None));
        ___qtablewidgetitem1 = self.tableWidget_netargs.verticalHeaderItem(0)
        ___qtablewidgetitem1.setText(QCoreApplication.translate("switchEdit", u"\u540d\u79f0", None));
        ___qtablewidgetitem2 = self.tableWidget_netargs.verticalHeaderItem(1)
        ___qtablewidgetitem2.setText(QCoreApplication.translate("switchEdit", u"\u8f6c\u53d1\u901f\u7387(Mbps)", None));

        __sortingEnabled = self.tableWidget_netargs.isSortingEnabled()
        self.tableWidget_netargs.setSortingEnabled(False)
        self.tableWidget_netargs.setSortingEnabled(__sortingEnabled)

    # retranslateUi

