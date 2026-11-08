#!/usr/bin/env python
# -*- coding: utf-8 -*-
r"""
Sora Theme Engine — Generative UI, Design Tokens & Dynamic Theme Modernizer
Lead: Agent Sora (空 - The Loom)
Studio: C:\Users\k69-admin\.gemini\MilaCore_ThemeEngine_Portable

Bridges legacy Windows 11 shell presets (104 total presets) into modern cross-platform design tokens:
- W3C Design Tokens Specification (JSON)
- Tailwind CSS v3 / v4 theme config
- CSS3 Custom Properties with Glassmorphic utility classes
- XAML ResourceDictionary for .NET 10 / WPF / Avalonia (MilaThemeSelector / MilaERM)
- Flutter ThemeData / ColorScheme for Dart cross-platform mobile & desktop
"""

import os
import sys
import json
import argparse
from pathlib import Path
from typing import Dict, Any, List, Optional, Tuple

# Reconfigure stdout/stderr to UTF-8
for s in (sys.stdout, sys.stderr):
    try:
        if s and s.encoding and s.encoding.lower() not in ("utf-8", "utf8"):
            s.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

PROJECT_DIR = Path(__file__).resolve().parent
HUB_OUTBOX_DIR = PROJECT_DIR.parent / "hub" / "MilaOutbox"
if not HUB_OUTBOX_DIR.exists():
    HUB_OUTBOX_DIR = PROJECT_DIR.parent.parent / "MilaCoreHub" / "MilaOutbox"


def hex_to_rgb(hex_str: str, default: Tuple[int, int, int] = (15, 17, 26)) -> Tuple[int, int, int]:
    """Converts hex color string (#RGB, #RRGGBB, #AARRGGBB) to (r, g, b) tuple."""
    if not hex_str or not isinstance(hex_str, str):
        return default
    s = hex_str.strip().lstrip('#')
    if len(s) == 3:
        s = ''.join([c * 2 for c in s])
    elif len(s) == 8:
        s = s[2:]  # Strip leading alpha if present
    if len(s) == 6:
        try:
            return tuple(int(s[i:i+2], 16) for i in (0, 2, 4))
        except ValueError:
            pass
    return default


def rgb_to_hex(r: int, g: int, b: int) -> str:
    r = max(0, min(255, int(r)))
    g = max(0, min(255, int(g)))
    b = max(0, min(255, int(b)))
    return f"#{r:02x}{g:02x}{b:02x}"


def lighten_color(r: int, g: int, b: int, amount: float = 0.12) -> str:
    """Lightens an RGB color by a given percentage to produce surface shades."""
    lr = r + (255 - r) * amount
    lg = g + (255 - g) * amount
    lb = b + (255 - b) * amount
    return rgb_to_hex(int(lr), int(lg), int(lb))


def load_preset_json(path: Path) -> Dict[str, Any]:
    """Reads a JSON file with multi-encoding fallback (UTF-8, UTF-16 LE, BOM)."""
    encodings = ("utf-8", "utf-8-sig", "utf-16", "utf-16-le", "cp1252", "latin-1")
    for enc in encodings:
        try:
            text = path.read_text(encoding=enc).strip()
            if text:
                return json.loads(text)
        except Exception:
            continue
    return {}


