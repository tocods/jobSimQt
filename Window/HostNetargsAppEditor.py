from qdarktheme.qtpy.QtWidgets import (
    QDialog,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QPushButton,
    QLabel,
    QHBoxLayout,
    QMessageBox,
    QMenu,
    QComboBox,
)
from qdarktheme.qtpy.QtGui import QAction
from qdarktheme.qtpy.QtCore import Qt


class HostNetargsAppEditor(QDialog):
    def __init__(self, json_data):
        QDialog.__init__(self)

        self.current_index = 0
        self.json_data = json_data

        self.setup_ui()
        self.add_source_button.clicked.connect(self.add_source)
        self.add_sink_button.clicked.connect(self.add_sink)
        self.update_table()
    def get_key_chinese(self):
        key_chinese = {
            "typename": "类型名",
            "packetLength": "发包长度",
            "productionInterval": "发包间隔",
            "destAddress": "目标地址（名称）",
            "destPort": "目标端口",
            "sendBytes": "发送长度",
            "localPort": "本机端口",
            "connectAddress": "目标地址（名称）",
            "connectPort": "目标端口",
            "localPort": "本地端口",
            "destinationQueuePairNumber": "目标队列序号",
            "localQueuePairNumber": "目标队列序号",
            "pcp": "优先级",
            "messageType": "消息类型",
            "publish": "发布主题",
            "subscribeTopic": "订阅主题",
            "subscribePort": "订阅端口",
            "nackCountdown": "nackCountdown",
            "flowName": "flow名称",
        }
        return key_chinese

    def setup_ui(self):
        self.setWindowTitle("编辑器")
        self.setGeometry(100, 100, 600, 400)

        self.table_widget = QTableWidget()
        self.table_widget.setColumnCount(2)
        self.table_widget.setHorizontalHeaderLabels(["参数", "值"])
        self.table_widget.itemChanged.connect(self.update_json_data)  # 监听单元格更改

        self.next_button = QPushButton("下一页")
        self.next_button.clicked.connect(self.next_page)
        self.prev_button = QPushButton("上一页")
        self.prev_button.clicked.connect(self.prev_page)

        self.add_source_button = QPushButton("添加发送端")
        self.add_sink_button = QPushButton("添加接收端")
        self.delete_button = QPushButton("删除应用配置")
        self.delete_button.clicked.connect(self.delete_object)
        self.applyButton = QPushButton("保存")
        self.applyButton.clicked.connect(self.accept)

        self.info_label = QLabel("", alignment=Qt.AlignmentFlag.AlignCenter)

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

        self.setLayout(layout)

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
        for row, (field, value) in enumerate(current_object.copy().items()):
            if field in self.get_key_chinese():
                field_name = self.get_key_chinese()[field]
                self.table_widget.setItem(row, 0, QTableWidgetItem(field_name))
            else:
                self.table_widget.setItem(row, 0, QTableWidgetItem(field))
            self.table_widget.setItem(row, 1, QTableWidgetItem(str(value)))
            item = self.table_widget.item(row, 0)
            item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEditable)
            if field == "typename":
                item = self.table_widget.item(row, 1)
                item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEditable)

    def update_json_data(self, item):
        if not self.json_data:
            return

        row = item.row()
        col = item.column()

        current_object = self.json_data[self.current_index]
        keys = list(current_object.keys())

        if col == 0:
            return
        elif col == 1:
            # 修改字段值
            key = keys[row]
            current_object[key] = item.text()

    def add_source(self):
        """添加一个空的 JSON 对象并跳转到新对象"""
        new_object = {"typename": "没有类型"}
        self.json_data.append(new_object)
        self.current_index = len(self.json_data) - 1  # 跳转到新对象
        self.update_table()

    def add_sink(self):
        """添加一个空的 JSON 对象并跳转到新对象"""
        new_object = {"typename": "没有类型"}
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


