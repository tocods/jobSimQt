from PyQt5.QtCore import Qt
from qdarktheme.qtpy.QtWidgets import (
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QPushButton,
    QHBoxLayout,
    QMessageBox,
    QWidget,
    QComboBox
)
from UI.localisation import CHINESE_KEYS
import globaldata


class DictEditor(QWidget):
    def __init__(self, fields: list, data: dict={}, hasSaveButton=True) -> None:
        super().__init__()
        self.fields = fields
        self.data = data
                # 设置表格
        self.table_widget = QTableWidget()
        self.table_widget.setRowCount(len(self.fields))
        self.table_widget.setColumnCount(1)
        chinese_fields = []
        for field in self.fields:
            if field in CHINESE_KEYS:
                chinese_fields.append(CHINESE_KEYS[field])
            else:
                chinese_fields.append(field)

        self.table_widget.setVerticalHeaderLabels(chinese_fields)
        self.table_widget.setHorizontalHeaderLabels(["值"])

        # 增加、删除和保存按钮
        if hasSaveButton:
            self.save_button = QPushButton("保存")

        # 布局
        layout = QVBoxLayout()
        layout.addWidget(self.table_widget)

        button_layout = QHBoxLayout()
        layout.addLayout(button_layout)
        if hasSaveButton:
            layout.addWidget(self.save_button)

        self.setLayout(layout)

        # 显示数据
        self.showDict()

    def showDict(self):
        """显示 JSON 对象数组在表格中"""
        for row, field in enumerate(self.fields):
            value = self.data.get(field, "")
            item = QTableWidgetItem(str(value))
            self.table_widget.setItem(row, 0, item)
        return
    
    def setDict(self, data):
        self.data = data
        self.showDict()
    
    def getDict(self):
        for row, field in enumerate(self.fields):
            item = self.table_widget.item(row, 0)
            self.data[field] = item.text() if item else ""
        return self.data