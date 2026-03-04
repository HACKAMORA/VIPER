import { Maximize2, Minus, Plus } from "lucide-react";
import { useCallback, useEffect, useMemo, useRef, useState } from "react";
import type { NetworkNode } from "../types";
import { cn } from "../utils/cn";
import { NodeLegend } from "./NodeLegend";
import { Panel } from "./ui";

type TooltipState =
  | { open: false }
  | { open: true; x: number; y: number; node: NetworkNode; statusText: string };

const VIEW_W = 800;
const VIEW_H = 520;

export function NetworkTopologyMap({
  nodes,
  selectedNodeId,
  onSelectNode,
}: {
  nodes: NetworkNode[];
  selectedNodeId: string | null;
  onSelectNode: (id: string) => void;
}) {
  const containerRef = useRef<HTMLDivElement | null>(null);
  const svgRef = useRef<SVGSVGElement | null>(null);
  const [zoom, setZoom] = useState(1);
  const [layout, setLayout] = useState<NetworkNode[]>(nodes);
  const [tooltip, setTooltip] = useState<TooltipState>({ open: false });
  const dragRef = useRef<{
    id: string;
    dx: number;
    dy: number;
    pointerId: number;
  } | null>(null);

  useEffect(() => setLayout(nodes), [nodes]);

  const edges = useMemo(() => {
    const gw = layout.find((n) => n.type === "gateway") ?? layout[0];
    if (!gw) return [];
    return layout
      .filter((n) => n.id !== gw.id)
      .map((n) => ({ from: gw.id, to: n.id }));
  }, [layout]);

  const nodeById = useMemo(() => {
    const m = new Map<string, NetworkNode>();
    for (const n of layout) m.set(n.id, n);
    return m;
  }, [layout]);

  const setZoomClamped = useCallback((next: number) => {
    setZoom(Math.max(0.85, Math.min(1.65, Math.round(next * 100) / 100)));
  }, []);

  const toSvgPoint = useCallback((clientX: number, clientY: number) => {
    const svg = svgRef.current;
    if (!svg) return null;
    const pt = svg.createSVGPoint();
    pt.x = clientX;
    pt.y = clientY;
    const ctm = svg.getScreenCTM();
    if (!ctm) return null;
    return pt.matrixTransform(ctm.inverse());
  }, []);

  const onPointerDownNode = useCallback(
    (e: React.PointerEvent, node: NetworkNode) => {
      const pt = toSvgPoint(e.clientX, e.clientY);
      if (!pt) return;
      (e.currentTarget as SVGGElement).setPointerCapture(e.pointerId);
      dragRef.current = {
        id: node.id,
        dx: node.x - pt.x,
        dy: node.y - pt.y,
        pointerId: e.pointerId,
      };
    },
    [toSvgPoint],
  );

  const onPointerMove = useCallback(
    (e: React.PointerEvent) => {
      if (!dragRef.current) return;
      const pt = toSvgPoint(e.clientX, e.clientY);
      if (!pt) return;
      const { id, dx, dy } = dragRef.current;
      setLayout((prev) =>
        prev.map((n) =>
          n.id === id
            ? {
                ...n,
                x: Math.max(40, Math.min(VIEW_W - 40, pt.x + dx)),
                y: Math.max(40, Math.min(VIEW_H - 40, pt.y + dy)),
              }
            : n,
        ),
      );
    },
    [toSvgPoint],
  );

  const onPointerUp = useCallback(() => {
    dragRef.current = null;
  }, []);

  const toggleFullscreen = useCallback(async () => {
    const el = containerRef.current;
    if (!el) return;
    if (document.fullscreenElement) {
      await document.exitFullscreen();
      return;
    }
    await el.requestFullscreen();
  }, []);

  return (
    <Panel className="relative">
      <div className="flex items-center justify-between border-b border-viper-border/80 px-4 py-3">
        <div className="flex items-center gap-2">
          <div className="h-2 w-2 rounded-full bg-viper-cyan shadow-glowCyan" />
          <div className="text-sm font-bold tracking-[0.14em] text-viper-text-primary/90">
            NETWORK DISCOVERY
          </div>
          <div className="mono text-xs font-semibold text-viper-text-muted">74% Fingerprinting</div>
        </div>
        <div className="mono text-xs font-semibold text-viper-text-muted">Interactive Topology</div>
      </div>

      <div ref={containerRef} className="relative h-[520px] w-full">
        <svg
          ref={svgRef}
          viewBox={`0 0 ${VIEW_W} ${VIEW_H}`}
          className="h-full w-full"
          onPointerMove={onPointerMove}
          onPointerUp={onPointerUp}
          onPointerCancel={onPointerUp}
          onPointerLeave={() => setTooltip({ open: false })}
        >
          <defs>
            <linearGradient id="viperLine" x1="0" y1="0" x2="1" y2="1">
              <stop offset="0" stopColor="rgba(0,212,255,0.16)" />
              <stop offset="1" stopColor="rgba(148,163,184,0.14)" />
            </linearGradient>
            <filter id="softGlow" x="-30%" y="-30%" width="160%" height="160%">
              <feGaussianBlur stdDeviation="2.6" result="b" />
              <feColorMatrix
                in="b"
                type="matrix"
                values="1 0 0 0 0  0 1 0 0 0  0 0 1 0 0  0 0 0 0.55 0"
                result="g"
              />
              <feMerge>
                <feMergeNode in="g" />
                <feMergeNode in="SourceGraphic" />
              </feMerge>
            </filter>
          </defs>

          <g
            transform={zoomTransform(zoom)}
            style={{ transformOrigin: "center", transformBox: "fill-box" }}
          >
            {edges.map((e) => {
              const a = nodeById.get(e.from);
              const b = nodeById.get(e.to);
              if (!a || !b) return null;
              return (
                <line
                  key={`${e.from}-${e.to}`}
                  x1={a.x}
                  y1={a.y}
                  x2={b.x}
                  y2={b.y}
                  stroke="url(#viperLine)"
                  strokeWidth={1.2}
                  opacity={0.9}
                />
              );
            })}

            {layout.map((n) => (
              <NodeGlyph
                key={n.id}
                node={n}
                selected={n.id === selectedNodeId}
                onSelect={() => onSelectNode(n.id)}
                onPointerDown={onPointerDownNode}
                onHover={(ev, statusText) => {
                  const rect = (containerRef.current ?? document.body).getBoundingClientRect();
                  setTooltip({
                    open: true,
                    x: ev.clientX - rect.left,
                    y: ev.clientY - rect.top,
                    node: n,
                    statusText,
                  });
                }}
                onLeave={() => setTooltip({ open: false })}
              />
            ))}
          </g>
        </svg>

        <div className="absolute bottom-4 left-4">
          <NodeLegend />
        </div>

        <div className="absolute bottom-4 right-4 flex flex-col gap-2">
          <MapButton onClick={() => setZoomClamped(zoom + 0.1)} label="Zoom in">
            <Plus className="h-4 w-4" />
          </MapButton>
          <MapButton onClick={() => setZoomClamped(zoom - 0.1)} label="Zoom out">
            <Minus className="h-4 w-4" />
          </MapButton>
          <MapButton onClick={toggleFullscreen} label="Fullscreen">
            <Maximize2 className="h-4 w-4" />
          </MapButton>
        </div>

        {tooltip.open ? (
          <div
            className={cn(
              "pointer-events-none absolute z-10 min-w-[180px] rounded-lg border border-viper-border bg-viper-bg-panel/95 px-3 py-2",
              "shadow-[0_0_0_1px_rgba(0,212,255,0.12)]",
            )}
            style={{
              left: Math.min(tooltip.x + 12, (containerRef.current?.clientWidth ?? 800) - 200),
              top: Math.max(tooltip.y - 10, 12),
            }}
          >
            <div className="mono text-sm font-bold text-viper-text-primary">{tooltip.node.ip}</div>
            <div className="text-xs font-semibold text-viper-text-muted">{tooltip.statusText}</div>
          </div>
        ) : null}
      </div>
    </Panel>
  );
}

