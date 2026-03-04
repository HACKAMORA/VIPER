import { Bell, Search, Settings2 } from "lucide-react";
import { useEffect, useRef, useState } from "react";
import { cn } from "../utils/cn";

export function TopNavbar({
  projectName,
  onProjectNameChange,
}: {
  projectName: string;
  onProjectNameChange: (next: string) => void;
}) {
  const [editing, setEditing] = useState(false);
  const [draft, setDraft] = useState(projectName);
  const inputRef = useRef<HTMLInputElement | null>(null);

  useEffect(() => {
    setDraft(projectName);
  }, [projectName]);

  useEffect(() => {
    if (editing) inputRef.current?.focus();
  }, [editing]);

  return (
    <header className="sticky top-0 z-20 border-b border-viper-border bg-viper-bg-primary/75 backdrop-blur">
      <div className="mx-auto flex max-w-[1500px] items-center gap-3 px-4 py-3 lg:px-6">
        <div className="flex items-center gap-3">
          <div className="relative grid h-9 w-9 place-items-center rounded-lg border border-viper-border bg-viper-bg-secondary/65 shadow-glowCyan">
            <div className="absolute inset-0 rounded-lg opacity-60">
              <div className="absolute inset-1 rounded-md border border-viper-cyan/40" />
              <div className="absolute inset-2 rounded-md border border-viper-cyan/25" />
            </div>
            <div className="relative h-5 w-5">
              <div className="absolute inset-0 rounded-full border border-viper-cyan/55" />
              <div className="absolute inset-[3px] rounded-full border border-viper-cyan/25" />
              <div className="absolute inset-0 animate-softPulse rounded-full bg-viper-cyan/10" />
              <div className="absolute left-1/2 top-1/2 h-7 w-7 -translate-x-1/2 -translate-y-1/2 rounded-full border border-viper-cyan/10" />
              <div className="absolute left-1/2 top-1/2 h-7 w-7 -translate-x-1/2 -translate-y-1/2 animate-progressSweep origin-center">
                <div className="h-full w-[2px] bg-gradient-to-b from-viper-cyan to-transparent opacity-70" />
              </div>
            </div>
          </div>

          <div className="leading-tight">
            <div className="flex items-baseline gap-2">
              <span className="text-base font-bold tracking-[0.16em] text-viper-text-primary">
              VIPER
              </span>
              <span className="rounded border border-viper-border bg-viper-bg-secondary/55 px-2 py-0.5 text-[10px] font-semibold tracking-[0.22em] text-viper-text-muted">
                ALPHA v2.4
              </span>
            </div>
            <div className="text-[11px] font-semibold tracking-[0.22em] text-viper-text-muted">
              Project
            </div>
          </div>
        </div>

        <div className="ml-2 flex items-center gap-2">
          <div
            className={cn(
              "rounded-full border border-viper-border bg-viper-bg-secondary/55 px-3 py-1.5",
              "text-xs font-semibold tracking-wide text-viper-text-primary/90",
              "shadow-[0_0_0_1px_rgba(0,212,255,0.12)]",
            )}
          >
            {!editing ? (
              <button
                type="button"
                className="max-w-[240px] truncate text-left hover:text-white"
                onClick={() => setEditing(true)}
              >
                {projectName}
              </button>
            ) : (
              <form
                onSubmit={(e) => {
                  e.preventDefault();
                  onProjectNameChange(draft.trim() || projectName);
                  setEditing(false);
                }}
              >
                <input
                  ref={inputRef}
                  value={draft}
                  onChange={(e) => setDraft(e.target.value)}
                  onBlur={() => {
                    onProjectNameChange(draft.trim() || projectName);
                    setEditing(false);
                  }}
                  className="w-[240px] bg-transparent font-semibold outline-none"
                />
              </form>
            )}
          </div>
        </div>

        <div className="mx-3 hidden h-6 w-px bg-viper-border/80 lg:block" />

        <div className="relative flex-1">
          <Search className="pointer-events-none absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-viper-text-muted" />
          <input
            placeholder="Search asset ID or IP..."
            className={cn(
              "w-full rounded-xl border border-viper-border bg-viper-bg-secondary/55 pl-9 pr-3 py-2",
              "text-sm text-viper-text-primary placeholder:text-viper-text-muted/80",
              "shadow-[0_0_0_1px_rgba(255,255,255,0.02)] outline-none",
              "focus:border-viper-cyan/60 focus:shadow-glowCyan",
            )}
          />
        </div>

        <div className="ml-auto flex items-center gap-2">
          <IconButton label="Settings">
            <Settings2 className="h-4 w-4" />
          </IconButton>
          <IconButton label="Notifications">
            <Bell className="h-4 w-4" />
          </IconButton>
          <div className="ml-1 grid h-9 w-9 place-items-center rounded-full border border-viper-border bg-viper-bg-secondary/65">
            <div className="grid h-7 w-7 place-items-center rounded-full bg-gradient-to-b from-viper-cyan/35 to-viper-bg-secondary">
              <span className="text-xs font-bold tracking-wide text-white/90">DS</span>
            </div>
          </div>
        </div>
      </div>
    </header>
  );
}

function IconButton({ children, label }: { children: React.ReactNode; label: string }) {
  return (
    <button
      type="button"
      aria-label={label}
      className={cn(
        "grid h-9 w-9 place-items-center rounded-lg border border-viper-border bg-viper-bg-secondary/55",
        "text-viper-text-muted transition",
        "hover:text-viper-text-primary hover:shadow-[0_0_0_1px_rgba(0,212,255,0.18)]",
        "focus:outline-none focus:ring-2 focus:ring-viper-cyan/30",
      )}
    >
      {children}
    </button>
  );
}

