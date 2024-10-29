import inet.networks.base.WiredNetworkBase;
import inet.node.inet.StandardHost;
import inet.node.ethernet.EthernetSwitch;

network TargetNetwork extends WiredNetworkBase
{
    submodules:
        udp_cpu: StandardHost {
        }
        udp_cpu2: StandardHost {
        }
        udp_switch: EthernetSwitch {
        }
    connections:
        udp_cpu.ethg++ <--> { datarate=100Mbps;} <--> udp_switch.ethg++;
        udp_cpu2.ethg++ <--> { datarate=100Mbps;} <--> udp_switch.ethg++;
}
