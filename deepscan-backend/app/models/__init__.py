# app/models/__init__.py
from .host import Host, HostStatus, NodeType
from .scan import Scan, ScanPhase, ScanStatus

__all__ = ["Host", "HostStatus", "NodeType", "Scan", "ScanPhase", "ScanStatus"]