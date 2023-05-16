from scapy.all import *

# Function to handle incoming packets from the queue
def handle_packet(packet):
	#Check if the packet matches the criteria for blocking
    if IPv6 in packet and UDP in packet:
        src_ip = packet[IPv6].src
        dst_ip = packet[IPv6].dst
        # Perform actions based on the source and destination IP addresses
        print(src_ip, dst_ip)

print("Firewall Started.")
sniff(prn = handle_packet)