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
    def __init__(self, parent=None, type="Udp"):
        QDialog.__init__(self)
        self.ui = udp_ui()
        self.type = type

    def on_cell_edited(self, row, col):
        return

    def setHostGraphicItem(self, hostGraphicItem):
        print("Error:未指定类型")

    def apply_setting(self):
        print("Error:未指定类型")


class EditHostNetargsWindowNormal(EditHostNetargsWindow):
    def __init__(self, parent=None, type="Udp"):
        super().__init__(parent, type)
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
        item = self.ui.tableWidget_netargs.item(0, 0)
        # 判断是否为整数
        if not item.text().isdigit():
            item.setText("0")
        print(
            f"Host {self.hostGraphicItem.hostAttr.name} total_traffic change to {item.text()}"
        )
        self.hostGraphicItem.hostAttr.numApps = self.tmp_numApps
        self.hostGraphicItem.hostAttr.appArgs = self.tmp_appArgs
        self.hide()

    def setHostGraphicItem(self, hostGraphicItem):
        print("set hostgraphicitem normal")
        self.tmp_appArgs = hostGraphicItem.hostAttr.appArgs.copy()
        self.tmp_numApps = len(self.tmp_appArgs)
        self.hostGraphicItem = hostGraphicItem

        # 将当前主机的属性显示在界面上
        self.ui.tableWidget_netargs.setItem(
            0, 0, QTableWidgetItem(str(self.hostGraphicItem.hostAttr.numApps))
        )
        button = QPushButton("编辑应用参数")
        button.clicked.connect(lambda _: self.open_json_object_array_editor())
        self.ui.tableWidget_netargs.setCellWidget(1, 0, button)
        self.ui.tableWidget_netargs.item(0, 0).setFlags(
            Qt.ItemFlag.ItemIsSelectable | Qt.ItemFlag.ItemIsEnabled
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
            self.ui.tableWidget_netargs.setItem(
                0, 0, QTableWidgetItem(str(self.tmp_numApps))
            )
            QMessageBox.information(self, "Success", "成功修改app参数")


class EditHostNetargsWindowUdp(EditHostNetargsWindow):
    def __init__(self, parent=None, type="Udp"):
        super().__init__(parent, type)
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
        item = self.ui.tableWidget_netargs.item(0, 0)
        # 判断是否为整数
        if not item.text().isdigit():
            item.setText("0")
        print(
            f"Host {self.hostGraphicItem.hostAttr.name} total_traffic change to {item.text()}"
        )
        self.hostGraphicItem.hostAttr.numApps = self.tmp_numApps
        self.hostGraphicItem.hostAttr.appArgs = self.tmp_appArgs
        self.hide()

    def setHostGraphicItem(self, hostGraphicItem):
        print("set hostgraphicitem udp")
        self.tmp_appArgs = hostGraphicItem.hostAttr.appArgs.copy()
        self.tmp_numApps = len(self.tmp_appArgs)
        self.hostGraphicItem = hostGraphicItem

        # 将当前主机的属性显示在界面上
        self.ui.tableWidget_netargs.setItem(
            0, 0, QTableWidgetItem(str(self.hostGraphicItem.hostAttr.numApps))
        )
        button = QPushButton("编辑应用参数")
        button.clicked.connect(lambda _: self.open_json_object_array_editor())
        self.ui.tableWidget_netargs.setCellWidget(1, 0, button)
        self.ui.tableWidget_netargs.item(0, 0).setFlags(
            Qt.ItemFlag.ItemIsSelectable | Qt.ItemFlag.ItemIsEnabled
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
                0, 0, QTableWidgetItem(str(self.tmp_numApps))
            )
            QMessageBox.information(self, "Success", "成功修改app参数")


class EditHostNetargsWindowTcp(EditHostNetargsWindow):
    def __init__(self, parent=None, type="Tcp"):
        super().__init__(parent, type)
        self.ui = udp_ui()
        self.ui.setupUi(self)
        self.setWindowTitle("编辑主机网络属性")

        self.hostGraphicItem = None
        self.tmp_numApps = 0
        self.tmp_appArgs = []

        self.ui.applyButton.clicked.connect(self.apply_setting)
        self.hide()

    def apply_setting(self):
        item = self.ui.tableWidget_netargs.item(0, 0)
        if not item.text().isdigit():
            item.setText("0")
        print(
            f"Host {self.hostGraphicItem.hostAttr.name} total_traffic change to {item.text()}"
        )
        self.hostGraphicItem.hostAttr.numApps = self.tmp_numApps
        self.hostGraphicItem.hostAttr.appArgs = self.tmp_appArgs
        self.hide()

    def setHostGraphicItem(self, hostGraphicItem):
        print("set hostgraphicitem tcp")
        self.tmp_appArgs = hostGraphicItem.hostAttr.appArgs.copy()
        self.tmp_numApps = len(self.tmp_appArgs)
        self.hostGraphicItem = hostGraphicItem

        self.ui.tableWidget_netargs.setItem(
            0, 0, QTableWidgetItem(str(self.hostGraphicItem.hostAttr.numApps))
        )
        button = QPushButton("编辑应用参数")
        button.clicked.connect(lambda _: self.open_json_object_array_editor())
        self.ui.tableWidget_netargs.setCellWidget(1, 0, button)
        self.ui.tableWidget_netargs.item(0, 0).setFlags(
            Qt.ItemFlag.ItemIsSelectable | Qt.ItemFlag.ItemIsEnabled
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
                0, 0, QTableWidgetItem(str(self.tmp_numApps))
            )
            QMessageBox.information(self, "Success", "成功修改app参数")


class EditHostNetargsWindowRdma(EditHostNetargsWindow):
    def __init__(self, parent=None, type="Rdma"):
        super().__init__(parent, type)
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
        item = self.ui.tableWidget_netargs.item(0, 0)
        # 判断是否为整数
        if not item.text().isdigit():
            item.setText("0")
        print(
            f"Host {self.hostGraphicItem.hostAttr.name} total_traffic change to {item.text()}"
        )
        self.hostGraphicItem.hostAttr.numApps = self.tmp_numApps
        self.hostGraphicItem.hostAttr.appArgs = self.tmp_appArgs
        self.hostGraphicItem.hostAttr.rdmaArgs = self.tmp_rdmaArgs

        self.hide()

    def setHostGraphicItem(self, hostGraphicItem):
        print("set hostgraphicitem rdma")
        self.tmp_appArgs = hostGraphicItem.hostAttr.appArgs.copy()
        self.tmp_rdmaArgs = hostGraphicItem.hostAttr.rdmaArgs.copy()
        self.tmp_numApps = len(self.tmp_appArgs)
        self.hostGraphicItem = hostGraphicItem

        # 将当前主机的属性显示在界面上
        self.ui.tableWidget_netargs.setItem(
            0, 0, QTableWidgetItem(str(self.hostGraphicItem.hostAttr.numApps))
        )
        app_button = QPushButton("编辑应用参数")
        app_button.clicked.connect(lambda _: self.open_appArgs_editor())
        self.ui.tableWidget_netargs.setCellWidget(1, 0, app_button)
        self.ui.tableWidget_netargs.item(0, 0).setFlags(
            Qt.ItemFlag.ItemIsSelectable | Qt.ItemFlag.ItemIsEnabled
        )

    def open_appArgs_editor(self):
        json_data = self.tmp_appArgs.copy()

        editor = HostNetargsAppEditorRdma(json_data)
        if editor.exec() == QDialog.DialogCode.Accepted:
            # 更新 JSON 数据
            self.tmp_appArgs = editor.get_json_data()
            self.tmp_numApps = len(self.tmp_appArgs)
            self.ui.tableWidget_netargs.setItem(
                0, 0, QTableWidgetItem(str(self.tmp_numApps))
            )
            QMessageBox.information(self, "Success", "应用参数已保存")


class EditHostNetargsWindowTsn(EditHostNetargsWindow):
    def __init__(self, parent=None, type="Tsn"):
        super().__init__(parent, type)
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
        item = self.ui.tableWidget_netargs.item(0, 0)
        # 判断是否为整数
        if not item.text().isdigit():
            item.setText("0")
        print(
            f"Host {self.hostGraphicItem.hostAttr.name} total_traffic change to {item.text()}"
        )
        self.hostGraphicItem.hostAttr.numApps = self.tmp_numApps
        self.hostGraphicItem.hostAttr.appArgs = self.tmp_appArgs
        self.hostGraphicItem.hostAttr.tsnArgs = self.tmp_tsnArgs

        self.hide()

    def setHostGraphicItem(self, hostGraphicItem):
        print("set hostgraphicitem tsn")
        self.tmp_appArgs = hostGraphicItem.hostAttr.appArgs.copy()
        self.tmp_numApps = len(self.tmp_appArgs)
        self.tmp_tsnArgs = hostGraphicItem.hostAttr.tsnArgs.copy()
        self.hostGraphicItem = hostGraphicItem

        # 将当前主机的属性显示在界面上
        self.ui.tableWidget_netargs.setItem(
            0, 0, QTableWidgetItem(str(self.hostGraphicItem.hostAttr.numApps))
        )
        app_button = QPushButton("编辑应用参数")
        app_button.clicked.connect(lambda _: self.open_appArgs_editor())
        self.ui.tableWidget_netargs.setCellWidget(1, 0, app_button)
        self.ui.tableWidget_netargs.item(0, 0).setFlags(
            Qt.ItemFlag.ItemIsSelectable | Qt.ItemFlag.ItemIsEnabled
        )

        identifier_button = QPushButton("编辑TSN参数")
        identifier_button.clicked.connect(lambda _: self.open_tsnArgs_editor())
        self.ui.tableWidget_netargs.setCellWidget(2, 0, identifier_button)

    def open_appArgs_editor(self):
        """打开 JSON 对象数组编辑器窗口"""
        json_data = self.tmp_appArgs.copy()

        editor = HostNetargsAppEditorUdp(json_data)
        if editor.exec() == QDialog.DialogCode.Accepted:
            # 更新 JSON 数据
            self.tmp_appArgs = editor.get_json_data()
            self.tmp_numApps = len(self.tmp_appArgs)
            self.ui.tableWidget_netargs.setItem(
                0, 0, QTableWidgetItem(str(self.tmp_numApps))
            )
            QMessageBox.information(self, "Success", "应用参数已保存")

    def open_tsnArgs_editor(self):
        json_data = self.tmp_tsnArgs.copy()

        editor = JsonArrayEditor(
            json_data,
            ["stream", "packetFilter", "pcp"],
            ["best-effort", "expr(udp.destPort == 1000)", "0"],
        )
        if editor.exec() == QDialog.DialogCode.Accepted:
            # 更新 JSON 数据
            self.tmp_tsnArgs = editor.get_json_data()
            QMessageBox.information(self, "Success", "TSN参数已保存")


class EditHostNetargsWindowDds(EditHostNetargsWindow):
    def __init__(self, parent=None, type="Dds"):
        super().__init__(parent, type)
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
        item = self.ui.tableWidget_netargs.item(0, 0)
        # 判断是否为整数
        if not item.text().isdigit():
            item.setText("0")
        print(
            f"Host {self.hostGraphicItem.hostAttr.name} total_traffic change to {item.text()}"
        )
        self.hostGraphicItem.hostAttr.numApps = self.tmp_numApps
        self.hostGraphicItem.hostAttr.appArgs = self.tmp_appArgs
        self.hide()

    def setHostGraphicItem(self, hostGraphicItem):
        print("set hostgraphicitem dds")
        self.tmp_appArgs = hostGraphicItem.hostAttr.appArgs.copy()
        self.tmp_numApps = len(self.tmp_appArgs)
        self.hostGraphicItem = hostGraphicItem

        # 将当前主机的属性显示在界面上
        self.ui.tableWidget_netargs.setItem(
            0, 0, QTableWidgetItem(str(self.hostGraphicItem.hostAttr.numApps))
        )
        button = QPushButton("编辑应用参数")
        button.clicked.connect(lambda _: self.open_json_object_array_editor())
        self.ui.tableWidget_netargs.setCellWidget(1, 0, button)
        self.ui.tableWidget_netargs.item(0, 0).setFlags(
            Qt.ItemFlag.ItemIsSelectable | Qt.ItemFlag.ItemIsEnabled
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
                0, 0, QTableWidgetItem(str(self.tmp_numApps))
            )
            QMessageBox.information(self, "Success", "成功修改app参数")
