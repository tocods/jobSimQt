from entity.network_device import NetworkDevice
import json
import globaldata


# Host类继承自NetworkDevice
class Host(NetworkDevice):
    def __init__(self, name, host_type="StandardHost"):
        super().__init__(name, host_type)
        self.numApps = 0
        self.appArgs = []
        self.ip = "0.0.0.0"
        self.mac = "00:1A:2B:3C:4D:5E"
        self.packet_size = "100"
        self.packet_interval = "100"
        self.total_traffic = "1000"
        self.type = host_type
        self.only_cpu = True

        print(f"Host name:{name} host_type:{host_type} created")

    def getPhysicsAttr(self):
        result = {
            "name": self.name,
            "ip": self.ip,
            "mac": self.mac,
            "packet_size": self.packet_size,
            "packet_interval": self.packet_interval,
        }

        return result

    def applyPhysicsAttr(self, data):
        self.set_name(data["name"])
        self.ip = data["ip"]
        self.mac = data["mac"]
        self.packet_size = data["packet_size"]
        self.packet_interval = data["packet_interval"]

    def generateINI(self, f):
        tmp = self.appArgs.copy()
        nonTsnAppList = []
        for index, app in enumerate(self.appArgs):
            if app["typename"] != "TSN":
                nonTsnAppList.append(app)
        self.numApps = len(nonTsnAppList)
        self.appArgs = nonTsnAppList
        f.write(f"*.{self.name}.numApps = {self.numApps}\n")
        for index in range(0, len(self.appArgs)):
            appArg = self.appArgs[index]
            if appArg["typename"] == "UdpApp615":
                self.generateINIUdp(f, index)
            if appArg["typename"] == "TcpSessionApp":
                self.generateINITcpSource(f, index)
            if appArg["typename"] == "TcpSinkApp":
                self.generateINITcpSink(f, index)
            if appArg["typename"] == "DDSPublishApp":
                self.generateINIDdsSource(f, index)
            if appArg["typename"] == "DDSSubscribeApp":
                self.generateINIDdsSink(f, index)
            f.write("\n")
        
        self.appArgs = tmp

    def getNumber(self, s: str):
        i = 0
        while i < len(s):
            if not str(s[i]).isdigit():
                break
            i = i + 1

        return s[:i]

    def generateINIUdp(self, f, index):
        appArg = self.appArgs[index]
        if len(appArg) > 3:
            f.write(f'*.{self.name}.app[{index}].typename = "{appArg["typename"]}"\n')
            f.write(
                f'*.{self.name}.app[{index}].source.packetLength = {appArg["packetLength"]}\n'
            )
            f.write(
                f'*.{self.name}.app[{index}].source.productionInterval = exponential({appArg["productionInterval"]})\n'
            )
            f.write(
                f'*.{self.name}.app[{index}].io.destAddress = "{appArg["destAddress"]}"\n'
            )
            f.write(f'*.{self.name}.app[{index}].io.destPort = {appArg["destPort"]}\n')
            f.write(f'*.{self.name}.app[{index}].sink.typename = ""\n')
        else:
            f.write(f'*.{self.name}.app[{index}].typename = "{appArg["typename"]}"\n')

            f.write(f'*.{self.name}.app[{index}].source.typename = ""\n')
            f.write(f"*.{self.name}.app[{index}].io.destPort = {-1}\n")
            f.write(
                f'*.{self.name}.app[{index}].io.localPort = {appArg["localPort"]}\n'
            )
            f.write(
                f'*.{self.name}.app[{index}].sink.flowName = "{appArg["flowName"]}"\n'
            )

    def generateINITcpSource(self, f, index):
        appArg = self.appArgs[index]
        f.write(f'*.{self.name}.app[{index}].typename = "{appArg["typename"]}"\n')
        f.write(f'*.{self.name}.app[{index}].sendBytes = {appArg["sendBytes"]}\n')
        f.write(f"*.{self.name}.app[{index}].active = true\n")
        f.write(f'*.{self.name}.app[{index}].localPort = {appArg["localPort"]}\n')
        f.write(
            f'*.{self.name}.app[{index}].connectAddress = "{appArg["connectAddress"]}"\n'
        )
        f.write(f'*.{self.name}.app[{index}].connectPort = {appArg["connectPort"]}\n')
        f.write(f"*.{self.name}.app[{index}].tOpen = 0s\n")
        f.write(f"*.{self.name}.app[{index}].tSend = 0s\n")
        f.write(f"*.{self.name}.app[{index}].tClose = 0s\n")
        f.write(f'*.{self.name}.app[{index}].sendScript = ""\n')

    def generateINITcpSink(self, f, index):
        appArg = self.appArgs[index]
        f.write(f'*.{self.name}.app[{index}].typename = "{appArg["typename"]}"\n')
        f.write(f'*.{self.name}.app[{index}].localPort = {appArg["localPort"]}\n')
        f.write(f'*.{self.name}.app[{index}].flowName = "{appArg["flowName"]}"\n')

    def generateINIDdsSource(self, f, index):
        appArg = self.appArgs[index]
        f.write(f'*.{self.name}.app[{index}].typename = "{appArg["typename"]}"\n')
        f.write(f"*.{self.name}.app[{index}].io.receiveBroadcast = true\n")
        f.write(f'*.{self.name}.app[{index}].io.publish = "{appArg["publish"]}"\n')
        f.write(f'*.{self.name}.app[{index}].io.destPort = {appArg["destPort"]}\n')
        f.write(
            f'*.{self.name}.app[{index}].io.historyCacheLength = {appArg["historyCacheLength"]}\n'
        )
        f.write(f"*.{self.name}.ipv4.ip.limitedBroadcast = true\n")

        f.write(
            f'*.{self.name}.app[{index}].source.packetLength = {appArg["packetLength"]}\n'
        )
        f.write(
            f'*.{self.name}.app[{index}].source.productionInterval = exponential({appArg["productionInterval"]})\n'
        )
        f.write(f'*.{self.name}.app[{index}].sink.typename = ""\n')

    def generateINIDdsSink(self, f, index):
        appArg = self.appArgs[index]
        f.write(f'*.{self.name}.app[{index}].typename = "{appArg["typename"]}"\n')
        f.write(
            f'*.{self.name}.app[{index}].source.subscribe = "{appArg["subscribeTopic"] + "@" + appArg["subscribePort"]}"\n'
        )
        f.write(f'*.{self.name}.app[{index}].io.localPort = {appArg["localPort"]}\n')
        f.write(
            f'*.{self.name}.app[{index}].io.receiverBufferLength = {appArg["receiverBufferLength"]}\n'
        )
        f.write(
            f'*.{self.name}.app[{index}].io.nackCountdown = {appArg["nackCountdown"]}\n'
        )
        f.write(f"*.{self.name}.app[{index}].source.packetLength = 20B\n")
        f.write(f"*.{self.name}.ipv4.ip.limitedBroadcast = true \n")
        f.write(f'*.{self.name}.app[{index}].sink.flowName = "{appArg["flowName"]}"\n')

    def generateNED(self, f):
        f.write(f"        {self.name}: {self.type} {{\n")
        f.write("        }\n")

    def setXMLElement(self, element):
        # for appArg in self.appArgs:
        #     if appArg["typename"] == "UdpApp615" and len(appArg) > 3:
        #         packet_interval = self.getNumber(appArg["productionInterval"])
        #         packet_size = self.getNumber(appArg["packetLength"])
        element.set("name", self.name)
        element.set("type", self.type)
        element.set("ip", self.ip)
        element.set("mac", self.mac)
        element.set("packet_size", self.packet_size)
        element.set("packet_interval", self.packet_interval)
        element.set("total_traffic", self.total_traffic)
        element.set("numApps", str(self.numApps))
        element.set("appArgs", json.dumps(self.appArgs))
        element.set("only_cpu", str(self.only_cpu))

    def readXMLElement(self, element):
        self.name = element.get("name")
        self.ip = element.get("ip")
        self.mac = element.get("mac")
        self.numApps = int(element.get("numApps"))
        self.appArgs = json.loads(element.get("appArgs"))
        self.packet_size = element.get("packet_size")
        self.packet_interval = element.get("packet_interval")
        self.total_traffic = element.get("total_traffic")