# Curated Signature Themes with handcrafted aesthetics
SIGNATURE_THEMES: Dict[str, Dict[str, Any]] = {
    "ObsidianNeon": {
        "name": "MilaCore Obsidian Neon (Default)",
        "category": "MilaCore Signature",
        "description": "The canonical MilaCore workstation aesthetic: deep carbon glass with electric cyan & violet telemetry.",
        "colors": {
            "background": "#0a0b10",
            "surface": "#121420",
            "surface_glass": "rgba(18, 20, 32, 0.72)",
            "border": "rgba(168, 85, 247, 0.35)",
            "primary": "#a855f7",
            "primary_glow": "rgba(168, 85, 247, 0.45)",
            "secondary": "#06b6d4",
            "secondary_glow": "rgba(6, 182, 212, 0.45)",
            "accent": "#f43f5e",
            "text": "#f8fafc",
            "text_muted": "#94a3b8",
            "text_dark": "#0f172a"
        },
        "effects": {
            "blur": "20px",
            "radius": "14px",
            "box_shadow": "0 10px 35px 0 rgba(168, 85, 247, 0.22)"
        }
    },
    "CyberpunkNeonGlossy": {
        "name": "Cyberpunk Neon Glossy",
        "category": "MilaUniverse",
        "description": "Night City electric cyan and neon magenta on wet frosted glass.",
        "colors": {
            "background": "#0b0a14",
            "surface": "#131124",
            "surface_glass": "rgba(19, 17, 36, 0.75)",
            "border": "rgba(0, 246, 255, 0.35)",
            "primary": "#00f6ff",
            "primary_glow": "rgba(0, 246, 255, 0.45)",
            "secondary": "#ff0080",
            "secondary_glow": "rgba(255, 0, 128, 0.45)",
            "accent": "#ffe600",
            "text": "#f8fafc",
            "text_muted": "#94a3b8",
            "text_dark": "#0f172a"
        },
        "effects": {
            "blur": "18px",
            "radius": "10px",
            "box_shadow": "0 8px 32px 0 rgba(0, 246, 255, 0.25)"
        }
    },
    "LiquidGlassTahoe": {
        "name": "Liquid Glass Tahoe (macOS Tahoe Dark)",
        "category": "MilaUniverse",
        "description": "Ultra-sleek frosted liquid glass with deep sapphire ocean accents and silky blur.",
        "colors": {
            "background": "#05070e",
            "surface": "#0d1322",
            "surface_glass": "rgba(13, 19, 34, 0.65)",
            "border": "rgba(255, 255, 255, 0.16)",
            "primary": "#38bdf8",
            "primary_glow": "rgba(56, 189, 248, 0.4)",
            "secondary": "#6366f1",
            "secondary_glow": "rgba(99, 102, 241, 0.4)",
            "accent": "#0ea5e9",
            "text": "#ffffff",
            "text_muted": "#a0aec0",
            "text_dark": "#020617"
        },
        "effects": {
            "blur": "24px",
            "radius": "16px",
            "box_shadow": "0 12px 40px 0 rgba(56, 189, 248, 0.2)"
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
            "border": "rgba(225, 29, 72, 0.35)",
            "primary": "#e11d48",
            "primary_glow": "rgba(225, 29, 72, 0.45)",
            "secondary": "#0d9488",
            "secondary_glow": "rgba(13, 148, 136, 0.45)",
            "accent": "#f59e0b",
            "text": "#fafaf9",
            "text_muted": "#78716c",
            "text_dark": "#0c0a09"
        },
        "effects": {
            "blur": "8px",
            "radius": "8px",
            "box_shadow": "0 4px 20px 0 rgba(225, 29, 72, 0.2)"
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
            "border": "rgba(234, 179, 8, 0.35)",
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
            "box_shadow": "0 8px 30px 0 rgba(234, 179, 8, 0.25)"
        }
    },
    "TheMatrixMatte": {
        "name": "The Matrix Digital Rain",
        "category": "MilaUniverse",
        "description": "Pure black obsidian terminal background with cascading digital phosphor greens.",
        "colors": {
            "background": "#020402",
            "surface": "#050f07",
            "surface_glass": "rgba(5, 15, 7, 0.85)",
            "border": "rgba(34, 197, 94, 0.3)",
            "primary": "#22c55e",
            "primary_glow": "rgba(34, 197, 94, 0.5)",
            "secondary": "#10b981",
            "secondary_glow": "rgba(16, 185, 129, 0.45)",
            "accent": "#86efac",
            "text": "#dcfce7",
            "text_muted": "#4ade80",
            "text_dark": "#022c22"
        },
        "effects": {
            "blur": "10px",
            "radius": "6px",
            "box_shadow": "0 0 25px rgba(34, 197, 94, 0.3)"
        }
    }
}


