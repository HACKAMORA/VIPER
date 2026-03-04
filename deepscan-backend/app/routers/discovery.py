from __future__ import annotations

from math import tau
from typing import Annotated

from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException, Query, status
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from ..database import AsyncSessionLocal, get_session
from ..models import Host, HostStatus, NodeType, Scan, ScanPhase, ScanStatus
from ..schemas import (
  HostDetail,
  HostListResponse,
  ScanCreate,
  ScanCreatedResponse,
  ScanListResponse,
  ScanStatusResponse,
  ScanSummary,
  TopologyEdge,
  TopologyNode,
  TopologyResponse,
)
from ..services import NetworkScanner
from ..utils import lowest_ip, normalize_cidr

router = APIRouter(prefix="/api/discovery", tags=["network-discovery"])


SessionDep = Annotated[AsyncSession, Depends(get_session)]


def get_scanner() -> NetworkScanner:
  return NetworkScanner(AsyncSessionLocal)


@router.post(
  "/scan",
  response_model=ScanCreatedResponse,
  status_code=status.HTTP_202_ACCEPTED,
)
async def start_scan(
  payload: ScanCreate,
  background: BackgroundTasks,
  session: SessionDep,
) -> ScanCreatedResponse:
  if not payload.target:
    raise HTTPException(status_code=400, detail="Target network is required.")

  cidr = normalize_cidr(payload.target)

  scan = Scan(
    name=payload.name,
    target=cidr,
    status=ScanStatus.PENDING,
    phase=ScanPhase.DISCOVERY,
  )
  session.add(scan)
  await session.commit()
  await session.refresh(scan)

  scanner = get_scanner()
  background.add_task(scanner.run_full_discovery, scan.id, cidr, payload.options.model_dump())

  return ScanCreatedResponse(scan_id=scan.id, status="running", message="Scan started")


@router.get("/scan/{scan_id}", response_model=ScanStatusResponse)
async def get_scan_status(scan_id: str, session: SessionDep) -> ScanStatusResponse:
  scan = await session.get(Scan, scan_id)
  if not scan:
    raise HTTPException(status_code=404, detail="Scan not found.")

  hosts_count = await session.scalar(
    select(func.count()).select_from(Host).where(Host.scan_id == scan_id)
  )
  progress = 0
  if scan.status in {ScanStatus.COMPLETED, ScanStatus.FAILED}:
    progress = 100
  elif scan.status == ScanStatus.RUNNING:
    progress = 74

  return ScanStatusResponse(
    scan_id=scan.id,
    name=scan.name,
    target=scan.target,
    status=scan.status,
    phase=scan.phase,
    progress_pct=progress,
    hosts_found=int(hosts_count or 0),
    started_at=scan.started_at,
    completed_at=scan.completed_at,
    message=None,
  )


@router.get("/scan/{scan_id}/hosts", response_model=HostListResponse)
async def list_scan_hosts(scan_id: str, session: SessionDep) -> HostListResponse:
  scan = await session.get(Scan, scan_id)
  if not scan:
    raise HTTPException(status_code=404, detail="Scan not found.")

  result = await session.execute(select(Host).where(Host.scan_id == scan_id))
  hosts = result.scalars().all()

  return HostListResponse(
    scan_id=scan.id,
    total=len(hosts),
    hosts=[HostDetail.model_validate(h) for h in hosts],
  )


@router.get("/scan/{scan_id}/hosts/{host_id}", response_model=HostDetail)
async def get_host_detail(scan_id: str, host_id: str, session: SessionDep) -> HostDetail:
  host = await session.get(Host, host_id)
  if not host or host.scan_id != scan_id:
    raise HTTPException(status_code=404, detail="Host not found for this scan.")
  return HostDetail.model_validate(host)


@router.get("/scan/{scan_id}/topology", response_model=TopologyResponse)
async def get_topology(scan_id: str, session: SessionDep) -> TopologyResponse:
  scan = await session.get(Scan, scan_id)
  if not scan:
    raise HTTPException(status_code=404, detail="Scan not found.")

  result = await session.execute(select(Host).where(Host.scan_id == scan_id))
  hosts = result.scalars().all()

  if not hosts:
    return TopologyResponse(nodes=[], edges=[])

  cidr = scan.target
  gw_ip = lowest_ip(cidr)
  gateway = next((h for h in hosts if h.ip_address == gw_ip), None)
  if not gateway:
    gateway = hosts[0]

  nodes: list[TopologyNode] = []
  edges: list[TopologyEdge] = []

  center_x, center_y = 400.0, 260.0
  radius = 180.0

  nodes.append(
    TopologyNode(
      id=gateway.id,
      ip=gateway.ip_address,
      type=NodeType.GATEWAY,
      status=gateway.status,
      x=center_x,
      y=center_y,
    )
  )

  other_hosts = [h for h in hosts if h.id != gateway.id]
  count = max(len(other_hosts), 1)
  for idx, host in enumerate(other_hosts):
    angle = (idx / count) * tau
    x = center_x + radius * 0.9 * float(__import__("math").cos(angle))
    y = center_y + radius * 0.6 * float(__import__("math").sin(angle))

    nodes.append(
      TopologyNode(
        id=host.id,
        ip=host.ip_address,
        type=host.node_type,
        status=host.status,
        x=x,
        y=y,
      )
    )
    edges.append(TopologyEdge(source=gateway.id, target=host.id))

  return TopologyResponse(nodes=nodes, edges=edges)


@router.get("/scans", response_model=ScanListResponse)
async def list_scans(
  session: SessionDep,
  page: int = Query(1, ge=1),
  limit: int = Query(10, ge=1, le=100),
) -> ScanListResponse:
  total = await session.scalar(select(func.count()).select_from(Scan))
  offset = (page - 1) * limit
  result = await session.execute(
    select(Scan).order_by(Scan.created_at.desc()).offset(offset).limit(limit)
  )
  scans = result.scalars().all()

  summaries = [
    ScanSummary(
      scan_id=s.id,
      name=s.name,
      target=s.target,
      status=s.status,
      phase=s.phase,
      progress_pct=100 if s.status in {ScanStatus.COMPLETED, ScanStatus.FAILED} else 74,
      hosts_found=0,
      started_at=s.started_at,
      completed_at=s.completed_at,
    )
    for s in scans
  ]

  return ScanListResponse(
    total=int(total or 0),
    page=page,
    limit=limit,
    scans=summaries,
  )


@router.delete("/scan/{scan_id}", status_code=status.HTTP_204_NO_CONTENT, response_model=None)
async def delete_scan(scan_id: str, session: SessionDep) -> None:
  scan = await session.get(Scan, scan_id)
  if not scan:
    raise HTTPException(status_code=404, detail="Scan not found.")
  await session.delete(scan)
  await session.commit()