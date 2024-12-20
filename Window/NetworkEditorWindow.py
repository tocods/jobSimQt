from qdarktheme.qtpy.QtWidgets import (
    QWidget,
    QTreeWidgetItem,
    QMenu,
)
from qdarktheme.qtpy.QtCore import Qt
from entity.host import *
from entity.switch import *
from qdarktheme.qtpy.QtGui import QAction
from Window.SetSimtimeWindow import SetSimtimeWindow
from Window.NetworkGlobalConfig import NetworkGlobalConfig
from UI.Network.network_editor_ui import Ui_Form
import os
import globaldata
import xml.etree.ElementTree as ET


class NetworkEditorWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.setSimtimeWindow = SetSimtimeWindow(self)
        self.networkGlobalConfigWindow = NetworkGlobalConfig()
        self.init_add_node_menu()
        self.ui.add.clicked.connect(self.show_context_menu)
        self.ui.conf.clicked.connect(self.show_network_global_config)
        self.ui.run.clicked.connect(self.action_set_netsim_time_cb)
        self.update_tree_view()

    def show_context_menu(self):
        button = self.ui.add
        button_pos = button.mapToGlobal(button.rect().bottomLeft())
        self.context_menu.move(button_pos)
        self.context_menu.show()

    def action_set_netsim_time_cb(self):
        self.setSimtimeWindow.show()

    def init_add_node_menu(self):
        self.context_menu = QMenu(self)

        menu_item_names = [
            "Udp cpu型主机",
            "Tcp cpu型主机",
            "Rdma cpu型主机",
            "Tsn cpu型主机",
            "Dds cpu型主机",
            "Udp cpu-gpu型主机",
            "Tcp cpu-gpu型主机",
            "Rdma cpu-gpu型主机",
            "Tsn cpu-gpu型主机",
            "Dds cpu-gpu型主机",
            "Udp交换机",
            "Tcp交换机",
            "Rdma交换机",
            "Tsn交换机",
            "Dds交换机",
        ]
        for index in range(0, len(menu_item_names)):
            item_name = menu_item_names[index]
            action = QAction(item_name, self)
            action.triggered.connect(
                lambda _, i=index: self.add_node_menu_item_selected(i)
            )
            self.context_menu.addAction(action)

    def show_network_global_config(self):
        self.networkGlobalConfigWindow.show()

    def add_node_menu_item_selected(self, index):
        name_list = [
            "udp_cpu",
            "tcp_cpu",
            "rdma_cpu",
            "tsn_cpu",
            "dds_cpu",
            "udp_mix",
            "tcp_mix",
            "rdma_mix",
            "tsn_mix",
            "dds_mix",
            "udp_switch",
            "tcp_switch",
            "rdma_switch",
            "tsn_switch",
            "dds_switch",
        ]
        type_list = [
            "StandardHost",
            "StandardHost",
            "StandardHost",
            "TsnDevice",
            "StandardHost",
            "StandardHost",
            "StandardHost",
            "StandardHost",
            "TsnDevice",
            "StandardHost",
            "EthernetSwitch",
            "EthernetSwitch",
            "EthernetSwitch",
            "EthernetSwitch",
            "EthernetSwitch",
        ]
        img_list = [
            "img/UDP_CPU_Host.png",
            "img/TCP_CPU_Host.png",
            "img/RDMA_CPU_Host.png",
            "img/TSN_CPU_Host.png",
            "img/DDS_CPU_Host.png",
            "img/UDP_CPU_GPU_Host.png",
            "img/TCP_CPU_GPU_Host.png",
            "img/RDMA_CPU_GPU_Host.png",
            "img/TSN_CPU_GPU_Host.png",
            "img/DDS_CPU_GPU_Host.png",
            "img/UDP_Switch.png",
            "img/TCP_Switch.png",
            "img/RDMA_Switch.png",
            "img/TSN_Switch.png",
            "img/DDS_Switch.png",
        ]
        only_cpu_list = [
            True,
            True,
            True,
            True,
            True,
            False,
            False,
            False,
            False,
            False,
            True,
            True,
            True,
            True,
            True,
        ]
        class_list = [
            UdpHost,
            TcpHost,
            RdmaHost,
            TsnHost,
            DdsHost,
            UdpHost,
            TcpHost,
            RdmaHost,
            TsnHost,
            DdsHost,
            UdpSwitch,
            TcpSwitch,
            RdmaSwitch,
            TsnSwitch,
            DdsSwitch,
        ]

        # image = QImage(img_list[index])
        # width = image.width()
        # height = image.height()
        if index < 10:
            self.ui.graphicsView.createGraphicHostItem(
                name_list[index],
                type_list[index],
                img_list[index],
                100,
                100,
                only_cpu_list[index],
                class_list[index],
            )
        else:
            self.ui.graphicsView.createGraphicSwitchItem(
                name_list[index],
                type_list[index],
                img_list[index],
                100,
                100,
                class_list[index],
            )

        self.update_tree_view()

    def update_tree_view(self):
        self.ui.infoList.clear()
        tree_widget = self.ui.infoList
        tree_widget.setHeaderLabel("节点")

        itemhost = QTreeWidgetItem(tree_widget, ["主机"])
        for host in globaldata.hostList:
            item = QTreeWidgetItem([host.hostAttr.name])
            itemhost.addChild(item)
        itemjob = QTreeWidgetItem(tree_widget, ["交换机"])
        for switch in globaldata.switchList:
            item = QTreeWidgetItem([switch.switchAttr.name])
            itemjob.addChild(item)

        tree_widget.expandAll()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_Delete:
            self.ui.graphicsView.delete_node()
            self.update_tree_view()


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
            os.path.exists(globaldata.currentProjectInfo.path + "network_data.xml")
            == False
        ):
            print("Could not find network_data.xml")
            return

        # Load the XML from the file
        tree = ET.parse(globaldata.currentProjectInfo.path + "network_data.xml")
        root = tree.getroot()

        # Clear existing lists
        globaldata.hostList.clear()
        globaldata.switchList.clear()
        globaldata.linkList.clear()
        globaldata.NetworkDevice.name_registry.clear()
        globaldata.Link.name_registry.clear()

        # 清除画布上所有内容
        graphicView = self.ui.graphicsView
        for item in graphicView.gr_scene.items():
            graphicView.gr_scene.removeItem(item)
        graphicView.gr_scene.clear()

        # Parse Hosts
        hosts_element = root.find("Hosts")
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
        for udp_host_element in udp_hosts_element.findall("UdpHost"):
            create_host_from_xml(udp_host_element, globaldata.UdpHost)

        for tcp_host_element in tcp_hosts_element.findall("TcpHost"):
            create_host_from_xml(tcp_host_element, globaldata.TcpHost)

        for rdma_host_element in rdma_hosts_element.findall("RdmaHost"):
            create_host_from_xml(rdma_host_element, globaldata.RdmaHost)

        for tsn_host_element in tsn_hosts_element.findall("TsnHost"):
            create_host_from_xml(tsn_host_element, globaldata.TsnHost)

        for dds_host_element in dds_hosts_element.findall("DdsHost"):
            create_host_from_xml(dds_host_element, globaldata.DdsHost)

        # Parse Switches
        switches_element = root.find("Switches")
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
            item = (
                self.ui.graphicsView.createGraphicSwitchItem(
                    name, type, para, width, height, Switch_class=switch_class
                )
            )
            item.setPos(pos_x, pos_y)

            item.switchAttr.readXMLElement(element)

        # Load all switch types
        for udp_switch_element in udp_switches_element.findall("UdpSwitch"):
            create_switch_from_xml(udp_switch_element, globaldata.UdpSwitch)

        for tcp_switch_element in tcp_switches_element.findall("TcpSwitch"):
            create_switch_from_xml(tcp_switch_element, globaldata.TcpSwitch)

        for rdma_switch_element in rdma_switches_element.findall("RdmaSwitch"):
            create_switch_from_xml(rdma_switch_element, globaldata.RdmaSwitch)

        for tsn_switch_element in tsn_switches_element.findall("TsnSwitch"):
            create_switch_from_xml(tsn_switch_element, globaldata.TsnSwitch)

        for dds_switch_element in dds_switches_element.findall("DdsSwitch"):
            create_switch_from_xml(dds_switch_element, globaldata.DdsSwitch)

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
            edge = graphicView.createGraphicLink(
                endpoint1, endpoint2
            )
            edge.linkAttr.type = element.get("type")
            edge.linkAttr.link_bandwidth = element.get("link_bandwidth")

        # Load all links
        for link_element in links_element.findall("Link"):
            # print(link_element)
            create_link_from_xml(link_element)

        print("Network loaded from XML!")

        self.update_tree_view()

