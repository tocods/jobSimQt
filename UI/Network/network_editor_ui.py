# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'network_editor.ui'
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
from PySide6.QtWidgets import (QApplication, QGraphicsView, QGridLayout, QHBoxLayout,
    QHeaderView, QLabel, QPushButton, QSizePolicy,
    QTabWidget, QTreeWidget, QTreeWidgetItem, QVBoxLayout,
    QWidget)
from scene import GraphicScene
from view import GraphicView

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(918, 948)
        self.horizontalLayout_3 = QHBoxLayout(Form)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.label = QLabel(Form)
        self.label.setObjectName(u"label")

        self.horizontalLayout_2.addWidget(self.label)


        self.verticalLayout_2.addLayout(self.horizontalLayout_2)

        self.verticalLayout_3 = QVBoxLayout()
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.infoList = QTreeWidget(Form)
        self.infoList.setObjectName(u"infoList")
        self.infoList.setColumnCount(0)

        self.verticalLayout_3.addWidget(self.infoList)

        self.label_2 = QLabel(Form)
        self.label_2.setObjectName(u"label_2")

        self.verticalLayout_3.addWidget(self.label_2)

        self.add = QGridLayout()
        self.add.setObjectName(u"add")
        self.global_setting = QPushButton(Form)
        self.global_setting.setObjectName(u"global_setting")
        icon = QIcon()
        icon.addFile(u"../../img/MaterialSymbolsSettings.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.global_setting.setIcon(icon)

        self.add.addWidget(self.global_setting, 2, 1, 1, 1)

        self.add_switch = QPushButton(Form)
        self.add_switch.setObjectName(u"add_switch")
        icon1 = QIcon()
        icon1.addFile(u"../../img/MdiSwitch.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.add_switch.setIcon(icon1)

        self.add.addWidget(self.add_switch, 0, 1, 1, 1)

        self.add_line = QPushButton(Form)
        self.add_line.setObjectName(u"add_line")
        icon2 = QIcon()
        icon2.addFile(u"../../img/WhhLine.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.add_line.setIcon(icon2)

        self.add.addWidget(self.add_line, 2, 0, 1, 1)

        self.add_host = QPushButton(Form)
        self.add_host.setObjectName(u"add_host")
        icon3 = QIcon()
        icon3.addFile(u"../../img/Host.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.add_host.setIcon(icon3)

        self.add.addWidget(self.add_host, 0, 0, 1, 1)


        self.verticalLayout_3.addLayout(self.add)

        self.run = QPushButton(Form)
        self.run.setObjectName(u"run")
        icon4 = QIcon()
        icon4.addFile(u"fe/img/\u64ad\u653e\u6309\u94ae.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.run.setIcon(icon4)

        self.verticalLayout_3.addWidget(self.run)


        self.verticalLayout_2.addLayout(self.verticalLayout_3)


        self.horizontalLayout.addLayout(self.verticalLayout_2)

        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.graphicsView = GraphicView(GraphicScene(Form), parent=Form)
        self.graphicsView.setObjectName(u"graphicsView")

        self.verticalLayout.addWidget(self.graphicsView)


        self.horizontalLayout.addLayout(self.verticalLayout)

        self.verticalLayout_5 = QVBoxLayout()
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.label_3 = QLabel(Form)
        self.label_3.setObjectName(u"label_3")

        self.horizontalLayout_4.addWidget(self.label_3)

        self.hostApply = QPushButton(Form)
        self.hostApply.setObjectName(u"hostApply")

        self.horizontalLayout_4.addWidget(self.hostApply)


        self.verticalLayout_5.addLayout(self.horizontalLayout_4)

        self.hostSet = QTabWidget(Form)
        self.hostSet.setObjectName(u"hostSet")

        self.verticalLayout_5.addWidget(self.hostSet)

        self.horizontalLayout_6 = QHBoxLayout()
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.label_6 = QLabel(Form)
        self.label_6.setObjectName(u"label_6")

        self.horizontalLayout_6.addWidget(self.label_6)

        self.switchApply = QPushButton(Form)
        self.switchApply.setObjectName(u"switchApply")

        self.horizontalLayout_6.addWidget(self.switchApply)


        self.verticalLayout_5.addLayout(self.horizontalLayout_6)

        self.switchSet = QTabWidget(Form)
        self.switchSet.setObjectName(u"switchSet")

        self.verticalLayout_5.addWidget(self.switchSet)

        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.label_5 = QLabel(Form)
        self.label_5.setObjectName(u"label_5")

        self.horizontalLayout_5.addWidget(self.label_5)

        self.linkApply = QPushButton(Form)
        self.linkApply.setObjectName(u"linkApply")

        self.horizontalLayout_5.addWidget(self.linkApply)


        self.verticalLayout_5.addLayout(self.horizontalLayout_5)

        self.linkSet = QTabWidget(Form)
        self.linkSet.setObjectName(u"linkSet")

        self.verticalLayout_5.addWidget(self.linkSet)


        self.horizontalLayout.addLayout(self.verticalLayout_5)

        self.horizontalLayout.setStretch(0, 1)
        self.horizontalLayout.setStretch(1, 5)
        self.horizontalLayout.setStretch(2, 2)

        self.horizontalLayout_3.addLayout(self.horizontalLayout)


        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.label.setText(QCoreApplication.translate("Form", u"\u7f51\u7edc\u7ed3\u6784", None))
        self.label_2.setText(QCoreApplication.translate("Form", u"\u6dfb\u52a0", None))
        self.global_setting.setText(QCoreApplication.translate("Form", u"\u5168\u5c40\u8bbe\u7f6e", None))
        self.add_switch.setText(QCoreApplication.translate("Form", u"\u4ea4\u6362\u673a", None))
        self.add_line.setText(QCoreApplication.translate("Form", u"\u8fde\u7ebf", None))
        self.add_host.setText(QCoreApplication.translate("Form", u"\u4e3b\u673a", None))
        self.run.setText(QCoreApplication.translate("Form", u"\u8fd0\u884c\u4eff\u771f", None))
        self.label_3.setText(QCoreApplication.translate("Form", u"\u4e3b\u673a\u914d\u7f6e", None))
        self.hostApply.setText(QCoreApplication.translate("Form", u"\u5e94\u7528", None))
        self.label_6.setText(QCoreApplication.translate("Form", u"\u4ea4\u6362\u673a\u914d\u7f6e", None))
        self.switchApply.setText(QCoreApplication.translate("Form", u"\u5e94\u7528", None))
        self.label_5.setText(QCoreApplication.translate("Form", u"\u94fe\u8def\u914d\u7f6e", None))
        self.linkApply.setText(QCoreApplication.translate("Form", u"\u5e94\u7528", None))
    # retranslateUi