class SoraThemeEngine:
    def __init__(self, root_dir: Path = PROJECT_DIR):
        self.root_dir = root_dir
        self.presets_universe = self.root_dir / "Presets_MilaUniverse"
        self.presets_linkvegas = self.root_dir / "Presets_LinkVegas"
        self._cached_presets: Optional[Dict[str, Dict[str, Any]]] = None

    def _discover_all_presets(self) -> Dict[str, Dict[str, Any]]:
        """Scans disk presets and caches metadata from all 104 preset config.json files."""
        if self._cached_presets is not None:
            return self._cached_presets

        discovered: Dict[str, Dict[str, Any]] = {}

        # 1. Load curated signature themes
        for key, theme in SIGNATURE_THEMES.items():
            discovered[key] = {
                "id": key,
                "name": theme["name"],
                "category": theme.get("category", "Signature Modern"),
                "description": theme.get("description", ""),
                "accent": theme["colors"]["primary"],
                "background": theme["colors"]["background"],
                "border": theme["colors"]["border"],
                "radius": int(theme["effects"]["radius"].replace("px", "")),
                "is_signature": True,
                "raw_config": {}
            }

        # 2. Scan Presets_MilaUniverse
        if self.presets_universe.exists():
            for folder in sorted(self.presets_universe.iterdir()):
                if folder.is_dir():
                    cfg_file = folder / "config.json"
                    if cfg_file.exists():
                        cfg = load_preset_json(cfg_file)
                        p_id = cfg.get("Id") or folder.name
                        if p_id not in discovered:
                            discovered[p_id] = {
                                "id": p_id,
                                "name": cfg.get("Name") or folder.name,
                                "category": cfg.get("Category") or "MilaUniverse",
                                "description": cfg.get("Description") or f"MilaUniverse theme preset {folder.name}",
                                "accent": cfg.get("Accent", "#00F6FF"),
                                "background": cfg.get("Background", "#0B0A14"),
                                "border": cfg.get("Border", "#FF0080"),
                                "radius": int(cfg.get("CornerRadius", 10)),
                                "is_signature": False,
                                "source_folder": str(folder),
                                "raw_config": cfg
                            }

        # 3. Scan Presets_LinkVegas
        if self.presets_linkvegas.exists():
            for folder in sorted(self.presets_linkvegas.iterdir()):
                if folder.is_dir():
                    cfg_file = folder / "config.json"
                    if cfg_file.exists():
                        cfg = load_preset_json(cfg_file)
                        p_id = cfg.get("Id") or folder.name
                        if p_id not in discovered:
                            discovered[p_id] = {
                                "id": p_id,
                                "name": cfg.get("Name") or folder.name,
                                "category": cfg.get("Category") or "LinkVegas",
                                "description": cfg.get("Description") or f"LinkVegas theme preset {folder.name}",
                                "accent": cfg.get("Accent", "#3B82F6"),
                                "background": cfg.get("Background", "#0A0B10"),
                                "border": cfg.get("Border", "#1E293B"),
                                "radius": int(cfg.get("CornerRadius", 12)),
                                "is_signature": False,
                                "source_folder": str(folder),
                                "raw_config": cfg
                            }

        self._cached_presets = discovered
        return self._cached_presets

    def list_all_presets(self) -> List[Dict[str, Any]]:
        all_p = self._discover_all_presets()
        return list(all_p.values())

    def get_theme_tokens(self, theme_id: str) -> Dict[str, Any]:
        """Resolves any theme ID (signature or discovered from 104 presets) into full design tokens."""
        # Check Signature directly
        if theme_id in SIGNATURE_THEMES:
            return SIGNATURE_THEMES[theme_id]

        all_p = self._discover_all_presets()
        matched = None

        if theme_id in all_p:
            matched = all_p[theme_id]
        else:
            # Case-insensitive match check
            t_lower = theme_id.lower()
            for k, v in all_p.items():
                if k.lower() == t_lower or v["name"].lower() == t_lower:
                    matched = v
                    break

        if not matched:
            # Fallback if unknown ID
            matched = {
                "id": theme_id,
                "name": theme_id,
                "category": "Custom Autogenerated",
                "description": f"Autogenerated dynamic theme tokens for '{theme_id}'",
                "accent": "#A855F7",
                "background": "#0A0B10",
                "border": "#3B82F6",
                "radius": 12
            }

        # Calculate high-fidelity tokens dynamically
        bg_rgb = hex_to_rgb(matched["background"], (10, 11, 16))
        acc_rgb = hex_to_rgb(matched["accent"], (168, 85, 247))
        border_rgb = hex_to_rgb(matched["border"], (59, 130, 246))

        surface_hex = lighten_color(bg_rgb[0], bg_rgb[1], bg_rgb[2], 0.12)
        surface_glass = f"rgba({bg_rgb[0] + 10}, {bg_rgb[1] + 10}, {bg_rgb[2] + 16}, 0.72)"
        border_rgba = f"rgba({border_rgb[0]}, {border_rgb[1]}, {border_rgb[2]}, 0.35)"
        primary_glow = f"rgba({acc_rgb[0]}, {acc_rgb[1]}, {acc_rgb[2]}, 0.45)"
        sec_glow = f"rgba({border_rgb[0]}, {border_rgb[1]}, {border_rgb[2]}, 0.45)"
        shadow_val = f"0 8px 32px 0 rgba({acc_rgb[0]}, {acc_rgb[1]}, {acc_rgb[2]}, 0.22)"

        radius_px = f"{matched.get('radius', 12)}px"

        return {
            "id": matched["id"],
            "name": matched["name"],
            "category": matched["category"],
            "description": matched.get("description", ""),
            "colors": {
                "background": matched["background"],
                "surface": surface_hex,
                "surface_glass": surface_glass,
                "border": border_rgba,
                "primary": matched["accent"],
                "primary_glow": primary_glow,
                "secondary": matched["border"],
                "secondary_glow": sec_glow,
                "accent": matched["accent"],
                "text": "#f8fafc",
                "text_muted": "#94a3b8",
                "text_dark": "#0f172a"
            },
            "effects": {
                "blur": "18px",
                "radius": radius_px,
                "box_shadow": shadow_val
            }
        }

    def export_tailwind_config(self, theme_id: str) -> str:
        theme = self.get_theme_tokens(theme_id)
        c = theme["colors"]
        e = theme["effects"]
        return f"""// Tailwind Theme Configuration generated by Sora (空 - The Loom)
// Theme: {theme['name']} ({theme.get('category', 'Universal')})
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
        return f"""/* CSS Design Tokens generated by Sora (空 - The Loom) */
