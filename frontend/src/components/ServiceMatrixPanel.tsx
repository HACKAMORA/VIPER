import { Cable, Download } from "lucide-react";
import type { ServiceCategory, ServicePort } from "../types";
import { cn } from "../utils/cn";
import { Panel } from "./ui";

export function ServiceMatrixPanel({
  services,
  selectedNodeIp,
}: {
  services: ServiceCategory[];
  selectedNodeIp: string;
}) {
  return (
    <Panel>
      <div className="flex flex-wrap items-center justify-between gap-3 border-b border-viper-border/80 px-4 py-3">
        <div className="text-sm font-bold tracking-[0.14em] text-viper-text-primary/90">
          SERVICE MATRIX <span className="text-viper-text-muted">(SELECTED NODE)</span>
          <span className="ml-2 mono text-xs text-viper-text-muted">{selectedNodeIp}</span>
        </div>
        <div className="flex items-center gap-2">
          <SmallButton icon={<Download className="h-4 w-4" />}>Export CSV</SmallButton>
          <SmallButton icon={<Cable className="h-4 w-4" />}>Raw TCP</SmallButton>
        </div>
      </div>

      <div className="space-y-4 px-4 py-4">
        {services.map((cat) => (
          <div key={cat.category} className="grid grid-cols-1 gap-3 md:grid-cols-[160px_1fr]">
            <div className="text-xs font-bold tracking-[0.22em] text-viper-text-muted">
              {cat.category}
            </div>
            <div className="flex flex-wrap gap-2">
              {cat.ports.map((p) => (
                <PortBadge key={`${p.port}-${p.proto}`} port={p} />
              ))}
            </div>
          </div>
        ))}
      </div>
    </Panel>
  );
}

function SmallButton({ children, icon }: { children: string; icon: React.ReactNode }) {
  return (
    <button
      type="button"
      className={cn(
        "inline-flex h-8 items-center gap-2 rounded-lg border border-viper-border bg-viper-bg-secondary/45 px-3",
        "text-xs font-semibold tracking-wide text-viper-text-muted",
        "hover:border-viper-cyan/40 hover:text-viper-text-primary",
      )}
    >
      {icon}
      {children}
    </button>
  );
}

function PortBadge({ port }: { port: ServicePort }) {
  const isOpen = port.status === "open";
  const base = cn(
    "group inline-flex items-center gap-2 rounded-full border px-3 py-1 text-xs font-bold tracking-wide",
    "transition",
  );

  const tone = isOpen
    ? port.port === 443
      ? "border-viper-cyan/40 bg-viper-cyan/10 text-viper-cyan"
      : "border-viper-green/40 bg-viper-green/10 text-viper-green"
    : "border-viper-border bg-viper-bg-secondary/40 text-viper-text-muted opacity-70";

  return (
    <div className={cn(base, tone, "hover:shadow-glowCyan")}>
      <span className="mono">
        {port.port}/{port.proto}
      </span>
      <span className="text-viper-text-primary/80 group-hover:text-viper-text-primary">
        {port.service ?? "—"}
      </span>
    </div>
  );
}

