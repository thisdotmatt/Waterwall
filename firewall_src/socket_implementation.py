import socket
import struct

# Create a raw socket
sniffer = socket.socket(socket.AF_PACKET, socket.SOCK_RAW, socket.ntohs(0x0003))
# Capture packets from lower level, capture raw packets, and capture ethernet/WIFI packets


# Set the network interface in promiscuous mode
sniffer.setsockopt(socket.SOL_SOCKET, 25, b'\x00' * 16)

def process_packet(packet):
    # Extract Ethernet header
    eth_header = packet[:14]
    eth_type = 0
    if len(packet) >= 14:
        eth_type = struct.unpack('!H', eth_header[12:14])[0]
    else:
        print("Hmmm...", packet)

    # Determine protocol based on EtherType
    if eth_type == 0x0800:  # IPv4
        process_ipv4_packet(packet[14:])
    elif eth_type == 0x86DD:  # IPv6
        process_ipv6_packet(packet[14:])
    else:
        print("Unsupported protocol")

def process_ipv4_packet(packet):
    # Extract IPv4 header
    ip_header = packet[:20]

    # Extract source and destination IP addresses
    src_ip = socket.inet_ntoa(ip_header[12:16])
    dst_ip = socket.inet_ntoa(ip_header[16:20])
    print(src_ip, dst_ip)


def process_ipv6_packet(packet):
    # Extract IPv6 header
    ip_header = packet[:40]

    # Extract source and destination IP addresses
    src_ip = socket.inet_ntop(socket.AF_INET6, ip_header[8:24])
    dst_ip = socket.inet_ntop(socket.AF_INET6, ip_header[24:40])
    print(src_ip, dst_ip)

# Receive and process packets
while True:
    #print("Running")
    packet = sniffer.recvfrom(0)
    #0 is used for packets of any size, to be filtered down later

    # Extract the packet data
    raw_packet = packet[0]
    print(packet)
    # Process and filter the packet
    process_packet(raw_packet)
    header=struct.unpack('!BBHHHBBHBBBBBBBB', packet[:20])
    if(header[6]==6): #header[6] is the field of the Protocol
        print("Protocol = TCP")
    elif(header[6]==17):
        print("Protocol = UDP")
    elif(header[5]==1):
        print("Protocol = ICMP") 
    

