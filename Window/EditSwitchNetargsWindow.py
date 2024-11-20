from qdarktheme.qtpy.QtWidgets import (
    QMessageBox,
    QDialog,
    QTableWidgetItem,
    QPushButton,
)
from qdarktheme.qtpy.QtCore import Qt
from UI.Network.edit_switch_netargs_ui import Ui_Dialog
from UI.Network.edit_switch_netargs_tsn_ui import Ui_Dialog as tsn_ui
from Window.JsonArrayEditor import JsonArrayEditor


class EditSwitchNetargsWindow(QDialog):
    def __init__(self, parent=None, type="Udp"):
        QDialog.__init__(self)
        self.parent = parent
        self.ui = Ui_Dialog()
        self.type = type
        self.ui.setupUi(self)
        self.setWindowTitle("编辑交换机网络属性")

        self.switchGraphicItem = None

        self.ui.lineEdit_name.textEdited.connect(self.lineEdit_name_cb)

        self.ui.applyButton.clicked.connect(self.apply_settings)
        self.hide()

    def setSwitchGraphicItem(self, switchGraphicItem):
        self.switchGraphicItem = switchGraphicItem
        # 将当前交换机的属性显示在界面上
        self.ui.lineEdit_name.setText(self.switchGraphicItem.switchAttr.name)
        self.ui.tableWidget_netargs.setItem(
            0,
            0,
            QTableWidgetItem(str(self.switchGraphicItem.switchAttr.transmission_rate)),
        )
        return

    def lineEdit_name_cb(self):
        name = self.ui.lineEdit_name.text()

        # 更新主机名称
        if name != self.switchGraphicItem.switchAttr.name:
            self.switchGraphicItem.switchAttr.set_name(name)
            # 若重名自动添加编号后缀时，更新画布上的交换机名称
            self.ui.lineEdit_name.setText(self.switchGraphicItem.switchAttr.name)

        self.switchGraphicItem.setName(name)
        print("Switch name: " + self.switchGraphicItem.switchAttr.name)

    def on_cell_edited(self, row, col):
        return

    def apply_settings(self):
        item = self.ui.tableWidget_netargs.item(0, 0)
        print(
            f"Switch {self.switchGraphicItem.switchAttr.name} transmission_rate change to {item.text()}"
        )
        self.switchGraphicItem.switchAttr.transmission_rate = int(item.text())
        self.parent.parent.update_tree_view()
        self.hide()


class EditSwitchNetargsWindowNormal(EditSwitchNetargsWindow):
    def __init__(self, parent=None, type="Normal"):
        super().__init__(parent, type)


class EditSwitchNetargsWindowUdp(EditSwitchNetargsWindow):
    def __init__(self, parent=None, type="Udp"):
        super().__init__(parent, type)


class EditSwitchNetargsWindowTcp(EditSwitchNetargsWindow):
    def __init__(self, parent=None, type="Tcp"):
        super().__init__(parent, type)


class EditSwitchNetargsWindowRdma(EditSwitchNetargsWindow):
    def __init__(self, parent=None, type="Rdma"):
        super().__init__(parent, type)


class EditSwitchNetargsWindowTsn(EditSwitchNetargsWindow):
    def __init__(self, parent=None, type="Tsn"):
        QDialog.__init__(self)
        self.type = type
        self.ui = tsn_ui()
        self.ui.setupUi(self)
        self.setWindowTitle("编辑交换机网络属性")

        self.switchGraphicItem = None
        self.ui.lineEdit_name.textEdited.connect(self.lineEdit_name_cb)

        self.ui.applyButton.clicked.connect(self.apply_settings)
        self.hide()

    def apply_settings(self):
        item = self.ui.tableWidget_netargs.item(0, 0)
        print(
            f"Switch {self.switchGraphicItem.switchAttr.name} transmission_rate change to {item.text()}"
        )
        self.switchGraphicItem.switchAttr.transmission_rate = int(item.text())
        self.hide()
        return

    def setSwitchGraphicItem(self, switchGraphicItem):
        self.switchGraphicItem = switchGraphicItem
        self.ui.lineEdit_name.setText(self.switchGraphicItem.switchAttr.name)
        self.ui.tableWidget_netargs.setItem(
            0,
            0,
            QTableWidgetItem(str(self.switchGraphicItem.switchAttr.transmission_rate)),
        )
        button = QPushButton("编辑tsn队列信息")
        button.clicked.connect(lambda _: self.open_json_object_array_editor())
        self.ui.tableWidget_netargs.setCellWidget(1, 0, button)
        self.ui.tableWidget_netargs.item(0, 0).setFlags(
            Qt.ItemFlag.ItemIsSelectable | Qt.ItemFlag.ItemIsEnabled
        )
        return

    def open_json_object_array_editor(self):
        """打开 JSON 对象数组编辑器窗口"""
        json_data = self.switchGraphicItem.switchAttr.tsn_queue

        # 打开编辑窗口
        editor = JsonArrayEditor(
            json_data,
            {
                "display-name": "default",
                "offset": "0ms",
                "durations": "[1ms, 10ms]",
                "initiallyOpen": "true",
                "packetCapacity": "100",
            },
        )
        if editor.exec() == QDialog.DialogCode.Accepted:
            # 更新 JSON 数据
            updated_data = editor.get_json_data()
            self.switchGraphicItem.switchAttr.tsn_queue = (
                updated_data  # 转回 JSON 数组字符串
            )
            QMessageBox.information(self, "Success", "编辑完成")


class EditSwitchNetargsWindowDds(EditSwitchNetargsWindow):
    def __init__(self, parent=None, type="Dds"):
        super().__init__(parent, type)
