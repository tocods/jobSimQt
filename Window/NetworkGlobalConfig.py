from qdarktheme.qtpy.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QComboBox,
    QTableWidget,
    QTableWidgetItem,
    QPushButton,
    QMessageBox,
)
import globaldata


class NetworkGlobalConfig(QWidget):
    def __init__(self):
        super().__init__()
        self.option = {
            "forwarding": ["true", "false"],
            "connectionType": ["RELIABLE_CONNECTION", "UNRELIABLE_CONNECTION"],
            "tcpAlgorithmClass": [
                "TcpReno",
                "TcpTahoe",
                "TcpNewReno",
                "TcpNoCongestionControl",
                "DumbTcp",
            ],
        }
        self.tmp_data = globaldata.networkGlobalConfig.copy()
        self.setWindowTitle("全局参数设置")
        self.setGeometry(100, 100, 400, 300)

        self.layout = QVBoxLayout(self)

        self.combo_box = QComboBox(self)
        for key, _ in globaldata.networkGlobalConfig.items():
            self.combo_box.addItem(key)
        self.combo_box.currentTextChanged.connect(self.update_table)
        self.layout.addWidget(self.combo_box)

        self.table_widget = QTableWidget(self)
        self.layout.addWidget(self.table_widget)

        self.save_button = QPushButton("保存", self)
        self.save_button.clicked.connect(self.save_data)
        self.layout.addWidget(self.save_button)

        self.update_table(self.combo_box.currentText())

    def set_data(self, json_data):
        self.tmp_data = json_data

    def update_table(self, selection):

        # 清空表格
        self.table_widget.clear()
        self.table_widget.setRowCount(0)
        self.table_widget.setColumnCount(2)
        self.table_widget.setHorizontalHeaderLabels(["参数", "值"])

        # 获取当前选项的数据
        items = self.tmp_data.get(selection, {}).items()

        # 填充表格
        for key, value in items:
            row_position = self.table_widget.rowCount()
            self.table_widget.insertRow(row_position)
            self.table_widget.setItem(row_position, 0, QTableWidgetItem(key))
            if key in self.option:
                combo_box = QComboBox()
                combo_box.addItems(self.option[key])
                combo_box.setCurrentText(value)
                self.table_widget.setCellWidget(row_position, 1, combo_box)
            else:
                self.table_widget.setItem(row_position, 1, QTableWidgetItem(value))

    def save_data(self):
        data = {}
        for row in range(self.table_widget.rowCount()):
            key = (
                self.table_widget.item(row, 0).text()
                if self.table_widget.item(row, 0)
                else ""
            )
            value_item = self.table_widget.cellWidget(row, 1)

            if value_item:  # 如果是 QComboBox
                value = value_item.currentText()
            else:  # 否则是普通的 QTableWidgetItem
                value = (
                    self.table_widget.item(row, 1).text()
                    if self.table_widget.item(row, 1)
                    else ""
                )
            data[key] = value
        globaldata.networkGlobalConfig[self.combo_box.currentText()] = data
        # 显示保存内容（你可以将其写入文件或数据库）
        QMessageBox.information(self, "Success", "保存成功")
        self.close()