function MapButton({
  children,
  label,
  onClick,
}: {
  children: React.ReactNode;
  label: string;
  onClick: () => void;
}) {
  return (
    <button
      type="button"
      aria-label={label}
      onClick={onClick}
      className={cn(
        "grid h-9 w-9 place-items-center rounded-lg border border-viper-border bg-viper-bg-secondary/60",
        "text-viper-text-muted shadow-[0_0_0_1px_rgba(255,255,255,0.02)]",
        "hover:border-viper-cyan/45 hover:text-viper-text-primary hover:shadow-glowCyan",
      )}
    >
      {children}
    </button>
  );
}

function zoomTransform(z: number) {
  const cx = VIEW_W / 2;
  const cy = VIEW_H / 2;
  const tx = (1 - z) * cx;
  const ty = (1 - z) * cy;
  return `translate(${tx} ${ty}) scale(${z})`;
}

function NodeGlyph({
  node,
  selected,
  onSelect,
  onPointerDown,
  onHover,
  onLeave,
}: {
  node: NetworkNode;
  selected: boolean;
  onSelect: () => void;
  onPointerDown: (e: React.PointerEvent, node: NetworkNode) => void;
  onHover: (e: React.PointerEvent, statusText: string) => void;
  onLeave: () => void;
}) {
  const tone =
    node.type === "gateway"
      ? { fill: "rgba(0,212,255,0.12)", stroke: "rgba(0,212,255,0.65)" }
      : node.type === "server"
        ? { fill: "rgba(168,85,247,0.14)", stroke: "rgba(168,85,247,0.65)" }
        : { fill: "rgba(148,163,184,0.10)", stroke: "rgba(148,163,184,0.55)" };

  const r = node.type === "gateway" ? 34 : 26;
  const label = `${node.ip}${node.label ? ` (${node.label})` : ""}`;
  const statusText = node.status === "active" ? "Active · Local Subnet" : "Discovered node";

  return (
    <g
      role="button"
      tabIndex={0}
      transform={`translate(${node.x} ${node.y})`}
      onClick={onSelect}
      onPointerDown={(e) => onPointerDown(e, node)}
      onPointerEnter={(e) => onHover(e, statusText)}
      onPointerMove={(e) => onHover(e, statusText)}
      onPointerLeave={onLeave}
      style={{ cursor: "grab" }}
    >
      {node.type === "gateway" ? (
        <circle
          r={r + 10}
          fill="none"
          stroke="rgba(0,255,136,0.22)"
          strokeWidth={1.5}
          style={{ transformBox: "fill-box", transformOrigin: "center" }}
          className="animate-ripple"
        />
      ) : null}

      {selected ? (
        <circle
          r={r + 10}
          fill="none"
          stroke="rgba(0,212,255,0.75)"
          strokeWidth={2}
          strokeDasharray="7 5"
          className="animate-dashRotate"
          filter="url(#softGlow)"
        />
      ) : null}

      <circle r={r} fill={tone.fill} stroke={tone.stroke} strokeWidth={2} filter="url(#softGlow)" />

      {node.type === "server" ? (
        <rect
          x={-16}
          y={-16}
          width={32}
          height={32}
          rx={6}
          fill={tone.fill}
          stroke={tone.stroke}
          strokeWidth={1.8}
        />
      ) : null}

      <GlyphIcon type={node.type} />

      {node.type === "gateway" && node.status === "active" ? (
        <circle cx={r - 8} cy={-(r - 8)} r={4} fill="rgba(0,255,136,1)" />
      ) : null}

      <text
        y={r + 22}
        textAnchor="middle"
        className="mono"
        fontSize={12}
        fill="rgba(148,163,184,0.95)"
      >
        {label}
      </text>
    </g>
  );
}

