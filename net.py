# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'net.ui'
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
from PySide6.QtWidgets import (QApplication, QHBoxLayout, QSizePolicy, QTabWidget,
    QWidget)

class Ui_Net(object):
    def setupUi(self, Net):
        if not Net.objectName():
            Net.setObjectName(u"Net")
        Net.resize(400, 300)
        self.horizontalLayout = QHBoxLayout(Net)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.tabWidget = QTabWidget(Net)
        self.tabWidget.setObjectName(u"tabWidget")

        self.horizontalLayout.addWidget(self.tabWidget)


        self.retranslateUi(Net)

        QMetaObject.connectSlotsByName(Net)
    # setupUi

    def retranslateUi(self, Net):
        Net.setWindowTitle(QCoreApplication.translate("Net", u"Form", None))
    # retranslateUi

