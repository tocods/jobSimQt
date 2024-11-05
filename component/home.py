# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'home.ui'
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
from PySide6.QtWidgets import (QApplication, QHBoxLayout, QHeaderView, QLabel,
    QPushButton, QSizePolicy, QTabWidget, QTextEdit,
    QTreeWidget, QTreeWidgetItem, QVBoxLayout, QWidget)

class Ui_home(object):
    def setupUi(self, home):
        if not home.objectName():
            home.setObjectName(u"home")
        home.resize(854, 511)
        self.horizontalLayout_3 = QHBoxLayout(home)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.label = QLabel(home)
        self.label.setObjectName(u"label")

        self.horizontalLayout.addWidget(self.label)

        self.add = QPushButton(home)
        self.add.setObjectName(u"add")
        self.add.setStyleSheet(u"border:none;")
        icon = QIcon()
        icon.addFile(u"../../fe/img/\u65b0\u589e\u6587\u4ef6\u5939.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.add.setIcon(icon)

        self.horizontalLayout.addWidget(self.add)

        self.pushButton = QPushButton(home)
        self.pushButton.setObjectName(u"pushButton")
        self.pushButton.setStyleSheet(u"border:none;")
        icon1 = QIcon()
        icon1.addFile(u"../../fe/img/24gl-folderMinus-copy.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.pushButton.setIcon(icon1)

        self.horizontalLayout.addWidget(self.pushButton)


        self.verticalLayout_2.addLayout(self.horizontalLayout)

        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.infoList = QTreeWidget(home)
        self.infoList.setObjectName(u"infoList")
        self.infoList.setColumnCount(0)

        self.verticalLayout.addWidget(self.infoList)

        self.run = QPushButton(home)
        self.run.setObjectName(u"run")
        icon2 = QIcon()
        icon2.addFile(u"../../fe/img/\u64ad\u653e\u6309\u94ae.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.run.setIcon(icon2)

        self.verticalLayout.addWidget(self.run)


        self.verticalLayout_2.addLayout(self.verticalLayout)


        self.horizontalLayout_2.addLayout(self.verticalLayout_2)

        self.verticalLayout_4 = QVBoxLayout()
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.tabWidget = QTabWidget(home)
        self.tabWidget.setObjectName(u"tabWidget")

        self.verticalLayout_4.addWidget(self.tabWidget)

        self.verticalLayout_3 = QVBoxLayout()
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.label_2 = QLabel(home)
        self.label_2.setObjectName(u"label_2")

        self.verticalLayout_3.addWidget(self.label_2)

        self.textEdit = QTextEdit(home)
        self.textEdit.setObjectName(u"textEdit")

        self.verticalLayout_3.addWidget(self.textEdit)


        self.verticalLayout_4.addLayout(self.verticalLayout_3)

        self.verticalLayout_4.setStretch(0, 6)
        self.verticalLayout_4.setStretch(1, 1)

        self.horizontalLayout_2.addLayout(self.verticalLayout_4)

        self.horizontalLayout_2.setStretch(0, 1)
        self.horizontalLayout_2.setStretch(1, 6)

        self.horizontalLayout_3.addLayout(self.horizontalLayout_2)


        self.retranslateUi(home)

        self.tabWidget.setCurrentIndex(-1)


        QMetaObject.connectSlotsByName(home)
    # setupUi

    def retranslateUi(self, home):
        home.setWindowTitle(QCoreApplication.translate("home", u"home", None))
        self.label.setText(QCoreApplication.translate("home", u"\u4eff\u771f\u73af\u5883", None))
        self.add.setText("")
        self.pushButton.setText("")
        self.run.setText(QCoreApplication.translate("home", u"\u8fd0\u884c\u4eff\u771f", None))
        self.label_2.setText(QCoreApplication.translate("home", u"\u8f93\u51fa", None))
    # retranslateUi

