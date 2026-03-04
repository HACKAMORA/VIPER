import { Panel } from "./ui";

export function NodeLegend() {
  return (
    <Panel className="w-[220px] px-4 py-3">
      <div className="mb-2 text-[11px] font-bold tracking-[0.22em] text-viper-text-muted">
        NODE TYPES
      </div>
      <ul className="space-y-2 text-sm">
        <LegendRow colorClass="bg-viper-cyan" label="Gateway / Router" />
        <LegendRow colorClass="bg-viper-purple" label="Server / Infrastructure" />
        <LegendRow colorClass="bg-viper-text-muted" label="Workstation / Endpoint" />
      </ul>
    </Panel>
  );
}

function LegendRow({ colorClass, label }: { colorClass: string; label: string }) {
  return (
    <li className="flex items-center gap-2 text-[12px] font-semibold text-viper-text-primary/90">
      <span className={`h-2 w-2 rounded-full ${colorClass}`} />
      <span>{label}</span>
    </li>
  );
}

