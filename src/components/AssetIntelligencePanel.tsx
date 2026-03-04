import { Cpu, Download, Settings2 } from "lucide-react";
import type { AssetIntel } from "../types";
import { cn } from "../utils/cn";
import { RiskScoreGauge } from "./RiskScoreGauge";
import { Panel, SectionHeader } from "./ui";
export function AssetIntelligencePanel({ asset }: { asset: AssetIntel }) {
  return (
    <aside className="xl:sticky xl:top-[118px] xl:self-start">
      <Panel className="overflow-hidden">
        <SectionHeader
          title="ASSET INTELLIGENCE"
          right={<div className="h-2 w-2 rounded-full bg-viper-green shadow-glowGreen" />}
        />

        <div className="space-y-4 px-4 py-4">
          <div className="space-y-2">
            <Row label="IP Address" value={<span className="mono font-bold">{asset.ip}</span>} i={0} />
            <Row label="Hostname" value={asset.hostname} i={1} />
          </div>

          <SectionTitle title="SYSTEM ARCHITECTURE" i={2} />
          <div className="space-y-2">
            <Row
              label="OS Family"
              value={
                <span className="inline-flex items-center gap-2">
                  <Cpu className="h-4 w-4 text-viper-text-muted" />
                  {asset.osFamily}
                </span>
              }
              i={3}
            />
            <Row label="Distribution" value={asset.distro} i={4} />
            <Row label="Kernel" value={asset.kernel} i={5} />
            <Row
              label="Uptime"
              value={<span className="mono font-semibold text-viper-cyan">{asset.uptime}</span>}
              i={6}
            />
          </div>

          <SectionTitle title="NETWORK INTERFACE" i={7} />
          <div className="space-y-2">
            <Row label="MAC Address" value={<span className="mono">{asset.mac}</span>} i={8} />
            <Row label="Vendor" value={asset.vendor} i={9} />
            <Row label="Hops" value={asset.hops} i={10} />
          </div>

          <SectionTitle title="RISK ANALYSIS" i={11} />
          <div className="space-y-2">
            <div
              className={cn(
                "flex items-baseline justify-between gap-3",
                "animate-riseFade [animation-delay:220ms]",
              )}
            >
              <div className="text-sm font-semibold text-viper-text-primary/90">Risk Score</div>
              <div className="mono text-sm font-bold text-viper-green">
                {asset.riskLabel} ({asset.riskScore}/100)
              </div>
            </div>
            <div className="animate-riseFade [animation-delay:260ms]">
              <RiskScoreGauge score={asset.riskScore} color="green" />
            </div>
            <p className="text-sm leading-relaxed text-viper-text-muted animate-riseFade [animation-delay:320ms]">
              {asset.riskDescription}
            </p>
          </div>

          <div className="pt-2">
            <button
              type="button"
              className={cn(
                "mt-2 inline-flex w-full items-center justify-center gap-2 rounded-xl border border-viper-cyan/45 bg-transparent px-4 py-2.5",
                "text-sm font-bold tracking-[0.12em] text-viper-cyan",
                "hover:bg-viper-cyan/5 hover:shadow-glowCyan",
              )}
            >
              <Settings2 className="h-4 w-4" />
              Initiate Vuln Scan
            </button>
            <button
              type="button"
              className={cn(
                "mt-2 inline-flex w-full items-center justify-center gap-2 rounded-xl border border-viper-border bg-transparent px-4 py-2.5",
                "text-sm font-bold tracking-[0.12em] text-viper-text-muted",
                "hover:border-viper-cyan/40 hover:text-viper-text-primary",
              )}
            >
              <Download className="h-4 w-4" />
              Export Node Data
            </button>
          </div>
        </div>
      </Panel>
    </aside>
  );
}

function SectionTitle({ title, i }: { title: string; i: number }) {
  return (
    <div
      className={cn(
        "pt-1 text-[11px] font-bold tracking-[0.22em] text-viper-text-muted",
        "animate-riseFade",
      )}
      style={{ animationDelay: `${80 + i * 20}ms` }}
    >
      {title}
    </div>
  );
}

function Row({
  label,
  value,
  i,
}: {
  label: string;
  value: React.ReactNode;
  i: number;
}) {
  return (
    <div
      className={cn(
        "flex items-start justify-between gap-6 rounded-lg border border-transparent px-2 py-1.5",
        "hover:border-viper-border hover:bg-viper-bg-secondary/35",
        "animate-riseFade",
      )}
      style={{ animationDelay: `${80 + i * 28}ms` }}
    >
      <div className="text-xs font-semibold tracking-wide text-viper-text-muted">{label}</div>
      <div className="text-right text-sm font-semibold text-viper-text-primary/90">{value}</div>
    </div>
  );
}

