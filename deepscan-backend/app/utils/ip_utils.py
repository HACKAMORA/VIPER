from __future__ import annotations

import ipaddress
from typing import Iterable


def is_valid_cidr(value: str) -> bool:
  try:
    ipaddress.ip_network(value, strict=False)
    return True
  except ValueError:
    return False


def normalize_cidr(value: str) -> str:
  return str(ipaddress.ip_network(value, strict=False))


def iter_hosts(cidr: str) -> Iterable[str]:
  network = ipaddress.ip_network(cidr, strict=False)
  for host in network.hosts():
    yield str(host)


def lowest_ip(cidr: str) -> str:
  network = ipaddress.ip_network(cidr, strict=False)
  return str(next(network.hosts()))


