def protect_ip(ip_address):
    # Protect the IP address from unauthorized access
    protected_ips = ["192.168.1.100", "192.168.1.101"]
    if ip_address in protected_ips:
        return True
    else:
        return False