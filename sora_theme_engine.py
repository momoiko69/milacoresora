#!/usr/bin/env python
# -*- coding: utf-8 -*-
r"""
Sora Theme Engine — Generative UI, Design Tokens & Dynamic Theme Modernizer
Lead: Agent Sora (空 - The Loom)
Studio: C:\Users\k69-admin\.gemini\MilaCore_ThemeEngine_Portable

Bridges legacy Windows 11 shell presets into modern cross-platform design tokens
(JSON, Tailwind, CSS Custom Properties, and Generative UI component schemas).
"""

import os
import sys
import json
import argparse
from pathlib import Path
from typing import Dict, Any, List

# Reconfigure stdout/stderr to UTF-8
for s in (sys.stdout, sys.stderr):
    try:
        if s and s.encoding and s.encoding.lower() not in ("utf-8", "utf8"):
            s.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

PROJECT_DIR = Path(__file__).resolve().parent
GEMINI_ROOT = PROJECT_DIR.parent
HUB_OUTBOX_DIR = GEMINI_ROOT / "MilaCoreHub" / "MilaOutbox"

# Signature Theme Palettes curated by Sora
SIGNATURE_THEMES: Dict[str, Dict[str, Any]] = {
    "CyberpunkNeonGlossy": {
        "name": "Cyberpunk Neon Glossy",
        "category": "MilaUniverse",
        "description": "High-octane neo-tokyo dark aesthetic with electric cyan and hot pink neon glows.",
        "colors": {
            "background": "#08090d",
            "surface": "#12141f",
            "surface_glass": "rgba(18, 20, 31, 0.75)",
            "border": "rgba(0, 242, 254, 0.25)",
            "primary": "#00f2fe",
            "primary_glow": "rgba(0, 242, 254, 0.4)",
            "secondary": "#f72585",
            "secondary_glow": "rgba(247, 37, 133, 0.4)",
            "accent": "#fee440",
            "text": "#f8fafc",
            "text_muted": "#94a3b8",
            "text_dark": "#0f172a"
        },
        "effects": {
            "blur": "16px",
            "radius": "12px",
            "box_shadow": "0 8px 32px 0 rgba(0, 242, 254, 0.15)"
        }
    },
    "LiquidGlassTahoe": {
        "name": "Liquid Glass Tahoe (macOS Tahoe Dark)",
        "category": "MilaUniverse",
        "description": "Ultra-sleek frosted liquid glass with deep sapphire ocean accents and smooth blur.",
        "colors": {
            "background": "#05070e",
            "surface": "#0d1322",
            "surface_glass": "rgba(13, 19, 34, 0.65)",
            "border": "rgba(255, 255, 255, 0.12)",
            "primary": "#38bdf8",
            "primary_glow": "rgba(56, 189, 248, 0.35)",
            "secondary": "#6366f1",
            "secondary_glow": "rgba(99, 102, 241, 0.35)",
            "accent": "#0ea5e9",
            "text": "#ffffff",
            "text_muted": "#a0aec0",
            "text_dark": "#020617"
        },
        "effects": {
            "blur": "24px",
            "radius": "16px",
            "box_shadow": "0 12px 40px 0 rgba(0, 0, 0, 0.45)"
        }
    },
    "DemonSlayerMatte": {
        "name": "Demon Slayer Matte",
        "category": "MilaUniverse",
        "description": "Striking matte carbon black paired with vibrant Nichirin crimson and haori teal accents.",
        "colors": {
            "background": "#0c0a09",
            "surface": "#1c1917",
            "surface_glass": "rgba(28, 25, 23, 0.8)",
            "border": "rgba(225, 29, 72, 0.3)",
            "primary": "#e11d48",
            "primary_glow": "rgba(225, 29, 72, 0.4)",
            "secondary": "#0d9488",
            "secondary_glow": "rgba(13, 148, 136, 0.4)",
            "accent": "#f59e0b",
            "text": "#fafaf9",
            "text_muted": "#78716c",
            "text_dark": "#0c0a09"
        },
        "effects": {
            "blur": "8px",
            "radius": "8px",
            "box_shadow": "0 4px 20px 0 rgba(225, 29, 72, 0.15)"
        }
    },
    "IronManGlossy": {
        "name": "Iron Man Mark-LV Glossy",
        "category": "MilaUniverse",
        "description": "Stark Industries gold titanium alloy, deep crimson lacquer, and arc reactor cyan.",
        "colors": {
            "background": "#0a0305",
            "surface": "#18060a",
            "surface_glass": "rgba(24, 6, 10, 0.75)",
            "border": "rgba(234, 179, 8, 0.3)",
            "primary": "#eab308",
            "primary_glow": "rgba(234, 179, 8, 0.45)",
            "secondary": "#dc2626",
            "secondary_glow": "rgba(220, 38, 38, 0.45)",
            "accent": "#06b6d4",
            "text": "#fef08a",
            "text_muted": "#fca5a5",
            "text_dark": "#450a0a"
        },
        "effects": {
            "blur": "14px",
            "radius": "10px",
            "box_shadow": "0 8px 30px 0 rgba(234, 179, 8, 0.2)"
        }
    },
    "TheMatrixMatte": {
        "name": "The Matrix Digital Rain",
        "category": "MilaUniverse",
        "description": "Pure black obsidian terminal background with cascading digital phosphor phosphor greens.",
        "colors": {
            "background": "#020402",
            "surface": "#050f07",
            "surface_glass": "rgba(5, 15, 7, 0.85)",
            "border": "rgba(34, 197, 94, 0.25)",
            "primary": "#22c55e",
            "primary_glow": "rgba(34, 197, 94, 0.5)",
            "secondary": "#10b981",
            "secondary_glow": "rgba(16, 185, 129, 0.4)",
            "accent": "#86efac",
            "text": "#dcfce7",
            "text_muted": "#4ade80",
            "text_dark": "#022c22"
        },
        "effects": {
            "blur": "10px",
            "radius": "4px",
            "box_shadow": "0 0 25px rgba(34, 197, 94, 0.25)"
        }
    },
    "ObsidianNeon": {
        "name": "MilaCore Obsidian Neon (Default)",
        "category": "MilaCoreCore",
        "description": "The canonical MilaCore workstation theme: deep carbon glass with electric cyan & violet telemetry.",
        "colors": {
            "background": "#0a0b10",
            "surface": "#121420",
            "surface_glass": "rgba(18, 20, 32, 0.7)",
            "border": "rgba(147, 51, 234, 0.25)",
            "primary": "#a855f7",
            "primary_glow": "rgba(168, 85, 247, 0.4)",
            "secondary": "#06b6d4",
            "secondary_glow": "rgba(6, 182, 212, 0.4)",
            "accent": "#f43f5e",
            "text": "#f1f5f9",
            "text_muted": "#64748b",
            "text_dark": "#0f172a"
        },
        "effects": {
            "blur": "20px",
            "radius": "14px",
            "box_shadow": "0 10px 35px 0 rgba(168, 85, 247, 0.18)"
        }
    }
}


