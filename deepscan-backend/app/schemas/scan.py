from __future__ import annotations

from datetime import datetime
from typing import Literal, Optional

from pydantic import BaseModel, ConfigDict, Field

from ..models import ScanPhase, ScanStatus


class DiscoveryOptions(BaseModel):
  model_config = ConfigDict(extra="ignore")

  ping_sweep: bool = True
  port_scan: bool = True
  os_detection: bool = True
  service_version: bool = True
  arp_scan: bool = True


class ScanCreate(BaseModel):
  name: str = Field(..., max_length=255)
  target: str = Field(..., description="CIDR or target range, e.g. 192.168.1.0/24")
  options: DiscoveryOptions = Field(default_factory=DiscoveryOptions)


class ScanSummary(BaseModel):
  id: str = Field(alias="scan_id")
  name: str
  target: str
  status: ScanStatus
  phase: ScanPhase
  progress_pct: int = 0
  hosts_found: int = 0
  started_at: datetime
  completed_at: Optional[datetime] = None

  model_config = ConfigDict(populate_by_name=True)


class ScanListResponse(BaseModel):
  total: int
  page: int
  limit: int
  scans: list[ScanSummary]


class ScanStatusResponse(ScanSummary):
  message: str | None = None


class ScanCreatedResponse(BaseModel):
  scan_id: str
  status: Literal["running", "pending"]
  message: str

