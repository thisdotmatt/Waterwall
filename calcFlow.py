from scapy.all import sniff, IP, TCP, UDP, Raw
import time
import statistics
from collections import defaultdict, deque
import zlib
import csv
from constants import unsw_columns, port_to_service, SYN, ACK, PSH, RST

def save_flows_to_csv(completed_flows, filename):
    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(unsw_columns)  # Write the header
        count = 0
        for flow_id, flow in completed_flows.items():
            # Extract necessary data from the flow
            row = [
                count,                               # 'id'
                flow['duration'],                      # 'dur'
                flow['proto_name'],                    # 'proto'
                port_to_service.get(flow_id[2], '-'),        # 'service'
                flow.get('state', '-'),          # 'state'
                flow['spkts'],                         # 'spkts'
                flow['dpkts'],                         # 'dpkts'
                flow['sbytes'],                        # 'sbytes'
                flow['dbytes'],                        # 'dbytes'
                flow['rate'],                          # 'rate'
                flow['sttl'],                          # 'sttl'
                flow['dttl'],                          # 'dttl'
                flow['sload'],                         # 'sload'
                flow['dload'],                         # 'dload'
                1,                                     # 'sloss' (not calculated here)
                1,                                     # 'dloss' (not calculated here)
                flow['sinpkt'],                        # 'sinpkt'
                flow['dinpkt'],                        # 'dinpkt'
                flow['sjit'],                          # 'sjit'
                flow['djit'],                          # 'djit'
                flow['swin'],                          # 'swin'
                flow['stcpb'],                         # 'stcpb'
                flow['dtcpb'],                         # 'dtcpb'
                flow['dwin'],                          # 'dwin'
                flow['tcprtt'],                        # 'tcprtt'
                flow['synack'],                        # 'synack'
                flow['ackdat'],                        # 'ackdat'
                flow['smean'],                         # 'smean'
                flow['dmean'],                         # 'dmean'
                flow['trans_depth'],                   # 'trans_depth'
                flow['response_body_len'],             # 'response_body_len'
                flow['ct_srv_src'],                    # 'ct_srv_src'
                flow['ct_state_ttl'],                  # 'ct_state_ttl'
                flow['ct_dst_ltm'],                    # 'ct_dst_ltm'
                flow['ct_src_dport_ltm'],              # 'ct_src_dport_ltm'
                flow['ct_dst_sport_ltm'],              # 'ct_dst_sport_ltm'
                flow['ct_dst_src_ltm'],                # 'ct_dst_src_ltm'
                flow['ct_ftp_cmd'],                    # 'ct_ftp_cmd'
                flow['ct_flw_http_mthd'],              # 'ct_flw_http_mthd'
                flow['ct_src_ltm'],                    # 'ct_src_ltm'
                flow['ct_srv_dst'],                    # 'ct_srv_dst'
            ]
            writer.writerow(row)
            count += 1

def ip_proto(pkt):
    proto_field = pkt.get_field('proto')
    return proto_field.i2s[pkt.proto]

recent_connections = deque(maxlen=100) # for retrieving last 100 connections
active_flows = defaultdict(lambda: {
    'start_time': 0,
    'last_packet_time': 0,
    'spkts': 0,
    'dpkts': 0,
    'sbytes': 0,
    'dbytes': 0,
    'sttl': [],
    'dttl': [],
    'sinter_arrival': [],
    'dinter_arrival': [],
    'last_src_time': None,
    'last_dst_time': None,
    'stcpb': 0,
    'dtcpb': 0,
    'sbytes_list': [],
    'dbytes_list': [],
    'swin': 0,
    'dwin': 0,
    'syn_time': None,
    'synack_time': None,
    'ackdat_time': None,
    'requests': [],
    'responses': [],
    'response_body': b'',
    'trans_depth': 0,
    'response_body_len': 0,
    'ftp_cmds': 0,
    'http_methods': [],
})
completed_flows = {}

def generate_flow_id(src_ip, src_port, dst_ip, dst_port, proto):
    return tuple(sorted([(src_ip, src_port), (dst_ip, dst_port)])) + (proto,) # src to dst treated adjacent to dst to src

def get_response_body_length(response_packet):
    body = response_packet[Raw].load
    content_encoding = response_packet[IP].load.get('Content-Encoding', '')

    if content_encoding == 'gzip':
        body = zlib.decompress(body, zlib.MAX_WBITS | 16)
    elif content_encoding == 'deflate':
        body = zlib.decompress(body)

    return len(body)

