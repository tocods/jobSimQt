# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'start.ui'
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
from PySide6.QtWidgets import (QApplication, QHBoxLayout, QHeaderView, QLabel,
    QMainWindow, QPushButton, QSizePolicy, QTreeWidget,
    QTreeWidgetItem, QVBoxLayout, QWidget)

class Ui_start(object):
    def setupUi(self, start):
        if not start.objectName():
            start.setObjectName(u"start")
        start.resize(800, 600)
        self.centralwidget = QWidget(start)
        self.centralwidget.setObjectName(u"centralwidget")
        self.horizontalLayout_2 = QHBoxLayout(self.centralwidget)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.label = QLabel(self.centralwidget)
        self.label.setObjectName(u"label")
        font = QFont()
        font.setPointSize(13)
        self.label.setFont(font)

        self.horizontalLayout.addWidget(self.label)

        self.newP = QPushButton(self.centralwidget)
        self.newP.setObjectName(u"newP")

        self.horizontalLayout.addWidget(self.newP)

        self.openP = QPushButton(self.centralwidget)
        self.openP.setObjectName(u"openP")

        self.horizontalLayout.addWidget(self.openP)

        self.shutdown = QPushButton(self.centralwidget)
        self.shutdown.setObjectName(u"shutdown")

        self.horizontalLayout.addWidget(self.shutdown)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.projects = QTreeWidget(self.centralwidget)
        self.projects.setObjectName(u"projects")

        self.verticalLayout.addWidget(self.projects)

        self.verticalLayout.setStretch(0, 1)
        self.verticalLayout.setStretch(1, 5)

        self.horizontalLayout_2.addLayout(self.verticalLayout)

        start.setCentralWidget(self.centralwidget)

        self.retranslateUi(start)

        QMetaObject.connectSlotsByName(start)
    # setupUi

    def retranslateUi(self, start):
        start.setWindowTitle(QCoreApplication.translate("start", u"MainWindow", None))
        self.label.setText(QCoreApplication.translate("start", u"\u7cfb\u7edf\u7ba1\u7406\u5efa\u6a21\u548c\u4eff\u771f\u5de5\u5177                ", None))
        self.newP.setText(QCoreApplication.translate("start", u"\u65b0\u5efa\u9879\u76ee", None))
        self.openP.setText(QCoreApplication.translate("start", u"\u6253\u5f00", None))
        self.shutdown.setText(QCoreApplication.translate("start", u"\u5173\u95ed", None))
    # retranslateUi

