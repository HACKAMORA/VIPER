import { FileText, Pause, Play } from "lucide-react";
import { cn } from "../utils/cn";

type ScanStatusBarProps = {
  status: "pending" | "running" | "completed" | "failed";
  progressPct: number;
  onStartScan: () => void;
  isStarting: boolean;
};

export function ScanStatusBar({
  status,
  progressPct,
  onStartScan,
  isStarting,
}: ScanStatusBarProps) {
  const isActive = status === "running";
  const statusLabel =
    status === "running"
      ? "Active Scan"
      : status === "completed"
        ? "Scan Completed"
        : status === "failed"
          ? "Scan Failed"
          : "Idle";

  const discoveryPct = progressPct;
  const reconPct = Math.min(100, Math.max(10, Math.floor(discoveryPct * 0.6)));
  const fingerprintPct = discoveryPct > 90 ? discoveryPct : 74;

  return (
    <div className="border-b border-viper-border bg-viper-bg-primary/55">
      <div className="mx-auto flex max-w-[1500px] flex-wrap items-center gap-3 px-4 py-3 lg:px-6">
        <div className="flex items-center gap-3">
          <div className="flex items-center gap-2 rounded-full border border-viper-border bg-viper-bg-secondary/55 px-3 py-1.5">
            <span
              className={cn(
                "inline-flex h-2 w-2 rounded-full shadow-glowGreen",
                isActive
                  ? "animate-blink bg-viper-green"
                  : status === "failed"
                    ? "bg-viper-red"
                    : "bg-viper-text-muted",
              )}
            />
            <span className="text-[11px] font-semibold tracking-[0.22em] text-viper-text-muted">
              STATUS
            </span>
            <span className="text-xs font-semibold text-viper-text-primary">{statusLabel}</span>
          </div>
        </div>

        <div className="flex min-w-[420px] flex-1 items-center gap-2">
          <PipelineStep label="Reconnaissance" pct={reconPct} state="complete" />
          <PipelineStep label="Network Discovery" pct={discoveryPct} state={isActive ? "active" : "complete"} />
          <PipelineStep label="Fingerprinting" pct={fingerprintPct} state="pulsing" />
        </div>

        <div className="ml-auto flex items-center gap-2">
          <button
            type="button"
            className={cn(
              "inline-flex h-10 items-center gap-2 rounded-xl border border-viper-border bg-viper-bg-secondary/55 px-3",
              "text-viper-text-primary/90 shadow-[0_0_0_1px_rgba(255,255,255,0.02)]",
              "hover:border-viper-cyan/50 hover:shadow-glowCyan",
            )}
          >
            <Pause className="h-4 w-4 text-viper-text-muted" />
            <span className="text-xs font-semibold tracking-[0.2em] text-viper-text-muted">PAUSE</span>
          </button>

          <button
            type="button"
            onClick={onStartScan}
            className={cn(
              "inline-flex h-10 items-center gap-2 rounded-xl border border-viper-cyan/45 bg-gradient-to-b from-viper-cyan/20 to-viper-bg-secondary px-4",
              "text-sm font-bold tracking-[0.14em] text-viper-text-primary shadow-glowCyan",
              "hover:border-viper-cyan/70 hover:from-viper-cyan/25 disabled:cursor-not-allowed disabled:opacity-60",
            )}
            disabled={isStarting}
          >
            {isStarting || !isActive ? (
              <Play className="h-4 w-4 text-viper-cyan" />
            ) : (
              <FileText className="h-4 w-4 text-viper-cyan" />
            )}
            {isStarting || !isActive ? "START SCAN" : "GENERATE REPORT"}
          </button>
        </div>
      </div>
    </div>
  );
}

function PipelineStep({
  label,
  pct,
  state,
}: {
  label: string;
  pct: number;
  state: "complete" | "active" | "pulsing";
}) {
  const accent =
    state === "complete"
      ? "bg-viper-green"
      : state === "active"
        ? "bg-viper-cyan"
        : "bg-viper-cyan";

  return (
    <div className="min-w-0 flex-1">
      <div className="mb-1 flex items-center justify-between gap-2">
        <div className="truncate text-[12px] font-semibold text-viper-text-primary/90">{label}</div>
        <div
          className={cn(
            "mono text-[11px] font-semibold tracking-wide text-viper-text-muted",
            state === "pulsing" && "text-viper-cyan",
          )}
        >
          {pct}%
        </div>
      </div>
      <div className="relative h-2 overflow-hidden rounded-full border border-viper-border bg-viper-bg-secondary/45">
        <div
          className={cn(
            "h-full rounded-full",
            accent,
            state === "pulsing" && "animate-softPulse",
          )}
          style={{ width: `${pct}%` }}
        />
        {state === "active" ? (
          <div className="absolute inset-0">
            <div className="absolute inset-y-0 -left-[40%] w-[40%] animate-progressSweep bg-gradient-to-r from-transparent via-white/12 to-transparent" />
          </div>
        ) : null}
      </div>
    </div>
  );
}

