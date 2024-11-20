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
        self.type = host_type
        self.only_cpu = True

        print(f"Host name:{name} host_type:{host_type} created")

    def generateINI(self, f):
        f.write(f"*.{self.name}.numApps = {len(self.appArgs)}\n")
        for index in range(0, len(self.appArgs)):
            appArg = self.appArgs[index]
            if appArg["typename"] == "UdpApp615":
                self.generateINIUdp(f, index)
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
                f.write(
                    f'*.{self.name}.app[{index}].flowName = "{appArg["flowName"]}"\n'
                )
            f.write("\n")

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

    def generateNED(self, f):
        f.write(f"        {self.name}: {self.type} {{\n")
        f.write("        }\n")

    def setXMLElement(self, element):
        packet_size = "100"
        packet_interval = "100"
        total_traffic = "1000"
        for appArg in self.appArgs:
            if appArg["typename"] == "UdpApp615" and len(appArg) > 3:
                packet_interval = self.getNumber(appArg["productionInterval"])
                packet_size = self.getNumber(appArg["packetLength"])
        element.set("name", self.name)
        element.set("type", self.type)
        element.set("ip", self.ip)
        element.set("mac", self.mac)
        element.set("packet_size", packet_size)
        element.set("packet_interval", packet_interval)
        element.set("total_traffic", total_traffic)
        element.set("numApps", str(self.numApps))
        element.set("appArgs", json.dumps(self.appArgs))
        element.set("only_cpu", str(self.only_cpu))

    def readXMLElement(self, element):
        self.ip = element.get("ip")
        self.mac = element.get("mac")
        self.numApps = int(element.get("numApps"))
        self.appArgs = json.loads(element.get("appArgs"))


class NormalHost(Host):
    def __init__(self, name):
        super().__init__(name, "StandardHost")

    def generateINI(self, f):
        return super().generateINI(f)

    def generateNED(self, f):
        return super().generateNED(f)

    def setXMLElement(self, element):
        return super().setXMLElement(element)

    def readXMLElement(self, element):
        return super().readXMLElement(element)


class UdpHost(Host):
    def __init__(self, name):
        super().__init__(name, "StandardHost")

    def generateINI(self, f):
        return super().generateINI(f)

    def generateNED(self, f):
        return super().generateNED(f)

    def setXMLElement(self, element):
        return super().setXMLElement(element)

    def readXMLElement(self, element):
        return super().readXMLElement(element)


class TcpHost(Host):
    def __init__(self, name):
        super().__init__(name, "StandardHost")

    def generateINI(self, f):
        return super().generateINI(f)

    def generateNED(self, f):
        return super().generateNED(f)

    def setXMLElement(self, element):
        return super().setXMLElement(element)

    def readXMLElement(self, element):
        return super().readXMLElement(element)


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
            
            f'        {self.name}: RoceHostNew {{\n'
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

        # tsn
        self.tsnArgs = []

    def generateINI(self, f):
        super().generateINI(f)
        f.write(f"*.{self.name}.hasOutgoingStreams = true\n")
        if len(self.tsnArgs) != 0:
            f.write(f"*.{self.name}.bridging.streamIdentifier.identifier.mapping = [")
            for index in range(0, len(self.tsnArgs)):
                tmp = self.tsnArgs[index]
                f.write("{")
                f.write(f'stream: "{tmp["stream"]}", ')
                f.write(f'packetfilter: {tmp["packetFilter"]}')
                f.write("}")
                if index < len(self.tsnArgs) - 1:
                    f.write(",")
            f.write("]\n")
        f.write(f"*.{self.name}.bridging.streamCoder.encoder.mapping = [")
        tsnQueue = globaldata.networkGlobalConfig['common']['TsnQueue']
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
        element.set("tsnArgs", json.dumps(self.tsnArgs))

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
                f.write(
                    f'*.{self.name}.app[{index}].io.publish = "{appArg["publish"]}"\n'
                )
                f.write(
                    f'*.{self.name}.app[{index}].io.destPort = {appArg["destPort"]}\n'
                )
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

            if appArg["typename"] == "DDSSubscribeApp":
                f.write(
                    f'*.{self.name}.app[{index}].typename = "{appArg["typename"]}"\n'
                )
                f.write(
                    f'*.{self.name}.app[{index}].source.subscribe = "{appArg["subscribeTopic"] + "@" + appArg["subscribePort"]}"\n'
                )
                f.write(
                    f'*.{self.name}.app[{index}].io.localPort = {appArg["localPort"]}\n'
                )
                f.write(
                    f'*.{self.name}.app[{index}].io.receiverBufferLength = {appArg["receiverBufferLength"]}\n'
                )
                f.write(
                    f'*.{self.name}.app[{index}].io.nackCountdown = {appArg["nackCountdown"]}\n'
                )
                f.write(f"*.{self.name}.app[{index}].source.packetLength = 20B\n")
                f.write(f"*.{self.name}.ipv4.ip.limitedBroadcast = true \n")
                f.write(
                    f'*.{self.name}.app[{index}].sink.flowName = "{appArg["flowName"]}"\n'
                )
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
