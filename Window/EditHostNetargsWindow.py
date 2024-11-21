from UI.Network.Host.edit_host_netargs_udp_ui import Ui_Udp as udp_ui
from UI.Network.Host.edit_host_netargs_tsn_ui import Ui_Tsn as tsn_ui
from UI.Network.Host.edit_host_netargs_dds_ui import Ui_Udp as dds_ui
from UI.Network.Host.edit_host_netargs_rdma_ui import Ui_Rdma as rdma_ui
from Window.HostNetargsAppEditor import *
from Window.JsonArrayEditor import JsonArrayEditor
from qdarktheme.qtpy.QtWidgets import (
    QDialog,
    QTableWidgetItem,
    QPushButton,
    QMessageBox,
)
from qdarktheme.qtpy.QtCore import Qt


class EditHostNetargsWindow(QDialog):
    def __init__(self, parent=None, jobSim=None, type="Udp"):
        QDialog.__init__(self)
        self.parent = parent
        self.jobSim = jobSim
        self.ui = udp_ui()
        self.type = type

    def on_cell_edited(self, row, col):
        return

    def setHostGraphicItem(self, hostGraphicItem):
        print("Error:未指定类型")

    def apply_setting(self):
        print("Error:未指定类型")

    def lineEdit_name_cb(self):
        name = self.ui.tableWidget_netargs.item(0, 0).text()

        # 网络属性，更新主机名称
        if name != self.hostGraphicItem.hostAttr.name:
            #self.hostGraphicItem.hostAttr.del_name(self.hostGraphicItem.hostAttr.name)
            self.hostGraphicItem.hostAttr.set_name(name)

        print("Host name: " + self.hostGraphicItem.hostAttr.name)
        self.hostGraphicItem.setName(name)

        # 主机属性
        self.jobSim.hosts[self.hostGraphicItem].name = name
        print("名称：" + name)

        self.parent.parent.update_tree_view()



class EditHostNetargsWindowNormal(EditHostNetargsWindow):
    def __init__(self, parent=None, jobSim=None, type="Udp"):
        super().__init__(parent, jobSim, type)
        self.ui = udp_ui()
        self.ui.setupUi(self)
        self.setWindowTitle("编辑主机网络属性")

        self.hostGraphicItem = None
        self.tmp_numApps = 0
        self.tmp_appArgs = []

        self.ui.applyButton.clicked.connect(self.apply_setting)
        self.hide()

    def apply_setting(self):
        """app数量"""
        item = self.ui.tableWidget_netargs.item(1, 0)
        # 判断是否为整数
        if not item.text().isdigit():
            item.setText("0")
        print(
            f"Host {self.hostGraphicItem.hostAttr.name} total_traffic change to {item.text()}"
        )
        self.hostGraphicItem.hostAttr.numApps = self.tmp_numApps
        self.hostGraphicItem.hostAttr.appArgs = self.tmp_appArgs
        self.lineEdit_name_cb()
        self.hide()

    def setHostGraphicItem(self, hostGraphicItem):
        print("set hostgraphicitem normal")
        self.tmp_appArgs = hostGraphicItem.hostAttr.appArgs.copy()
        self.tmp_numApps = len(self.tmp_appArgs)
        self.hostGraphicItem = hostGraphicItem

        # 将当前主机的属性显示在界面上
        self.ui.tableWidget_netargs.setItem(
            0, 0, QTableWidgetItem(str(self.hostGraphicItem.hostAttr.name))
        )
        self.ui.tableWidget_netargs.setItem(
            1, 0, QTableWidgetItem(str(self.hostGraphicItem.hostAttr.numApps))
        )
        button = QPushButton("编辑应用参数")
        button.clicked.connect(self.open_json_object_array_editor)
        self.ui.tableWidget_netargs.setCellWidget(2, 0, button)
        self.ui.tableWidget_netargs.item(1, 0).setFlags(
            Qt.ItemFlag.ItemIsSelectable | Qt.ItemFlag.ItemIsEnabled
        )
        self.ui.tableWidget_netargs.setItem(
            3, 0, QTableWidgetItem(str(self.hostGraphicItem.hostAttr.ip))
        )
        self.ui.tableWidget_netargs.setItem(
            4, 0, QTableWidgetItem(str(self.hostGraphicItem.hostAttr.mac))
        )

    def open_json_object_array_editor(self):
        """打开 JSON 对象数组编辑器窗口"""
        json_data = self.tmp_appArgs.copy()
        print(json_data)

        # 打开编辑窗口
        editor = HostNetargsAppEditorNormal(json_data)
        if editor.exec() == QDialog.DialogCode.Accepted:
            # 更新 JSON 数据
            self.tmp_appArgs = editor.get_json_data()
            self.tmp_numApps = len(self.tmp_appArgs)
            print("111" + str(self.tmp_numApps))
            self.ui.tableWidget_netargs.setItem(
                1, 0, QTableWidgetItem(str(self.tmp_numApps))
            )
            QMessageBox.information(self, "Success", "成功修改app参数")


