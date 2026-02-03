#!/bin/bash
# Network Lockdown Script for Black Swarm
# Only allows connections to Groq API and localhost

set -e

echo "[NETWORK] Applying network isolation rules..."

# Flush existing rules
iptables -F OUTPUT 2>/dev/null || true

# Allow loopback (localhost)
iptables -A OUTPUT -o lo -j ACCEPT

# Allow DNS (needed for hostname resolution)
iptables -A OUTPUT -p udp --dport 53 -j ACCEPT
iptables -A OUTPUT -p tcp --dport 53 -j ACCEPT

# Allow HTTPS to Groq API only
# Groq API endpoint: api.groq.com
iptables -A OUTPUT -p tcp --dport 443 -d api.groq.com -j ACCEPT

# Allow established connections (responses)
iptables -A OUTPUT -m state --state ESTABLISHED,RELATED -j ACCEPT

# Log and drop everything else
iptables -A OUTPUT -j LOG --log-prefix "[BLOCKED] " --log-level 4
iptables -A OUTPUT -j DROP

echo "[NETWORK] Isolation rules applied. Only Groq API and localhost allowed."
echo "[NETWORK] Blocked destinations will be logged."

# Drop privileges and run the command
echo "[NETWORK] Dropping to user 'swarm'..."
exec su -s /bin/bash swarm -c "$*"
