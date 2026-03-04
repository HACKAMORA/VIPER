import type { Config } from "tailwindcss";

export default {
  content: ["./index.html", "./src/**/*.{ts,tsx}"],
  theme: {
    extend: {
      fontFamily: {
        display: ["Rajdhani", "system-ui", "sans-serif"],
        mono: ["JetBrains Mono", "ui-monospace", "SFMono-Regular", "Menlo", "monospace"],
      },
      colors: {
        viper: {
          bg: {
            primary: "var(--bg-primary)",
            secondary: "var(--bg-secondary)",
            panel: "var(--bg-panel)",
          },
          border: "var(--border)",
          cyan: "var(--accent-cyan)",
          green: "var(--accent-green)",
          red: "var(--accent-red)",
          purple: "var(--accent-purple)",
          text: {
            primary: "var(--text-primary)",
            muted: "var(--text-muted)",
            data: "var(--text-data)",
          },
        },
      },
      boxShadow: {
        glowCyan: "0 0 0 1px rgba(0, 212, 255, 0.35), 0 0 22px rgba(0, 212, 255, 0.18)",
        glowGreen: "0 0 0 1px rgba(0, 255, 136, 0.35), 0 0 22px rgba(0, 255, 136, 0.18)",
      },
      keyframes: {
        scanline: {
          "0%": { transform: "translateY(-20%)" },
          "100%": { transform: "translateY(120%)" },
        },
        softPulse: {
          "0%, 100%": { opacity: "0.55" },
          "50%": { opacity: "1" },
        },
        blink: {
          "0%, 100%": { opacity: "1" },
          "50%": { opacity: "0.25" },
        },
        progressSweep: {
          "0%": { transform: "translateX(-60%)" },
          "100%": { transform: "translateX(110%)" },
        },
        dashRotate: {
          "0%": { strokeDashoffset: "0" },
          "100%": { strokeDashoffset: "-28" },
        },
        ripple: {
          "0%": { transform: "scale(0.9)", opacity: "0.55" },
          "70%": { transform: "scale(1.35)", opacity: "0.05" },
          "100%": { transform: "scale(1.35)", opacity: "0" },
        },
        riseFade: {
          "0%": { opacity: "0", transform: "translateY(6px)" },
          "100%": { opacity: "1", transform: "translateY(0)" },
        },
      },
      animation: {
        scanline: "scanline 4.2s linear infinite",
        softPulse: "softPulse 1.7s ease-in-out infinite",
        blink: "blink 1.2s ease-in-out infinite",
        progressSweep: "progressSweep 1.4s ease-in-out infinite",
        dashRotate: "dashRotate 1.2s linear infinite",
        ripple: "ripple 2.2s ease-out infinite",
        riseFade: "riseFade 520ms ease-out both",
      },
    },
  },
  plugins: [],
} satisfies Config;