class HostNetargsAppEditorNormal(HostNetargsAppEditor):
    def __init__(self, json_data):
        QDialog.__init__(self)
        self.current_index = 0
        self.json_data = json_data
        self.setup_ui()
        self.add_source_menu = self.create_add_source_menu()
        self.add_source_button.setMenu(self.add_source_menu)
        self.add_sink_menu = self.create_add_sink_menu()
        self.add_sink_button.setMenu(self.add_sink_menu)
        self.update_table()

    def create_add_source_menu(self):
        menu = QMenu(self)
        sources = ["Udp", "Tcp"]
        for source in sources:
            action = QAction(source, self)
            action.triggered.connect(lambda checked, s=source: self.add_source(s))
            menu.addAction(action)
        return menu

    def create_add_sink_menu(self):
        menu = QMenu(self)
        sinks = ["Udp", "Tcp"]  # 示例接收端类型
        for sink in sinks:
            action = QAction(sink, self)
            action.triggered.connect(lambda checked, s=sink: self.add_sink(s))
            menu.addAction(action)
        return menu

    def add_source(self, source_type):
        udp_source = {
            "typename": "UdpApp615",
            "packetLength": "1000B",
            "productionInterval": "100us",
            "destAddress": "",
            "destPort": "",
        }
        tcp_source = {
            "typename": "TcpSessionApp",
            "sendBytes": "1000MiB",
            "localPort": "",
            "connectAddress": "",
            "connectPort": "",
        }
        new_source = {"Udp": udp_source, "Tcp": tcp_source}
        self.json_data.append(new_source[source_type])
        self.current_index = len(self.json_data) - 1
        self.update_table()

    def add_sink(self, sink_type):
        udp_sink = {"typename": "UdpApp615", "localPort": "", "flowName": "default"}
        tcp_sink = {"typename": "TcpSinkApp", "localPort": "", "flowName": "default"}
        new_sink = {"Udp": udp_sink, "Tcp": tcp_sink}
        self.json_data.append(new_sink[sink_type])
        self.current_index = len(self.json_data) - 1
        self.update_table()


class HostNetargsAppEditorUdp(HostNetargsAppEditor):
    def add_source(self):
        """添加一个空的 JSON 对象并跳转到新对象"""
        new_object = {
            "typename": "UdpApp615",
            "packetLength": "1000B",
            "productionInterval": "100us",
            "destAddress": "",
            "destPort": "",
            "sinkTypename": "",
        }
        self.json_data.append(new_object)
        self.current_index = len(self.json_data) - 1  # 跳转到新对象
        self.update_table()

    def add_sink(self):
        """添加一个空的 JSON 对象并跳转到新对象"""
        new_object = {"typename": "UdpApp615", "localPort": ""}
        self.json_data.append(new_object)
        self.current_index = len(self.json_data) - 1  # 跳转到新对象
        self.update_table()


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
        new_object = {"typename": "UdpSinkApp", "localPort": "", "flowName": "default"}
        self.json_data.append(new_object)
        self.current_index = len(self.json_data) - 1  # 跳转到新对象
        self.update_table()


class HostNetargsAppEditorRdma(HostNetargsAppEditor):
    def update_table(self):
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

        current_object = self.json_data[self.current_index]

        self.table_widget.setRowCount(len(current_object))
        for row, (field, value) in enumerate(current_object.items()):
            if field in self.get_key_chinese():
                field_name = self.get_key_chinese()[field]
                self.table_widget.setItem(row, 0, QTableWidgetItem(field_name))
            else:
                self.table_widget.setItem(row, 0, QTableWidgetItem(field))
            self.table_widget.setItem(row, 1, QTableWidgetItem(str(value)))
            item = self.table_widget.item(row, 0)
            item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEditable)
            if field == "typename":
                item = self.table_widget.item(row, 1)
                item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEditable)
            if field == "messageType":
                combo_box = QComboBox()
                combo_box.addItems(["SEND", "RDMA_READ", "RDMA_WRITE"])
                combo_box.setCurrentText(value)
                self.table_widget.setCellWidget(row, 1, combo_box)
            if field == "pcp":
                combo_box = QComboBox()
                combo_box.addItems(["0", "1", "2", "3", "4", "5", "6", "7"])
                combo_box.setCurrentText(value)
                self.table_widget.setCellWidget(row, 1, combo_box)

    def add_source(self):
        new_object = {
            "typename": "Rocev2App",
            "packetLength": "1000B",
            "productionInterval": "100us",
            "destAddress": "",
            "destinationQueuePairNumber": "100",
            "localQueuePairNumber": "100",
            "pcp": "0",
            "messageType": "SEND",
        }
        self.json_data.append(new_object)
        self.current_index = len(self.json_data) - 1  # 跳转到新对象
        self.update_table()

    def add_sink(self):
        """添加一个空的 JSON 对象并跳转到新对象"""
        new_object = {
            "typename": "Rocev2App",
            "localQueuePairNumber": "100",
        }
        self.json_data.append(new_object)
        self.current_index = len(self.json_data) - 1  # 跳转到新对象
        self.update_table()


