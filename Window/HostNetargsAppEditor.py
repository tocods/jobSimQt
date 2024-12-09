from qdarktheme.qtpy.QtWidgets import (
    QDialog,
    QTabWidget,
    QVBoxLayout,
    QPushButton,
    QHBoxLayout,
)
from Window.JsonArrayEditor import JsonArrayEditor

DEFAULT_SOURCE = {
    "udp": {
        "typename": "UdpApp615",
        "packetLength": "1000B",
        "productionInterval": "100us",
        "destAddress": "",
        "destPort": "",
    },
    "tcp": {
        "typename": "TcpSessionApp",
        "sendBytes": "1000MiB",
        "localPort": "",
        "connectAddress": "",
        "connectPort": "",
    },
    "rdma": {
        "typename": "Rocev2App",
        "packetLength": "1000B",
        "productionInterval": "100us",
        "destAddress": "",
        "destinationQueuePairNumber": "100",
        "localQueuePairNumber": "100",
        "pcp": "0",
        "messageType": "SEND",
    },
    "dds": {
        "typename": "DDSPublishApp",
        "publish": "",
        "destPort": "",
        "packetLength": "5000B",
        "productionInterval": "200ms",
        "historyCacheLength": "10"
    },
}
DEFAULT_SINK = {
    "udp": {
        "typename": "UdpApp615",
        "localPort": "",
        "flowName": "default",
    },
    "tcp": {
        "typename": "TcpSinkApp",
        "localPort": "",
        "flowName": "default",
    },
    "rdma": {
        "typename": "Rocev2App",
        "localQueuePairNumber": "100",
    },
    "dds": {
        "typename": "DDSSubscribeApp",
        "subscribeTopic": "Topic1",
        "subscribePort": "1000",
        "localPort": "1000",
        "nackCountdown": "0.25ms",
        "flowName": "default",
        "receiverBufferLength": "1000"
    },
}


class HostNetargsAppEditor(QDialog):
    def __init__(self, json_data, noButton=False):
        QDialog.__init__(self)

        self.json_data = json_data
        self.tabs = {}

        self.setup_ui(noButton)
        self.update_table()

    def get_key_chinese(self):
        key_chinese = {}
        return key_chinese

    def setup_ui(self, noButton=False):
        self.setWindowTitle("编辑器")
        self.setGeometry(100, 100, 800, 600)
        self.tabWidget = QTabWidget()
        self.setupTab()
        for title, tab in self.tabs.items():
            self.tabWidget.addTab(tab, title)
        if not noButton:
            self.applyButton = QPushButton("保存")
            self.applyButton.clicked.connect(self.save)

        layout = QVBoxLayout()
        layout.addWidget(self.tabWidget)

        if not noButton:
            edit_layout = QHBoxLayout()
            edit_layout.addWidget(self.applyButton)

            layout.addLayout(edit_layout)
        self.setLayout(layout)

    def save(self):
        self.json_data = []
        for _, tab in self.tabs.items():
            self.json_data += tab.get_json_data()
        self.accept()

    def clean(self):
        for _, tab in self.tabs.items():
            tab.clean()
    
    def setData(self, data: list):
        self.clean()
        self.json_data = data
        self.update_table()
        self.get_json_data()

    def update_table(self):
        for obj in self.json_data:
            for _, tab in self.tabs.items():
                if tab.defaultObj["typename"] == obj["typename"]:
                    if tab.try_insert_object(obj):
                        break
        return
    
    def get_json_data(self):
        self.json_data = []
        for _, tab in self.tabs.items():
            self.json_data += tab.get_json_data()

        return self.json_data


class HostNetargsAppEditorApp(HostNetargsAppEditor):
    def setupTab(self):
        self.tabs = {
            "Udp发送端": JsonArrayEditor([], DEFAULT_SOURCE["udp"], False),
            "Tcp发送端": JsonArrayEditor([], DEFAULT_SOURCE["tcp"], False),
            "Rdma发送端": JsonArrayEditor([], DEFAULT_SOURCE["rdma"], False),
            "Udp接收端": JsonArrayEditor([], DEFAULT_SINK["udp"], False),
            "Tcp接收端": JsonArrayEditor([], DEFAULT_SINK["tcp"], False),
            "Rdma接收端": JsonArrayEditor([], DEFAULT_SINK["rdma"], False),
            "TSN": JsonArrayEditor(
            [],
            {
                "typename": "TSN",
                "stream": "default",
                "packetFilter": "expr(udp.destPort == 1000)",
            },
        )
        }
class HostNetargsAppEditorMiddleware(HostNetargsAppEditor):
    def setupTab(self):
        self.tabs = {
             "Dds发送端": JsonArrayEditor([], DEFAULT_SOURCE["dds"], False),
             "Dds接收端": JsonArrayEditor([], DEFAULT_SINK["dds"], False),
        }

class HostNetargsAppEditorNormal(HostNetargsAppEditor):
    def setupTab(self):
        self.tabs = {
            "Udp发送端": JsonArrayEditor([], DEFAULT_SOURCE["udp"], False),
            "Tcp发送端": JsonArrayEditor([], DEFAULT_SOURCE["tcp"], False),
            "Udp接收端": JsonArrayEditor([], DEFAULT_SINK["udp"], False),
            "Tcp接收端": JsonArrayEditor([], DEFAULT_SINK["tcp"], False),
        }


class HostNetargsAppEditorUdp(HostNetargsAppEditor):
    def setupTab(self):
        self.tabs = {
            "Udp发送端": JsonArrayEditor([], DEFAULT_SOURCE["udp"], False),
            "Udp接收端": JsonArrayEditor([], DEFAULT_SINK["udp"], False),
        }


class HostNetargsAppEditorTcp(HostNetargsAppEditor):
    def setupTab(self):
        self.tabs = {
            "Tcp发送端": JsonArrayEditor([], DEFAULT_SOURCE["tcp"], False),
            "Tcp接收端": JsonArrayEditor([], DEFAULT_SINK["tcp"], False),
        }


class HostNetargsAppEditorRdma(HostNetargsAppEditor):
    def setupTab(self):
        self.tabs = {
            "Rdma发送端": JsonArrayEditor([], DEFAULT_SOURCE["rdma"], False),
            "Rdma接收端": JsonArrayEditor([], DEFAULT_SINK["rdma"], False),
        }


class HostNetargsAppEditorTsn(HostNetargsAppEditor):
    def setupTab(self):
        self.tabs = {
            "Udp发送端": JsonArrayEditor([], DEFAULT_SOURCE["udp"], False),
            "Tcp发送端": JsonArrayEditor([], DEFAULT_SOURCE["tcp"], False),
            "Udp接收端": JsonArrayEditor([], DEFAULT_SINK["udp"], False),
            "Tcp接收端": JsonArrayEditor([], DEFAULT_SINK["tcp"], False),
        }


class HostNetargsAppEditorDds(HostNetargsAppEditor):
    def setupTab(self):
        self.tabs = {
            "Udp发送端": JsonArrayEditor([], DEFAULT_SOURCE["udp"], False),
            "Tcp发送端": JsonArrayEditor([], DEFAULT_SOURCE["tcp"], False),
            "Dds发送端": JsonArrayEditor([], DEFAULT_SOURCE["dds"], False),
            "Udp接收端": JsonArrayEditor([], DEFAULT_SINK["udp"], False),
            "Tcp接收端": JsonArrayEditor([], DEFAULT_SINK["tcp"], False),
            "Dds接收端": JsonArrayEditor([], DEFAULT_SINK["dds"], False),
        }
