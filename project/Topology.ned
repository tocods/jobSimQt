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
network TargetNetwork extends WiredNetworkBase
{
    submodules:
        tsn: <default("TsnDevice")> like IEthernetNetworkNode {
        }
        tsn2: <default("TsnDevice")> like IEthernetNetworkNode {
        }
        tsn3: <default("TsnDevice")> like IEthernetNetworkNode {
        }
        tsn_switch: <default("TsnSwitch")> like IEthernetNetworkNode {
        }
    connections:
        tsn.ethg++ <--> { datarate=100Mbps;} <--> tsn_switch.ethg++;
        tsn_switch.ethg++ <--> { datarate=100Mbps;} <--> tsn2.ethg++;
        tsn_switch.ethg++ <--> { datarate=100Mbps;} <--> tsn3.ethg++;
}
