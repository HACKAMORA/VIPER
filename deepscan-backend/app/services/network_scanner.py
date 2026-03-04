from __future__ import annotations

import asyncio
import traceback
from typing import Any

import nmap  # type: ignore[import-untyped]
from mac_vendor_lookup import MacLookup
from scapy.all import ARP, Ether, srp  # type: ignore[import-untyped]
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from ..models import Host, HostStatus, NodeType, Scan, ScanPhase, ScanStatus
from ..utils import lowest_ip, normalize_cidr
from .fingerprint import Fingerprinter


class NetworkScanner:
  def __init__(self, session_factory):
    self._session_factory = session_factory
    self._fingerprinter = Fingerprinter()
    self._mac_lookup = MacLookup()

  async def run_full_discovery(self, scan_id: str, target: str, options: dict) -> None:
    normalized_target = normalize_cidr(target)

    async with self._session_factory() as session:  # type: AsyncSession
      await self._mark_scan_running(session, scan_id)

    try:
      arp_results = await self.arp_sweep(normalized_target) if options.get("arp_scan", False) else []

      nmap_args = "-T4"
      if options.get("ping_sweep", True):
        nmap_args += " -sn"
      if options.get("port_scan", True):
        nmap_args += " -sS --top-ports 1000"
      if options.get("service_version", True):
        nmap_args += " -sV"
      if options.get("os_detection", True):
        nmap_args += " -O"

      nmap_data = await self.nmap_scan(normalized_target, nmap_args)

      hosts_payload: list[dict[str, Any]] = []
      for ip, host_blob in nmap_data.get("scan", {}).items():
        addr_info = host_blob.get("addresses", {})
        mac = addr_info.get("mac")
        hostname = next(iter(host_blob.get("hostnames", [{}])), {}).get("name") or None
        vendor = self._fingerprinter.get_mac_vendor(mac) or host_blob.get("vendor", {}).get(mac)

        os_info = self._fingerprinter.extract_os_info(host_blob)
        ports = self._fingerprinter.extract_services(host_blob)
        uptime = self._fingerprinter.estimate_uptime(host_blob)

        state = host_blob.get("status", {}).get("state", "unknown")
        status = HostStatus.UP if state == "up" else HostStatus.DOWN if state == "down" else HostStatus.FILTERED

        node_type = self.classify_node_type(
          {
            "ip": ip,
            "os_family": os_info.get("os_family"),
            "services": ports,
            "vendor": vendor,
          }
        )

        hosts_payload.append(
          {
            "scan_id": scan_id,
            "ip_address": ip,
            "hostname": hostname,
            "mac_address": mac,
            "vendor": vendor,
            "os_family": os_info.get("os_family"),
            "os_distribution": os_info.get("os_distribution"),
            "os_kernel": os_info.get("os_kernel"),
            "uptime": uptime,
            "hops": host_blob.get("hops"),
            "status": status,
            "node_type": node_type,
            "open_ports": ports or None,
            "risk_score": None,
          }
        )

      async with self._session_factory() as session:
        await self._persist_hosts(session, scan_id, hosts_payload)
        await self._mark_scan_completed(session, scan_id)

    except Exception as e:
      print(f"SCAN ERROR: {e}")
      traceback.print_exc()
      async with self._session_factory() as session:
        await self._mark_scan_failed(session, scan_id)
      raise

  def classify_node_type(self, host_data: dict) -> NodeType:
    os_family = (host_data.get("os_family") or "").lower()
    vendor = (host_data.get("vendor") or "").lower()
    services = host_data.get("services") or []
    ip = host_data.get("ip") or ""

    ports = {svc.get("port") for svc in services}

    if ip.endswith(".1") or ip.endswith(".254"):
      if {80, 443, 22} & ports:
        return NodeType.GATEWAY

    if "router" in os_family or "routeros" in os_family:
      return NodeType.GATEWAY

    if "printer" in vendor or any(v in vendor for v in ["hp", "canon", "epson", "xerox"]):
      return NodeType.PRINTER
    if {9100, 631} & ports:
      return NodeType.PRINTER

    if "windows" in os_family or "mac os" in os_family or "macos" in os_family:
      return NodeType.WORKSTATION

    server_ports = {80, 443, 22, 3306, 5432}
    if server_ports & ports or "linux" in os_family:
      return NodeType.SERVER

    return NodeType.UNKNOWN

  async def arp_sweep(self, network: str) -> list[dict[str, str]]:
    def _scan() -> list[dict[str, str]]:
      cidr = normalize_cidr(network)
      ether = Ether(dst="ff:ff:ff:ff:ff:ff")
      arp = ARP(pdst=cidr)
      answered, _ = srp(ether / arp, timeout=2, verbose=False)
      results: list[dict[str, str]] = []
      for _, recv in answered:
        results.append({"ip": recv.psrc, "mac": recv.hwsrc})
      return results

    return await asyncio.to_thread(_scan)

  async def nmap_scan(self, target: str, arguments: str) -> dict:
    def _scan() -> dict:
      scanner = nmap.PortScanner()
      scanner.scan(hosts=target, arguments=arguments)
      return scanner._scan_result

    return await asyncio.to_thread(_scan)

  async def _mark_scan_running(self, session: AsyncSession, scan_id: str) -> None:
    await session.execute(
      update(Scan)
      .where(Scan.id == scan_id)
      .values(status=ScanStatus.RUNNING, phase=ScanPhase.DISCOVERY)
    )
    await session.commit()

  async def _mark_scan_completed(self, session: AsyncSession, scan_id: str) -> None:
    stmt = (
      update(Scan)
      .where(Scan.id == scan_id)
      .values(status=ScanStatus.COMPLETED, phase=ScanPhase.DISCOVERY)
    )
    await session.execute(stmt)
    await session.commit()

  async def _mark_scan_failed(self, session: AsyncSession, scan_id: str) -> None:
    stmt = update(Scan).where(Scan.id == scan_id).values(status=ScanStatus.FAILED)
    await session.execute(stmt)
    await session.commit()

  async def _persist_hosts(
    self, session: AsyncSession, scan_id: str, hosts_payload: list[dict[str, Any]]
  ) -> None:
    existing_hosts = await session.execute(select(Host.id).where(Host.scan_id == scan_id))
    existing_ids = {row[0] for row in existing_hosts}
    if existing_ids:
      await session.execute(Host.__table__.delete().where(Host.scan_id == scan_id))

    objects = [Host(**payload) for payload in hosts_payload]
    session.add_all(objects)
    await session.commit()