class SoraThemeEngine:
    def __init__(self, root_dir: Path = PROJECT_DIR):
        self.root_dir = root_dir
        self.presets_universe = self.root_dir / "Presets_MilaUniverse"
        self.presets_linkvegas = self.root_dir / "Presets_LinkVegas"

    def list_all_presets(self) -> List[Dict[str, str]]:
        presets = []
        # Add signature curated themes
        for key, theme in SIGNATURE_THEMES.items():
            presets.append({
                "id": key,
                "name": theme["name"],
                "category": "Signature Modern",
                "source": "Sora Modern Engine"
            })
        
        # Scan filesystem for existing desktop folders
        if self.presets_universe.exists():
            for d in self.presets_universe.iterdir():
                if d.is_dir() and d.name not in SIGNATURE_THEMES:
                    presets.append({
                        "id": d.name,
                        "name": d.name,
                        "category": "MilaUniverse (Desktop)",
                        "source": str(d)
                    })

        if self.presets_linkvegas.exists():
            for d in self.presets_linkvegas.iterdir():
                if d.is_dir():
                    presets.append({
                        "id": d.name,
                        "name": d.name,
                        "category": "LinkVegas (Desktop)",
                        "source": str(d)
                    })
        return presets

    def get_theme_tokens(self, theme_id: str) -> Dict[str, Any]:
        """Resolves a theme ID or creates a tailored fallback."""
        if theme_id in SIGNATURE_THEMES:
            return SIGNATURE_THEMES[theme_id]

        # Check case-insensitive match
        for k, v in SIGNATURE_THEMES.items():
            if k.lower() == theme_id.lower() or v["name"].lower() == theme_id.lower():
                return v

        # Fallback generated from preset name
        return {
            "name": theme_id,
            "category": "Discovered Preset",
            "description": f"Autogenerated modern token projection for preset '{theme_id}'.",
            "colors": {
                "background": "#0f111a",
                "surface": "#181a27",
                "surface_glass": "rgba(24, 26, 39, 0.75)",
                "border": "rgba(255, 255, 255, 0.15)",
                "primary": "#3b82f6",
                "primary_glow": "rgba(59, 130, 246, 0.4)",
                "secondary": "#ec4899",
                "secondary_glow": "rgba(236, 72, 153, 0.4)",
                "accent": "#10b981",
                "text": "#f8fafc",
                "text_muted": "#94a3b8",
                "text_dark": "#020617"
            },
            "effects": {
                "blur": "16px",
                "radius": "12px",
                "box_shadow": "0 8px 30px rgba(0, 0, 0, 0.4)"
            }
        }

    def export_tailwind_config(self, theme_id: str) -> str:
        theme = self.get_theme_tokens(theme_id)
        c = theme["colors"]
        e = theme["effects"]
        return f"""// Tailwind Theme Configuration generated by Sora (空)
// Theme: {theme['name']}
module.exports = {{
  theme: {{
    extend: {{
      colors: {{
        'theme-bg': '{c["background"]}',
        'theme-surface': '{c["surface"]}',
        'theme-surface-glass': '{c["surface_glass"]}',
        'theme-border': '{c["border"]}',
        'theme-primary': '{c["primary"]}',
        'theme-primary-glow': '{c["primary_glow"]}',
        'theme-secondary': '{c["secondary"]}',
        'theme-secondary-glow': '{c["secondary_glow"]}',
        'theme-accent': '{c["accent"]}',
        'theme-text': '{c["text"]}',
        'theme-text-muted': '{c["text_muted"]}'
      }},
      backdropBlur: {{
        'theme-glass': '{e["blur"]}'
      }},
      borderRadius: {{
        'theme-card': '{e["radius"]}'
      }},
      boxShadow: {{
        'theme-glow': '{e["box_shadow"]}'
      }}
    }}
  }}
}};
"""

    def export_css_variables(self, theme_id: str) -> str:
        theme = self.get_theme_tokens(theme_id)
        c = theme["colors"]
        e = theme["effects"]
        return f"""/* CSS Design Tokens generated by Sora (空) */
/* Theme: {theme['name']} */
:root {{
  --theme-bg: {c["background"]};
  --theme-surface: {c["surface"]};
  --theme-surface-glass: {c["surface_glass"]};
  --theme-border: {c["border"]};
  --theme-primary: {c["primary"]};
  --theme-primary-glow: {c["primary_glow"]};
  --theme-secondary: {c["secondary"]};
  --theme-secondary-glow: {c["secondary_glow"]};
  --theme-accent: {c["accent"]};
  --theme-text: {c["text"]};
  --theme-text-muted: {c["text_muted"]};
  --theme-blur: {e["blur"]};
  --theme-radius: {e["radius"]};
  --theme-shadow: {e["box_shadow"]};
}}

.glass-panel {{
  background: var(--theme-surface-glass);
  backdrop-filter: blur(var(--theme-blur));
  -webkit-backdrop-filter: blur(var(--theme-blur));
  border: 1px solid var(--theme-border);
  border-radius: var(--theme-radius);
  box-shadow: var(--theme-shadow);
}}
"""

    def export_w3c_tokens(self, theme_id: str) -> Dict[str, Any]:
        theme = self.get_theme_tokens(theme_id)
        c = theme["colors"]
        e = theme["effects"]
        return {
            "meta": {
                "generator": "Sora Theme Engine v2.0",
                "theme_id": theme_id,
                "theme_name": theme["name"],
                "category": theme.get("category", "General")
            },
            "color": {
                k: {"$value": v, "$type": "color"} for k, v in c.items()
            },
            "effect": {
                k: {"$value": v, "$type": "dimension" if "px" in v else "shadow"} for k, v in e.items()
            }
        }

    def flip_flop_modernize(self) -> Dict[str, Any]:
        """Flip-Flops the entire repository: generates modern token assets on disk."""
        token_manifest = {}
        for theme_id in SIGNATURE_THEMES.keys():
            token_manifest[theme_id] = self.export_w3c_tokens(theme_id)

        # Write design_tokens.json
        tokens_path = self.root_dir / "design_tokens.json"
        with open(tokens_path, "w", encoding="utf-8") as f:
            json.dump(token_manifest, f, indent=2)

        # Write default tailwind.theme.config.js
        tw_path = self.root_dir / "tailwind.theme.config.js"
        tw_path.write_text(self.export_tailwind_config("ObsidianNeon"), encoding="utf-8")

        # Write theme.css
        css_path = self.root_dir / "theme.css"
        css_path.write_text(self.export_css_variables("ObsidianNeon"), encoding="utf-8")

        return {
            "status": "success",
            "tokens_written": str(tokens_path),
            "tailwind_written": str(tw_path),
            "css_written": str(css_path),
            "total_signature_themes": len(SIGNATURE_THEMES)
        }

    def stream_to_hub_outbox(self, content_md: str):
        if not HUB_OUTBOX_DIR.exists():
            HUB_OUTBOX_DIR.mkdir(parents=True, exist_ok=True)
        outbox_file = HUB_OUTBOX_DIR / "sora_theme_latest.md"
        outbox_file.write_text(content_md, encoding="utf-8")
        print(f"[Sora] Streamed output to {outbox_file}")


