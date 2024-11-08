# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'netanalysis.ui'
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
from PySide6.QtWidgets import (QApplication, QGraphicsView, QHBoxLayout, QPushButton,
    QSizePolicy, QTabWidget, QVBoxLayout, QWidget, QTableWidget)

class Ui_NetAnalysis(object):
    def setupUi(self, NetAnalysis):
        if not NetAnalysis.objectName():
            NetAnalysis.setObjectName(u"NetAnalysis")
        NetAnalysis.resize(919, 773)
        self.horizontalLayout_3 = QHBoxLayout(NetAnalysis)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.chose = QPushButton(NetAnalysis)
        self.chose.setObjectName(u"chose")

        self.horizontalLayout.addWidget(self.chose)

        self.run = QPushButton(NetAnalysis)
        self.run.setObjectName(u"run")

        self.horizontalLayout.addWidget(self.run)

        self.horizontalLayout.setStretch(0, 1)
        self.horizontalLayout.setStretch(1, 1)

        self.verticalLayout.addLayout(self.horizontalLayout)

        self.shows = QTableWidget(NetAnalysis)
        self.shows.setObjectName(u"shows")

        self.verticalLayout.addWidget(self.shows)


        self.horizontalLayout_2.addLayout(self.verticalLayout)

        self.nets = QGraphicsView(NetAnalysis)
        self.nets.setObjectName(u"nets")

        self.horizontalLayout_2.addWidget(self.nets)

        self.results = QTabWidget(NetAnalysis)
        self.results.setObjectName(u"results")

        self.horizontalLayout_2.addWidget(self.results)

        self.horizontalLayout_2.setStretch(0, 1)
        self.horizontalLayout_2.setStretch(1, 2)
        self.horizontalLayout_2.setStretch(2, 1)

        self.horizontalLayout_3.addLayout(self.horizontalLayout_2)


        self.retranslateUi(NetAnalysis)

        QMetaObject.connectSlotsByName(NetAnalysis)
    # setupUi

    def retranslateUi(self, NetAnalysis):
        NetAnalysis.setWindowTitle(QCoreApplication.translate("NetAnalysis", u"Form", None))
        self.chose.setText(QCoreApplication.translate("NetAnalysis", u"\u9009\u62e9\u6d41", None))
        self.run.setText(QCoreApplication.translate("NetAnalysis", u"\u5f00\u59cb\u6f14\u7b97", None))
    # retranslateUi

