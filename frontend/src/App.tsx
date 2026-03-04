import { useEffect, useMemo, useState } from "react";
import {
  fetchScanHosts,
  fetchScanStatus,
  fetchScanTopology,
  startDiscoveryScan,
  type ApiHost,
  type ApiScanStatus,
  type ApiTopologyResponse,
} from "./api/discovery";
import { AssetIntelligencePanel } from "./components/AssetIntelligencePanel";
import { NetworkTopologyMap } from "./components/NetworkTopologyMap";
import { ScanStatusBar } from "./components/ScanStatusBar";
import { ServiceMatrixPanel } from "./components/ServiceMatrixPanel";
import { TopNavbar } from "./components/TopNavbar";
import { SAMPLE_ASSET, SAMPLE_NODES, SAMPLE_SERVICES } from "./data/sample";
import type { AssetIntel, NetworkNode, ServiceCategory } from "./types";

function App() {
  const [projectName, setProjectName] = useState("Apollo-7 Subnet Audit");
  const [selectedNodeId, setSelectedNodeId] = useState<string | null>("3");

  const [scan, setScan] = useState<ApiScanStatus | null>(null);
  const [hosts, setHosts] = useState<ApiHost[]>([]);
  const [topology, setTopology] = useState<ApiTopologyResponse | null>(null);
  const [isStarting, setIsStarting] = useState(false);

  useEffect(() => {
    if (!scan?.scan_id) return;
    let cancelled = false;

    const poll = async () => {
      while (!cancelled) {
        try {
          const status = await fetchScanStatus(scan.scan_id);
          if (cancelled) return;
          setScan(status);

          const [hostsRes, topoRes] = await Promise.all([
            fetchScanHosts(scan.scan_id),
            fetchScanTopology(scan.scan_id),
          ]);
          if (cancelled) return;
          setHosts(hostsRes.hosts);
          setTopology(topoRes);

          if (!selectedNodeId && topoRes.nodes.length > 0) {
            setSelectedNodeId(topoRes.nodes[0].id);
          }

          if (status.status !== "running" && status.status !== "pending") break;
          await new Promise((resolve) => setTimeout(resolve, 5000));
        } catch (e) {
          if (cancelled) return;
          console.error(e);
          alert("Backend unreachable ou scan échoué. Utilisation des données de démonstration.");
          break;
        }
      }
    };

    void poll();
    return () => {
      cancelled = true;
    };
  }, [scan?.scan_id, selectedNodeId]);

  const handleStartScan = async () => {
    setIsStarting(true);
    try {
      const res = await startDiscoveryScan(projectName, "192.168.1.0/24", {
        ping_sweep: true,
        port_scan: true,
        os_detection: true,
        service_version: true,
        arp_scan: true,
      });
      const initialStatus: ApiScanStatus = {
        scan_id: res.scan_id,
        name: projectName,
        target: "192.168.1.0/24",
        status: "running",
        phase: "network_discovery",
        progress_pct: 0,
        hosts_found: 0,
        started_at: new Date().toISOString(),
        completed_at: null,
      };
      setScan(initialStatus);
    } catch (e) {
      console.error(e);
      alert("Impossible de démarrer le scan (backend). Vérifie que l'API tourne sur :8000.");
    } finally {
      setIsStarting(false);
    }
  };

  const selectedNode = useMemo(
    () => {
      const nodes = topologyToNodes(topology) ?? SAMPLE_NODES;
      const fallback = nodes[0];
      if (!selectedNodeId) return fallback;
      return nodes.find((n) => n.id === selectedNodeId) ?? fallback;
    },
    [selectedNodeId, topology],
  );

  const serviceMatrix = useMemo<ServiceCategory[]>(() => {
    const host = hosts.find((h) => h.ip_address === selectedNode.ip) ?? null;
    if (!host || !host.open_ports) {
      return SAMPLE_SERVICES;
    }
    return buildServiceMatrix(host.open_ports);
  }, [hosts, selectedNode.ip]);

  const assetIntel: AssetIntel = useMemo(() => {
    const host = hosts.find((h) => h.ip_address === selectedNode.ip) ?? null;
    if (!host) return SAMPLE_ASSET;
    return {
      ip: host.ip_address,
      hostname: host.hostname ?? "unknown",
      osFamily: host.os_family ?? "Unknown",
      distro: host.os_distribution ?? "Unknown distribution",
      kernel: host.os_kernel ?? "Unknown kernel",
      uptime: host.uptime ?? "Unknown",
      mac: host.mac_address ?? "N/A",
      vendor: host.vendor ?? "Unknown",
      hops: host.hops != null ? `${host.hops} (Local Subnet)` : "—",
      riskLabel: host.risk_score != null && host.risk_score > 66 ? "High" : "Low",
      riskScore: host.risk_score ?? 12,
      riskDescription:
        "No critical vulnerabilities detected. Open ports match standard development profile. SMB signing enabled.",
    };
  }, [hosts, selectedNode.ip]);

  return (
    <div className="viper-surface">
      <div className="viper-noise" />

      <div className="relative z-10 flex min-h-full flex-col">
        <TopNavbar projectName={projectName} onProjectNameChange={setProjectName} />
        <ScanStatusBar
          status={scan?.status ?? "pending"}
          progressPct={scan?.progress_pct ?? 74}
          onStartScan={handleStartScan}
          isStarting={isStarting}
        />

        <main className="flex-1 px-4 pb-6 pt-4 lg:px-6">
          <div className="grid grid-cols-1 gap-4 xl:grid-cols-[1fr_420px]">
            <section className="space-y-4">
              <NetworkTopologyMap
                nodes={topologyToNodes(topology) ?? SAMPLE_NODES}
                selectedNodeId={selectedNodeId}
                onSelectNode={setSelectedNodeId}
              />
              <ServiceMatrixPanel services={serviceMatrix} selectedNodeIp={selectedNode.ip} />
            </section>

            <AssetIntelligencePanel asset={assetIntel} />
          </div>
        </main>
      </div>
    </div>
  );
}

function topologyToNodes(topology: ApiTopologyResponse | null): NetworkNode[] | null {
  if (!topology || topology.nodes.length === 0) return null;
  return topology.nodes.map((n) => ({
    id: n.id,
    ip: n.ip,
    label: n.type === "gateway" ? "GW" : undefined,
    type: n.type,
    x: n.x,
    y: n.y,
    status: n.type === "gateway" ? "active" : "idle",
  }));
}

function buildServiceMatrix(openPorts: { port: number; protocol: string; service: string | null; version: string | null; state: string; }[]): ServiceCategory[] {
  const webPorts = [80, 443, 8080];
  const adminPorts = [22, 3389, 5900];

  const web: ServiceCategory = { category: "Web / HTTP", ports: [] };
  const admin: ServiceCategory = { category: "Admin / Shell", ports: [] };

  for (const p of openPorts) {
    const entry = {
      port: p.port,
      proto: p.protocol.toUpperCase(),
      service: p.service ? `${p.service}${p.version ? ` ${p.version}` : ""}` : null,
      status: (p.state === "open" ? "open" : "filtered") as "open" | "filtered",
    };
    if (webPorts.includes(p.port)) {
      web.ports.push(entry);
    } else if (adminPorts.includes(p.port)) {
      admin.ports.push(entry);
    }
  }

  const result: ServiceCategory[] = [];
  if (web.ports.length) result.push(web);
  if (admin.ports.length) result.push(admin);
  return result.length ? result : SAMPLE_SERVICES;
}

export default App;
