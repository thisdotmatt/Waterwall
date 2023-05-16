#Matthew Grimalovsky 2023
#Work-in-Progress

from scapy.all import *
from netfilterqueue import NetfilterQueue
import os
import subprocess
import netifaces

interface_dict = {}
my_interfaces = netifaces.interfaces()
#Etablish interface: IP address Dictionary
for interface in my_interfaces:
	interface_dict[interface] = []
	addr_dict = netifaces.ifaddresses(interface)
	for num in addr_dict:
		for i in range(len(addr_dict[num])):
			interface_dict[interface].append(addr_dict[num][i]['addr'])

mode = "block_focus"
blocked_ip = [] #List of Blocked IPs
sport = 0
dport = 0
blocked_sports = []
blocked_dports = []
blocked_proto = [] #List of Blocked Protocols, see README for protocol nums
ip_watch_list = {} #dictionary for currently observed IPs

def check_root_privileges():
    if os.geteuid() != 0:
        print("This program requires root privileges. Please run it as a root user.")
        exit(1)

# Call the function to check for root privileges
check_root_privileges()
command = "sudo iptables -I INPUT -j NFQUEUE --queue-num 1"
subprocess.run(command, shell=True)
command = "sudo iptables -I OUTPUT -j NFQUEUE --queue-num 1"
subprocess.run(command, shell=True)
command = "sudo iptables -I FORWARD -j NFQUEUE --queue-num 1"
subprocess.run(command, shell=True)


# Function to handle incoming packets from the queue
def handle_packet(packet):
	#Handle
	pkt = IP(packet.get_payload())
	if pkt.proto in blocked_proto:
		packet.drop()
	if pkt.src in blocked_ip or pkt.dst in blocked_ip:
		packet.drop()
	if TCP in pkt:
		dport = pkt[TCP].dport
		sport = pkt[TCP].sport
		if dport in blocked_dports:
			packet.drop()
		if sport in blocked_sports:
			packet.drop()
	if UDP in pkt:
		dport = pkt[UDP].dport
		sport = pkt[UDP].sport
		if dport in blocked_dports:
			packet.drop()
		if sport in blocked_sports:
			packet.drop()
	packet.accept()

nfqueue = NetfilterQueue()
nfqueue.bind(1, handle_packet)

print("Running good so far")
# Run the queue
try:
	print("Working")
	nfqueue.run()
except KeyboardInterrupt:
	pass
	print("Interrupted")

# Cleanup
nfqueue.unbind()