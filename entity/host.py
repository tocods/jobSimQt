from entity.network_device import NetworkDevice
import json


# Host类继承自NetworkDevice
class Host(NetworkDevice):
    def __init__(self, name, host_type="StandardHost"):
        super().__init__(name, host_type)
        # 网络属性，初始化为默认值
        self.numApps = 0
        self.appArgs = []
        # self.typename = "UdpSourceApp"
        # self.total_traffic = 1000
        # self.packet_size = 100
        # self.packet_interval = 100
        # self.destination_host = ""
        self.ip = "0.0.0.0"
        self.type = host_type
        self.only_cpu = True

        print(f"Host name:{name} host_type:{host_type} created")

    def generateINI(self, f):
        print("no impl")

    def generateNED(self, f):
        f.write(f"        {self.name}: {self.type} {{\n")
        f.write("        }\n")

    def setXMLElement(self, element):
        return super().setXMLElement(element)

    def readXMLElement(self, element):
        return super().readXMLElement(element)


class UdpHost(Host):
    def __init__(self, name):
        super().__init__(name, "StandardHost")

    def generateINI(self, f):
        f.write(f"*.{self.name}.numApps = {len(self.appArgs)}\n")
        for index in range(0, len(self.appArgs)):
            appArg = self.appArgs[index]
            if appArg["typename"] == "UdpSourceApp":
                f.write(
                    f'*.{self.name}.app[{index}].typename = "{appArg["typename"]}"\n'
                )
                f.write(
                    f'*.{self.name}.app[{index}].source.packetLength = {appArg["packetLength"]}\n'
                )
                f.write(
                    f'*.{self.name}.app[{index}].source.productionInterval = exponential({appArg["productionInterval"]})\n'
                )
                f.write(
                    f'*.{self.name}.app[{index}].io.destAddress = "{appArg["destAddress"]}"\n'
                )
                f.write(
                    f'*.{self.name}.app[{index}].io.destPort = {appArg["destPort"]}\n'
                )
            if appArg["typename"] == "UdpSinkApp":
                f.write(
                    f'*.{self.name}.app[{index}].typename = "{appArg["typename"]}"\n'
                )
                f.write(
                    f'*.{self.name}.app[{index}].io.localPort = {appArg["localPort"]}\n'
                )
            f.write("\n")

    def generateNED(self, f):
        f.write(f"        {self.name}: {self.type} {{\n")
        f.write("        }\n")

    def setXMLElement(self, element):
        element.set("name", self.name)
        element.set("type", self.type)
        element.set("ip", self.ip)
        element.set("numApps", str(self.numApps))
        element.set("appArgs", json.dumps(self.appArgs))
        element.set("only_cpu", str(self.only_cpu))

    def readXMLElement(self, element):
        self.ip = element.get("ip")
        self.numApps = int(element.get("numApps"))
        self.appArgs = json.loads(element.get("appArgs"))


class TcpHost(Host):
    def __init__(self, name):
        super().__init__(name, "StandardHost")

    def generateINI(self, f):
        f.write(f"*.{self.name}.numApps = {len(self.appArgs)}\n")
        for index in range(0, len(self.appArgs)):
            appArg = self.appArgs[index]
            if appArg["typename"] == "TcpSessionApp":
                f.write(
                    f'*.{self.name}.app[{index}].typename = "{appArg["typename"]}"\n'
                )
                f.write(
                    f'*.{self.name}.app[{index}].sendBytes = {appArg["sendBytes"]}\n'
                )
                f.write(f"*.{self.name}.app[{index}].active = true\n")
                f.write(
                    f'*.{self.name}.app[{index}].localPort = {appArg["localPort"]}\n'
                )
                f.write(
                    f'*.{self.name}.app[{index}].connectAddress = "{appArg["connectAddress"]}"\n'
                )
                f.write(
                    f'*.{self.name}.app[{index}].connectPort = {appArg["connectPort"]}\n'
                )
                f.write(f"*.{self.name}.app[{index}].tOpen = 0s\n")
                f.write(f"*.{self.name}.app[{index}].tSend = 0s\n")
                f.write(f"*.{self.name}.app[{index}].tClose = 0s\n")
                f.write(f'*.{self.name}.app[{index}].sendScript = ""\n')
            if appArg["typename"] == "TcpSinkApp":
                f.write(
                    f'*.{self.name}.app[{index}].typename = "{appArg["typename"]}"\n'
                )
                f.write(
                    f'*.{self.name}.app[{index}].localPort = {appArg["localPort"]}\n'
                )
            f.write("\n")

    def generateNED(self, f):
        f.write(f"        {self.name}: {self.type} {{\n")
        f.write("        }\n")

    def setXMLElement(self, element):
        element.set("name", self.name)
        element.set("type", self.type)
        element.set("ip", self.ip)
        element.set("numApps", str(self.numApps))
        element.set("appArgs", json.dumps(self.appArgs))
        element.set("only_cpu", str(self.only_cpu))

    def readXMLElement(self, element):
        self.ip = element.get("ip")
        self.numApps = int(element.get("numApps"))
        self.appArgs = json.loads(element.get("appArgs"))


# 不同类型的Host类
class RdmaHost(Host):
    def __init__(self, name):
        super().__init__(name, "StandardHost")

    def generateINI(self, f):
        return super().generateINI(f)


