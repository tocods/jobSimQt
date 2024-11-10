import os
import platform
from qdarktheme.qtpy.QtWidgets import (
    QFormLayout,
    QDialog,
    QLineEdit,
    QComboBox,
    QPushButton,
)
import globaldata
from item import HostGraphicItem


class SetSimtimeWindow(QDialog):

    def __init__(self, parent=None):
        QDialog.__init__(self)
        layout = QFormLayout()

        self.time_input = QLineEdit()
        self.time_input.setText("1.5")
        self.type_combo = QComboBox()
        self.type_combo.addItems(["通用", "RDMA"])

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
        project = globaldata.currentProjectInfo.path
        print(f"开始仿真\n 仿真时间:{time}")

        self.generateNED()
        self.generateINI(time)
        os_type = platform.system()
        print(project)
        if os_type == "Windows":
            omnetpp_src = "D:/omnetpp-6.0/samples/inet4.5/src"
            command = f"omnet_tools\\opp_run.exe -r 0 -m -u Cmdenv -c General -n {project};{omnetpp_src}; -l {omnetpp_src}/INET {project}/Parameters.ini"
            exit_code = os.system(command)
            print(f"仿真完毕 exit_code:{exit_code}")
        else:
            omnetpp_src = "/Users/shi/omnetpp_new/samples/inet4.5/src"
            command = f"opp_run -r 0 -m -u Cmdenv -c General -n {project}:{omnetpp_src} -l {omnetpp_src}/INET {project}/Parameters.ini"
            exit_code = os.system(command)
            print(f"仿真完毕 exit_code:{exit_code}")
        self.hide()

    # 在当前工程（globaldata.currentProjectInfo.path）中生成.ned文件
    def generateNED(self):
        with open(
            os.path.join(globaldata.currentProjectInfo.path, "Topology.ned"), "w"
        ) as f:
            self.generateNEDHeader(f)
            for host in globaldata.hostList:
                host.hostAttr.generateNED(f)
            for switch in globaldata.switchList:
                switch.switchAttr.generateNED(f)

            f.write("    connections:\n")
            for link in globaldata.linkList:
                linkAttr = link.linkAttr
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

    def generateNEDHeader(self, f):
        f.write(
            f"import inet.linklayer.configurator.gatescheduling.contract.IGateScheduleConfigurator;\n"
        )
        f.write(
            f"import inet.networklayer.configurator.contract.INetworkConfigurator;\n"
        )
        f.write(f"import inet.node.tsn.TsnDevice;\n")
        f.write(f"import inet.node.tsn.TsnSwitch;\n")
        f.write(f"import inet.networks.base.WiredNetworkBase;\n")
        f.write(f"import inet.node.contract.IEthernetNetworkNode;\n")
        f.write(f"import inet.node.ethernet.EthernetLink;\n")
        f.write(f"import inet.node.ethernet.Eth100M;\n")
        f.write(f"import inet.node.inet.StandardHost;\n")
        f.write(f"import inet.node.ethernet.EthernetSwitch;\n")
        f.write(f"import inet.node.inet.DDSStandardHost;\n")
        f.write(f'network TargetNetwork extends WiredNetworkBase\n')
        f.write(f'{"{"}\n')
        f.write('    submodules:\n')

    def generateINI(self, time):
        with open(
            os.path.join(globaldata.currentProjectInfo.path, "Parameters.ini"), "w"
        ) as f:
            self.generateINIHeader(f, time)
            for host in globaldata.hostList:
                host.hostAttr.generateINI(f)
            for switch in globaldata.switchList:
                switch.switchAttr.generateINI(f)
            f.write("\n")
        return

    def generateINIHeader(self, f, time):
        f.write("[General]\n")
        f.write("network = TargetNetwork\n")
        f.write(f"sim-time-limit = {time}s\n")
        f.write("\n")
        f.write(f'*.*.ethernet.typename = "EthernetLayer"\n')
        f.write(f'*.*.eth[*].typename = "LayeredEthernetInterface"\n')
        f.write(f'*.*.eth[*].bitrate = 100Mbps\n')
        data = globaldata.networkGlobalConfig["common"]
        f.write(f'**.eth[*].queue.typename = "{data["queueTypename"]}"\n')
        f.write(f'**.eth[*].queue.packetCapacity = {data["queuePacketCapacity"]}\n')
        self.generateTcpINIHeader(f)
        self.generateDdsINIHeader(f)
        # self.generateRdmaINIHeader(f)

    def generateTcpINIHeader(self, f):
        data = globaldata.networkGlobalConfig["Tcp"]
        f.write(f'**.forwarding = {data["forwarding"]}\n')
        f.write(f'**.arp.retryTimeout = {data["retryTimeout"]}\n')
        f.write(f'**.arp.retryCount = {data["retryCount"]}\n')
        f.write(f'**.arp.cacheTimeout = {data["cacheTimeout"]}\n')
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

    def generateDdsINIHeader(self, f):
        f.write(
            "*.configurator.config = xml(\"<config><interface hosts='**' address='192.x.x.x' netmask='255.x.x.x'/></config>\")\n"
        )

    def generateRdmaINIHeader(self, f):
        f.write('*.*.llc.typename = ""\n')
        f.write('*.*.bridging.typename = "BridgingLayer"\n')
        f.write('*.*.bridging.macTableModule = ""\n')
        f.write("*.switch*.bridging.directionReverser.reverser.forwardVlan = true\n")
        f.write("*.switch*.bridging.directionReverser.reverser.forwardPcp = true\n")
        f.write('*.host*.bridging.directionReverser.typename = ""\n')
        f.write('*.host*.bridging.interfaceRelay.typename = ""\n')
        f.write('*.*.ieee8021q.typename = "Ieee8021qProtocol"\n')
        f.write('*.*.bridging.vlanPolicy.typename = "VlanPolicyLayer"\n')
        f.write(
            '*.*.bridging.vlanPolicy.inboundFilter.acceptedVlanIds = {"*" : [42]}\n'
        )
        f.write(
            '*.*.bridging.vlanPolicy.outboundFilter.acceptedVlanIds = {"*" : [42]}\n'
        )
        f.write('*.*.eth[*].macLayer.queue.typename = "Ieee8021qTimeAwareShaper"\n')
        f.write("*.*.eth[*].macLayer.queue.numTrafficClasses = 8\n")
        f.write('*.*.eth[*].macLayer.queue.transmissionGate[*] = ""\n')
        f.write(
            '*.*.eth[*].macLayer.queue.transmissionSelectionAlgorithm[*] = "QbbGate"\n'
        )
        f.write("*.host*.eth[*].macLayer.queue.queue[*].dataCapacity = 16384\n")
        f.write(
            '*.switch*.eth[*].macLayer.queue.queue[*].typename  = "RedDropperQueue"\n'
        )
        f.write("*.switch*.eth[*].macLayer.queue.queue[*].red.useEcn         = true\n")
        f.write("*.switch*.eth[*].macLayer.queue.queue[*].red.wq             = 1.0\n")
        f.write("*.switch*.eth[*].macLayer.queue.queue[*].red.minth          = 0\n")
        f.write("*.switch*.eth[*].macLayer.queue.queue[*].red.maxth          = 6\n")
        f.write("*.switch*.eth[*].macLayer.queue.queue[*].red.maxp           = 1.0\n")
        f.write(
            "*.switch*.eth[*].macLayer.queue.queue[*].red.pkrate         = 833.3333\n"
        )
        f.write("*.switch*.eth[*].macLayer.queue.queue[*].red.packetCapacity = 500\n")
        f.write("*.switch*.eth[*].macLayer.queue.queue[*].fifo.dataCapacity = 16384\n")
