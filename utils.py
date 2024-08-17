from scapy.all import sniff, IP, TCP, UDP, ICMP

def serialize(packet):
    """Converts a Scapy packet to a serialized format with decimal integers."""
    fields = []

    if IP in packet:
        ip_layer = packet[IP]
        fields.append(ip_layer.version)  # IP version
        fields.append(ip_layer.ihl)  # IP header length
        fields.append(ip_layer.len)  # Total length
        fields.append(ip_layer.id)  # Identification
        fields.append(ip_layer.flags)  # Flags
        fields.append(ip_layer.ttl)  # Time to Live
        fields.append(ip_layer.proto)  # Protocol number
        fields.append(ip_layer.chksum)  # Checksum
        fields.append(ip_layer.src)  # Source IP address
        fields.append(ip_layer.dst)  # Destination IP address
        
    if TCP in packet:
        tcp_layer = packet[TCP]
        fields.append(tcp_layer.sport)  # Source port
        fields.append(tcp_layer.dport)  # Destination port
        fields.append(tcp_layer.seq)  # Sequence number
        fields.append(tcp_layer.ack)  # Acknowledgment number
        fields.append(tcp_layer.dataofs)  # Data offset
        fields.append(tcp_layer.flags)  # TCP flags
        fields.append(tcp_layer.window)  # Window size
        fields.append(tcp_layer.chksum)  # Checksum

    if UDP in packet:
        udp_layer = packet[UDP]
        fields.append(udp_layer.sport)  # Source port
        fields.append(udp_layer.dport)  # Destination port
        fields.append(udp_layer.len)  # Length
        fields.append(udp_layer.chksum)  # Checksum

    if ICMP in packet:
        icmp_layer = packet[ICMP]
        fields.append(icmp_layer.type)  # Type
        fields.append(icmp_layer.code)  # Code
        fields.append(icmp_layer.id)  # Identification
        fields.append(icmp_layer.seq)  # Sequence number

    serialized_str = " ".join(map(str, fields))
    
    return serialized_str