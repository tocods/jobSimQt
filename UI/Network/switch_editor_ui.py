# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'switch_editor.ui'
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

class Ui_switchEdit(object):
    def setupUi(self, switchEdit):
        if not switchEdit.objectName():
            switchEdit.setObjectName(u"switchEdit")
        switchEdit.resize(986, 699)
        self.verticalLayout = QVBoxLayout(switchEdit)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.table = QTableWidget(switchEdit)
        if (self.table.columnCount() < 1):
            self.table.setColumnCount(1)
        __qtablewidgetitem = QTableWidgetItem()
        self.table.setHorizontalHeaderItem(0, __qtablewidgetitem)
        if (self.table.rowCount() < 2):
            self.table.setRowCount(2)
        __qtablewidgetitem1 = QTableWidgetItem()
        self.table.setVerticalHeaderItem(0, __qtablewidgetitem1)
        __qtablewidgetitem2 = QTableWidgetItem()
        self.table.setVerticalHeaderItem(1, __qtablewidgetitem2)
        __qtablewidgetitem3 = QTableWidgetItem()
        __qtablewidgetitem3.setTextAlignment(Qt.AlignCenter);
        self.table.setItem(1, 0, __qtablewidgetitem3)
        self.table.setObjectName(u"table")
        self.table.setLayoutDirection(Qt.LeftToRight)
        self.table.setStyleSheet(u"")
        self.table.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.table.horizontalHeader().setCascadingSectionResizes(False)
        self.table.horizontalHeader().setDefaultSectionSize(300)
        self.table.horizontalHeader().setHighlightSections(True)
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.verticalHeader().setDefaultSectionSize(50)
        self.table.verticalHeader().setStretchLastSection(False)

        self.verticalLayout.addWidget(self.table)


        self.retranslateUi(switchEdit)

        QMetaObject.connectSlotsByName(switchEdit)
    # setupUi

    def retranslateUi(self, switchEdit):
        switchEdit.setWindowTitle(QCoreApplication.translate("switchEdit", u"Form", None))
        ___qtablewidgetitem = self.table.horizontalHeaderItem(0)
        ___qtablewidgetitem.setText(QCoreApplication.translate("switchEdit", u"\u503c", None));
        ___qtablewidgetitem1 = self.table.verticalHeaderItem(0)
        ___qtablewidgetitem1.setText(QCoreApplication.translate("switchEdit", u"\u540d\u79f0", None));
        ___qtablewidgetitem2 = self.table.verticalHeaderItem(1)
        ___qtablewidgetitem2.setText(QCoreApplication.translate("switchEdit", u"\u8f6c\u53d1\u901f\u7387(Mbps)", None));

        __sortingEnabled = self.table.isSortingEnabled()
        self.table.setSortingEnabled(False)
        self.table.setSortingEnabled(__sortingEnabled)

    # retranslateUi

