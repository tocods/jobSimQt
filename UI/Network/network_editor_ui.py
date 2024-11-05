# Form implementation generated from reading ui file 'UI\Network\network_editor.ui'
#
# Created by: PyQt6 UI code generator 6.4.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from qdarktheme.qtpy import QtCore, QtGui, QtWidgets
from scene import GraphicScene
from view import GraphicView
from resources import *


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(916, 692)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(Form)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label = QtWidgets.QLabel(parent=Form)
        self.label.setObjectName("label")
        self.horizontalLayout_2.addWidget(self.label)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem)
        self.conf = QtWidgets.QPushButton(parent=Form)
        self.conf.setStyleSheet("border:none;")
        self.conf.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("UI\\Network\\../../img/省略号.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.conf.setIcon(icon)
        self.conf.setObjectName("conf")
        self.horizontalLayout_2.addWidget(self.conf)
        self.add = QtWidgets.QPushButton(parent=Form)
        self.add.setStyleSheet("border:none;")
        self.add.setText("")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("UI\\Network\\../../img/plus.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.add.setIcon(icon1)
        self.add.setObjectName("add")
        self.horizontalLayout_2.addWidget(self.add)
        self.verticalLayout_2.addLayout(self.horizontalLayout_2)
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.infoList = QtWidgets.QTreeWidget(parent=Form)
        self.infoList.setColumnCount(0)
        self.infoList.setObjectName("infoList")
        self.verticalLayout_3.addWidget(self.infoList)
        self.run = QtWidgets.QPushButton(parent=Form)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap("UI\\Network\\fe/img/播放按钮.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.run.setIcon(icon2)
        self.run.setObjectName("run")
        self.verticalLayout_3.addWidget(self.run)
        self.verticalLayout_2.addLayout(self.verticalLayout_3)
        self.horizontalLayout.addLayout(self.verticalLayout_2)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.graphicsView = GraphicView(GraphicScene(Form) , parent=Form)
        self.graphicsView.setObjectName("graphicsView")
        self.verticalLayout.addWidget(self.graphicsView)
        self.horizontalLayout.addLayout(self.verticalLayout)
        self.horizontalLayout.setStretch(0, 1)
        self.horizontalLayout.setStretch(1, 5)
        self.horizontalLayout_3.addLayout(self.horizontalLayout)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.label.setText(_translate("Form", "网络结构"))
        self.run.setText(_translate("Form", "运行仿真"))