class EditHostNetargsWindowUdp(EditHostNetargsWindow):
    def __init__(self, parent=None, jobSim=None, type="Udp"):
        super().__init__(parent, jobSim, type)
        self.ui = udp_ui()
        self.ui.setupUi(self)
        self.setWindowTitle("编辑主机网络属性")

        self.hostGraphicItem = None
        self.tmp_numApps = 0
        self.tmp_appArgs = []

        self.ui.applyButton.clicked.connect(self.apply_setting)
        self.hide()

    def apply_setting(self):
        """app数量"""
        item = self.ui.tableWidget_netargs.item(1, 0)
        # 判断是否为整数
        if not item.text().isdigit():
            item.setText("0")
        print(
            f"Host {self.hostGraphicItem.hostAttr.name} total_traffic change to {item.text()}"
        )
        self.hostGraphicItem.hostAttr.numApps = self.tmp_numApps
        self.hostGraphicItem.hostAttr.appArgs = self.tmp_appArgs
        self.lineEdit_name_cb()
        self.hide()

    def setHostGraphicItem(self, hostGraphicItem):
        print("set hostgraphicitem udp")
        self.tmp_appArgs = hostGraphicItem.hostAttr.appArgs.copy()
        self.tmp_numApps = len(self.tmp_appArgs)
        self.hostGraphicItem = hostGraphicItem

        # 将当前主机的属性显示在界面上
        self.ui.tableWidget_netargs.setItem(
            0, 0, QTableWidgetItem(str(self.hostGraphicItem.hostAttr.name))
        )
        self.ui.tableWidget_netargs.setItem(
            1, 0, QTableWidgetItem(str(self.hostGraphicItem.hostAttr.numApps))
        )
        button = QPushButton("编辑应用参数")
        button.clicked.connect(lambda _: self.open_json_object_array_editor())
        self.ui.tableWidget_netargs.setCellWidget(2, 0, button)
        self.ui.tableWidget_netargs.item(1, 0).setFlags(
            Qt.ItemFlag.ItemIsSelectable | Qt.ItemFlag.ItemIsEnabled
        )
        self.ui.tableWidget_netargs.setItem(
            3, 0, QTableWidgetItem(str(self.hostGraphicItem.hostAttr.ip))
        )
        self.ui.tableWidget_netargs.setItem(
            4, 0, QTableWidgetItem(str(self.hostGraphicItem.hostAttr.mac))
        )

    def open_json_object_array_editor(self):
        """打开 JSON 对象数组编辑器窗口"""
        json_data = self.tmp_appArgs.copy()
        print(json_data)

        # 打开编辑窗口
        editor = HostNetargsAppEditorUdp(json_data)
        if editor.exec() == QDialog.DialogCode.Accepted:
            # 更新 JSON 数据
            self.tmp_appArgs = editor.get_json_data()
            self.tmp_numApps = len(self.tmp_appArgs)
            self.ui.tableWidget_netargs.setItem(
                1, 0, QTableWidgetItem(str(self.tmp_numApps))
            )
            QMessageBox.information(self, "Success", "成功修改app参数")


