# utils/cidr_helpers.py

import ipaddress


def limit_cidr_size(cidr: str, max_hosts: int = 256):
    network = ipaddress.ip_network(cidr, strict=False)
    if network.num_addresses > max_hosts:
        return None
    return str(network)