def packet_calculations(flow, flow_id):
    flow['end_time'] = flow['last_packet_time']
    flow['duration'] = flow['end_time'] - flow['start_time'] if flow['end_time'] - flow['start_time'] > 0 else 0.001
    flow['rate'] = (flow['spkts'] + flow['dpkts']) / flow['duration'] if flow['duration'] > 0 else 0
    flow['sload'] = flow['sbytes'] * 8 / flow['duration'] if flow['duration'] > 0 else 0
    flow['dload'] = flow['dbytes'] * 8 / flow['duration'] if flow['duration'] > 0 else 0
    flow['sttl'] = sum(flow['sttl']) / len(flow['sttl']) if len(flow['sttl']) > 0 else 0
    flow['dttl'] = sum(flow['dttl']) / len(flow['dttl']) if len(flow['dttl']) > 0 else 0
    flow['sinpkt'] = sum(flow['sinter_arrival']) / len(flow['sinter_arrival']) if len(flow['sinter_arrival']) > 0 else 0
    flow['dinpkt'] = sum(flow['dinter_arrival']) / len(flow['dinter_arrival']) if len(flow['dinter_arrival']) > 0 else 0
    flow['sjit'] = statistics.stdev(flow['sinter_arrival']) if len(flow['sinter_arrival']) > 1 else 0
    flow['djit'] = statistics.stdev(flow['dinter_arrival']) if len(flow['dinter_arrival']) > 1 else 0
    flow['stcpb'] = flow['stcpb']
    flow['dtcpb'] = flow['dtcpb']
    flow['smean'] = (sum(flow['sbytes_list']) / len(flow['sbytes_list'])) if len(flow['sbytes_list']) > 0 else 0
    flow['dmean'] = (sum(flow['dbytes_list']) / len(flow['dbytes_list'])) if len(flow['dbytes_list']) > 0 else 0
    flow['swin'] = flow['swin']
    flow['dwin'] = flow['dwin']
    flow['syn_time'] = flow['syn_time'] if flow['syn_time'] else 0
    flow['synack_time'] = flow['synack_time'] if flow['synack_time'] else 0
    flow['ackdat_time'] = flow['ackdat_time'] if flow['ackdat_time'] else 0
    flow['trans_depth'] = max(0, len(flow['requests']) + len(flow['responses']))
    flow['response_body_len'] = len(flow['response_body'])

    # Calculate RTT for TCP connections
    if flow['ackdat_time'] and flow['syn_time']:
        flow['tcprtt'] = flow['ackdat_time'] - flow['syn_time']
    else:
        flow['tcprtt'] = 0

    # Calculate SYN-ACK time
    if flow['synack_time'] and flow['syn_time']:
        flow['synack'] = flow['synack_time'] - flow['syn_time']
    else:
        flow['synack'] = 0

    # Calculate ACK-DAT time
    if flow['ackdat_time'] and flow['synack_time']:
        flow['ackdat'] = flow['ackdat_time'] - flow['synack_time']
    else:
        flow['ackdat'] = 0

    # Extract source and destination from the flow_id
    (src_ip, src_port), (dst_ip, dst_port) = flow_id[:2]
    srv_src = 0
    state_ttl = 0
    dst_ltm = 0
    dport_ltm = 0
    sport_ltm = 0
    dst_src_ltm = 0

    flow_http_mthd = 0
    src_ltm = 0
    srv_dst = 0
    
    for entry in recent_connections:
        conn_id = entry[0]
        conn = entry[1]
        (conn_src_ip, conn_src_port), (conn_dst_ip, conn_dst_port) = conn_id[:2]
        srv_src += 1 if (conn_src_ip == src_ip) and conn_dst_port == dst_port else 0
        state_ttl += 1 if conn['sttl'] == flow['sttl'] and conn['dttl'] == flow['dttl'] else 0
        dst_ltm += 1 if conn_dst_ip == dst_ip else 0
        dport_ltm += 1 if conn_dst_port == dst_port and conn_src_ip == src_ip else 0
        sport_ltm += 1 if conn_src_port == src_port and conn_src_ip == src_ip else 0
        dst_src_ltm += 1 if conn_dst_ip == dst_ip and conn_src_ip == src_ip else 0
        src_ltm += 1 if conn_src_ip == src_ip else 0
        srv_dst += 1 if conn_dst_ip == dst_ip and conn_dst_port == dst_port else 0
         
        for header in list(set(flow['http_methods'])):
            if header in list(set(conn['http_methods'])):
                flow_http_mthd += 1

    # Store the counts in the flow dictionary
    flow['ct_src_ltm'] = src_ltm
    flow['ct_srv_src'] = srv_src
    flow['ct_state_ttl'] = state_ttl
    flow['ct_dst_ltm'] = dst_ltm
    flow['ct_src_dport_ltm'] = dport_ltm
    flow['ct_dst_sport_ltm'] = sport_ltm
    flow['ct_dst_src_ltm'] = dst_src_ltm
    flow['ct_srv_dst'] = srv_dst

    # Count FTP commands and HTTP methods
    flow['ct_ftp_cmd'] = flow['ftp_cmds']
    flow['ct_flw_http_mthd'] = flow_http_mthd

    return flow

