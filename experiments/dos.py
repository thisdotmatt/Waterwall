from scapy.all import send, IP, TCP
import time

def send_packets(target_ip, target_port, num_packets, packet_size, interval):
    packet = IP(dst=target_ip) / TCP(dport=target_port) / ("X" * packet_size)
    print(f"Sending {num_packets} TCP packets to {target_ip}:{target_port}...")
    
    for i in range(num_packets):
        send(packet, verbose=False)
        print(f"Packet {i + 1} sent")
        
        if interval > 0:
            time.sleep(interval)

if __name__ == "__main__":
    target_ip = "10.0.0.0" # replace with your IP
    num_packets = 2000000  # number of packets to send
    packet_size = 100000  # size of each packet in bytes
    interval = 0  # Interval between packets in seconds
    target_port = 20
    send_packets(target_ip, target_port, num_packets, packet_size, interval)
