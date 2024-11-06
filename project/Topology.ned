import inet.networks.base.WiredNetworkBase;
import inet.common.misc.ThruputMeteringChannel;
import inet.node.ethernet.EthernetSwitch;
import inet.node.inet.StandardHost;
import inet.node.ethernet.Eth100M;
network TargetNetwork extends WiredNetworkBase
{
    parameters:
    types:
    submodules:
        udp_tcp_cpu: StandardHost {
        }
        udp_tcp_cpu2: StandardHost {
        }
        switch: EthernetSwitch {
        }
    connections:
        udp_tcp_cpu.ethg++ <--> { datarate=100Mbps;} <--> switch.ethg++;
        udp_tcp_cpu2.ethg++ <--> { datarate=100Mbps;} <--> switch.ethg++;
}
