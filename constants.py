import torch
unsw_columns = [
    'id', 'dur', 'proto', 'service', 'state', 'spkts', 'dpkts', 'sbytes', 'dbytes', 'rate', 
    'sttl', 'dttl', 'sload', 'dload', 'sloss', 'dloss', 'sinpkt', 'dinpkt', 'sjit', 'djit', 
    'swin', 'stcpb', 'dtcpb', 'dwin', 'tcprtt', 'synack', 'ackdat', 'smean', 'dmean', 
    'trans_depth', 'response_body_len', 'ct_srv_src', 'ct_state_ttl', 'ct_dst_ltm', 
    'ct_src_dport_ltm', 'ct_dst_sport_ltm', 'ct_dst_src_ltm', 'ct_ftp_cmd', 
    'ct_flw_http_mthd', 'ct_src_ltm', 'ct_srv_dst'
]

port_to_service = {
    20: 'ftp-data',        # FTP Data Transfer
    21: 'ftp',             # FTP Command Control
    22: 'ssh',             # Secure Shell (SSH)
    23: 'telnet',          # Telnet
    25: 'smtp',            # Simple Mail Transfer Protocol (SMTP)
    53: 'domain',          # Domain Name System (DNS)
    67: 'dhcp',            # DHCP (Dynamic Host Configuration Protocol)
    68: 'dhcp',            # DHCP (Dynamic Host Configuration Protocol)
    69: 'tftp',            # Trivial File Transfer Protocol (TFTP)
    80: 'http',            # Hypertext Transfer Protocol (HTTP)
    110: 'pop3',           # Post Office Protocol (POP3)
    111: 'rpcbind',        # RPC Bind (Remote Procedure Call)
    119: 'nntp',           # Network News Transfer Protocol (NNTP)
    123: 'ntp',            # Network Time Protocol (NTP)
    135: 'msrpc',          # Microsoft RPC
    137: 'netbios-ns',     # NetBIOS Name Service
    138: 'netbios-dgm',    # NetBIOS Datagram Service
    139: 'netbios-ssn',    # NetBIOS Session Service
    143: 'imap',           # Internet Message Access Protocol (IMAP)
    161: 'snmp',           # Simple Network Management Protocol (SNMP)
    162: 'snmptrap',       # SNMP Trap
    179: 'bgp',            # Border Gateway Protocol (BGP)
    194: 'irc',            # Internet Relay Chat (IRC)
    389: 'ldap',           # Lightweight Directory Access Protocol (LDAP)
    443: 'https',          # Hypertext Transfer Protocol Secure (HTTPS)
    445: 'microsoft-ds',   # Microsoft Directory Services
    514: 'syslog',         # Syslog
    515: 'printer',        # Line Printer Daemon (LPD)
    520: 'rip',            # Routing Information Protocol (RIP)
    587: 'smtp',           # Simple Mail Transfer Protocol (SMTP) - Mail Submission
    631: 'ipp',            # Internet Printing Protocol (IPP)
    993: 'imaps',          # Internet Message Access Protocol over SSL (IMAPS)
    995: 'pop3s',          # Post Office Protocol 3 over SSL (POP3S)
    1080: 'socks',         # SOCKS Proxy
    1194: 'openvpn',       # OpenVPN
    1433: 'ms-sql-s',      # Microsoft SQL Server
    1434: 'ms-sql-m',      # Microsoft SQL Monitor
    1723: 'pptp',          # Point-to-Point Tunneling Protocol (PPTP)
    1900: 'ssdp',          # Simple Service Discovery Protocol (SSDP)
    3306: 'mysql',         # MySQL
    3389: 'rdp',           # Remote Desktop Protocol (RDP)
    5060: 'sip',           # Session Initiation Protocol (SIP)
    51413: 'bittorrent',   # BitTorrent
    8080: 'http-proxy',    # HTTP Proxy / Alternate HTTP
    8443: 'https-alt',     # HTTPS Alternate
    9000: 'cslistener',    # CloudStack Client Listener
    10000: 'snet-sensor-mgmt', # Network Data Management Protocol (NDMP)
}

FIN = 0x01
SYN = 0x02
RST = 0x04
PSH = 0x08
ACK = 0x10
URG = 0x20
ECE = 0x40
CWR = 0x80

dataset_mean = torch.tensor([3.4122e+00, 8.1465e-01, 1.5120e+00, 2.4407e+00, 6.6419e-01, 1.4704e-01,
        6.0494e+00, 3.3197e-01, 8.4520e-03, 1.0876e+00, 4.1495e+00, 5.3080e-01,
        7.1667e-01, 8.6842e-03, 9.7937e-01, 6.8601e-01, 5.8108e-01, 7.9124e-01,
        8.0943e-01, 4.1496e+00, 7.5768e-01, 1.9619e+00, 4.4494e-03, 3.3291e-01,
        1.6517e-02, 1.6631e+00, 2.7308e+00, 8.7905e-01, 1.9856e-01, 6.0442e-01,
        1.7955e+02, 7.9610e+01, 1.1626e+02, 1.1501e+02, 1.0598e-01, 1.3042e+00,
        1.3307e-01])
dataset_std = torch.tensor([1.8036e+00, 1.0551e+00, 1.6931e+00, 2.5182e+00, 3.7906e-01, 2.8424e-01,
        2.0259e+00, 4.3166e-01, 1.5987e-02, 1.0975e+00, 4.5866e+00, 3.5831e-01,
        3.7993e-01, 1.7024e-02, 1.2328e+00, 9.1873e-01, 3.9274e-01, 4.2000e-01,
        4.1223e-01, 4.5870e+00, 4.2881e-01, 3.1027e-01, 3.6713e-02, 4.9056e-01,
        2.9994e-02, 1.7207e+00, 7.1909e-01, 4.9707e-01, 7.9420e-01, 6.7411e-01,
        1.0294e+02, 1.1051e+02, 1.2700e+02, 1.2689e+02, 7.7691e-01, 9.5441e-01,
        7.0121e-01])