import { cn } from "../utils/cn";

export function RiskScoreGauge({
  score,
  color = "green",
}: {
  score: number;
  color?: "green" | "cyan" | "red";
}) {
  const cl =
    color === "red" ? "bg-viper-red" : color === "cyan" ? "bg-viper-cyan" : "bg-viper-green";

  return (
    <div className="mt-2">
      <div className="relative h-2 overflow-hidden rounded-full border border-viper-border bg-viper-bg-secondary/55">
        <div
          className={cn("h-full rounded-full transition-[width] duration-700 ease-out", cl)}
          style={{ width: `${Math.max(0, Math.min(100, score))}%` }}
        />
        <div className="pointer-events-none absolute inset-0">
          <div className="absolute inset-y-0 -left-[35%] w-[35%] animate-progressSweep bg-gradient-to-r from-transparent via-white/10 to-transparent" />
        </div>
      </div>
    </div>
  );
}

