from __future__ import annotations

from datetime import timedelta
from typing import Any

from mac_vendor_lookup import MacLookup


class Fingerprinter:
  def __init__(self) -> None:
    self._mac_lookup = MacLookup()

  def extract_os_info(self, nmap_host: dict) -> dict:
    osmatches = (nmap_host.get("osmatch") or [])[:1]
    if not osmatches:
      return {"os_family": None, "os_distribution": None, "os_kernel": None}

    best = osmatches[0]
    name: str = best.get("name") or ""
    family = None
    distro = None
    kernel = None

    lowered = name.lower()
    for token in ("linux", "windows", "routeros", "ios", "bsd", "mac os x", "macos"):
      if token in lowered:
        family = token
        break

    distro = name

    if "linux" in lowered and " " in name:
      kernel = name.split()[-1]

    return {"os_family": family, "os_distribution": distro, "os_kernel": kernel}

  def extract_services(self, nmap_host: dict) -> list[dict]:
    ports: list[dict] = []
    tcp = nmap_host.get("tcp") or {}
    udp = nmap_host.get("udp") or {}

    for proto, table in (("tcp", tcp), ("udp", udp)):
      for port, data in table.items():
        ports.append(
          {
            "port": int(port),
            "protocol": proto,
            "service": data.get("name"),
            "version": data.get("version"),
            "state": data.get("state", "unknown"),
          }
        )
    return ports

  def get_mac_vendor(self, mac: str | None) -> str | None:
    if not mac:
      return None
    try:
      return self._mac_lookup.lookup(mac)
    except Exception:
      return None

  def estimate_uptime(self, nmap_host: dict) -> str | None:
    uptime = nmap_host.get("uptime") or {}
    seconds = uptime.get("seconds")
    if not seconds:
      return None
    td = timedelta(seconds=int(seconds))
    days = td.days
    hours, rem = divmod(td.seconds, 3600)
    mins, _ = divmod(rem, 60)
    return f"{days}d {hours}h {mins}m"

