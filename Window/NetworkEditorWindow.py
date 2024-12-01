from qdarktheme.qtpy.QtWidgets import (
    QWidget,
    QTreeWidgetItem,
    QMenu,
)
from qdarktheme.qtpy.QtCore import Qt
from entity.host import *
from entity.switch import *
from entity.link import *
from qdarktheme.qtpy.QtGui import QAction
from Window.SetSimtimeWindow import SetSimtimeWindow
from Window.NetworkGlobalConfig import NetworkGlobalConfig
from UI.Network.network_editor_ui import Ui_Form
import os
import globaldata
import xml.etree.ElementTree as ET
from edge import GraphicEdge
from item import HostGraphicItem, SwitchGraphicItem
from Window.HostNetargsAppEditor import (
    HostNetargsAppEditorApp,
    HostNetargsAppEditorMiddleware,
)
from Window.JsonArrayEditor import JsonArrayEditor
from Window.DictEditor import DictEditor
from util.jobSim import sysSim


class NetworkEditorWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.setupSide()
        self.setSimtimeWindow = SetSimtimeWindow(sysSim, self)
        self.networkGlobalConfigWindow = NetworkGlobalConfig()
        self.init_add_node_menu()
        self.ui.add_host.setMenu(self.add_host_menu)

        self.ui.add_switch.setMenu(self.add_switch_menu)
        self.ui.add_switch.clicked.connect(self.stop_adding)
        self.ui.add_line.clicked.connect(self.ui.graphicsView.lineToolStateChange)
        self.ui.global_setting.clicked.connect(self.show_network_global_config)
        self.ui.run.clicked.connect(self.action_set_netsim_time_cb)
        self.ui.hostApply.clicked.connect(self.applyHost)
        self.ui.switchApply.clicked.connect(self.applySwitch)
        self.ui.linkApply.clicked.connect(self.applyLink)

        self.update_tree_view()

        self.curHostItem = None
        self.curSwitchItem = None
        self.curLinkItem = None

    def setupSide(self):
        self.ui.hostSet.clear()
        self.ui.switchSet.clear()
        self.ui.linkSet.clear()

        self.hostPhysics = DictEditor(["name", "ip", "mac", "packet_size", "packet_interval"], {}, False)
        self.ui.hostSet.addTab(self.hostPhysics, "物理层")
        self.hostApp = HostNetargsAppEditorApp("", True)
        self.ui.hostSet.addTab(self.hostApp, "协议层")
        self.hostMiddleware = HostNetargsAppEditorMiddleware("", True)
        self.ui.hostSet.addTab(self.hostMiddleware, "中间件层")

        self.linkEditor = DictEditor(["link_bandwidth", "error_rate"], {}, False)
        self.ui.linkSet.addTab(self.linkEditor, "链路速率")

        self.switchEditor = DictEditor(["name", "transmission_rate"], {}, False)
        self.ui.switchSet.addTab(self.switchEditor, "交换机")
        self.tsnQueue = JsonArrayEditor(
            "",
            {
                
                "display-name": "default",
                "offset": "0ms",
                "durations": "[1ms, 10ms]",
                "initiallyOpen": "true",
                "packetCapacity": "100",
            },
            False,
        )
        self.ui.switchSet.addTab(self.tsnQueue, "tsn队列配置")

    def action_set_netsim_time_cb(self):
        self.setSimtimeWindow.show()

    def init_add_host_menu(self):
        self.add_host_menu = QMenu(self)
        menu_item_names = [
            "UDP-TCP通用型主机",
            "RDMA型主机",
            "TSN型主机",
        ]

        for index in range(0, len(menu_item_names)):
            item_name = menu_item_names[index]
            action = QAction(item_name, self)
            action.triggered.connect(
                lambda _, i=index: self.add_host_menu_item_selected(i)
            )
            self.add_host_menu.addAction(action)
        action = QAction("停止添加", self)
        action.triggered.connect(self.stop_adding)
        self.add_host_menu.addAction(action)

    def init_add_switch_menu(self):
        self.add_switch_menu = QMenu(self)
        menu_item_names = [
            "通用交换机",
            "Rdma型交换机",
            "Tsn型交换机",
        ]

        for index in range(0, len(menu_item_names)):
            item_name = menu_item_names[index]
            action = QAction(item_name, self)
            action.triggered.connect(
                lambda _, i=index: self.add_switch_menu_item_selected(i)
            )
            self.add_switch_menu.addAction(action)
        action = QAction("停止添加", self)
        action.triggered.connect(self.stop_adding)
        self.add_switch_menu.addAction(action)

    def init_add_node_menu(self):
        self.init_add_host_menu()
        self.init_add_switch_menu()

    def show_network_global_config(self):
        self.networkGlobalConfigWindow.set_data(globaldata.networkGlobalConfig.copy())
        self.networkGlobalConfigWindow.show()

    def add_host_menu_item_selected(self, index):
        name_list = [
            "udp_tcp",
            "rdma",
            "tsn",
        ]
        type_list = [
            "StandardHost",
            "StandardHost",
            "TsnDevice",
        ]
        img_list = [
            "img/Normal_CPU_Host.png",
            "img/RDMA_CPU_Host.png",
            "img/TSN_CPU_Host.png",
        ]
        only_cpu_list = [
            True,
            True,
            True,
        ]
        class_list = [
            NormalHost,
            RdmaHost,
            TsnHost,
        ]

        self.ui.graphicsView.setHostToAdd(
            name_list[index],
            type_list[index],
            img_list[index],
            100,
            100,
            only_cpu_list[index],
            class_list[index],
        )

    def stop_adding(self):
        self.ui.graphicsView.stopAdding()

    def add_switch_menu_item_selected(self, index):
        name_list = [
            "switch",
            "rdma_switch",
            "tsn_switch",
        ]
        type_list = [
            "EthernetSwitch",
            "EthernetSwitch",
            "EthernetSwitch",
        ]
        img_list = [
            "img/Normal_Switch.png",
            "img/RDMA_Switch.png",
            "img/TSN_Switch.png",
        ]
        class_list = [
            NormalSwitch,
            RdmaSwitch,
            TsnSwitch,
        ]

        self.ui.graphicsView.setSwitchToAdd(
            name_list[index],
            type_list[index],
            img_list[index],
            100,
            100,
            class_list[index],
        )

    def update_tree_view(self):
        print("update_tree_view")
        self.ui.infoList.clear()
        tree_widget = self.ui.infoList
        tree_widget.setHeaderLabel("节点")

        itemhost = QTreeWidgetItem(tree_widget, ["主机"])
        for host in globaldata.hostList:
            item = QTreeWidgetItem([host.hostAttr.name])
            item.addChild(QTreeWidgetItem([sysSim.manager[host.hostAttr.name].name]))
            # for app in host.hostAttr.appArgs:
            #     item.addChild(QTreeWidgetItem([app["typename"]]))
            for name in sysSim.jobs:
                job = sysSim.jobs[name]
                if job.host == host.hostAttr.name:
                    item.addChild(QTreeWidgetItem([job.name]))
            itemhost.addChild(item)
        itemjob = QTreeWidgetItem(tree_widget, ["交换机"])
        for switch in globaldata.switchList:
            item = QTreeWidgetItem([switch.switchAttr.name])
            itemjob.addChild(item)
        itemFault = QTreeWidgetItem(tree_widget, ["故障"])
        for fault in sysSim.faults:
            item = QTreeWidgetItem([fault])
            itemFault.addChild(item)

        tree_widget.expandAll()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_Delete:
            self.ui.graphicsView.delete_node()
            self.update_tree_view()

    def cancelSelect(self):
        self.curHostItem = None
        self.hostPhysics.setDict({})
        self.hostApp.clean()
        self.curSwitchItem = None
        self.switchEditor.setDict({})
        self.curLinkItem = None
        self.linkEditor.setDict({})

    def selectHost(self, hostItem: HostGraphicItem):
        self.curHostItem = hostItem
        self.hostPhysics.setDict(hostItem.hostAttr.getPhysicsAttr())
        self.hostApp.setData(hostItem.hostAttr.appArgs.copy())
        self.hostMiddleware.setData(hostItem.hostAttr.appArgs.copy())
        return
    
    def selectHostApp(self, hostItem: HostGraphicItem):
        return

    def selectSwitch(self, switchItem: SwitchGraphicItem):
        self.curSwitchItem = switchItem
        self.switchEditor.setDict(switchItem.switchAttr.getAttr())
        self.tsnQueue.clean()
        for obj in self.curSwitchItem.switchAttr.getTsnQueue():
            self.tsnQueue.add_object(obj)
        return

    def selectLink(self, linkItem: GraphicEdge):
        self.curLinkItem = linkItem
        self.linkEditor.setDict(linkItem.getLinkAttr())
        return
    
    def changeHostName(self, name):
        data = self.hostPhysics.getDict()
        data["name"] = name
        self.hostPhysics.setDict(data)
        self.curHostItem.setName(data["name"])
        self.curHostItem.hostAttr.applyPhysicsAttr(data)
        data = self.hostApp.get_json_data() + self.hostMiddleware.get_json_data()
        self.curHostItem.hostAttr.appArgs = data
        self.update_tree_view()

    def applyHost(self):
        data = self.hostPhysics.getDict()
        sysSim.hosts[data["name"]] =  sysSim.hosts[self.curHostItem.hostAttr.name]
        sysSim.hosts.pop(self.curHostItem.hostAttr.name)
        sysSim.hosts[data["name"]].name = data["name"]
        for name in sysSim.jobs:
            job = sysSim.jobs[name]
            if job.host == self.curHostItem.hostAttr.name:
                job.host = data["name"]
        sysSim.manager[data["name"]] = sysSim.manager[self.curHostItem.hostAttr.name]
        if data["name"] != self.curHostItem.hostAttr.name:
            print("bbb")
            sysSim.manager.pop(self.curHostItem.hostAttr.name)
        for name in sysSim.faults:
            fault = sysSim.faults[name]
            if fault.aim == self.curHostItem.hostAttr.name:
                fault.aim = data["name"]
        self.curHostItem.setName(data["name"])
        self.curHostItem.hostAttr.applyPhysicsAttr(data)
        data = self.hostApp.get_json_data() + self.hostMiddleware.get_json_data()
        self.curHostItem.hostAttr.appArgs = data
        self.update_tree_view()

        return
    


    def applySwitch(self):
        data = self.switchEditor.getDict()
        self.curSwitchItem.setName(data["name"])
        self.curSwitchItem.switchAttr.applyAttr(data)
        self.switchEditor.setDict(self.curSwitchItem.switchAttr.getAttr())

        data = self.tsnQueue.get_json_data()
        self.curSwitchItem.switchAttr.setTsnQueue(data)

        self.update_tree_view()
        return

    def applyLink(self):
        data = self.linkEditor.getDict()
        self.curLinkItem.edge_wrap.linkAttr.applyAttr(data)
        self.linkEditor.setDict(self.curLinkItem.getLinkAttr())
        self.update_tree_view()
        return

    def load_network_from_xml(self):
        # Helper function to find a host or switch by name
        def find_host_or_switch_by_name(name):
            for host in globaldata.hostList:
                if host.hostAttr.name == name:
                    return host
            for switch in globaldata.switchList:
                if switch.switchAttr.name == name:
                    return switch
            return None

        print(globaldata.currentProjectInfo.path)
        if (
            os.path.exists(
                os.path.join(globaldata.currentProjectInfo.path, "network_data.xml")
            )
            == False
        ):
            print("Could not find network_data.xml")
            return

        # Load the XML from the file
        tree = ET.parse(
            os.path.join(globaldata.currentProjectInfo.path, "network_data.xml")
        )
        root = tree.getroot()

        # Clear existing lists
        globaldata.hostList.clear()
        globaldata.switchList.clear()
        globaldata.linkList.clear()
        NetworkDevice.name_registry.clear()
        Link.name_registry.clear()

        # 清除画布上所有内容
        graphicView = self.ui.graphicsView
        for item in graphicView.gr_scene.items():
            graphicView.gr_scene.removeItem(item)
        graphicView.gr_scene.clear()

        # Parse Hosts
        hosts_element = root.find("Hosts")
        normal_hosts_element = hosts_element.find("NormalHosts")
        udp_hosts_element = hosts_element.find("UdpHosts")
        tcp_hosts_element = hosts_element.find("TcpHosts")
        rdma_hosts_element = hosts_element.find("RdmaHosts")
        tsn_hosts_element = hosts_element.find("TsnHosts")
        dds_hosts_element = hosts_element.find("DdsHosts")

        # Function to create a host from XML element
        def create_host_from_xml(element, host_class):

            name = element.get("name")
            type = element.get("type")

            width = float(element.get("graphic_width"))
            height = float(element.get("graphic_height"))
            para = element.get("graphic_image")
            pos_x = float(element.get("graphic_pos_x"))
            pos_y = float(element.get("graphic_pos_y"))

            # 字符串等于"True"时为True，否则为False
            onlyCpu = element.get("only_cpu") == "True"

            # Host graphic item creation
            graphicView = self.ui.graphicsView
            item = graphicView.createGraphicHostItem(
                name, type, para, width, height, onlyCpu=onlyCpu, Host_class=host_class
            )
            item.setPos(pos_x, pos_y)

            item.hostAttr.readXMLElement(element)

            # item = HostGraphicItem(host_name, host_type, img, width, height, Host_class=Host_class)
            # item.setPos(0, 0)
            # self.jobSim.addHostItem(item, onlyCPU=onlyCpu)
            # self.gr_scene.add_node(item)

        # Load all host types
        for normal_host_element in normal_hosts_element.findall("NormalHost"):
            create_host_from_xml(normal_host_element, NormalHost)

        for udp_host_element in udp_hosts_element.findall("UdpHost"):
            create_host_from_xml(udp_host_element, UdpHost)

        for tcp_host_element in tcp_hosts_element.findall("TcpHost"):
            create_host_from_xml(tcp_host_element, TcpHost)

        for rdma_host_element in rdma_hosts_element.findall("RdmaHost"):
            create_host_from_xml(rdma_host_element, RdmaHost)

        for tsn_host_element in tsn_hosts_element.findall("TsnHost"):
            create_host_from_xml(tsn_host_element, TsnHost)

        for dds_host_element in dds_hosts_element.findall("DdsHost"):
            create_host_from_xml(dds_host_element, DdsHost)

        # Parse Switches
        switches_element = root.find("Switches")
        normal_switches_element = switches_element.find("NormalSwitches")
        udp_switches_element = switches_element.find("UdpSwitches")
        tcp_switches_element = switches_element.find("TcpSwitches")
        rdma_switches_element = switches_element.find("RdmaSwitches")
        tsn_switches_element = switches_element.find("TsnSwitches")
        dds_switches_element = switches_element.find("DdsSwitches")

        # Function to create a switch from XML element
        def create_switch_from_xml(element, switch_class):

            name = element.get("name")
            type = element.get("type")

            width = float(element.get("graphic_width"))
            height = float(element.get("graphic_height"))
            para = element.get("graphic_image")
            pos_x = float(element.get("graphic_pos_x"))
            pos_y = float(element.get("graphic_pos_y"))

            # Switch graphic item creation
            item = self.ui.graphicsView.createGraphicSwitchItem(
                name, type, para, width, height, Switch_class=switch_class
            )
            item.setPos(pos_x, pos_y)

            item.switchAttr.readXMLElement(element)

        # Load all switch types
        for normal_switch_element in normal_switches_element.findall("NormalSwitch"):
            create_switch_from_xml(normal_switch_element, NormalSwitch)

        for udp_switch_element in udp_switches_element.findall("UdpSwitch"):
            create_switch_from_xml(udp_switch_element, UdpSwitch)

        for tcp_switch_element in tcp_switches_element.findall("TcpSwitch"):
            create_switch_from_xml(tcp_switch_element, TcpSwitch)

        for rdma_switch_element in rdma_switches_element.findall("RdmaSwitch"):
            create_switch_from_xml(rdma_switch_element, RdmaSwitch)

        for tsn_switch_element in tsn_switches_element.findall("TsnSwitch"):
            create_switch_from_xml(tsn_switch_element, TsnSwitch)

        for dds_switch_element in dds_switches_element.findall("DdsSwitch"):
            create_switch_from_xml(dds_switch_element, DdsSwitch)

        # Parse Links
        links_element = root.find("Links")

        # Function to create a link from XML element
        def create_link_from_xml(element):

            # Find the endpoints by their names
            endpoint1_name = element.get("endpoint1")
            endpoint2_name = element.get("endpoint2")

            # Assuming there are functions to find a host/switch by name
            endpoint1 = find_host_or_switch_by_name(endpoint1_name)
            endpoint2 = find_host_or_switch_by_name(endpoint2_name)

            if endpoint1 is None or endpoint2 is None:
                print("Error: Could not find host or switch by name")
                return

            graphicView = self.ui.graphicsView
            edge = graphicView.createGraphicLink(endpoint1, endpoint2)
            edge.linkAttr.type = element.get("type")
            edge.linkAttr.link_bandwidth = element.get("link_bandwidth")
            edge.linkAttr.error_rate = element.get("error_rate")

        # Load all links
        for link_element in links_element.findall("Link"):
            # print(link_element)
            create_link_from_xml(link_element)

        global_setting_element = root.find("GlobalSetting")
        globaldata.networkGlobalConfig = json.loads(
            global_setting_element.get("content")
        )

        print("Network loaded from XML!")

        self.update_tree_view()