class EditHostNetargsWindowTcp(EditHostNetargsWindow):
    def __init__(self, parent=None, jobSim=None, type="Tcp"):
        super().__init__(parent, jobSim, type)
        self.ui = udp_ui()
        self.ui.setupUi(self)
        self.setWindowTitle("编辑主机网络属性")

        self.hostGraphicItem = None
        self.tmp_numApps = 0
        self.tmp_appArgs = []

        self.ui.applyButton.clicked.connect(self.apply_setting)
        self.hide()

    def apply_setting(self):
        item = self.ui.tableWidget_netargs.item(1, 0)
        if not item.text().isdigit():
            item.setText("0")
        print(
            f"Host {self.hostGraphicItem.hostAttr.name} total_traffic change to {item.text()}"
        )
        self.hostGraphicItem.hostAttr.numApps = self.tmp_numApps
        self.hostGraphicItem.hostAttr.appArgs = self.tmp_appArgs
        self.lineEdit_name_cb()
        self.hide()

    def setHostGraphicItem(self, hostGraphicItem):
        print("set hostgraphicitem tcp")
        self.tmp_appArgs = hostGraphicItem.hostAttr.appArgs.copy()
        self.tmp_numApps = len(self.tmp_appArgs)
        self.hostGraphicItem = hostGraphicItem

        self.ui.tableWidget_netargs.setItem(
            0, 0, QTableWidgetItem(str(self.hostGraphicItem.hostAttr.name))
        )
        self.ui.tableWidget_netargs.setItem(
            1, 0, QTableWidgetItem(str(self.hostGraphicItem.hostAttr.numApps))
        )
        button = QPushButton("编辑应用参数")
        button.clicked.connect(lambda _: self.open_json_object_array_editor())
        self.ui.tableWidget_netargs.setCellWidget(2, 0, button)
        self.ui.tableWidget_netargs.item(1, 0).setFlags(
            Qt.ItemFlag.ItemIsSelectable | Qt.ItemFlag.ItemIsEnabled
        )
        self.ui.tableWidget_netargs.setItem(
            3, 0, QTableWidgetItem(str(self.hostGraphicItem.hostAttr.ip))
        )
        self.ui.tableWidget_netargs.setItem(
            4, 0, QTableWidgetItem(str(self.hostGraphicItem.hostAttr.mac))
        )

    def open_json_object_array_editor(self):
        json_data = self.tmp_appArgs.copy()
        print(json_data)

        editor = HostNetargsAppEditorTcp(json_data)
        if editor.exec() == QDialog.DialogCode.Accepted:
            # 更新 JSON 数据
            self.tmp_appArgs = editor.get_json_data()
            self.tmp_numApps = len(self.tmp_appArgs)
            self.ui.tableWidget_netargs.setItem(
                1, 0, QTableWidgetItem(str(self.tmp_numApps))
            )
            QMessageBox.information(self, "Success", "成功修改app参数")


class EditHostNetargsWindowRdma(EditHostNetargsWindow):
    def __init__(self, parent=None, jobSim=None, type="Rdma"):
        super().__init__(parent, jobSim, type)
        self.ui = rdma_ui()
        self.ui.setupUi(self)
        self.setWindowTitle("编辑主机网络属性")

        self.hostGraphicItem = None
        self.tmp_numApps = 0
        self.tmp_appArgs = []
        self.tmp_rdmaArgs = {}

        self.ui.applyButton.clicked.connect(self.apply_setting)
        self.hide()

    def apply_setting(self):
        """app数量"""
        item = self.ui.tableWidget_netargs.item(1, 0)
        # 判断是否为整数
        if not item.text().isdigit():
            item.setText("0")
        print(
            f"Host {self.hostGraphicItem.hostAttr.name} total_traffic change to {item.text()}"
        )
        self.hostGraphicItem.hostAttr.numApps = self.tmp_numApps
        self.hostGraphicItem.hostAttr.appArgs = self.tmp_appArgs
        self.hostGraphicItem.hostAttr.rdmaArgs = self.tmp_rdmaArgs
        self.lineEdit_name_cb()

        self.hide()

    def setHostGraphicItem(self, hostGraphicItem):
        print("set hostgraphicitem rdma")
        self.tmp_appArgs = hostGraphicItem.hostAttr.appArgs.copy()
        self.tmp_rdmaArgs = hostGraphicItem.hostAttr.rdmaArgs.copy()
        self.tmp_numApps = len(self.tmp_appArgs)
        self.hostGraphicItem = hostGraphicItem

        # 将当前主机的属性显示在界面上
        self.ui.tableWidget_netargs.setItem(
            0, 0, QTableWidgetItem(str(self.hostGraphicItem.hostAttr.name))
        )
        self.ui.tableWidget_netargs.setItem(
            1, 0, QTableWidgetItem(str(self.hostGraphicItem.hostAttr.numApps))
        )
        app_button = QPushButton("编辑应用参数")
        app_button.clicked.connect(lambda _: self.open_appArgs_editor())
        self.ui.tableWidget_netargs.setCellWidget(2, 0, app_button)
        self.ui.tableWidget_netargs.item(1, 0).setFlags(
            Qt.ItemFlag.ItemIsSelectable | Qt.ItemFlag.ItemIsEnabled
        )
        self.ui.tableWidget_netargs.setItem(
            3, 0, QTableWidgetItem(str(self.hostGraphicItem.hostAttr.ip))
        )
        self.ui.tableWidget_netargs.setItem(
            4, 0, QTableWidgetItem(str(self.hostGraphicItem.hostAttr.mac))
        )

    def open_appArgs_editor(self):
        json_data = self.tmp_appArgs.copy()

        editor = HostNetargsAppEditorRdma(json_data)
        if editor.exec() == QDialog.DialogCode.Accepted:
            # 更新 JSON 数据
            self.tmp_appArgs = editor.get_json_data()
            self.tmp_numApps = len(self.tmp_appArgs)
            self.ui.tableWidget_netargs.setItem(
                1, 0, QTableWidgetItem(str(self.tmp_numApps))
            )
            QMessageBox.information(self, "Success", "应用参数已保存")


