# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'cpu.ui'
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
from PySide6.QtWidgets import (QApplication, QHBoxLayout, QHeaderView, QSizePolicy,
    QTabWidget, QTableWidget, QTableWidgetItem, QWidget)

class Ui_Util(object):
    def setupUi(self, Util):
        if not Util.objectName():
            Util.setObjectName(u"Util")
        Util.resize(1033, 820)
        self.horizontalLayout_2 = QHBoxLayout(Util)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.tabWidget = QTabWidget(Util)
        self.tabWidget.setObjectName(u"tabWidget")

        self.horizontalLayout.addWidget(self.tabWidget)

        self.hostMore = QTableWidget(Util)
        self.hostMore.setObjectName(u"hostMore")

        self.horizontalLayout.addWidget(self.hostMore)

        self.horizontalLayout.setStretch(0, 4)
        self.horizontalLayout.setStretch(1, 1)

        self.horizontalLayout_2.addLayout(self.horizontalLayout)


        self.retranslateUi(Util)

        self.tabWidget.setCurrentIndex(-1)


        QMetaObject.connectSlotsByName(Util)
    # setupUi

    def retranslateUi(self, Util):
        Util.setWindowTitle(QCoreApplication.translate("Util", u"\u4e3b\u673a\u4fe1\u606f", None))
    # retranslateUi

