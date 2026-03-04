const API_BASE_URL = import.meta.env.VITE_API_BASE_URL ?? "http://localhost:8000";

export type ApiScanStatus = {
  scan_id: string;
  name: string;
  target: string;
  status: "pending" | "running" | "completed" | "failed";
  phase: string;
  progress_pct: number;
  hosts_found: number;
  started_at: string;
  completed_at: string | null;
};

export type ApiPort = {
  port: number;
  protocol: string;
  service: string | null;
  version: string | null;
  state: string;
};

export type ApiHost = {
  host_id: string;
  scan_id: string;
  ip_address: string;
  hostname: string | null;
  mac_address: string | null;
  vendor: string | null;
  os_family: string | null;
  os_distribution: string | null;
  os_kernel: string | null;
  uptime: string | null;
  hops: number | null;
  status: "up" | "down" | "filtered";
  node_type: "gateway" | "server" | "workstation" | "printer" | "unknown";
  open_ports: ApiPort[] | null;
  risk_score: number | null;
  discovered_at: string;
};

export type ApiHostListResponse = {
  scan_id: string;
  total: number;
  hosts: ApiHost[];
};

export type ApiTopologyNode = {
  id: string;
  ip: string;
  type: ApiHost["node_type"];
  status: ApiHost["status"];
  x: number;
  y: number;
};

export type ApiTopologyEdge = {
  source: string;
  target: string;
};

export type ApiTopologyResponse = {
  nodes: ApiTopologyNode[];
  edges: ApiTopologyEdge[];
};

export type DiscoveryOptionsInput = {
  ping_sweep?: boolean;
  port_scan?: boolean;
  os_detection?: boolean;
  service_version?: boolean;
  arp_scan?: boolean;
};

export async function startDiscoveryScan(
  name: string,
  target: string,
  options: DiscoveryOptionsInput,
) {
  const res = await fetch(`${API_BASE_URL}/api/discovery/scan`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ name, target, options }),
  });
  if (!res.ok) {
    const text = await res.text();
    throw new Error(`Failed to start scan: ${res.status} ${text}`);
  }
  return (await res.json()) as { scan_id: string; status: string; message: string };
}

export async function fetchScanStatus(scanId: string): Promise<ApiScanStatus> {
  const res = await fetch(`${API_BASE_URL}/api/discovery/scan/${scanId}`);
  if (!res.ok) {
    const text = await res.text();
    throw new Error(`Failed to fetch scan status: ${res.status} ${text}`);
  }
  return (await res.json()) as ApiScanStatus;
}

export async function fetchScanHosts(scanId: string): Promise<ApiHostListResponse> {
  const res = await fetch(`${API_BASE_URL}/api/discovery/scan/${scanId}/hosts`);
  if (!res.ok) {
    const text = await res.text();
    throw new Error(`Failed to fetch hosts: ${res.status} ${text}`);
  }
  return (await res.json()) as ApiHostListResponse;
}

export async function fetchScanTopology(scanId: string): Promise<ApiTopologyResponse> {
  const res = await fetch(`${API_BASE_URL}/api/discovery/scan/${scanId}/topology`);
  if (!res.ok) {
    const text = await res.text();
    throw new Error(`Failed to fetch topology: ${res.status} ${text}`);
  }
  return (await res.json()) as ApiTopologyResponse;
}

