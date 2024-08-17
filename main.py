from scapy.all import sniff, IP
import psutil
import sys
from utils import serialize

def get_enabled_interfaces():
    """Returns a list of enabled network interfaces with their addresses."""
    interfaces = psutil.net_if_stats()
    addresses = psutil.net_if_addrs()

    enabled_interfaces = []
    for iface, stats in interfaces.items():
        if stats.isup:
            enabled_interfaces.append(iface)
            print(f"{iface} (UP): {addresses[iface]}")
    
    return enabled_interfaces

def process_packet(packet):
    """Processes each captured packet."""
    if IP in packet:
        source_ip = packet[IP].src
        print(f"Packet received from: {source_ip}")
        #print(f"Raw: {int.from_bytes(packet, byteorder=sys.byteorder)}\n")
        #
        print(f"Raw: {bytes(packet)}\n")
        #print(serialize(packet=packet))

def start_sniffing():
    """Starts sniffing on the first available enabled network interface."""
    enabled_interfaces = get_enabled_interfaces()

    if enabled_interfaces:
        try:
            iface = enabled_interfaces[0]  #Automatically select the first enabled interface
            print(f"Sniffing on interface: {iface}")
            sniff(filter="ip", prn=process_packet, iface=iface)
        except Exception as e:
            print(f"Error sniffing on interface {iface}: {e}")
            if len(enabled_interfaces) >= 2:
                iface = enabled_interfaces[1]  #Try the next available interface
                print(f"Sniffing on interface: {iface}")
                sniff(filter="ip", prn=process_packet, iface=iface)
            else:
                print("No interfaces exist other than loopback.")
    else:
        print("No enabled network interfaces found.")

def main():
    """Main function to start the packet sniffer."""
    start_sniffing()

if __name__ == "__main__":
    main()