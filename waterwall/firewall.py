import subprocess
import argparse

def modify_firewall_rule(rule, action, ip_version="ipv4"):
    """Adds or deletes a firewall rule"""
    command = ["iptables"] if ip_version == "ipv4" else ["ip6tables"]
    try:
        if action == "add":
            subprocess_result = subprocess.run(command + rule, check=True, capture_output=True, text=True)
            return True, subprocess_result.stdout
        elif action == "delete":
            subprocess_result = subprocess.run(command + rule, check=True, capture_output=True, text=True)
            return True, subprocess_result.stdout
    except subprocess.CalledProcessError as e:
        return False, e.stderr

def list_firewall_rules(ip_version="ipv4"):
    """Lists all firewall rules"""
    command = ["iptables", "-L"] if ip_version == "ipv4" else ["ip6tables", "-L"]
    try:
        subprocess_result = subprocess.run(command, check=True, capture_output=True, text=True)
        return True, subprocess_result.stdout
    except subprocess.CalledProcessError as e:
        return False, e.stderr

def manage_ip(ip_address, action="add", ip_version="ipv4"):
    """Adds or deletes a firewall rule to block traffic from a specific IP address."""
    rule = ["-A", "INPUT", "-s", ip_address, "-j", "DROP"] if action == "add" else ["-D", "INPUT", "-s", ip_address, "-j", "DROP"]
    return modify_firewall_rule(rule, action, ip_version)

def manage_port(port, protocol="tcp", action="add", ip_version="ipv4"):
    """Adds or deletes a firewall rule to block traffic on a specific port and protocol."""
    rule = ["-A", "INPUT", "-p", protocol, "--dport", str(port), "-j", "DROP"] if action == "add" else ["-D", "INPUT", "-p", protocol, "--dport", str(port), "-j", "DROP"]
    return modify_firewall_rule(rule, action, ip_version)

def manage_protocol(protocol, action="add", ip_version="ipv4"):
    """Adds or deletes a firewall rule to block traffic for a specific protocol."""
    rule = ["-A", "INPUT", "-p", protocol, "-j", "DROP"] if action == "add" else ["-D", "INPUT", "-p", protocol, "-j", "DROP"]
    return modify_firewall_rule(rule, action, ip_version)

def manage_firewall_rule_dual_stack(rule_type, *args, **kwargs):
    """Manages firewall rules for both IPv4 and IPv6."""
    result_ipv4 = rule_type(*args, **kwargs, ip_version="ipv4")
    result_ipv6 = rule_type(*args, **kwargs, ip_version="ipv6")
    
    return result_ipv4, result_ipv6

def main():
    parser = argparse.ArgumentParser(description="Firewall management script with iptables")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    
    parser_manage_ip = subparsers.add_parser("manage_ip", help="Manage (add or delete) a specific IP address")
    parser_manage_ip.add_argument("ip", help="The IP address to manage")
    parser_manage_ip.add_argument("action", choices=["add", "delete"], help="Action to perform (add or delete)")

    parser_manage_port = subparsers.add_parser("manage_port", help="Manage (add or delete) a specific port")
    parser_manage_port.add_argument("port", type=int, help="The port number to manage")
    parser_manage_port.add_argument("--protocol", choices=["tcp", "udp"], default="tcp", help="The protocol to manage (default: tcp)")
    parser_manage_port.add_argument("action", choices=["add", "delete"], help="Action to perform (add or delete)")

    parser_manage_protocol = subparsers.add_parser("manage_protocol", help="Manage (add or delete) a specific protocol")
    parser_manage_protocol.add_argument("protocol", choices=["tcp", "udp", "icmp"], help="The protocol to manage")
    parser_manage_protocol.add_argument("action", choices=["add", "delete"], help="Action to perform (add or delete)")

    parser_list_rules = subparsers.add_parser("list_rules", help="List all current firewall rules")

    args = parser.parse_args()

    if args.command == "manage_ip":
        success, message = manage_ip(args.ip, args.action)
    elif args.command == "manage_port":
        success, message = manage_port(args.port, args.protocol, args.action)
    elif args.command == "manage_protocol":
        success, message = manage_protocol(args.protocol, args.action)
    elif args.command == "list_rules":
        success, message = list_firewall_rules()
    else:
        parser.print_help()
        return

    if success:
        print(f"Command executed successfully: {message}")
    else:
        print(f"Command failed: {message}")

if __name__ == "__main__":
    main()
