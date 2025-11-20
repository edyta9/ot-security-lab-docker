#!/bin/sh

# Flush previous rules
iptables -F

# Set default policy to DROP
iptables -P INPUT DROP
iptables -P OUTPUT DROP
iptables -P FORWARD DROP

# Allow localhost
iptables -A INPUT -i lo -j ACCEPT
iptables -A OUTPUT -o lo -j ACCEPT

# Allow ICMP (ping)
iptables -A INPUT -p icmp -j ACCEPT
iptables -A OUTPUT -p icmp -j ACCEPT
iptables -A FORWARD -p icmp -j ACCEPT

# HMI (10.0.0.30) → PLC (10.0.0.10) Modbus TCP
iptables -A FORWARD -s 10.0.0.30 -d 10.0.0.10 -p tcp --dport 502 -j ACCEPT
# HMI (10.0.0.30) →PLC2 (10.0.0.11) Modbus TCP
iptables -A FORWARD -s 10.0.0.30 -d 10.0.0.11 -p tcp --dport 502 -j ACCEPT

# Log all other forwarded traffic
iptables -A FORWARD -j LOG --log-prefix "FW-DROP: "

# Optional: allow log output
iptables -A OUTPUT -p tcp --dport 514 -j ACCEPT

echo "Firewall rules applied."

# Keep container alive
tail -f /dev/null
