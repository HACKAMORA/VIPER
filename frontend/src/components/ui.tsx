import type { PropsWithChildren } from "react";
import { cn } from "../utils/cn";

export function Panel({
  className,
  children,
}: PropsWithChildren<{
  className?: string;
}>) {
  return (
    <div
      className={cn(
        "relative overflow-hidden rounded-xl border border-viper-border bg-viper-bg-panel/90 shadow-[0_0_0_1px_rgba(255,255,255,0.03)]",
        "backdrop-blur supports-[backdrop-filter]:bg-viper-bg-panel/75",
        className,
      )}
    >
      {children}
    </div>
  );
}

export function SectionHeader({
  title,
  right,
}: {
  title: string;
  right?: React.ReactNode;
}) {
  return (
    <div className="flex items-center justify-between gap-3 border-b border-viper-border/80 px-4 py-3">
      <div className="flex items-center gap-2">
        <div className="h-1.5 w-1.5 rounded-full bg-viper-green shadow-glowGreen" />
        <h2 className="text-sm font-semibold tracking-[0.18em] text-viper-text-primary/90">
          {title}
        </h2>
      </div>
      {right}
    </div>
  );
}

export function Pill({
  className,
  children,
}: PropsWithChildren<{
  className?: string;
}>) {
  return (
    <span
      className={cn(
        "inline-flex items-center gap-2 rounded-full border border-viper-border bg-viper-bg-secondary/55 px-3 py-1 text-xs font-semibold tracking-wide text-viper-text-primary/90",
        className,
      )}
    >
      {children}
    </span>
  );
}

