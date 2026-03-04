# modules/network/discovery_service.py

import subprocess
import ipaddress
import platform
from typing import List


class DiscoveryService:

    @staticmethod
    def ping_host(ip: str) -> bool:
        """Ping single host - Windows/Unix compatible"""
        try:
            # Adapt ping command to operating system
            if platform.system() == "Windows":
                # Windows ping syntax: -n (count), -w (timeout in ms)
                cmd = ["ping", "-n", "1", "-w", "1000", ip]
            else:
                # Unix/Linux/macOS ping syntax: -c (count), -W (timeout in seconds)
                cmd = ["ping", "-c", "1", "-W", "1", ip]
            
            result = subprocess.run(
                cmd,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                timeout=3
            )
            return result.returncode == 0
        except Exception:
            return False

    @staticmethod
    def ping_sweep(cidr: str) -> List[str]:
        """Discover active hosts in CIDR range"""
        active_hosts = []

        try:
            network = ipaddress.ip_network(cidr, strict=False)

            for ip in network.hosts():
                ip_str = str(ip)
                if DiscoveryService.ping_host(ip_str):
                    active_hosts.append(ip_str)

            return active_hosts

        except Exception:
            return []

    @staticmethod
    def detect_cidr_from_ip(ip: str) -> str:
        """Simple CIDR guess (/24 default)"""
        try:
            network = ipaddress.ip_network(ip + "/24", strict=False)
            return str(network)
        except Exception:
            return None