class EditHostNetargsWindowTsn(EditHostNetargsWindow):
    def __init__(self, parent=None, jobSim=None, type="Tsn"):
        super().__init__(parent, jobSim, type)
        self.ui = tsn_ui()
        self.ui.setupUi(self)
        self.setWindowTitle("编辑主机网络属性")

        self.hostGraphicItem = None
        self.tmp_numApps = 0
        self.tmp_appArgs = []
        self.tmp_tsnArgs = []

        self.ui.applyButton.clicked.connect(self.apply_setting)
        self.hide()

    def apply_setting(self):
        """app数量"""
        item = self.ui.tableWidget_netargs.item(1, 0)
        # 判断是否为整数
        if not item.text().isdigit():
            item.setText("0")
        print(
            f"Host {self.hostGraphicItem.hostAttr.name} total_traffic change to {item.text()}"
        )
        self.hostGraphicItem.hostAttr.numApps = self.tmp_numApps
        self.hostGraphicItem.hostAttr.appArgs = self.tmp_appArgs
        self.hostGraphicItem.hostAttr.tsnArgs = self.tmp_tsnArgs
        self.lineEdit_name_cb()

        self.hide()

    def setHostGraphicItem(self, hostGraphicItem):
        print("set hostgraphicitem tsn")
        self.tmp_appArgs = hostGraphicItem.hostAttr.appArgs.copy()
        self.tmp_numApps = len(self.tmp_appArgs)
        self.tmp_tsnArgs = hostGraphicItem.hostAttr.tsnArgs.copy()
        self.hostGraphicItem = hostGraphicItem

        # 将当前主机的属性显示在界面上
        self.ui.tableWidget_netargs.setItem(
            0, 0, QTableWidgetItem(str(self.hostGraphicItem.hostAttr.name))
        )
        self.ui.tableWidget_netargs.setItem(
            1, 0, QTableWidgetItem(str(self.hostGraphicItem.hostAttr.numApps))
        )
        app_button = QPushButton("编辑应用参数")
        app_button.clicked.connect(lambda _: self.open_appArgs_editor())
        self.ui.tableWidget_netargs.setCellWidget(2, 0, app_button)
        self.ui.tableWidget_netargs.item(1, 0).setFlags(
            Qt.ItemFlag.ItemIsSelectable | Qt.ItemFlag.ItemIsEnabled
        )

        identifier_button = QPushButton("编辑TSN参数")
        identifier_button.clicked.connect(lambda _: self.open_tsnArgs_editor())
        self.ui.tableWidget_netargs.setCellWidget(3, 0, identifier_button)

        self.ui.tableWidget_netargs.setItem(
            4, 0, QTableWidgetItem(str(self.hostGraphicItem.hostAttr.ip))
        )
        self.ui.tableWidget_netargs.setItem(
            5, 0, QTableWidgetItem(str(self.hostGraphicItem.hostAttr.mac))
        )
    def open_appArgs_editor(self):
        """打开 JSON 对象数组编辑器窗口"""
        json_data = self.tmp_appArgs.copy()

        editor = HostNetargsAppEditorTsn(json_data)
        if editor.exec() == QDialog.DialogCode.Accepted:
            # 更新 JSON 数据
            self.tmp_appArgs = editor.get_json_data()
            self.tmp_numApps = len(self.tmp_appArgs)
            self.ui.tableWidget_netargs.setItem(
                1, 0, QTableWidgetItem(str(self.tmp_numApps))
            )
            QMessageBox.information(self, "Success", "应用参数已保存")

    def open_tsnArgs_editor(self):
        json_data = self.tmp_tsnArgs.copy()

        editor = JsonArrayEditor(
            json_data,
            {
                "stream": "default",
                "packetFilter": "expr(udp.destPort == 1000)",
                "pcp": "0",
            },
        )
        if editor.exec() == QDialog.DialogCode.Accepted:
            # 更新 JSON 数据
            self.tmp_tsnArgs = editor.get_json_data()
            QMessageBox.information(self, "Success", "TSN参数已保存")


