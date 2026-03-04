from __future__ import annotations

import enum
from datetime import datetime
from typing import TYPE_CHECKING
from uuid import uuid4

from sqlalchemy import DateTime, Enum, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..database import Base

if TYPE_CHECKING:
  from .host import Host  # pragma: no cover


class ScanStatus(str, enum.Enum):
  PENDING = "pending"
  RUNNING = "running"
  COMPLETED = "completed"
  FAILED = "failed"


class ScanPhase(str, enum.Enum):
  RECON = "reconnaissance"
  DISCOVERY = "network_discovery"
  FINGERPRINT = "fingerprinting"
  EXPLOITATION = "exploitation"


class Scan(Base):
  __tablename__ = "scans"

  id: Mapped[str] = mapped_column(
    UUID(as_uuid=False), primary_key=True, default=lambda: str(uuid4())
  )
  name: Mapped[str] = mapped_column(String(255), nullable=False)
  target: Mapped[str] = mapped_column(String(255), nullable=False)
  status: Mapped[ScanStatus] = mapped_column(
    Enum(ScanStatus, name="scan_status_enum", native_enum=False),
    default=ScanStatus.PENDING,
    nullable=False,
  )
  phase: Mapped[ScanPhase] = mapped_column(
    Enum(ScanPhase, name="scan_phase_enum", native_enum=False),
    default=ScanPhase.DISCOVERY,
    nullable=False,
  )
  started_at: Mapped[datetime] = mapped_column(
    DateTime(timezone=True), default=datetime.utcnow, nullable=False
  )
  completed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
  created_at: Mapped[datetime] = mapped_column(
    DateTime(timezone=True), default=datetime.utcnow, nullable=False
  )

  hosts: Mapped[list["Host"]] = relationship(
    back_populates="scan", cascade="all, delete-orphan", lazy="selectin"
  )

