# Form implementation generated from reading ui file 'UI\open_project.ui'
#
# Created by: PyQt6 UI code generator 6.4.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from qdarktheme.qtpy import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(650, 362)
        self.label = QtWidgets.QLabel(parent=Dialog)
        self.label.setGeometry(QtCore.QRect(40, 70, 251, 61))
        font = QtGui.QFont()
        font.setPointSize(20)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.applyButton = QtWidgets.QPushButton(parent=Dialog)
        self.applyButton.setGeometry(QtCore.QRect(260, 220, 141, 41))
        font = QtGui.QFont()
        font.setPointSize(20)
        self.applyButton.setFont(font)
        self.applyButton.setAutoDefault(False)
        self.applyButton.setObjectName("applyButton")
        self.directoryButton = QtWidgets.QPushButton(parent=Dialog)
        self.directoryButton.setGeometry(QtCore.QRect(180, 80, 411, 51))
        font = QtGui.QFont()
        font.setPointSize(15)
        self.directoryButton.setFont(font)
        self.directoryButton.setStyleSheet("background-color: rgb(255, 255, 255);\n"
"text-align: left;")
        self.directoryButton.setText("")
        self.directoryButton.setAutoDefault(False)
        self.directoryButton.setObjectName("directoryButton")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.label.setText(_translate("Dialog", "打开工程："))
        self.applyButton.setText(_translate("Dialog", "确定"))