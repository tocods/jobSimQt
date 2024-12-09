from entity.network_device import NetworkDevice
import json
import globaldata


# Switch类继承自NetworkDevice
class Switch(NetworkDevice):
    def __init__(self, name, switch_type="EthernetSwitch"):
        super().__init__(name, switch_type)
        # 交换机属性，初始化为默认值
        self.num_ports = 1
        self.cur_port = 0
        self.transmission_rate = 100
        self.transmission_rate_list = "100,100,100,100,100,100,100,100"
        self.port_buffer_size = 100
        self.tsn_queue = []

        print(f"Switch name:{name} host_type:{switch_type} created")

    def getAttr(self):
        result = {
            "name": self.name,
            "transmission_rate_list": self.transmission_rate_list
        }
        return result
    
    def applyAttr(self, data):
        self.set_name(data["name"])
        self.transmission_rate_list = data["transmission_rate_list"]

    def getTsnQueue(self):
        return self.tsn_queue
    
    def setTsnQueue(self, tsn_queue):
        self.tsn_queue = tsn_queue

    def setXMLElement(self, element):
        element.set("name", self.name)
        element.set("type", self.type)
        element.set("num_ports", str(self.num_ports))
        element.set("transmission_rate", str(self.transmission_rate))
        element.set("port_buffer_size", str(self.port_buffer_size))
        element.set("transmission_rate_list", str(self.transmission_rate_list))

    def generateINI(self, f):
        f.write(f'*.{self.name}.eth[*].bitrate = {self.transmission_rate}Mbps\n')
        l = self.transmission_rate_list.split(",")
        for i in range(0, self.cur_port):
            if i < len(l):
                f.write(f'*.{self.name}.eth[{i}].bitrate = {l[i]}Mbps\n')
            else:
                f.write(f'*.{self.name}.eth[{i}].bitrate = 100Mbps\n')
        return

    def generateNED(self, f):
        f.write(f"        {self.name}: {self.type} {{\n")
        f.write(f"              gates:")
        f.write(f"                   ethg[{self.cur_port}];")
        f.write("        }\n")


class NormalSwitch(Switch):
    def __init__(self, name):
        super().__init__(name, "EthernetSwitch")

    def setXMLElement(self, element):
        return super().setXMLElement(element)

    def readXMLElement(self, element):
        return super().readXMLElement(element)

    def generateNED(self, f):
        return super().generateNED(f)


class UdpSwitch(Switch):
    def __init__(self, name):
        super().__init__(name, "EthernetSwitch")

    def setXMLElement(self, element):
        return super().setXMLElement(element)

    def readXMLElement(self, element):
        return super().readXMLElement(element)

    def generateNED(self, f):
        return super().generateNED(f)


class TcpSwitch(Switch):
    def __init__(self, name):
        super().__init__(name, "EthernetSwitch")

    def setXMLElement(self, element):
        return super().setXMLElement(element)

    def readXMLElement(self, element):
        return super().readXMLElement(element)

    def generateNED(self, f):
        return super().generateNED(f)


# 不同类型的Switch类
class RdmaSwitch(Switch):
    def __init__(self, name):
        super().__init__(name, "RoceSwitch")

    def generateINI(self, f):
        conf = globaldata.networkGlobalConfig["Rdma"]
        f.write(f'*.{self.name}.eth[*].bitrate = {self.transmission_rate}Mbps\n')
        f.write(f'*.{self.name}.eth[*].macLayer.queue.queue[*].red.wq = {conf["wq"]}\n')
        f.write(f'*.{self.name}.eth[*].macLayer.queue.queue[*].red.minth = {conf["minth"]}\n')
        f.write(f'*.{self.name}.eth[*].macLayer.queue.queue[*].red.maxth = {conf["maxth"]}\n')
        f.write(f'*.{self.name}.eth[*].macLayer.queue.queue[*].red.maxp = {conf["maxp"]}\n')
        f.write(f'*.{self.name}.eth[*].macLayer.queue.queue[*].red.pkrate = {conf["pkrate"]}\n')
        


class TsnSwitch(Switch):
    def __init__(self, name):
        super().__init__(name, "EthernetSwitch")

    def setXMLElement(self, element):
        element.set("name", self.name)
        element.set("type", self.type)
        element.set("num_ports", str(self.num_ports))
        element.set("transmission_rate", str(self.transmission_rate))
        element.set("port_buffer_size", str(self.port_buffer_size))
        element.set("tsn_queue", json.dumps(self.tsn_queue))

    def readXMLElement(self, element):
        self.num_ports = int(element.get("num_ports"))
        self.transmission_rate = int(element.get("transmission_rate"))
        self.port_buffer_size = int(element.get("port_buffer_size"))
        self.tsn_queue = json.loads(element.get("tsn_queue"))

    def generateINI(self, f):
        f.write(f'*.{self.name}.eth[*].bitrate = {self.transmission_rate}Mbps\n')
        f.write(f"*.{self.name}.hasEgressTrafficShaping = true\n")
        f.write(
            f'*.{self.name}.bridging.directionReverser.reverser.excludeEncapsulationProtocols = ["ieee8021qctag"]\n'
        )
        f.write(
            f"*.{self.name}.eth[*].macLayer.queue.numTrafficClasses = {len(self.tsn_queue)}\n"
        )
        for index in range(0, len(self.tsn_queue)):
            queue = self.tsn_queue[index]
            f.write(
                f'*.{self.name}.eth[*].macLayer.queue.*[{index}].display-name = "{queue["display-name"]}"\n'
            )
            f.write(
                f'*.{self.name}.eth[*].macLayer.queue.transmissionGate[{index}].offset = {queue["offset"]}\n'
            )
            f.write(
                f'*.{self.name}.eth[*].macLayer.queue.transmissionGate[{index}].durations = {queue["durations"]}\n'
            )
            f.write(
                f'*.{self.name}.eth[*].macLayer.queue.transmissionGate[{index}].initiallyOpen = {queue["initiallyOpen"]}\n'
            )
            f.write(
                f'*.{self.name}.eth[*].macLayer.queue.queue[{index}].packetCapacity = {queue["packetCapacity"]}\n'
            )
        f.write("\n")
        return

    def generateNED(self, f):
        f.write(
            f'        {self.name}: <default("TsnSwitch")> like IEthernetNetworkNode {{\n'
        )
        f.write("        }\n")


class DdsSwitch(Switch):
    def __init__(self, name):
        super().__init__(name, "EthernetSwitch")

    def setXMLElement(self, element):
        return super().setXMLElement(element)

    def readXMLElement(self, element):
        return super().readXMLElement(element)

    def generateNED(self, f):
        return super().generateNED(f)