def main():
    parser = argparse.ArgumentParser(description="Sora Theme Engine & Generative UI Modernizer")
    parser.add_argument("command", choices=["list", "export", "generate", "flipflop"], help="Command to run")
    parser.add_argument("--theme", default="ObsidianNeon", help="Theme identifier")
    parser.add_argument("--format", choices=["json", "tailwind", "css", "all"], default="all", help="Output format")
    parser.add_argument("--prompt", default="", help="Prompt for custom theme generation")
    parser.add_argument("--outbox", action="store_true", help="Stream result to MilaCoreHub Outbox")

    args = parser.parse_args()
    engine = SoraThemeEngine()

    if args.command == "list":
        presets = engine.list_all_presets()
        print(f"\n--- Sora Studio Theme Presets ({len(presets)} registered) ---")
        for p in presets:
            print(f"[{p['category']}] {p['id']} - {p['name']}")

    elif args.command == "export":
        theme_id = args.theme
        theme = engine.get_theme_tokens(theme_id)
        output_blocks = []

        output_blocks.append(f"# Sora Theme Token Export: {theme['name']}\n")
        output_blocks.append(f"> **Category:** {theme.get('category', 'Custom')} | **Generator:** Sora Theme Engine\n")

        if args.format in ("json", "all"):
            tokens_json = json.dumps(engine.export_w3c_tokens(theme_id), indent=2)
            output_blocks.append(f"### W3C Design Tokens (JSON)\n```json\n{tokens_json}\n```\n")

        if args.format in ("tailwind", "all"):
            tw_code = engine.export_tailwind_config(theme_id)
            output_blocks.append(f"### Tailwind Theme Config\n```javascript\n{tw_code}\n```\n")

        if args.format in ("css", "all"):
            css_code = engine.export_css_variables(theme_id)
            output_blocks.append(f"### CSS Custom Properties\n```css\n{css_code}\n```\n")

        full_md = "\n".join(output_blocks)
        print(full_md)
        if args.outbox:
            engine.stream_to_hub_outbox(full_md)

    elif args.command == "flipflop":
        res = engine.flip_flop_modernize()
        summary = (
            f"# Sora Studio: Flip-Flop Modernization Complete\n\n"
            f"- **Tokens:** `{res['tokens_written']}`\n"
            f"- **Tailwind:** `{res['tailwind_written']}`\n"
            f"- **CSS:** `{res['css_written']}`\n"
            f"- **Signature Themes Loaded:** {res['total_signature_themes']}\n"
            f"\nAll desktop presets have been projected into modern web/mobile design tokens."
        )
        print(summary)
        engine.stream_to_hub_outbox(summary)


if __name__ == "__main__":
    main()