class HostNetargsAppEditorTsn(HostNetargsAppEditor):
    def __init__(self, json_data):
        QDialog.__init__(self)
        self.current_index = 0
        self.json_data = json_data
        self.setup_ui()
        self.add_source_menu = self.create_add_source_menu()
        self.add_source_button.setMenu(self.add_source_menu)
        self.add_sink_menu = self.create_add_sink_menu()
        self.add_sink_button.setMenu(self.add_sink_menu)
        self.update_table()

    def create_add_source_menu(self):
        menu = QMenu(self)
        sources = ["Udp", "Tcp"]
        for source in sources:
            action = QAction(source, self)
            action.triggered.connect(lambda checked, s=source: self.add_source(s))
            menu.addAction(action)
        return menu

    def create_add_sink_menu(self):
        menu = QMenu(self)
        sinks = ["Udp", "Tcp"]
        for sink in sinks:
            action = QAction(sink, self)
            action.triggered.connect(lambda checked, s=sink: self.add_sink(s))
            menu.addAction(action)
        return menu

    def add_source(self, source_type):
        udp_source = {
            "typename": "UdpApp615",
            "packetLength": "1000B",
            "productionInterval": "100us",
            "destAddress": "",
            "destPort": "",
        }
        tcp_source = {
            "typename": "TcpSessionApp",
            "sendBytes": "1000MiB",
            "localPort": "",
            "connectAddress": "",
            "connectPort": "",
        }

        new_source = {"Udp": udp_source, "Tcp": tcp_source}
        self.json_data.append(new_source[source_type])
        self.current_index = len(self.json_data) - 1
        self.update_table()

    def add_sink(self, sink_type):
        udp_sink = {"typename": "UdpApp615", "localPort": "", "flowName": "default"}
        tcp_sink = {"typename": "TcpSinkApp", "localPort": "", "flowName": "default"}
        new_sink = {"Udp": udp_sink, "Tcp": tcp_sink}
        self.json_data.append(new_sink[sink_type])
        self.current_index = len(self.json_data) - 1
        self.update_table()


class HostNetargsAppEditorDds(HostNetargsAppEditor):
    def __init__(self, json_data):
        QDialog.__init__(self)
        self.current_index = 0
        self.json_data = json_data
        self.setup_ui()
        self.add_source_menu = self.create_add_source_menu()
        self.add_source_button.setMenu(self.add_source_menu)
        self.add_sink_menu = self.create_add_sink_menu()
        self.add_sink_button.setMenu(self.add_sink_menu)
        self.update_table()

    def create_add_source_menu(self):
        menu = QMenu(self)
        sources = ["Udp", "Tcp", "Dds"]
        for source in sources:
            action = QAction(source, self)
            action.triggered.connect(lambda checked, s=source: self.add_source(s))
            menu.addAction(action)
        return menu

    def create_add_sink_menu(self):
        menu = QMenu(self)
        sinks = ["Udp", "Tcp", "Dds"]
        for sink in sinks:
            action = QAction(sink, self)
            action.triggered.connect(lambda checked, s=sink: self.add_sink(s))
            menu.addAction(action)
        return menu

    def add_source(self, source_type):
        udp_source = {
            "typename": "UdpSourceApp",
            "packetLength": "1000B",
            "productionInterval": "100us",
            "destAddress": "",
            "destPort": "",
        }
        tcp_source = {
            "typename": "TcpSessionApp",
            "sendBytes": "1000MiB",
            "localPort": "",
            "connectAddress": "",
            "connectPort": "",
        }

        dds_source = {
            "typename": "DDSPublishApp",
            "publish": "",
            "destPort": "",
            "packetLength": "5000B",
            "productionInterval": "200ms",
        }
        new_source = {"Udp": udp_source, "Tcp": tcp_source, "Dds": dds_source}
        self.json_data.append(new_source[source_type])
        self.current_index = len(self.json_data) - 1
        self.update_table()

    def add_sink(self, sink_type):
        udp_sink = {"typename": "UdpSinkApp", "localPort": ""}
        tcp_sink = {"typename": "TcpSinkApp", "localPort": ""}
        dds_sink = {
            "typename": "DDSSubscribeApp",
            "subscribeTopic": "Topic1",
            "subscribePort": "1000",
            "localPort": "1000",
            "nackCountdown": "0.25ms",
            "flowName": "default",
        }
        new_sink = {"Udp": udp_sink, "Tcp": tcp_sink, "Dds": dds_sink}
        self.json_data.append(new_sink[sink_type])
        self.current_index = len(self.json_data) - 1
        self.update_table()
