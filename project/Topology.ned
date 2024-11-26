import inet.linklayer.configurator.gatescheduling.contract.IGateScheduleConfigurator;
import inet.networklayer.configurator.contract.INetworkConfigurator;
import inet.node.tsn.TsnDevice;
import inet.node.tsn.TsnSwitch;
import inet.networks.base.WiredNetworkBase;
import inet.node.contract.IEthernetNetworkNode;
import inet.node.ethernet.EthernetLink;
import inet.node.ethernet.Eth100M;
import inet.node.inet.StandardHost;
import inet.node.ethernet.EthernetSwitch;
import inet.node.inet.DDSStandardHost;
import inet.node.rocev2.RoceHost;
import inet.node.rocev2.RoceHostNew;
import inet.node.rocev2.RoceSwitch;
import inet.transportLayer.contract.IRoce;
network TargetNetwork extends WiredNetworkBase
{
    submodules:
        udp_sender: StandardHost {
        }
        tcp_sender: StandardHost {
        }
        udp_receiver: StandardHost {
        }
        tcp_receiver: StandardHost {
        }
        tsn_sender1: <default("TsnDevice")> like IEthernetNetworkNode {
        }
        tsn_sender2: <default("TsnDevice")> like IEthernetNetworkNode {
        }
        tsn_receiver: <default("TsnDevice")> like IEthernetNetworkNode {
        }
        publisher1: DDSStandardHost {
        }
        subscriber3: DDSStandardHost {
        }
        subscriber2: DDSStandardHost {
        }
        subscriber1: DDSStandardHost {
        }
        switch: EthernetSwitch {
        }
        tsn_switch: <default("TsnSwitch")> like IEthernetNetworkNode {
        }
    connections:
        tsn_sender1.ethg++ <--> { datarate=100Mbps;} <--> tsn_switch.ethg++;
        tsn_sender2.ethg++ <--> { datarate=100Mbps;} <--> tsn_switch.ethg++;
        tsn_receiver.ethg++ <--> { datarate=100Mbps;} <--> tsn_switch.ethg++;
        publisher1.ethg++ <--> { datarate=100Mbps;} <--> switch.ethg++;
        udp_sender.ethg++ <--> { datarate=100Mbps;} <--> switch.ethg++;
        tcp_sender.ethg++ <--> { datarate=100Mbps;} <--> switch.ethg++;
        switch.ethg++ <--> { datarate=100Mbps;} <--> udp_receiver.ethg++;
        tcp_receiver.ethg++ <--> { datarate=100Mbps;} <--> switch.ethg++;
        switch.ethg++ <--> { datarate=100Mbps;} <--> subscriber2.ethg++;
        switch.ethg++ <--> { datarate=100Mbps;} <--> subscriber1.ethg++;
        switch.ethg++ <--> { datarate=100Mbps;} <--> subscriber3.ethg++;
        switch.ethg++ <--> { datarate=100Mbps;} <--> tsn_switch.ethg++;
}