def process_packet(packet):
    if IP in packet and (TCP in packet or UDP in packet):
        src_ip = packet[IP].src
        dst_ip = packet[IP].dst
        proto = packet[IP].proto
        src_port = packet[TCP].sport if TCP in packet else packet[UDP].sport
        dst_port = packet[TCP].dport if TCP in packet else packet[UDP].dport
        flow_id = generate_flow_id(src_ip, src_port, dst_ip, dst_port, proto)
        
        timestamp = packet.time
        
        # Initialize the flow if not already tracked
        if flow_id not in active_flows:
            active_flows[flow_id]['proto_name'] = ip_proto(packet[IP])
            active_flows[flow_id]['start_time'] = timestamp
            active_flows[flow_id]['last_packet_time'] = timestamp

        flow = active_flows[flow_id]
        flow['last_packet_time'] = timestamp
        

        if TCP in packet:
            if (src_ip, src_port) == flow_id[0]:
                if flow['stcpb'] == 0:
                    flow['stcpb'] = packet[TCP].seq
                flow['stcpb'] = packet[TCP].seq
                flow['swin'] = packet[TCP].window
            else:
                if flow['dtcpb'] == 0:
                    flow['dtcpb'] = packet[TCP].seq
                flow['dtcpb'] = packet[TCP].seq
                flow['dwin'] = packet[TCP].window

            try: 
                #Track TCP handshake times
                if packet[TCP].flags & SYN:
                    flow['syn_time'] = timestamp
                if packet[TCP].flags & SYN and ((packet[TCP].flags & ACK) or (packet[TCP].flags & PSH)):
                    if flow['syn_time'] is not None:
                        flow['synack_time'] = timestamp
                if ((packet[TCP].flags & ACK) or (packet[TCP].flags & PSH)) and packet[TCP].dataofs > 0:
                    if flow['synack_time'] is not None:
                        flow['ackdat_time'] = timestamp
            except:
                print(packet[TCP])
                print(packet[TCP].dataofs)
                exit(1)

        if Raw in packet and b"HTTP" in packet[Raw].load: # Parse HTTP content
            payload = packet[Raw].load.decode('utf-8', errors='ignore')
            headers, body = payload.split('\r\n\r\n', 1)
            
            if 'HTTP/1.1' in headers or 'HTTP/2' in headers:
                print("yer!")
                if 'GET' in headers:
                    flow['requests'].append(timestamp)
                    flow['http_methods'].append('GET')
                elif 'POST' in headers:
                    flow['requests'].append(timestamp)
                    flow['http_methods'].append('POST')
                else:
                    flow['responses'].append(timestamp)
                    flow['response_body'] += body.encode()
                    
        if dst_port == 21: # Counts FTP commands
            flow['ftp_cmds'] += 1

        if (src_ip, src_port) == flow_id[0]:
            flow['spkts'] += 1
            flow['sbytes'] += len(packet)
            flow['sbytes_list'].append(len(packet))
            flow['sttl'].append(packet.ttl)
            if flow['last_src_time'] is not None:
                inter_arrival = (timestamp - flow['last_src_time'])  # convert to milliseconds
                flow['sinter_arrival'].append(inter_arrival)
            flow['last_src_time'] = timestamp
        else:
            flow['dpkts'] += 1
            flow['dbytes'] += len(packet)
            flow['dbytes_list'].append(len(packet))
            flow['dttl'].append(packet.ttl)
            if flow['last_dst_time'] is not None:
                inter_arrival = (timestamp - flow['last_dst_time'])  # convert to milliseconds
                flow['dinter_arrival'].append(inter_arrival)
            flow['last_dst_time'] = timestamp
        
        recent_connections.append([flow_id, flow]) # stores last 100 connections
        
    return None