class NormalHost(Host):
    def __init__(self, name):
        super().__init__(name, "StandardHost")

    def generateINI(self, f):
        f.write(f"*.{self.name}.numApps = {len(self.appArgs)}\n")
        for index in range(0, len(self.appArgs)):
            appArg = self.appArgs[index]
            if appArg["typename"] == "UdpApp615":
                self.generateINIUdp(f, index)
            if appArg["typename"] == "TcpSessionApp":
                self.generateINITcpSource(f, index)
            if appArg["typename"] == "TcpSinkApp":
                self.generateINITcpSink(f, index)
            if appArg["typename"] == "DDSPublishApp":
                self.generateINIDdsSource(f, index)
            if appArg["typename"] == "DDSSubscribeApp":
                self.generateINIDdsSink(f, index)
            f.write("\n")


class UdpHost(Host):
    def __init__(self, name):
        super().__init__(name, "StandardHost")


class TcpHost(Host):
    def __init__(self, name):
        super().__init__(name, "StandardHost")


# 不同类型的Host类
class RdmaHost(Host):
    def __init__(self, name):
        super().__init__(name, "StandardHost")

        self.rdmaArgs = {
            "connectionType": "RELIABLE_CONNECTION",
            "maxSendQueueSize": "256",
            "maxRecvQueueSize": "256",
        }

    def generateINI(self, f):
        f.write(f"")
        f.write(f"*.{self.name}.numApps = {len(self.appArgs)}\n")
        for index in range(0, len(self.appArgs)):
            appArg = self.appArgs[index]
            RdmaArg = globaldata.networkGlobalConfig["Rdma"]
            f.write(
                f'*.{self.name}.rocev2.connectionType = "{RdmaArg["connectionType"]}"\n'
            )
            f.write(
                f'*.{self.name}.rocev2.maxSendQueueSize = {RdmaArg["maxSendQueueSize"]}\n'
            )
            f.write(
                f'*.{self.name}.rocev2.maxRecvQueueSize = {RdmaArg["maxRecvQueueSize"]}\n'
            )
            f.write(f'*.{self.name}.rocev2.windowSize = "{RdmaArg["windowSize"]}"\n')
            f.write(
                f'*.{self.name}.rocev2.retransmitTimeout = {RdmaArg["retransmitTimeout"]}\n'
            )
            f.write(f'*.{self.name}.rocev2.rateLimit = {RdmaArg["rateLimit"]}\n')
            f.write(f'*.{self.name}.app[{index}].typename = "{appArg["typename"]}"\n')
            f.write(
                f'*.{self.name}.app[{index}].io.localQueuePairNumber = {appArg["localQueuePairNumber"]}\n'
            )
            if len(appArg) > 2:
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
                    f'*.{self.name}.app[{index}].io.destinationQueuePairNumber = {appArg["destinationQueuePairNumber"]}\n'
                )
                f.write(f'*.{self.name}.app[{index}].io.pcp = {appArg["pcp"]}\n')
                f.write(
                    f'*.{self.name}.app[{index}].io.messageType = "{appArg["messageType"]}"\n'
                )
            else:
                f.write(f'*.{self.name}.app[{index}].source.typename = ""\n')
                f.write(
                    f'*.{self.name}.app[{index}].sink.flowName = "QPN{appArg["localQueuePairNumber"]}"\n'
                )
            f.write("\n")

    def generateNED(self, f):
        f.write(
            # f'        {self.name}: <default("RoceHostNew")> like IRoce {{\n'
            f"        {self.name}: RoceHostNew {{\n"
        )
        f.write("        }\n")

    def setXMLElement(self, element):
        super().setXMLElement(element)
        element.set("rdmaArgs", json.dumps(self.rdmaArgs))

    def readXMLElement(self, element):
        self.ip = element.get("ip")
        self.numApps = int(element.get("numApps"))
        print(element.get("appArgs"))
        self.appArgs = json.loads(element.get("appArgs"))
        print(element.get("rdmaArgs"))
        self.rdmaArgs = json.loads(element.get("rdmaArgs"))


