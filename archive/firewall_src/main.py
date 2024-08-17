#Matthew Grimalovsky 2023
#Work-in-Progress

from scapy.all import *
from netfilterqueue import NetfilterQueue
import os
import subprocess
import netifaces
from mongo_db import *

interface_dict = {}
my_interfaces = netifaces.interfaces()

#Etablish interface: IP address Dictionary
for interface in my_interfaces:
	interface_dict[interface] = []
	addr_dict = netifaces.ifaddresses(interface)
	for num in addr_dict:
		for i in range(len(addr_dict[num])):
			interface_dict[interface].append(addr_dict[num][i]['addr'])

init_db()

mode = "block_focus"
packet_counter = 0
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
	
	#Update every 50 packets sent... TODO: Examine async implementation
	packet_counter += 1
	if packet_counter % 50 == 0:
		rules = get_db()
		blocked_ip = rules["blocked_ip"]
		blocked_dports = rules["blocked_dport"]
		blocked_sports = rules["blocked_sport"]
		blocked_proto = rules["blocked_proto"]

	pkt = IP(packet.get_payload())
	if pkt.proto in blocked_proto:
		packet.drop()
	if pkt.src in blocked_ip or pkt.dst in blocked_ip:
		packet.drop()
	if pkt.haslayer(TCP):
		dport = pkt[TCP].dport
		sport = pkt[TCP].sport
		if dport in blocked_dports:
			packet.drop()
		if sport in blocked_sports:
			packet.drop()
	if pkt.haslayer(UDP):
		dport = pkt[UDP].dport
		sport = pkt[UDP].sport
		if dport in blocked_dports:
			packet.drop()
		if sport in blocked_sports:
			packet.drop()
	packet.accept()

nfqueue = NetfilterQueue()
nfqueue.bind(1, handle_packet)

try:
	print("Waterwall 1.0 Running.")
	nfqueue.run()
except KeyboardInterrupt:
	pass
	print("Interrupted")
nfqueue.unbind()