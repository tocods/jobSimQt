import inet.networks.base.WiredNetworkBase;
import inet.node.ethernet.Eth100M;
import inet.node.inet.DDSStandardHost;
import inet.node.inet.StandardHost;
import inet.node.ethernet.EthernetSwitch;
network TargetNetwork extends WiredNetworkBase
{
    submodules:
        dds_cpu: DDSStandardHost {
        }
        dds_cpu2: DDSStandardHost {
        }
        dds_cpu3: DDSStandardHost {
        }
        dds_cpu4: DDSStandardHost {
        }
        dds_cpu5: DDSStandardHost {
        }
        dds_switch: EthernetSwitch {
        }
        dds_switch2: EthernetSwitch {
        }
    connections:
        dds_cpu.ethg++ <--> { datarate=100Mbps;} <--> dds_switch.ethg++;
        dds_cpu2.ethg++ <--> { datarate=100Mbps;} <--> dds_switch2.ethg++;
        dds_switch.ethg++ <--> { datarate=100Mbps;} <--> dds_cpu3.ethg++;
        dds_switch.ethg++ <--> { datarate=100Mbps;} <--> dds_cpu4.ethg++;
        dds_switch.ethg++ <--> { datarate=100Mbps;} <--> dds_cpu5.ethg++;
        dds_switch2.ethg++ <--> { datarate=100Mbps;} <--> dds_cpu3.ethg++;
        dds_switch2.ethg++ <--> { datarate=100Mbps;} <--> dds_cpu4.ethg++;
        dds_switch2.ethg++ <--> { datarate=100Mbps;} <--> dds_cpu5.ethg++;
}