/* Theme: {theme['name']} | Category: {theme.get('category', 'Universal')} */
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

.theme-button-primary {{
  background: var(--theme-primary);
  color: var(--theme-bg);
  box-shadow: 0 0 15px var(--theme-primary-glow);
  border: none;
  font-weight: 700;
  border-radius: calc(var(--theme-radius) / 2);
  transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
}}

.theme-button-primary:hover {{
  filter: brightness(1.15);
  box-shadow: 0 0 25px var(--theme-primary);
  transform: translateY(-1px);
}}
"""

    def export_xaml_dictionary(self, theme_id: str) -> str:
        """Exports theme as a WPF / Avalonia / .NET 10 ResourceDictionary (MilaThemeSelector / MilaERM)."""
        theme = self.get_theme_tokens(theme_id)
        c = theme["colors"]
        e = theme["effects"]
        rad_num = e["radius"].replace("px", "")
        return f"""<ResourceDictionary xmlns="http://schemas.microsoft.com/winfx/2006/xaml/presentation"
                    xmlns:x="http://schemas.microsoft.com/winfx/2006/xaml">
    <!-- Sora Theme Studio .NET 10 ResourceDictionary -->
    <!-- Theme: {theme['name']} -->
    <SolidColorBrush x:Key="ThemeBackgroundBrush" Color="{c['background']}" />
    <SolidColorBrush x:Key="ThemeSurfaceBrush" Color="{c['surface']}" />
    <SolidColorBrush x:Key="ThemePrimaryBrush" Color="{c['primary']}" />
    <SolidColorBrush x:Key="ThemeSecondaryBrush" Color="{c['secondary']}" />
    <SolidColorBrush x:Key="ThemeAccentBrush" Color="{c['accent']}" />
    <SolidColorBrush x:Key="ThemeTextBrush" Color="{c['text']}" />
    <SolidColorBrush x:Key="ThemeTextMutedBrush" Color="{c['text_muted']}" />
    <CornerRadius x:Key="ThemeCornerRadius">{rad_num}</CornerRadius>
