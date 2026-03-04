from __future__ import annotations

import enum
from datetime import datetime
from uuid import uuid4

from sqlalchemy import JSON, DateTime, Enum, ForeignKey, Integer, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..database import Base


class HostStatus(str, enum.Enum):
  UP = "up"
  DOWN = "down"
  FILTERED = "filtered"


class NodeType(str, enum.Enum):
  GATEWAY = "gateway"
  SERVER = "server"
  WORKSTATION = "workstation"
  PRINTER = "printer"
  UNKNOWN = "unknown"


class Host(Base):
  __tablename__ = "hosts"

  id: Mapped[str] = mapped_column(
    UUID(as_uuid=False), primary_key=True, default=lambda: str(uuid4())
  )
  scan_id: Mapped[str] = mapped_column(
    UUID(as_uuid=False), ForeignKey("scans.id", ondelete="CASCADE"), nullable=False, index=True
  )

  ip_address: Mapped[str] = mapped_column(String(64), nullable=False, index=True)
  hostname: Mapped[str | None] = mapped_column(String(255), nullable=True)
  mac_address: Mapped[str | None] = mapped_column(String(64), nullable=True)
  vendor: Mapped[str | None] = mapped_column(String(255), nullable=True)

  os_family: Mapped[str | None] = mapped_column(String(128), nullable=True)
  os_distribution: Mapped[str | None] = mapped_column(String(255), nullable=True)
  os_kernel: Mapped[str | None] = mapped_column(String(128), nullable=True)
  uptime: Mapped[str | None] = mapped_column(String(64), nullable=True)
  hops: Mapped[int | None] = mapped_column(Integer, nullable=True)

  status: Mapped[HostStatus] = mapped_column(
    Enum(HostStatus, name="host_status_enum", native_enum=False),
    default=HostStatus.UP,
    nullable=False,
  )
  node_type: Mapped[NodeType] = mapped_column(
    Enum(NodeType, name="node_type_enum", native_enum=False),
    default=NodeType.UNKNOWN,
    nullable=False,
  )

  open_ports: Mapped[list[dict] | None] = mapped_column(JSON, nullable=True)
  risk_score: Mapped[int | None] = mapped_column(Integer, nullable=True)

  discovered_at: Mapped[datetime] = mapped_column(
    DateTime(timezone=True), default=datetime.utcnow, nullable=False, index=True
  )

  scan: Mapped["Scan"] = relationship(back_populates="hosts")

