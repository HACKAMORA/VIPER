export type NodeType = "gateway" | "server" | "workstation" | "mobile" | "printer" | "unknown";

export type NetworkNode = {
  id: string;
  ip: string;
  label?: string;
  type: NodeType;
  x: number;
  y: number;
  status?: "active" | "idle" | "down" | "filtered";
};

export type PortStatus = "open" | "filtered";

export type ServicePort = {
  port: number;
  proto: string;
  service: string | null;
  status: PortStatus;
};

export type ServiceCategory = {
  category: string;
  ports: ServicePort[];
};

export type AssetIntel = {
  ip: string;
  hostname: string;
  osFamily: string;
  distro: string;
  kernel: string;
  uptime: string;
  mac: string;
  vendor: string;
  hops: string;
  riskLabel: string;
  riskScore: number;
  riskDescription: string;
};

