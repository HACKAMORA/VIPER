from __future__ import annotations

from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict, Field

from ..models import HostStatus, NodeType


class Port(BaseModel):
  port: int
  protocol: str
  service: str | None = None
  version: str | None = None
  state: str


class HostBase(BaseModel):
  ip_address: str
  hostname: str | None = None
  mac_address: str | None = None
  vendor: str | None = None

  os_family: str | None = None
  os_distribution: str | None = None
  os_kernel: str | None = None
  uptime: str | None = None
  hops: int | None = None

  status: HostStatus = HostStatus.UP
  node_type: NodeType = NodeType.UNKNOWN
  open_ports: list[Port] | None = None
  risk_score: int | None = None


class HostDetail(HostBase):
  id: str = Field(alias="host_id")
  scan_id: str
  discovered_at: datetime

  model_config = ConfigDict(from_attributes=True, populate_by_name=True)


class HostListResponse(BaseModel):
  scan_id: str
  total: int
  hosts: list[HostDetail]


class TopologyNode(BaseModel):
  id: str
  ip: str
  type: NodeType
  status: HostStatus
  x: float
  y: float


class TopologyEdge(BaseModel):
  source: str
  target: str


class TopologyResponse(BaseModel):
  nodes: list[TopologyNode]
  edges: list[TopologyEdge]