function GlyphIcon({ type }: { type: NetworkNode["type"] }) {
  const stroke = "rgba(226,232,240,0.85)";
  const thin = 1.6;

  if (type === "gateway") {
    return (
      <g fill="none" stroke={stroke} strokeWidth={thin} strokeLinecap="round">
        <path d="M-14 6 Q0 -8 14 6" opacity={0.85} />
        <path d="M-10 9 Q0 0 10 9" opacity={0.75} />
        <path d="M-6 12 Q0 7 6 12" opacity={0.65} />
        <circle cx="0" cy="14" r="1.8" fill={stroke} stroke="none" />
      </g>
    );
  }

  if (type === "server") {
    return (
      <g fill="none" stroke={stroke} strokeWidth={thin} strokeLinecap="round">
        <path d="M-9 -6 H9" />
        <path d="M-9 -1 H9" opacity={0.85} />
        <path d="M-9 4 H9" opacity={0.7} />
        <circle cx="-9" cy="-6" r="1.2" fill={stroke} stroke="none" />
        <circle cx="-9" cy="-1" r="1.2" fill={stroke} stroke="none" opacity={0.9} />
        <circle cx="-9" cy="4" r="1.2" fill={stroke} stroke="none" opacity={0.8} />
      </g>
    );
  }

  if (type === "printer") {
    return (
      <g fill="none" stroke={stroke} strokeWidth={thin} strokeLinejoin="round">
        <path d="M-10 -2 H10 V8 H-10 Z" opacity={0.85} />
        <path d="M-8 -8 H8 V-2 H-8 Z" opacity={0.75} />
        <path d="M-6 2 H6" opacity={0.8} />
      </g>
    );
  }

  if (type === "mobile") {
    return (
      <g fill="none" stroke={stroke} strokeWidth={thin} strokeLinejoin="round">
        <rect x={-7} y={-12} width={14} height={24} rx={3} opacity={0.85} />
        <circle cx="0" cy="9" r="1.4" fill={stroke} stroke="none" opacity={0.85} />
      </g>
    );
  }

  // workstation
  return (
    <g fill="none" stroke={stroke} strokeWidth={thin} strokeLinejoin="round">
      <rect x={-12} y={-10} width={24} height={16} rx={3} opacity={0.85} />
      <path d="M-6 10 H6" opacity={0.75} />
      <path d="M-2 6 V10" opacity={0.7} />
      <path d="M2 6 V10" opacity={0.7} />
    </g>
  );
}

