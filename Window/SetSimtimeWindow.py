import os
import platform
from qdarktheme.qtpy.QtWidgets import QFormLayout, QDialog, QLineEdit, QComboBox, QPushButton
import globaldata
from item import HostGraphicItem


class SetSimtimeWindow(QDialog):

    def __init__(self, parent=None):
        QDialog.__init__(self)
        layout = QFormLayout()

        self.time_input = QLineEdit()
        self.time_input.setText("1.5")
        self.type_combo = QComboBox()
        self.type_combo.addItems(["Udp", "Tcp", "Rdma", "Tsn", "Dds"])

        layout.addRow("时间:", self.time_input)
        layout.addRow("网络类型:", self.type_combo)

        submit_button = QPushButton("确定")
        submit_button.clicked.connect(self.apply_time)
        layout.addRow(submit_button)

        self.setLayout(layout)
        self.setWindowTitle("设置仿真时间")
        self.hide()

    def apply_time(self):
        time = float(self.time_input.text())
        project = globaldata.currentProjectInfo.fullname
        # 修改仿真时间
        # alterSimTime(project+'/Parameters.ini', time)
        print("开始仿真\n \t仿真工程:{project}\n \t仿真时间:{time}")
        # 生成NED和INI文件
        self.generateNED()
        self.generateINI(time)
        # 在此启动omnet进行仿真
        # 手动填写：omnetpp的src目录所在的绝对路径
        """ TODO:修改为使用生成的Topology.ned进行仿真 """
        os_type = platform.system()
        print(project)
        if os_type == "Windows":
            omnetpp_src = "D:/study/omnetpp-6.0/samples/inet4.5/src"
            # command = 'omnet_tools\\opp_run.exe -r 0 -m -u Cmdenv -c General -n {'omnet_template'};{omnetpp_src}; -l {omnetpp_src}/INET {'omnet_template'}/omnetpp.ini"
            command = f"omnet_tools\\opp_run.exe -r 0 -m -u Cmdenv -c General -n {project};{omnetpp_src}; -l {omnetpp_src}/INET {project}/Parameters.ini"
            exit_code = os.system(command)
        # elif os_type == "Darwin":
        # elif os_type == "Linux":
        else:
            omnetpp_src = "/Users/shi/omnetpp_new/samples/inet4.5/src"
            command = f"opp_run -r 0 -m -u Cmdenv -c General -n {project}:{omnetpp_src} -l {omnetpp_src}/INET {project}/Parameters.ini"
            exit_code = os.system(command)
        print("仿真完毕！！！！！！！")

        self.hide()

    # 在当前工程（globaldata.currentProjectInfo.path）中生成.ned文件
    def generateNED(self):
        with open(globaldata.currentProjectInfo.path + "Topology.ned", "w") as f:
            if self.type_combo.currentText() == "Udp":
                f.write("import inet.networks.base.WiredNetworkBase;\n")
                f.write("import inet.node.inet.StandardHost;\n")
                f.write("import inet.node.ethernet.EthernetSwitch;\n\n")
                f.write("network TargetNetwork extends WiredNetworkBase\n")
                f.write("{\n")
            if self.type_combo.currentText() == "Tsn":
                f.write("import inet.networks.base.TsnNetworkBase;\n")
                f.write("import inet.node.contract.IEthernetNetworkNode;\n")
                f.write("import inet.node.ethernet.EthernetLink;\n")
                f.write("network TargetNetwork extends TsnNetworkBase\n")
                f.write("{\n")
                f.write("parameters:")
                f.write("*.eth[*].bitrate = default(100Mbps);")
            if self.type_combo.currentText() == "Tcp":
                f.write("import inet.common.misc.ThruputMeteringChannel;\n")
                f.write(
                    "import inet.networklayer.configurator.ipv4.Ipv4NetworkConfigurator;\n"
                )
                f.write("import inet.node.ethernet.EthernetSwitch;\n")
                f.write("import inet.node.inet.StandardHost;\n")
                f.write("import inet.node.ethernet.Eth100M;\n")
                f.write("network TargetNetwork\n")
                f.write("{\n")
                f.write("    parameters:\n")
                f.write("    types:\n")
            if self.type_combo.currentText() == "Dds":
                f.write("import inet.networks.base.WiredNetworkBase;\n")
                f.write("import inet.node.ethernet.Eth100M;\n")
                f.write("import inet.node.inet.DDSStandardHost;\n")
                f.write("import inet.node.inet.StandardHost;\n")
                f.write("import inet.node.ethernet.EthernetSwitch;\n")
                f.write("network TargetNetwork extends WiredNetworkBase\n")
                f.write("{\n")
            f.write("    submodules:\n")
            if self.type_combo.currentText() == "Tcp":
                f.write("configurator: Ipv4NetworkConfigurator {}\n")

            for i, host in enumerate(globaldata.hostList):
                host.hostAttr.generateNED(f)
            for i, switch in enumerate(globaldata.switchList):
                switch.switchAttr.generateNED(f)

            f.write("    connections:\n")
            for i, link in enumerate(globaldata.linkList):
                linkAttr = link.linkAttr
                # end1Attr, end2Attr
                # 判断两端的类型，host/switch
                if isinstance(linkAttr.endpoint1, HostGraphicItem):
                    end1Attr = (linkAttr.endpoint1).hostAttr
                else:
                    end1Attr = (linkAttr.endpoint1).switchAttr
                if isinstance(linkAttr.endpoint2, HostGraphicItem):
                    end2Attr = (linkAttr.endpoint2).hostAttr
                else:
                    end2Attr = (linkAttr.endpoint2).switchAttr
                f.write(
                    f"        {end1Attr.name}.ethg++ <--> {{ datarate={linkAttr.link_bandwidth}Mbps;}} <--> {end2Attr.name}.ethg++;\n"
                )

            f.write("}\n")
        return

    # 在当前工程（globaldata.currentProjectInfo.path）中生成.ini文件
    def generateINI(self, time):
        with open(globaldata.currentProjectInfo.path + "Parameters.ini", "w") as f:
            f.write("[General]\n")
            f.write("network = TargetNetwork\n")
            f.write(f"sim-time-limit = {time}s\n")
            f.write("\n")
            if self.type_combo.currentText() == "Tcp":
                self.generateTcpHeader(f)
            if self.type_combo.currentText() == "Dds":
                f.write(
                    "*.configurator.config = xml(\"<config><interface hosts='**' address='192.x.x.x' netmask='255.x.x.x'/></config>\")\n"
                )
            # TODO: 考虑source向多个destinations发包
            for i, host in enumerate(globaldata.hostList):
                # hostAttr = host.hostAttr
                # if hostAttr.destination_host == '':
                # continue
                print("generateINI")
                host.hostAttr.generateINI(f)

            for i, switch in enumerate(globaldata.switchList):
                switchAttr = switch.switchAttr
                f.write(f'*.{switchAttr.name}.ethernet.typename = "EthernetLayer"\n')
                f.write(
                    f'*.{switchAttr.name}.eth[*].typename = "LayeredEthernetInterface"\n'
                )
                f.write(
                    f"*.{switchAttr.name}.eth[*].bitrate = {switchAttr.transmission_rate}Mbps\n"
                )
                switchAttr.generateINI(f)
            f.write("\n")
        return

    def generateTcpHeader(self, f):
        data = globaldata.networkGlobalConfig["Tcp"]
        f.write(f'**.forwarding = {data["forwarding"]}\n')
        f.write(f'**.arp.retryTimeout = {data["retryTimeout"]}\n')
        f.write(f'**.arp.retryCount = {data["retryCount"]}\n')
        f.write(f'**.arp.cacheTimeout = {data["cacheTimeout"]}\n')
        f.write(f'**.eth[*].queue.typename = "{data["queueTypename"]}"\n')
        f.write(f'**.eth[*].queue.packetCapacity = {data["queuePacketCapacity"]}\n')
        f.write(f'**.tcp.tcpAlgorithmClass = "{data["tcpAlgorithmClass"]}"\n')
        f.write('**.tcp.typename = "Tcp"\n')
        f.write("**.tcp.advertisedWindow = 65535\n")
        f.write("**.tcp.delayedAcksEnabled = false\n")
        f.write("**.tcp.nagleEnabled = true\n")
        f.write("**.tcp.limitedTransmitEnabled = false\n")
        f.write("**.tcp.increasedIWEnabled = false\n")
        f.write("**.tcp.sackSupport = false\n")
        f.write("**.tcp.windowScalingSupport = false\n")
        f.write("**.tcp.timestampSupport = false\n")
        f.write("**.tcp.mss = 1452\n")