# ends packet after 15 seconds of inactivity
def handle_timeouts(current_time, timeout=15):
    for flow_id, flow in list(active_flows.items()):
        if current_time - flow['last_packet_time'] > timeout:
            final_flow = packet_calculations(flow, flow_id)
            completed_flows[flow_id] = final_flow
            del active_flows[flow_id]

def main():
    sniff_duration = 60
    start_time = time.time()
    while time.time() - start_time < sniff_duration:
        sniff(prn=process_packet, timeout=1, store=False)
        handle_timeouts(time.time(), timeout=15)
        
    for flow_id, flow in active_flows.items():
        final_flow = packet_calculations(flow, flow_id)
        completed_flows[flow_id] = final_flow

    for flow_id, flow in completed_flows.items():
        print(f"Flow ID: {flow_id}")
        print(f"Flow Proto: {flow['proto_name']}")
        print(f"Duration: {flow['duration']:.5f} seconds")
        print(f"Source Packets: {flow['spkts']}, Source Bytes: {flow['sbytes']}")
        print(f"Destination Packets: {flow['dpkts']}, Destination Bytes: {flow['dbytes']}")
        print(f"Rate: {flow['rate']:.5f} packets/second")
        print(f"Source Inter-Packet Time: {flow['sinpkt']:.5f} seconds; Destination Inter-Packet Time: {flow['dinpkt']:.5f} seconds")
        print(f"Source Time-To-Live: {flow['sttl']:.5f} TTL; Destination Time-To-Live: {flow['dttl']:.5f} TTL")
        print(f"Source Jitter: {flow['sjit']*1000:.5f} milliseconds; Destination Jitter: {flow['djit']*1000:.5f} milliseconds")
        print(f"Source TCP Base: {flow['stcpb']}; Destination TCP Base: {flow['dtcpb']}")
        print(f"Source Mean Packet Size: {flow['smean']:.5f} bytes; Destination Mean Packet Size: {flow['dmean']:.5f} bytes")
        print(f"Source TCP Window Size: {flow['swin']}")
        print(f"Destination TCP Window Size: {flow['dwin']}")
        print(f"TCP RTT: {flow['tcprtt']:.5f} seconds")
        print(f"SYN-ACK Time: {flow['synack']:.5f} seconds")
        print(f"ACK-Data Time: {flow['ackdat']:.5f} seconds")
        print(f"Transaction Depth: {flow['trans_depth']}")
        print(f"Response Body Length: {flow['response_body_len']} bytes")
        print(f"ct_src_ltm: {flow['ct_src_ltm']}")  # Number of connections from the same source IP in the past 100 connections
        print(f"ct_srv_src: {flow['ct_srv_src']}")  # Number of connections to the same service from the same source IP in the past 100 connections
        print(f"ct_state_ttl: {flow['ct_state_ttl']}")  # Number of connections of the same state and using the same TTL in the past 100 connections
        print(f"ct_dst_ltm: {flow['ct_dst_ltm']}")  # Number of connections to the same destination IP in the past 100 connections
        print(f"ct_src_dport_ltm: {flow['ct_src_dport_ltm']}")  # Number of connections from the same source IP to the same destination port in the past 100 connections
        print(f"ct_dst_sport_ltm: {flow['ct_dst_sport_ltm']}")  # Number of connections to the same destination IP from the same source port in the past 100 connections
        print(f"ct_dst_src_ltm: {flow['ct_dst_src_ltm']}")  # Number of connections to the same destination IP from the same source IP in the past 100 connections

        print(f"ct_ftp_cmd: {flow['ct_ftp_cmd']}")  # Number of FTP commands in the connection
        print(f"ct_flw_http_mthd: {flow['ct_flw_http_mthd']}")  # Number of flows that use the same HTTP service method (e.g., GET, POST)")
        print()
    print(f"Number of Flows: {len(completed_flows)}")
    
    save_flows_to_csv(completed_flows, 'network_flows.csv') # save in CSV

if __name__ == "__main__":
    main()
