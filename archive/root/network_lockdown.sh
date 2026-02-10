#!/bin/bash
# Network Lockdown Script for Vivarium
# Only allows connections to Groq API and localhost

echo "[NETWORK] Applying network isolation rules..."

# Flush existing rules (ignore errors if no rules exist)
iptables -F OUTPUT 2>/dev/null || true

# Allow loopback (localhost)
iptables -A OUTPUT -o lo -j ACCEPT

# Allow DNS (needed for hostname resolution)
iptables -A OUTPUT -p udp --dport 53 -j ACCEPT
iptables -A OUTPUT -p tcp --dport 53 -j ACCEPT

# Allow HTTPS (port 443) - Groq API needs this
# We allow all 443 traffic but the code-level safety blocks non-Groq URLs
iptables -A OUTPUT -p tcp --dport 443 -j ACCEPT

# Allow established connections (responses)
iptables -A OUTPUT -m state --state ESTABLISHED,RELATED -j ACCEPT

# Drop everything else (no logging to reduce noise)
iptables -A OUTPUT -j DROP

echo "[NETWORK] Isolation rules applied. Only HTTPS and localhost allowed."
echo "[NETWORK] Code-level safety blocks non-Groq API calls."

# Drop privileges and run the command
echo "[NETWORK] Dropping to user 'swarm'..."
cd /app
exec su -s /bin/bash swarm -c "cd /app && $*"
