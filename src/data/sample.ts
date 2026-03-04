import type { AssetIntel, NetworkNode, ServiceCategory } from "../types";

export const SAMPLE_NODES: NetworkNode[] = [
  { id: "1", ip: "192.168.1.1", label: "GW", type: "gateway", x: 400, y: 320, status: "active" },
  { id: "2", ip: "192.168.1.10", type: "server", x: 250, y: 170 },
  { id: "3", ip: "192.168.1.15", type: "workstation", x: 560, y: 190 },
  { id: "4", ip: "192.168.1.42", type: "mobile", x: 230, y: 390 },
  { id: "5", ip: "192.168.1.99", type: "printer", x: 550, y: 390 },
];

export const SAMPLE_SERVICES: ServiceCategory[] = [
  {
    category: "Web / HTTP",
    ports: [
      { port: 80, proto: "HTTP", service: "nginx 1.18.0", status: "open" },
      { port: 443, proto: "HTTPS", service: "OpenSSL", status: "open" },
      { port: 8080, proto: "HTTP-ALT", service: null, status: "filtered" },
    ],
  },
  {
    category: "Admin / Shell",
    ports: [{ port: 22, proto: "SSH", service: "OpenSSH 8.2p1", status: "open" }],
  },
];

export const SAMPLE_ASSET: AssetIntel = {
  ip: "192.168.1.15",
  hostname: "dev-ubuntu-01.local",
  osFamily: "Linux",
  distro: "Ubuntu 20.04.4 LTS (Focal Fossa)",
  kernel: "5.4.0-104-generic",
  uptime: "14d 3h 22m",
  mac: "00:1A:2B:3C:4D:5E",
  vendor: "VMware, Inc.",
  hops: "1 (Local Subnet)",
  riskLabel: "Low",
  riskScore: 12,
  riskDescription:
    "No critical vulnerabilities detected. Open ports match standard development profile. SMB signing enabled.",
};

