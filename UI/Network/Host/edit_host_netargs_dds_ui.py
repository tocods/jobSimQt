# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'edit_host_netargs_dds.ui'
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
from PySide6.QtWidgets import (QApplication, QDialog, QHeaderView, QPushButton,
    QSizePolicy, QTableWidget, QTableWidgetItem, QVBoxLayout,
    QWidget)

class Ui_Udp(object):
    def setupUi(self, Udp):
        if not Udp.objectName():
            Udp.setObjectName(u"Udp")
        Udp.resize(836, 489)
        self.verticalLayout = QVBoxLayout(Udp)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.tableWidget_netargs = QTableWidget(Udp)
        if (self.tableWidget_netargs.columnCount() < 1):
            self.tableWidget_netargs.setColumnCount(1)
        __qtablewidgetitem = QTableWidgetItem()
        self.tableWidget_netargs.setHorizontalHeaderItem(0, __qtablewidgetitem)
        if (self.tableWidget_netargs.rowCount() < 5):
            self.tableWidget_netargs.setRowCount(5)
        __qtablewidgetitem1 = QTableWidgetItem()
        self.tableWidget_netargs.setVerticalHeaderItem(0, __qtablewidgetitem1)
        __qtablewidgetitem2 = QTableWidgetItem()
        self.tableWidget_netargs.setVerticalHeaderItem(1, __qtablewidgetitem2)
        __qtablewidgetitem3 = QTableWidgetItem()
        self.tableWidget_netargs.setVerticalHeaderItem(2, __qtablewidgetitem3)
        __qtablewidgetitem4 = QTableWidgetItem()
        self.tableWidget_netargs.setVerticalHeaderItem(3, __qtablewidgetitem4)
        __qtablewidgetitem5 = QTableWidgetItem()
        self.tableWidget_netargs.setVerticalHeaderItem(4, __qtablewidgetitem5)
        __qtablewidgetitem6 = QTableWidgetItem()
        __qtablewidgetitem6.setTextAlignment(Qt.AlignCenter);
        self.tableWidget_netargs.setItem(1, 0, __qtablewidgetitem6)
        __qtablewidgetitem7 = QTableWidgetItem()
        __qtablewidgetitem7.setTextAlignment(Qt.AlignCenter);
        self.tableWidget_netargs.setItem(2, 0, __qtablewidgetitem7)
        self.tableWidget_netargs.setObjectName(u"tableWidget_netargs")
        self.tableWidget_netargs.setLayoutDirection(Qt.LeftToRight)
        self.tableWidget_netargs.setStyleSheet(u"")
        self.tableWidget_netargs.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.tableWidget_netargs.horizontalHeader().setCascadingSectionResizes(False)
        self.tableWidget_netargs.horizontalHeader().setDefaultSectionSize(300)
        self.tableWidget_netargs.horizontalHeader().setHighlightSections(True)
        self.tableWidget_netargs.horizontalHeader().setStretchLastSection(True)
        self.tableWidget_netargs.verticalHeader().setDefaultSectionSize(50)
        self.tableWidget_netargs.verticalHeader().setStretchLastSection(False)

        self.verticalLayout.addWidget(self.tableWidget_netargs)

        self.applyButton = QPushButton(Udp)
        self.applyButton.setObjectName(u"applyButton")
        self.applyButton.setAutoDefault(False)

        self.verticalLayout.addWidget(self.applyButton)


        self.retranslateUi(Udp)

        QMetaObject.connectSlotsByName(Udp)
    # setupUi

    def retranslateUi(self, Udp):
        Udp.setWindowTitle(QCoreApplication.translate("Udp", u"Dialog", None))
        ___qtablewidgetitem = self.tableWidget_netargs.horizontalHeaderItem(0)
        ___qtablewidgetitem.setText(QCoreApplication.translate("Udp", u"\u503c", None));
        ___qtablewidgetitem1 = self.tableWidget_netargs.verticalHeaderItem(0)
        ___qtablewidgetitem1.setText(QCoreApplication.translate("Udp", u"\u540d\u79f0", None));
        ___qtablewidgetitem2 = self.tableWidget_netargs.verticalHeaderItem(1)
        ___qtablewidgetitem2.setText(QCoreApplication.translate("Udp", u"app\u6570\u91cf", None));
        ___qtablewidgetitem3 = self.tableWidget_netargs.verticalHeaderItem(2)
        ___qtablewidgetitem3.setText(QCoreApplication.translate("Udp", u"app\u53c2\u6570", None));
        ___qtablewidgetitem4 = self.tableWidget_netargs.verticalHeaderItem(3)
        ___qtablewidgetitem4.setText(QCoreApplication.translate("Udp", u"IP", None));
        ___qtablewidgetitem5 = self.tableWidget_netargs.verticalHeaderItem(4)
        ___qtablewidgetitem5.setText(QCoreApplication.translate("Udp", u"MAC", None));

        __sortingEnabled = self.tableWidget_netargs.isSortingEnabled()
        self.tableWidget_netargs.setSortingEnabled(False)
        self.tableWidget_netargs.setSortingEnabled(__sortingEnabled)

        self.applyButton.setText(QCoreApplication.translate("Udp", u"\u5e94\u7528", None))
    # retranslateUi

