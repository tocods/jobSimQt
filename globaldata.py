import os
import xml.etree.ElementTree as ET
from xml.dom import minidom

from entity.host import *
from entity.switch import *
from entity.link import Link

from PySide6.QtGui import QFont

global scheduler
scheduler = 0

global jobList
jobList = []

global hostList
""" hostList的元素类型为: HostGraphicItem """
hostList = []

global faultList
""" switchList的元素类型为: SwitchGraphicItem """
switchList = []
linkList = []
faultList = []

global duration
duration = 0

global projectPath
projectPath = "."


class ProjectInfo:
    def __init__(self):
        self.directory = ""
        self.name = ""
        self.fullname = ""
        self.path = ""
        return

    def setDirAndName(self, directory, name):  # 比如 D:/fe , omnet_template
        self.directory = directory
        self.name = name
        self.fullname = directory + "/" + name
        self.path = directory + "/" + name + "/"

    def setFullname(self, fullname):  # 比如 D:/fe/omnet_template
        directory, name = os.path.split(fullname)  # 分离文件名和路径
        self.directory = directory
        self.name = name
        self.fullname = directory + "/" + name
        self.path = directory + "/" + name + "/"

    def setPath(self, path):  # 比如 D:/fe/omnet_template/
        self.directory = path
    
    def setRelativePath(self, relativePath):
        self.directory = os.getcwd()
        self.name = relativePath
        self.fullname = self.directory + "\\" + relativePath
        self.path = self.directory + "\\" + relativePath + "\\"


global currentProjectInfo
currentProjectInfo = ProjectInfo()

global networkGlobalConfig
networkGlobalConfig = {
    "Udp": {},
    "Tcp": {
        "forwarding": "false",
        "retryTimeout": "1s",
        "retryCount": "3",
        "cacheTimeout": "100s",
        "queueTypename": "DropTailQueue",
        "queuePacketCapacity": "100",
        "tcpAlgorithmClass": "TcpReno",
    },
    "Rdma": {},
    "Tsn": {},
    "Dds": {},
}


def create_xml():
    # Create the root of the XML tree
    root = ET.Element("Network")

    # Add hosts
    hosts_element = ET.SubElement(root, "Hosts")

    # 添加主机不同类型
    udp_hosts_element = ET.SubElement(hosts_element, "UdpHosts")
    tcp_hosts_element = ET.SubElement(hosts_element, "TcpHosts")
    rdma_hosts_element = ET.SubElement(hosts_element, "RdmaHosts")
    tsn_hosts_element = ET.SubElement(hosts_element, "TsnHosts")
    dds_hosts_element = ET.SubElement(hosts_element, "DdsHosts")

    for host_graphic_item in hostList:
        # 判断主机类型
        if isinstance(host_graphic_item.hostAttr, UdpHost):
            host_element = ET.SubElement(udp_hosts_element, "UdpHost")
        elif isinstance(host_graphic_item.hostAttr, TcpHost):
            host_element = ET.SubElement(tcp_hosts_element, "TcpHost")
        elif isinstance(host_graphic_item.hostAttr, RdmaHost):
            host_element = ET.SubElement(rdma_hosts_element, "RdmaHost")
        elif isinstance(host_graphic_item.hostAttr, TsnHost):
            host_element = ET.SubElement(tsn_hosts_element, "TsnHost")
        elif isinstance(host_graphic_item.hostAttr, DdsHost):
            host_element = ET.SubElement(dds_hosts_element, "DdsHost")
        else:
            print("not a valid host!")

        host_graphic_item.hostAttr.setXMLElement(host_element)

        # 主机图形对象的位置信息
        host_element.set("graphic_pos_x", str(host_graphic_item.pos().x()))
        host_element.set("graphic_pos_y", str(host_graphic_item.pos().y()))
        host_element.set("graphic_image", host_graphic_item.para)
        host_element.set("graphic_width", str(host_graphic_item.width))
        host_element.set("graphic_height", str(host_graphic_item.height))
        # host_element.set("graphic_scene_pos_x", str(host_graphic_item.scenePos().x()))
        # host_element.set("graphic_scene_pos_y", str(host_graphic_item.scenePos().y()))

    # Add switches
    switches_element = ET.SubElement(root, "Switches")

    # 添加交换机不同类型
    udp_switches_element = ET.SubElement(switches_element, "UdpSwitches")
    tcp_switches_element = ET.SubElement(switches_element, "TcpSwitches")
    rdma_switches_element = ET.SubElement(switches_element, "RdmaSwitches")
    tsn_switches_element = ET.SubElement(switches_element, "TsnSwitches")
    dds_switches_element = ET.SubElement(switches_element, "DdsSwitches")

    for switch_graphic_item in switchList:
        # 判断交换机类型
        if isinstance(switch_graphic_item.switchAttr, UdpSwitch):
            switch_element = ET.SubElement(udp_switches_element, "UdpSwitch")
        elif isinstance(switch_graphic_item.switchAttr, TcpSwitch):
            switch_element = ET.SubElement(tcp_switches_element, "TcpSwitch")
        elif isinstance(switch_graphic_item.switchAttr, RdmaSwitch):
            switch_element = ET.SubElement(rdma_switches_element, "RdmaSwitch")
        elif isinstance(switch_graphic_item.switchAttr, TsnSwitch):
            switch_element = ET.SubElement(tsn_switches_element, "TsnSwitch")
        elif isinstance(switch_graphic_item.switchAttr, DdsSwitch):
            switch_element = ET.SubElement(dds_switches_element, "DdsSwitch")
        else:
            print("not a valid switch!")

        switch_graphic_item.switchAttr.setXMLElement(switch_element)

        # 交换机图形对象的位置信息
        switch_element.set("graphic_pos_x", str(switch_graphic_item.pos().x()))
        switch_element.set("graphic_pos_y", str(switch_graphic_item.pos().y()))
        switch_element.set("graphic_image", switch_graphic_item.para)
        switch_element.set("graphic_width", str(switch_graphic_item.width))
        switch_element.set("graphic_height", str(switch_graphic_item.height))

    # Add links
    links_element = ET.SubElement(root, "Links")
    for link_item in linkList:
        link_element = ET.SubElement(links_element, "Link")
        link_element.set("name", link_item.linkAttr.name)
        link_element.set("type", link_item.linkAttr.type)

        if isinstance(link_item.linkAttr.endpoint1.get_attr(), Host):
            link_element.set("endpoint1", link_item.linkAttr.endpoint1.hostAttr.name)
        elif isinstance(link_item.linkAttr.endpoint1.get_attr(), Switch):
            link_element.set("endpoint1", link_item.linkAttr.endpoint1.switchAttr.name)

        if isinstance(link_item.linkAttr.endpoint2.get_attr(), Host):
            link_element.set("endpoint2", link_item.linkAttr.endpoint2.hostAttr.name)
        elif isinstance(link_item.linkAttr.endpoint2.get_attr(), Switch):
            link_element.set("endpoint2", link_item.linkAttr.endpoint2.switchAttr.name)

        link_element.set("link_bandwidth", str(link_item.linkAttr.link_bandwidth))

    # Convert to a pretty XML string
    xml_str = ET.tostring(root, encoding="unicode")

    parsed_xml_str = minidom.parseString(xml_str)
    formatted_xml_str = parsed_xml_str.toprettyxml(indent="    ")

    return formatted_xml_str


def save_data():
    # Save the data to a file
    xml_str = create_xml()
    with open(currentProjectInfo.path + "network_data.xml", "w") as f:
        f.write(xml_str)


global font
font = QFont()
font.setPointSize(20)