class EditHostNetargsWindowDds(EditHostNetargsWindow):
    def __init__(self, parent=None, jobSim=None, type="Dds"):
        super().__init__(parent, jobSim, type)
        self.ui = dds_ui()
        self.ui.setupUi(self)
        self.setWindowTitle("编辑主机网络属性")

        self.hostGraphicItem = None
        self.tmp_numApps = 0
        self.tmp_appArgs = []

        self.ui.applyButton.clicked.connect(self.apply_setting)
        self.hide()

    def apply_setting(self):
        """app数量"""
        item = self.ui.tableWidget_netargs.item(1, 0)
        # 判断是否为整数
        if not item.text().isdigit():
            item.setText("0")
        print(
            f"Host {self.hostGraphicItem.hostAttr.name} total_traffic change to {item.text()}"
        )
        self.hostGraphicItem.hostAttr.numApps = self.tmp_numApps
        self.hostGraphicItem.hostAttr.appArgs = self.tmp_appArgs
        self.lineEdit_name_cb()
        self.hide()

    def setHostGraphicItem(self, hostGraphicItem):
        print("set hostgraphicitem dds")
        self.tmp_appArgs = hostGraphicItem.hostAttr.appArgs.copy()
        self.tmp_numApps = len(self.tmp_appArgs)
        self.hostGraphicItem = hostGraphicItem

        # 将当前主机的属性显示在界面上
        self.ui.tableWidget_netargs.setItem(
            0, 0, QTableWidgetItem(str(self.hostGraphicItem.hostAttr.name))
        )
        self.ui.tableWidget_netargs.setItem(
            1, 0, QTableWidgetItem(str(self.hostGraphicItem.hostAttr.numApps))
        )
        button = QPushButton("编辑应用参数")
        button.clicked.connect(lambda _: self.open_json_object_array_editor())
        self.ui.tableWidget_netargs.setCellWidget(2, 0, button)
        self.ui.tableWidget_netargs.item(1, 0).setFlags(
            Qt.ItemFlag.ItemIsSelectable | Qt.ItemFlag.ItemIsEnabled
        )
        self.ui.tableWidget_netargs.setItem(
            3, 0, QTableWidgetItem(str(self.hostGraphicItem.hostAttr.ip))
        )
        self.ui.tableWidget_netargs.setItem(
            4, 0, QTableWidgetItem(str(self.hostGraphicItem.hostAttr.mac))
        )

    def open_json_object_array_editor(self):
        """打开 JSON 对象数组编辑器窗口"""
        json_data = self.tmp_appArgs.copy()
        print(json_data)

        # 打开编辑窗口
        editor = HostNetargsAppEditorDds(json_data)
        if editor.exec() == QDialog.DialogCode.Accepted:
            # 更新 JSON 数据
            self.tmp_appArgs = editor.get_json_data()
            self.tmp_numApps = len(self.tmp_appArgs)
            self.ui.tableWidget_netargs.setItem(
                1, 0, QTableWidgetItem(str(self.tmp_numApps))
            )
            QMessageBox.information(self, "Success", "成功修改app参数")