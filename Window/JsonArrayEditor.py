from qdarktheme.qtpy.QtWidgets import (
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QPushButton,
    QHBoxLayout,
    QMessageBox,
    QDialog,
)


class JsonArrayEditor(QDialog):
    """弹出窗口用于编辑 JSON 对象数组数据"""

    def __init__(self, json_data, fields, defaults):
        super().__init__()
        self.fields = fields
        self.defaults = defaults
        self.json_data = json_data if isinstance(json_data, list) else []
        self.setWindowTitle("编辑器")
        self.setGeometry(200, 200, 600, 400)

        # 设置表格
        self.table_widget = QTableWidget()
        self.table_widget.setColumnCount(len(fields))
        self.table_widget.setHorizontalHeaderLabels(fields)

        # 增加、删除和保存按钮
        self.add_button = QPushButton("添加对象")
        self.add_button.clicked.connect(self.add_object)
        self.delete_button = QPushButton("删除选中对象")
        self.delete_button.clicked.connect(self.delete_object)
        self.save_button = QPushButton("保存")
        self.save_button.clicked.connect(self.accept)  # 保存后关闭窗口

        # 布局
        layout = QVBoxLayout()
        layout.addWidget(self.table_widget)

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.add_button)
        button_layout.addWidget(self.delete_button)
        layout.addLayout(button_layout)
        layout.addWidget(self.save_button)

        self.setLayout(layout)

        # 显示数据
        self.show_json_objects()

    def show_json_objects(self):
        """显示 JSON 对象数组在表格中"""
        self.table_widget.setRowCount(len(self.json_data))
        for row, obj in enumerate(self.json_data):
            for col, field in enumerate(self.fields):  # 假设字段名称固定
                value = obj.get(field, "")
                item = QTableWidgetItem(str(value))
                self.table_widget.setItem(row, col, item)

    def add_object(self):
        """添加新对象到数组"""
        new_obj = {self.fields[i]: self.defaults[i] for i in range(0, len(self.fields))}
        self.json_data.append(new_obj)

        row_position = self.table_widget.rowCount()
        self.table_widget.insertRow(row_position)
        for col, field in enumerate(self.fields):
            self.table_widget.setItem(
                row_position, col, QTableWidgetItem(new_obj[field])
            )

    def delete_object(self):
        """删除选中的对象"""
        selected_row = self.table_widget.currentRow()
        if selected_row == -1:
            QMessageBox.warning(self, "Warning", "未选中对象")
            return

        del self.json_data[selected_row]
        self.table_widget.removeRow(selected_row)

    def get_json_data(self):
        """返回编辑后的 JSON 对象数组"""
        new_data = []
        for row in range(self.table_widget.rowCount()):
            obj = {}
            for col, field in enumerate(self.fields):
                item = self.table_widget.item(row, col)
                obj[field] = item.text() if item else ""
            new_data.append(obj)
        self.json_data = new_data
        return self.json_data