class TsnHost(Host):
    def __init__(self, name):
        super().__init__(name, "StandardHost")

        # tsn
        self.tsnArgs = []

    def generateINI(self, f):
        f.write(f"*.{self.name}.numApps = {len(self.appArgs)}\n")
        for index in range(0, len(self.appArgs)):
            appArg = self.appArgs[index]
            if appArg["typename"] == "UdpSourceApp":
                f.write(
                    f'*.{self.name}.app[{index}].typename = "{appArg["typename"]}"\n'
                )
                f.write(
                    f'*.{self.name}.app[{index}].source.packetLength = {appArg["packetLength"]}\n'
                )
                f.write(
                    f'*.{self.name}.app[{index}].source.productionInterval = exponential({appArg["productionInterval"]})\n'
                )
                f.write(
                    f'*.{self.name}.app[{index}].io.destAddress = "{appArg["destAddress"]}"\n'
                )
                f.write(
                    f'*.{self.name}.app[{index}].io.destPort = {appArg["destPort"]}\n'
                )
            if appArg["typename"] == "UdpSinkApp":
                f.write(
                    f'*.{self.name}.app[{index}].typename = "{appArg["typename"]}"\n'
                )
                f.write(
                    f'*.{self.name}.app[{index}].io.localPort = {appArg["localPort"]}\n'
                )

            f.write(f"*.{self.name}.hasOutgoingStreams = true\n")
            if len(self.tsnArgs) != 0:
                f.write(
                    f"*.{self.name}.bridging.streamIdentifier.identifier.mapping = ["
                )
                for index in range(0, len(self.tsnArgs)):
                    tmp = self.tsnArgs[index]
                    f.write("{")
                    f.write(f'stream: "{tmp["stream"]}", ')
                    f.write(f'packetfilter: {tmp["packetFilter"]}')
                    f.write("}")
                    if index < len(self.tsnArgs) - 1:
                        f.write(",")
                f.write("]\n")
            if self.tsnArgs != "":
                f.write(f"*.{self.name}.bridging.streamCoder.encoder.mapping = [")
                for index in range(0, len(self.tsnArgs)):
                    tmp = self.tsnArgs[index]
                    f.write("{")
                    f.write(f'stream: "{tmp["stream"]}", ')
                    f.write(f'pcp: {tmp["pcp"]}')
                    f.write("}")
                    if index < len(self.tsnArgs) - 1:
                        f.write(",")
                f.write("]\n")
            f.write("\n")

    def generateNED(self, f):
        f.write(
            f'        {self.name}: <default("TsnDevice")> like IEthernetNetworkNode {{\n'
        )
        f.write("        }\n")

    def setXMLElement(self, element):
        element.set("name", self.name)
        element.set("type", self.type)
        element.set("ip", self.ip)
        element.set("numApps", str(self.numApps))
        element.set("appArgs", json.dumps(self.appArgs))
        element.set("tsnArgs", json.dumps(self.tsnArgs))
        element.set("only_cpu", str(self.only_cpu))

    def readXMLElement(self, element):
        self.ip = element.get("ip")
        self.numApps = int(element.get("numApps"))
        print(element.get("appArgs"))
        self.appArgs = json.loads(element.get("appArgs"))
        print(element.get("tsnArgs"))
        self.tsnArgs = json.loads(element.get("tsnArgs"))


class DdsHost(Host):
    def __init__(self, name):
        super().__init__(name, "DDSStandardHost")

    def generateINI(self, f):
        f.write(f"*.{self.name}.numApps = {len(self.appArgs)}\n")
        for index in range(0, len(self.appArgs)):
            appArg = self.appArgs[index]
            if appArg["typename"] == "DDSPublishApp":
                f.write(
                    f'*.{self.name}.app[{index}].typename = "{appArg["typename"]}"\n'
                )
                f.write(f"*.{self.name}.app[{index}].io.receiveBroadcast = true\n")
                f.write(f"*.{self.name}.ipv4.ip.limitedBroadcast = true\n")
                f.write(f'*.{self.name}.app[{index}].sink.typename = ""\n')
                f.write(
                    f'*.{self.name}.app[{index}].io.publish = "{appArg["publish"]}"\n'
                )
                f.write(
                    f'*.{self.name}.app[{index}].io.destPort = {appArg["destPort"]}\n'
                )
                f.write(
                    f'*.{self.name}.app[{index}].source.packetLength = {appArg["packetLength"]}\n'
                )
                f.write(
                    f'*.{self.name}.app[{index}].source.productionInterval = exponential({appArg["productionInterval"]})\n'
                )

            if appArg["typename"] == "DDSSubscribeApp":
                f.write(
                    f'*.{self.name}.app[{index}].typename = "{appArg["typename"]}"\n'
                )
                f.write(
                    f'*.{self.name}.app[{index}].io.localPort = {appArg["localPort"]}\n'
                )
                f.write(
                    f'*.{self.name}.app[{index}].source.subscribe = "{appArg["subscribeTopic"] + "@" + appArg["subscribePort"]}"\n'
                )
                f.write(f"*.{self.name}.app[{index}].source.packetLength = 20B\n")
                f.write(f"*.{self.name}.ipv4.ip.limitedBroadcast = true \n")
                f.write(f'*.{self.name}.app[{index}].sink.flowName = "{appArg["flowName"]}"\n')
            f.write("\n")

    def generateNED(self, f):
        f.write(f"        {self.name}: {self.type} {{\n")
        f.write("        }\n")

    def setXMLElement(self, element):
        element.set("name", self.name)
        element.set("type", self.type)
        element.set("ip", self.ip)
        element.set("numApps", str(self.numApps))
        element.set("appArgs", json.dumps(self.appArgs))
        element.set("only_cpu", str(self.only_cpu))

    def readXMLElement(self, element):
        self.ip = element.get("ip")
        self.numApps = int(element.get("numApps"))
        self.appArgs = json.loads(element.get("appArgs"))
