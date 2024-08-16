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