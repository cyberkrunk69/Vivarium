#!/bin/sh
set -e

echo "=========================================="
echo "  BLACK SWARM - Network Isolated Runtime"
echo "=========================================="

# Apply network lockdown if iptables is available
if command -v iptables > /dev/null 2>&1; then
    echo "[NETWORK] Applying network lockdown..."

    # Resolve API IPs
    GROQ_IPS=$(getent ahosts api.groq.com 2>/dev/null | awk '{print $1}' | sort -u || echo "")

    echo "[NETWORK] Groq API IPs: $GROQ_IPS"

    # Default DROP for outbound
    iptables -P OUTPUT DROP 2>/dev/null || true

    # Allow loopback
    iptables -A OUTPUT -o lo -j ACCEPT 2>/dev/null || true

    # Allow established connections
    iptables -A OUTPUT -m state --state ESTABLISHED,RELATED -j ACCEPT 2>/dev/null || true

    # Allow DNS
    iptables -A OUTPUT -p udp --dport 53 -j ACCEPT 2>/dev/null || true
    iptables -A OUTPUT -p tcp --dport 53 -j ACCEPT 2>/dev/null || true

    # Allow internal Docker network
    iptables -A OUTPUT -d 172.16.0.0/12 -j ACCEPT 2>/dev/null || true
    iptables -A OUTPUT -d 10.0.0.0/8 -j ACCEPT 2>/dev/null || true

    # Allow Groq API
    for ip in $GROQ_IPS; do
        iptables -A OUTPUT -d $ip -p tcp --dport 443 -j ACCEPT 2>/dev/null || true
        echo "[NETWORK] Allowed: $ip (Groq API)"
    done

    echo "[NETWORK] Lockdown applied - only Groq API and localhost allowed"
else
    echo "[NETWORK] WARNING: iptables not available"
fi

echo "[SWARM] Starting execution..."
cd /app

# Run the command passed to the container
exec "$@"