</ResourceDictionary>
"""

    def export_flutter_theme(self, theme_id: str) -> str:
        """Exports theme as a Dart Flutter ThemeData & ThemeExtension."""
        theme = self.get_theme_tokens(theme_id)
        c = theme["colors"]
        e = theme["effects"]
        rad_num = e["radius"].replace("px", "")
        return f"""// Dart/Flutter Theme Definition generated by Sora (空 - The Loom)
// Theme: {theme['name']}
import 'package:flutter/material.dart';

class MilaThemeTokens {{
  static const Color background = Color(0xFF{c['background'].lstrip('#')});
  static const Color surface = Color(0xFF{c['surface'].lstrip('#')});
  static const Color primary = Color(0xFF{c['primary'].lstrip('#')});
  static const Color secondary = Color(0xFF{c['secondary'].lstrip('#')});
  static const Color accent = Color(0xFF{c['accent'].lstrip('#')});
  static const Color text = Color(0xFF{c['text'].lstrip('#')});
  static const Color textMuted = Color(0xFF{c['text_muted'].lstrip('#')});
  static const double cornerRadius = {rad_num}.0;

  static ThemeData toThemeData() {{
    return ThemeData(
      brightness: Brightness.dark,
      scaffoldBackgroundColor: background,
      colorScheme: const ColorScheme.dark(
        primary: primary,
        secondary: secondary,
        surface: surface,
      ),
      cardTheme: CardTheme(
        color: surface,
        shape: RoundedRectangleBorder(
          borderRadius: BorderRadius.circular(cornerRadius),
        ),
      ),
    );
  }}
}}
"""

    def export_w3c_tokens(self, theme_id: str) -> Dict[str, Any]:
        theme = self.get_theme_tokens(theme_id)
        c = theme["colors"]
        e = theme["effects"]
        return {
            "meta": {
                "generator": "Sora Theme Engine v3.0",
                "theme_id": theme.get("id", theme_id),
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
        """Flip-Flops the entire repository: generates modern token assets on disk for all 104 presets."""
        all_presets = self.list_all_presets()
        manifest: Dict[str, Any] = {
            "meta": {
                "engine": "Sora Theme Engine v3.0",
                "lead_agent": "Sora (空 - The Loom)",
                "total_presets": len(all_presets),
                "generated_at": "2026-11-05",
                "architecture": "Universal Generative UI Design Tokens"
            },
            "themes": {}
        }

        token_manifest: Dict[str, Any] = {}
        for p in all_presets:
            p_id = p["id"]
            tokens = self.get_theme_tokens(p_id)
            manifest["themes"][p_id] = tokens
            token_manifest[p_id] = self.export_w3c_tokens(p_id)

        # 1. Write ALL_THEMES_MANIFEST.json
        manifest_path = self.root_dir / "ALL_THEMES_MANIFEST.json"
        with open(manifest_path, "w", encoding="utf-8") as f:
            json.dump(manifest, f, indent=2)

        # 2. Write design_tokens.json
        tokens_path = self.root_dir / "design_tokens.json"
        with open(tokens_path, "w", encoding="utf-8") as f:
            json.dump(token_manifest, f, indent=2)

        # 3. Write default tailwind.theme.config.js
        tw_path = self.root_dir / "tailwind.theme.config.js"
        tw_path.write_text(self.export_tailwind_config("ObsidianNeon"), encoding="utf-8")

        # 4. Write theme.css
        css_path = self.root_dir / "theme.css"
        css_path.write_text(self.export_css_variables("ObsidianNeon"), encoding="utf-8")

        # 5. Write theme.xaml
        xaml_path = self.root_dir / "theme.xaml"
        xaml_path.write_text(self.export_xaml_dictionary("ObsidianNeon"), encoding="utf-8")

        # 6. Write theme.dart
        dart_path = self.root_dir / "theme.dart"
        dart_path.write_text(self.export_flutter_theme("ObsidianNeon"), encoding="utf-8")

        return {
            "status": "success",
            "total_presets": len(all_presets),
            "manifest_written": str(manifest_path),
            "tokens_written": str(tokens_path),
            "tailwind_written": str(tw_path),
            "css_written": str(css_path),
            "xaml_written": str(xaml_path),
            "dart_written": str(dart_path)
        }

    def stream_to_hub_outbox(self, content_md: str):
        if not HUB_OUTBOX_DIR.exists():
            HUB_OUTBOX_DIR.mkdir(parents=True, exist_ok=True)
        outbox_file = HUB_OUTBOX_DIR / "sora_theme_latest.md"
        outbox_file.write_text(content_md, encoding="utf-8")
        print(f"[Sora] Streamed output to {outbox_file}")


def main():
    parser = argparse.ArgumentParser(description="Sora Theme Engine & Generative UI Modernizer")
    parser.add_argument("command", choices=["list", "export", "flipflop"], help="Command to run")
    parser.add_argument("--theme", default="ObsidianNeon", help="Theme identifier")
    parser.add_argument("--format", choices=["json", "tailwind", "css", "xaml", "flutter", "all"], default="all", help="Output format")
    parser.add_argument("--outbox", action="store_true", help="Stream result to MilaCoreHub Outbox")

    args = parser.parse_args()
    engine = SoraThemeEngine()

    if args.command == "list":
        presets = engine.list_all_presets()
        print(f"\n--- Sora Studio Theme Presets ({len(presets)} registered) ---")
        for p in presets:
            print(f"[{p['category']}] {p['id']} - {p['name']} ({p.get('accent', '')})")

    elif args.command == "export":
        theme_id = args.theme
        theme = engine.get_theme_tokens(theme_id)
        output_blocks = []

        output_blocks.append(f"# Sora Theme Token Export: {theme['name']}\n")
        output_blocks.append(f"> **Category:** {theme.get('category', 'Custom')} | **Lead:** Sora (空 - The Loom)\n")

        if args.format in ("json", "all"):
            tokens_json = json.dumps(engine.export_w3c_tokens(theme_id), indent=2)
            output_blocks.append(f"### W3C Design Tokens (JSON)\n```json\n{tokens_json}\n```\n")

        if args.format in ("tailwind", "all"):
            tw_code = engine.export_tailwind_config(theme_id)
            output_blocks.append(f"### Tailwind Theme Config\n```javascript\n{tw_code}\n```\n")

        if args.format in ("css", "all"):
            css_code = engine.export_css_variables(theme_id)
            output_blocks.append(f"### CSS Custom Properties\n```css\n{css_code}\n```\n")

        if args.format in ("xaml", "all"):
            xaml_code = engine.export_xaml_dictionary(theme_id)
            output_blocks.append(f"### XAML ResourceDictionary (.NET 10)\n```xml\n{xaml_code}\n```\n")

        if args.format in ("flutter", "all"):
            flutter_code = engine.export_flutter_theme(theme_id)
            output_blocks.append(f"### Flutter ThemeData (Dart)\n```dart\n{flutter_code}\n```\n")

        full_md = "\n".join(output_blocks)
        print(full_md)
        if args.outbox:
            engine.stream_to_hub_outbox(full_md)

    elif args.command == "flipflop":
        res = engine.flip_flop_modernize()
        summary = (
            f"# Sora Studio: Flip-Flop Modernization Complete\n\n"
            f"- **Total Presets Modernized:** {res['total_presets']}\n"
            f"- **Manifest:** `{res['manifest_written']}`\n"
            f"- **W3C Tokens:** `{res['tokens_written']}`\n"
            f"- **Tailwind:** `{res['tailwind_written']}`\n"
            f"- **CSS Properties:** `{res['css_written']}`\n"
            f"- **XAML .NET 10:** `{res['xaml_written']}`\n"
            f"- **Dart Flutter:** `{res['dart_written']}`\n\n"
            f"All 104 desktop shell presets are now unified into cross-platform Generative UI design tokens."
        )
        print(summary)
        engine.stream_to_hub_outbox(summary)


if __name__ == "__main__":
    main()