class TsnHost(Host):
    def __init__(self, name):
        super().__init__(name, "StandardHost")

    def generateINI(self, f):
        super().generateINI(f)
        tsnArgs = []
        for arg in self.appArgs:
            if arg["typename"] == "TSN":
                tsnArgs.append(arg)
        if len(tsnArgs) != 0:
            f.write(f"*.{self.name}.hasOutgoingStreams = true\n")
            f.write(f"*.{self.name}.bridging.streamIdentifier.identifier.mapping = [")
            for index in range(0, len(tsnArgs)):
                tmp = tsnArgs[index]
                f.write("{")
                f.write(f'stream: "{tmp["stream"]}", ')
                f.write(f'packetfilter: {tmp["packetFilter"]}')
                f.write("}")
                if index < len(tsnArgs) - 1:
                    f.write(",")
            f.write("]\n")
        f.write(f"*.{self.name}.bridging.streamCoder.encoder.mapping = [")
        tsnQueue = globaldata.networkGlobalConfig["common"]["TsnQueue"]
        for index in range(0, len(tsnQueue)):
            tmp = tsnQueue[index]
            f.write("{")
            f.write(f'stream: "{tmp["stream"]}", ')
            f.write(f'pcp: {tmp["pcp"]}')
            f.write("}")
            if index < len(tsnQueue) - 1:
                f.write(",")
        f.write("]\n")
        f.write("\n")

    def generateNED(self, f):
        f.write(
            f'        {self.name}: <default("TsnDevice")> like IEthernetNetworkNode {{\n'
        )
        f.write("        }\n")

    def setXMLElement(self, element):
        super().setXMLElement(element)

    def readXMLElement(self, element):
        self.ip = element.get("ip")
        self.numApps = int(element.get("numApps"))
        print(element.get("appArgs"))
        self.appArgs = json.loads(element.get("appArgs"))


class DdsHost(Host):
    def __init__(self, name):
        super().__init__(name, "DDSStandardHost")

    def generateINI(self, f):
        f.write(f"*.{self.name}.numApps = {len(self.appArgs)}\n")
        # for index in range(0, len(self.appArgs)):

        f.write("\n")

    def generateNED(self, f):
        f.write(f"        {self.name}: {self.type} {{\n")
        f.write("        }\n")

    def setXMLElement(self, element):
        super().setXMLElement(element)

    def readXMLElement(self, element):
        self.ip = element.get("ip")
        self.numApps = int(element.get("numApps"))
        self.appArgs = json.loads(element.get("appArgs"))
