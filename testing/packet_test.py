from scapy.all import *
#our ether IP: 00:0c:29:a2:bb:b1
#our address: 2601:84:8b00:b0::9

#packet = IP(src="192.168.222.129", dst="192.168.222.129") / UDP(dport=12345) / "Hello, World!"
#final_packet = IP(dst="192.168.222.129") / UDP(dport=12345) / b"Custom UDP payload"
#packet = IPv6(dst="2001:db8::1") / ICMPv6EchoRequest()
#packet = IPv6(dst="00:0c:29:a2:bb:b1") / UDP(dport=12345) / "Hello, World!"

ipv6_packet = IPv6(src="2001:db8::1", dst="fe80::634c:e1ca:2340:f3bd")
#fe80::634c:e1ca:2340:f3bd
# Create a UDP packet
udp_packet = UDP(sport=1234, dport=5678)

# Set the payload of the UDP packet
payload = "Custom UDP payload"

# Combine the packets
final_packet = ipv6_packet / udp_packet / payload

send(final_packet)