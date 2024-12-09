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
        udp_tcp: StandardHost {
        }
        udp_tcp2: StandardHost {
        }
        udp_tcp3: StandardHost {
        }
        udp_tcp4: StandardHost {
        }
        udp_tcp5: StandardHost {
        }
        udp_tcp6: StandardHost {
        }
        udp_tcp7: StandardHost {
        }
        udp_tcp8: StandardHost {
        }
        udp_tcp9: StandardHost {
        }
        udp_tcp10: StandardHost {
        }
        udp_tcp11: StandardHost {
        }
        udp_tcp12: StandardHost {
        }
        udp_tcp13: StandardHost {
        }
        udp_tcp14: StandardHost {
        }
        udp_tcp15: StandardHost {
        }
        udp_tcp16: StandardHost {
        }
        udp_tcp17: StandardHost {
        }
        udp_tcp18: StandardHost {
        }
        udp_tcp19: StandardHost {
        }
        udp_tcp20: StandardHost {
        }
        udp_tcp21: StandardHost {
        }
        udp_tcp22: StandardHost {
        }
        udp_tcp23: StandardHost {
        }
        udp_tcp24: StandardHost {
        }
        udp_tcp25: StandardHost {
        }
        udp_tcp26: StandardHost {
        }
        udp_tcp27: StandardHost {
        }
        udp_tcp28: StandardHost {
        }
        udp_tcp29: StandardHost {
        }
        udp_tcp30: StandardHost {
        }
        udp_tcp31: StandardHost {
        }
        udp_tcp32: StandardHost {
        }
        udp_tcp33: StandardHost {
        }
        udp_tcp34: StandardHost {
        }
        udp_tcp35: StandardHost {
        }
        udp_tcp36: StandardHost {
        }
        udp_tcp37: StandardHost {
        }
        udp_tcp38: StandardHost {
        }
        udp_tcp39: StandardHost {
        }
        udp_tcp40: StandardHost {
        }
        switch: EthernetSwitch {
              gates:                   ethg[9];        }
        switch2: EthernetSwitch {
              gates:                   ethg[9];        }
        switch3: EthernetSwitch {
              gates:                   ethg[9];        }
        switch4: EthernetSwitch {
              gates:                   ethg[9];        }
        switch5: EthernetSwitch {
              gates:                   ethg[8];        }
    connections:
        udp_tcp.ethg++ <--> { datarate=100Mbps; per=0;} <--> switch.ethg++;
        udp_tcp2.ethg++ <--> { datarate=100Mbps; per=0;} <--> switch.ethg++;
        udp_tcp3.ethg++ <--> { datarate=100Mbps; per=0;} <--> switch.ethg++;
        udp_tcp4.ethg++ <--> { datarate=100Mbps; per=0;} <--> switch.ethg++;
        udp_tcp5.ethg++ <--> { datarate=100Mbps; per=0;} <--> switch.ethg++;
        udp_tcp6.ethg++ <--> { datarate=100Mbps; per=0;} <--> switch.ethg++;
        udp_tcp7.ethg++ <--> { datarate=100Mbps; per=0;} <--> switch.ethg++;
        udp_tcp8.ethg++ <--> { datarate=100Mbps; per=0;} <--> switch.ethg++;
        udp_tcp9.ethg++ <--> { datarate=100Mbps; per=0;} <--> switch2.ethg++;
        udp_tcp10.ethg++ <--> { datarate=100Mbps; per=0;} <--> switch2.ethg++;
        udp_tcp11.ethg++ <--> { datarate=100Mbps; per=0;} <--> switch2.ethg++;
        udp_tcp12.ethg++ <--> { datarate=100Mbps; per=0;} <--> switch2.ethg++;
        udp_tcp13.ethg++ <--> { datarate=100Mbps; per=0;} <--> switch2.ethg++;
        udp_tcp14.ethg++ <--> { datarate=100Mbps; per=0;} <--> switch2.ethg++;
        udp_tcp15.ethg++ <--> { datarate=100Mbps; per=0;} <--> switch2.ethg++;
        udp_tcp16.ethg++ <--> { datarate=100Mbps; per=0;} <--> switch2.ethg++;
        udp_tcp17.ethg++ <--> { datarate=100Mbps; per=0;} <--> switch3.ethg++;
        udp_tcp18.ethg++ <--> { datarate=100Mbps; per=0;} <--> switch3.ethg++;
        udp_tcp19.ethg++ <--> { datarate=100Mbps; per=0;} <--> switch3.ethg++;
        udp_tcp20.ethg++ <--> { datarate=100Mbps; per=0;} <--> switch3.ethg++;
        udp_tcp22.ethg++ <--> { datarate=100Mbps; per=0;} <--> switch3.ethg++;
        udp_tcp21.ethg++ <--> { datarate=100Mbps; per=0;} <--> switch3.ethg++;
        udp_tcp23.ethg++ <--> { datarate=100Mbps; per=0;} <--> switch3.ethg++;
        udp_tcp24.ethg++ <--> { datarate=100Mbps; per=0;} <--> switch3.ethg++;
        udp_tcp25.ethg++ <--> { datarate=100Mbps; per=0;} <--> switch4.ethg++;
        udp_tcp26.ethg++ <--> { datarate=100Mbps; per=0;} <--> switch4.ethg++;
        udp_tcp28.ethg++ <--> { datarate=100Mbps; per=0;} <--> switch4.ethg++;
        udp_tcp27.ethg++ <--> { datarate=100Mbps; per=0;} <--> switch4.ethg++;
        udp_tcp29.ethg++ <--> { datarate=100Mbps; per=0;} <--> switch4.ethg++;
        udp_tcp30.ethg++ <--> { datarate=100Mbps; per=0;} <--> switch4.ethg++;
        udp_tcp31.ethg++ <--> { datarate=100Mbps; per=0;} <--> switch4.ethg++;
        udp_tcp32.ethg++ <--> { datarate=100Mbps; per=0;} <--> switch4.ethg++;
        udp_tcp33.ethg++ <--> { datarate=100Mbps; per=0;} <--> switch5.ethg++;
        udp_tcp34.ethg++ <--> { datarate=100Mbps; per=0;} <--> switch5.ethg++;
        udp_tcp35.ethg++ <--> { datarate=100Mbps; per=0;} <--> switch5.ethg++;
        udp_tcp36.ethg++ <--> { datarate=100Mbps; per=0;} <--> switch5.ethg++;
        udp_tcp37.ethg++ <--> { datarate=100Mbps; per=0;} <--> switch5.ethg++;
        udp_tcp38.ethg++ <--> { datarate=100Mbps; per=0;} <--> switch5.ethg++;
        udp_tcp39.ethg++ <--> { datarate=100Mbps; per=0;} <--> switch5.ethg++;
        udp_tcp40.ethg++ <--> { datarate=100Mbps; per=0;} <--> switch5.ethg++;
        switch.ethg++ <--> { datarate=100Mbps; per=0;} <--> switch2.ethg++;
        switch2.ethg++ <--> { datarate=100Mbps; per=0;} <--> switch3.ethg++;
        switch3.ethg++ <--> { datarate=100Mbps; per=0;} <--> switch4.ethg++;
        switch4.ethg++ <--> { datarate=100Mbps; per=0;} <--> switch5.ethg++;
}
