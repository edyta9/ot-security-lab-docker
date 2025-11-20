#!/bin/sh

echo "[fw] starting OT firewall..."

# Enable packet forwarding (simulating router behavior)
sysctl -w net.ipv4.ip_forward=1

# Clear existing rules
iptables -F
iptables -X
iptables -t nat -F
iptables -t nat -X

# Block everything by default
iptables -P INPUT DROP
iptables -P OUTPUT DROP
iptables -P FORWARD DROP

# Allow established communication
iptables -A INPUT   -m conntrack --ctstate ESTABLISHED,RELATED -j ACCEPT
iptables -A FORWARD -m conntrack --ctstate ESTABLISHED,RELATED -j ACCEPT

# Allow ping troubleshooting
iptables -A INPUT  -p icmp -j ACCEPT
iptables -A OUTPUT -p icmp -j ACCEPT
iptables -A FORWARD -p icmp -j ACCEPT

# Allow only HMI (10.0.0.30) → PLC (10.0.0.10) Modbus TCP (port 502)
iptables -A FORWARD -s 10.0.0.30 -d 10.0.0.10 -p tcp --dport 502 -j ACCEPT

# Log anything else
iptables -A FORWARD -j LOG --log-prefix "FW-DROP: "

echo "[fw] firewall rules loaded."
tail -f /dev/null
