# Waterwall
## Description
A comprehensive, local Linux firewall written in python and utilizing Scapy and NetfilterQueue. Waterwall is updateable in real time through a web-based interface and database. 

## Features of Waterwall:
- Filter IP addresses, ports, protocls
- Filter based on HTTP, HTTPS packets, block certain websites or categories of websites
- Analyze packets coming from sources and put them on a watch-list for further logging.  
- Analyze payload of packets rather than just one-by-one

## Basic Usage
- Currently under testing

## Further Developments
- Utilize UNSW-NB15 or NSL-KDD dataset to train the firewall to analyze content on its own, and block/allow packets accordingly
- Remake the firewall using sockets to avoid current packet-overflowing errors

## Addendum
### Handled Protocols and Associated Codes:
    1: ICMP (Internet Control Message Protocol)
    2: IGMP (Internet Group Management Protocol)
    6: TCP (Transmission Control Protocol)
    17: UDP (User Datagram Protocol)
    41: IPv6 (Internet Protocol version 6)
    47: GRE (Generic Routing Encapsulation)
    50: ESP (Encapsulating Security Payload)
    51: AH (Authentication Header)
    58: ICMPv6 (Internet Control Message Protocol version 6)
    89: OSPF (Open Shortest Path First)
    103: PIM (Protocol Independent Multicast)
    115: L2TP (Layer 2 Tunneling Protocol)
    132: SCTP (Stream Control Transmission Protocol)
    143: ETH_P_IPX (IPX over DIX)
    253: IGRP (Interior Gateway Routing Protocol)
    254: OSPFIGP (OSPF for Internet Protocol Version 2)
    255: All IP protocols