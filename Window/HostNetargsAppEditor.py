from qdarktheme.qtpy.QtWidgets import (
    QDialog,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QPushButton,
    QLabel,
    QHBoxLayout,
    QMessageBox,
)
from qdarktheme.qtpy.QtCore import Qt


class HostNetargsAppEditor(QDialog):
    def __init__(self, json_data):
        QDialog.__init__(self)
        self.current_index = 0
        self.json_data = json_data
        self.setWindowTitle("编辑器")
        self.setGeometry(100, 100, 600, 400)

        # 设置表格
        self.table_widget = QTableWidget()
        self.table_widget.setColumnCount(2)
        self.table_widget.setHorizontalHeaderLabels(["Field", "Value"])
        self.table_widget.itemChanged.connect(self.update_json_data)  # 监听单元格更改

        # 增加翻页和编辑按钮
        self.next_button = QPushButton("下一页")
        self.next_button.clicked.connect(self.next_page)
        self.prev_button = QPushButton("上一页")
        self.prev_button.clicked.connect(self.prev_page)

        self.add_source_button = QPushButton("添加发送端")
        self.add_source_button.clicked.connect(self.add_source)
        self.add_sink_button = QPushButton("添加接收端")
        self.add_sink_button.clicked.connect(self.add_sink)
        self.delete_button = QPushButton("删除应用配置")
        self.delete_button.clicked.connect(self.delete_object)
        self.applyButton = QPushButton("保存")
        self.applyButton.clicked.connect(self.accept)

        # 提示标签
        self.info_label = QLabel("", alignment=Qt.AlignmentFlag.AlignCenter)

        # 布局
        layout = QVBoxLayout()
        layout.addWidget(self.table_widget)

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.prev_button)
        button_layout.addWidget(self.next_button)

        edit_layout = QHBoxLayout()
        edit_layout.addWidget(self.add_source_button)
        edit_layout.addWidget(self.add_sink_button)
        edit_layout.addWidget(self.delete_button)
        edit_layout.addWidget(self.applyButton)

        layout.addLayout(button_layout)
        layout.addLayout(edit_layout)
        layout.addWidget(self.info_label)

        # container = QWidget()
        # container.setLayout(layout)
        # self.setCentralWidget(container)
        self.setLayout(layout)

        # 显示内容
        self.update_table()

    def update_table(self):
        """更新表格内容，显示当前索引的对象"""
        if not self.json_data:  # 检查数据是否为空
            self.table_widget.setRowCount(0)
            self.info_label.setText("没有数据")
            self.next_button.setEnabled(False)
            self.prev_button.setEnabled(False)
            self.delete_button.setEnabled(False)
            return
        else:
            self.info_label.setText(
                f" {self.current_index + 1} / {len(self.json_data)}"
            )
            self.next_button.setEnabled(self.current_index < len(self.json_data) - 1)
            self.prev_button.setEnabled(self.current_index > 0)
            self.delete_button.setEnabled(True)

        # 获取当前对象
        current_object = self.json_data[self.current_index]

        # 更新表格行数并填充数据
        self.table_widget.setRowCount(len(current_object))
        for row, (field, value) in enumerate(current_object.items()):
            self.table_widget.setItem(row, 0, QTableWidgetItem(field))
            self.table_widget.setItem(row, 1, QTableWidgetItem(str(value)))
            item = self.table_widget.item(row, 0)
            item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEditable)
            if field == "typename":
                item = self.table_widget.item(row, 1)
                item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEditable)

    def update_json_data(self, item):
        """将用户编辑的单元格数据保存到 JSON 对象"""
        if not self.json_data:
            return

        row = item.row()
        col = item.column()

        # 避免在迭代过程中修改字典，将键值先取出
        current_object = self.json_data[self.current_index]
        keys = list(current_object.keys())

        if col == 0:
            # 修改字段名
            old_key = keys[row]
            new_key = item.text()
            if new_key and new_key != old_key:
                # 更新字段名的方式
                value = current_object.pop(old_key)
                current_object[new_key] = value
                self.update_table()  # 刷新表格显示
        elif col == 1:
            # 修改字段值
            key = keys[row]
            current_object[key] = item.text()

    def add_source(self):
        """添加一个空的 JSON 对象并跳转到新对象"""
        new_object = {
            "typename": "UdpSourceApp",
            "packetLength": "1000B",
            "productionInterval": "100us",
            "destAddress": "",
            "destPort": "",
        }
        self.json_data.append(new_object)
        self.current_index = len(self.json_data) - 1  # 跳转到新对象
        self.update_table()

    def add_sink(self):
        """添加一个空的 JSON 对象并跳转到新对象"""
        new_object = {"typename": "UdpSinkApp", "localPort": ""}
        self.json_data.append(new_object)
        self.current_index = len(self.json_data) - 1  # 跳转到新对象
        self.update_table()

    def delete_object(self):
        """删除当前 JSON 对象"""
        if not self.json_data:
            return
        reply = QMessageBox.question(
            self,
            "删除",
            "是否确认删除?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No,
        )
        if reply == QMessageBox.StandardButton.Yes:
            del self.json_data[self.current_index]
            self.current_index = max(0, self.current_index - 1)  # 调整索引
            self.update_table()

    def next_page(self):
        """显示下一个对象"""
        if self.current_index < len(self.json_data) - 1:
            self.current_index += 1
            self.update_table()

    def prev_page(self):
        """显示上一个对象"""
        if self.current_index > 0:
            self.current_index -= 1
            self.update_table()

    def get_json_data(self):
        return self.json_data


class HostNetargsAppEditorTcp(HostNetargsAppEditor):
    def add_source(self):
        new_object = {
            "typename": "TcpSessionApp",
            "sendBytes": "1000MiB",
            "localPort": "",
            "connectAddress": "",
            "connectPort": "",
        }
        self.json_data.append(new_object)
        self.current_index = len(self.json_data) - 1  # 跳转到新对象
        self.update_table()

    def add_sink(self):
        """添加一个空的 JSON 对象并跳转到新对象"""
        new_object = {"typename": "TcpSinkApp", "localPort": ""}
        self.json_data.append(new_object)
        self.current_index = len(self.json_data) - 1  # 跳转到新对象
        self.update_table()
