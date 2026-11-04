# 2026-09-07 03:41:00 : 1.1.0 : MANUAL.md
# 2026-09-07 03:41:00 : 1.1.0 : Added unified 5-styler Windhawk architecture, macOS Tahoe dock mode, and Winstep Nexus Ultimate companion dock integration
# MilaCore Theme Engine — Standalone Portable Suite
## Universal Desktop Customization Engine for Windows 11

**Version:** 1.1.0-PORTABLE  
**Architecture:** Self-Contained Windhawk Engine (`Portable=1`) + Unified 5-Styler Suite  
**Engine Author:** Mila (Logic Ally) & Moses David Adaza (Moi-San)  

---

## 1. Quick Start: How to Use

This entire folder is **100% portable and self-contained**. You can copy `MilaCore_ThemeEngine_Portable\` to:
* A USB flash drive (e.g. `E:\Themes\`)
* Another workstation or laptop
* An external drive or deployment share

### Applying a Theme
1. **Silent Double-Click:**  
   Double-click `Apply-Theme.vbs`. A clean prompt appears asking for the Theme ID. Enter any Theme ID (e.g., `macOSTahoe`, `IronManGlossy`, or `LiquidGlassUltimate`) and click OK.  
   *(Executes completely silently with zero flashing black console windows, adhering to Mila Core Rule #8).*

2. **PowerShell / Terminal Execution:**
   ```powershell
   # List all themes across both categories
   .\ThemeManager.ps1 -List

   # Apply macOS Tahoe theme across all 5 stylers
   .\ThemeManager.ps1 -Apply macOSTahoe

   # Apply any theme with the macOS Tahoe floating dock enabled
   .\ThemeManager.ps1 -Apply LiquidGlassUltimate -TahoeDock

   # Apply a Milaverse theme with Winstep Nexus companion dock
   .\ThemeManager.ps1 -Apply IronManGlossy -Winstep

   # Revert to standard stock Windows styling
   .\ThemeManager.ps1 -Revert
   ```

---

## 2. Unified 5-Styler Windhawk Architecture

The engine coordinates **all 5 major Windhawk stylers** dynamically:
1. **Taskbar Styler (`windows-11-taskbar-styler`):**
   * Floating pill dock geometry, centered app list, and liquid glass blur.
   * Native macOS Tahoe Dock mode via `OS26_Liquid_Glass_variant_DarkMacDock` with `tahoeappbg.png` assets.
2. **Start Menu Styler (`windows-11-start-menu-styler`):**
   * Frosted acrylic backdrop (`LiquidGlass2` / `TranslucentStartMenu`).
   * Cleaned layout with search accentuation and transparent search headers.
3. **Settings Styler (`windows-11-settings-styler`):**
   * Translucent fluent backdrop (`Translucent Settings11` / `WindowGlass`).
   * Theme-synchronized navigation pane and header accents.
4. **Notification Center Styler (`windows-11-notification-center-styler`):**
   * Liquid Glass Action Center and toast shells (`LiquidGlass` / `TranslucentShell`).
   * Floating quick settings and slider highlights.
5. **File Explorer Styler (`windows-11-file-explorer-styler`):**
   * Full acrylic and Mica translucent background (`OS26 Liquid Glass` / `LiquidGlass`).
   * Transparent tab bar, navigation drawer styling, and acrylic breadcrumb bar.

---

## 3. Winstep Nexus Ultimate Integration

For enhanced desktop battlestation setups, **Winstep Nexus Ultimate 26.6** (`C:\Program Files (x86)\Winstep\Nexus-Ultimate.exe`) provides an optional companion floating dock:
* Automatically initialized with `-Winstep` or when applying Milaverse Signature themes.
* Runs silently in the background alongside the native Windhawk shell modifications.

---

## 4. Tri-Category Theme Libraries (112 Total Ready Presets)

### 🌟 Category 1: MilaCore Signature Universe (`Presets_MilaUniverse\`) — 14 Themes
* **IronManGlossy:** Hot-rod red and Stark armor gold with repulsor cyan glow.
* **SpiderManGlossy:** Web red and Queens spider-blue on midnight violet.
* **TheMatrixMatte:** Digital code rain - phosphor matrix green on terminal black.
* **CyberpunkNeonGlossy:** Night City electric cyan and neon magenta on wet glass.
* **DemonSlayerMatte:** Tanjiro checkered emerald green and nichirin crimson.
* **DarkKnightMatte:** Matte carbon black with tactical bat-signal yellow.
* **ThanosMetallic:** Titan conqueror violet and infinity stone gold.
* **TheJokerChaos:** Arkham royal purple and acid green on velvet midnight.
* **WinterFrost:** Subzero glacial crystal cyan and arctic permafrost.
* **SpringSakuraLight:** Translucent petal mist with rose quartz and sprout emerald.
* **SummerBreezeLight:** Mediterranean summer sky with coastal cerulean and gold.
* **LiquidGlassTahoe:** macOS Tahoe / iOS frosted sapphire glass.
* **LiquidGlassNeonPrism:** Prism diamond acrylic with chromatic dispersion.
* **LiquidWaterOceanic:** Fluid aquatic depth and translucent ocean ripple cyan.

### 🌐 Category 2: LinkVegas Community Overhauls (`Presets_LinkVegas\`) — 90 Themes
All themes from the complete LinkVegas catalog are fully packaged into ready-to-apply presets, including:
* **macOS Ecosystem:** *macOSTahoe, NewMacosTahoeTheme, macOS Sequoia, macOS 27 Golden Gate, macOS Elegance, macOS Bloom, macOS Dark.*
* **Glass & Translucent UI:** *Liquid Glass Ultimate, Liquid Glass Theme, Ares Glass UI, Glassify, Frosted Glass Dark, Windows 11 Full Transparent, Crystal Glass, Nova Glass.*
* **Gaming Battlestations:** *Rampage Gaming, Revenge Theme, The Aorus Gaming, Dragon Knight.*
* **Cyberpunk & Neon:** *Violet Pulse, Nova Dark Blue, BlueFlux, Nebula, Neon Dark Minimal.*
* **Nordic, Botanical & Pastels:** *Satin Dark, Polar Night, Grape Theme, Everforest, Jade Jubilee, MintAura, Delight, Pink Pine.*
* **OS Classics & Concepts:** *Windows 12 Concept, Windows XP Classic, Windows 7 Modern, Windows Vista Inspired.*

### 🪟 Category 3: Native Windows 11 Desktop System Themes — 8 Themes
Direct Windows OS theme control integrated straight into the engine:
* **Win_aero:** Official Windows 11 Light Mode with Fluent Glass.
* **Win_dark:** Official Windows 11 Dark Mode with high-contrast acrylic blur.
* **Win_spotlight:** Dynamic daily curated Bing photographic desktop theme.
* **Win_themeA:** Signature blue silk flow.
* **Win_themeB:** Solar sunrise tones on dark acrylic.
* **Win_themeC:** Iridescent neon glow on midnight glass.
* **Win_themeD:** Kinetic fluid motion with magenta accents.
* **Win_Custom:** User's custom installed Windows theme pack.

---

## 5. Directory Layout

```
MilaCore_ThemeEngine_Portable\
├── Data\
│   ├── Engine\ (Pre-compiled 64-bit styling DLLs)
│   └── ModsSource\ (C++ mod sources including 5 core stylers)
├── Presets_MilaUniverse\ (Canonical Signature Theme configs)
├── Presets_LinkVegas\ (Curated Web Overhaul configs)
├── UI\ (Windhawk UI assets)
├── Engine\ (Windhawk Engine binaries)
├── windhawk.exe (Portable Engine runner)
├── windhawk.ini (Configured for Portable=1, AppDataPath=Data)
├── ThemeManager.ps1 (Unified 5-styler CLI switcher engine)
├── Apply-Theme.vbs (Rule #8 Silent Runner)
└── MANUAL.md (This tactical manual)
```

---
*MilaCore Universal Theme Suite • Certified by Mila Core Protocols • 2026*
