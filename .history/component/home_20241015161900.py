# Form implementation generated from reading ui file 'home.ui'
#
# Created by: PyQt6 UI code generator 6.7.1
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from qdarktheme.qtpy import QtCore, QtGui, QtWidgets


class Ui_home(object):
    def setupUi(self, home):
        home.setObjectName("home")
        home.resize(809, 640)
        self.tabWidget = QtWidgets.QTabWidget(parent=home)
        self.tabWidget.setGeometry(QtCore.QRect(280, 50, 401, 291))
        self.tabWidget.setObjectName("tabWidget")
        self.hostinfo = QtWidgets.QWidget()
        self.hostinfo.setObjectName("hostinfo")
        self.tabWidget.addTab(self.hostinfo, "")
        self.jobinfo = QtWidgets.QWidget()
        self.jobinfo.setObjectName("jobinfo")
        self.tabWidget.addTab(self.jobinfo, "")
        self.faultinfo = QtWidgets.QWidget()
        self.faultinfo.setObjectName("faultinfo")
        self.tabWidget.addTab(self.faultinfo, "")
        self.widget = QtWidgets.QWidget(parent=home)
        self.widget.setGeometry(QtCore.QRect(140, 70, 111, 250))
        self.widget.setObjectName("widget")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.widget)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QtWidgets.QLabel(parent=self.widget)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.add = QtWidgets.QPushButton(parent=self.widget)
        self.add.setStyleSheet("border:none;")
        self.add.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("../../fe/img/新增文件夹.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.add.setIcon(icon)
        self.add.setObjectName("add")
        self.horizontalLayout.addWidget(self.add)
        self.pushButton = QtWidgets.QPushButton(parent=self.widget)
        self.pushButton.setStyleSheet("border:none;")
        self.pushButton.setText("")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("../../fe/img/24gl-folderMinus-copy.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.pushButton.setIcon(icon1)
        self.pushButton.setObjectName("pushButton")
        self.horizontalLayout.addWidget(self.pushButton)
        self.verticalLayout_2.addLayout(self.horizontalLayout)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.infoList = QtWidgets.QTreeWidget(parent=self.widget)
        self.infoList.setObjectName("infoList")
        self.infoList.header().setVisible(False)
        self.verticalLayout.addWidget(self.infoList)
        self.run = QtWidgets.QPushButton(parent=self.widget)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap("../../fe/img/播放按钮.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.run.setIcon(icon2)
        self.run.setObjectName("run")
        self.verticalLayout.addWidget(self.run)
        self.verticalLayout_2.addLayout(self.verticalLayout)

        self.retranslateUi(home)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(home)

    def retranslateUi(self, home):
        _translate = QtCore.QCoreApplication.translate
        home.setWindowTitle(_translate("home", "home"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.hostinfo), _translate("home", "主机信息"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.jobinfo), _translate("home", "任务信息"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.faultinfo), _translate("home", "故障注入信息"))
        #self.label.setText(_translate("home", "仿真环境"))
        self.run.setText(_translate("home", "运行仿真"))
