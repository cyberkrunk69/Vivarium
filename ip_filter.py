import ipaddress

def filter_request(ip_address):
    # Define authorized IP addresses
    authorized_ips = ["192.168.1.0/24"]
    
    # Check if the IP address is authorized
    for authorized_ip in authorized_ips:
        if ipaddress.ip_address(ip_address) in ipaddress.ip_network(authorized_ip):
            return True
    
    return False