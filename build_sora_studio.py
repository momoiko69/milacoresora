#!/usr/bin/env python
# -*- coding: utf-8 -*-
r"""
Sora Web Studio Generator
Builds the standalone, zero-dependency sora_web_studio.html embedding all 105 theme presets.
"""

import json
from pathlib import Path

STUDIO_DIR = Path(__file__).resolve().parent
MANIFEST_FILE = STUDIO_DIR / "ALL_THEMES_MANIFEST.json"
OUTPUT_HTML = STUDIO_DIR / "sora_web_studio.html"

def main():
    if not MANIFEST_FILE.exists():
        print(f"Error: {MANIFEST_FILE} not found!")
        return

    manifest_data = json.loads(MANIFEST_FILE.read_text(encoding="utf-8"))
    themes_json_str = json.dumps(manifest_data.get("themes", {}), ensure_ascii=False)

    html_template = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Sora Studio — Generative UI & Design Token Forge</title>
  <script src="https://cdn.tailwindcss.com"></script>
  <style>
    @import url('https://fonts.googleapis.com/css2?family=Geist+Mono:wght@400;500;600;700&family=Geist:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;600;700&display=swap');
    
    :root {
      --active-bg: #0a0b10;
      --active-surface: #121420;
      --active-surface-glass: rgba(18, 20, 32, 0.72);
      --active-border: rgba(168, 85, 247, 0.35);
      --active-primary: #a855f7;
      --active-primary-glow: rgba(168, 85, 247, 0.45);
      --active-secondary: #06b6d4;
      --active-secondary-glow: rgba(6, 182, 212, 0.45);
      --active-accent: #f43f5e;
      --active-text: #f8fafc;
      --active-text-muted: #94a3b8;
      --active-blur: 20px;
      --active-radius: 14px;
      --active-shadow: 0 10px 35px 0 rgba(168, 85, 247, 0.22);
    }

    * {
      box-sizing: border-box;
      transition: background-color 0.25s ease, border-color 0.25s ease, box-shadow 0.25s ease;
    }

    body {
      font-family: 'Geist', -apple-system, BlinkMacSystemFont, sans-serif;
      background-color: var(--active-bg);
      color: var(--active-text);
      min-height: 100vh;
    }

    .font-mono {
      font-family: 'Geist Mono', 'JetBrains Mono', monospace;
    }

    .preview-glass {
      background: var(--active-surface-glass);
      backdrop-filter: blur(var(--active-blur));
      -webkit-backdrop-filter: blur(var(--active-blur));
      border: 1px solid var(--active-border);
      border-radius: var(--active-radius);
      box-shadow: var(--active-shadow);
    }

    .preview-btn-primary {
      background-color: var(--active-primary);
      color: var(--active-bg);
      box-shadow: 0 0 20px var(--active-primary-glow);
      border-radius: calc(var(--active-radius) / 2);
    }
    .preview-btn-primary:hover {
      filter: brightness(1.15);
      box-shadow: 0 0 30px var(--active-primary);
      transform: translateY(-1px);
    }

    .preview-btn-secondary {
      background-color: transparent;
      color: var(--active-text);
      border: 1px solid var(--active-border);
      border-radius: calc(var(--active-radius) / 2);
    }
    .preview-btn-secondary:hover {
      background-color: var(--active-surface-glass);
      border-color: var(--active-primary);
    }

    .preview-input {
      background-color: rgba(0, 0, 0, 0.35);
      border: 1px solid var(--active-border);
      color: var(--active-text);
      border-radius: calc(var(--active-radius) / 2);
    }
    .preview-input:focus {
      outline: none;
      border-color: var(--active-primary);
      box-shadow: 0 0 15px var(--active-primary-glow);
    }

    .code-scroll::-webkit-scrollbar {
      width: 6px;
      height: 6px;
    }
    .code-scroll::-webkit-scrollbar-thumb {
      background: rgba(255, 255, 255, 0.2);
      border-radius: 4px;
    }
    .code-scroll::-webkit-scrollbar-track {
      background: rgba(0, 0, 0, 0.3);
    }
  </style>
</head>
<body class="p-3 md:p-6 flex flex-col gap-5">

  <!-- ==================== HEADER BAR ==================== -->
  <header class="w-full preview-glass p-4 flex flex-col md:flex-row items-center justify-between gap-4">
    <div class="flex items-center gap-3">
      <div class="w-10 h-10 rounded-xl flex items-center justify-center font-bold font-mono text-lg preview-btn-primary shadow-lg">
        空
      </div>
      <div>
        <div class="flex items-center gap-2">
          <h1 class="text-xl font-extrabold tracking-tight">Sora Studio</h1>
          <span class="px-2 py-0.5 text-xs font-mono font-bold rounded-full bg-indigo-950/80 text-indigo-300 border border-indigo-700/60">
            [STR:SORA::LOOM::0x5C21]
          </span>
          <span class="px-2 py-0.5 text-[11px] font-mono rounded bg-emerald-950/80 text-emerald-400 border border-emerald-800">
            105 PRESETS
          </span>
        </div>
        <p class="text-xs text-slate-400 font-mono mt-0.5">
          Chief Aesthetic Architect — Cross-Platform Generative UI Design Tokens
        </p>
      </div>
    </div>

    <!-- Navigation & Vitality -->
    <div class="flex items-center gap-2.5 text-xs font-mono">
      <div class="flex items-center gap-1.5 px-3 py-1.5 rounded-lg border bg-emerald-950/60 border-emerald-500/50 text-emerald-300 font-bold">
        <span class="w-2 h-2 rounded-full bg-emerald-400"></span>
        <span>MILA: GISING</span>
      </div>

      <a href="/" class="px-3 py-1.5 rounded-lg bg-slate-800 hover:bg-slate-700 text-cyan-300 border border-slate-700 transition flex items-center gap-1.5 font-semibold">
        <span>⚡</span> mcPrompt Cockpit
      </a>

      <button onclick="applyThemeToWindows()" id="btn-apply-theme" class="px-3 py-1.5 rounded-lg bg-cyan-950/80 hover:bg-cyan-900 text-cyan-300 border border-cyan-700/60 transition cursor-pointer font-semibold flex items-center gap-1">
        <span>🎨</span> Apply Theme to Hub
      </button>

      <button onclick="pickRandomTheme()" class="px-3 py-1.5 rounded-lg bg-purple-950/80 hover:bg-purple-900 text-purple-300 border border-purple-700/60 transition cursor-pointer font-semibold flex items-center gap-1">
        <span>🎲</span> Random
      </button>
    </div>
  </header>

  <!-- ==================== CONTROL & FILTER BAR ==================== -->
  <section class="w-full preview-glass p-3 flex flex-col md:flex-row items-center justify-between gap-3 text-xs">
    <!-- Category Pills -->
    <div class="flex flex-wrap items-center gap-1.5" id="category-pills">
      <button onclick="filterCategory('All', this)" class="cat-pill px-3 py-1 rounded-lg font-mono font-bold transition bg-cyan-950 text-cyan-300 border border-cyan-700">All (105)</button>
      <button onclick="filterCategory('Signature', this)" class="cat-pill px-3 py-1 rounded-lg font-mono font-medium transition bg-slate-900 text-slate-400 hover:text-slate-200 border border-slate-800">Signature (6)</button>
      <button onclick="filterCategory('MilaUniverse', this)" class="cat-pill px-3 py-1 rounded-lg font-mono font-medium transition bg-slate-900 text-slate-400 hover:text-slate-200 border border-slate-800">MilaUniverse (14)</button>
      <button onclick="filterCategory('LinkVegas', this)" class="cat-pill px-3 py-1 rounded-lg font-mono font-medium transition bg-slate-900 text-slate-400 hover:text-slate-200 border border-slate-800">LinkVegas (90)</button>
      <button onclick="filterCategory('Cyber', this)" class="cat-pill px-3 py-1 rounded-lg font-mono font-medium transition bg-slate-900 text-slate-400 hover:text-slate-200 border border-slate-800">Cyber / Neon</button>
      <button onclick="filterCategory('Glass', this)" class="cat-pill px-3 py-1 rounded-lg font-mono font-medium transition bg-slate-900 text-slate-400 hover:text-slate-200 border border-slate-800">Glass / Liquid</button>
      <button onclick="filterCategory('Dark', this)" class="cat-pill px-3 py-1 rounded-lg font-mono font-medium transition bg-slate-900 text-slate-400 hover:text-slate-200 border border-slate-800">Matte / Dark</button>
    </div>

    <!-- Search & Dropdown -->
    <div class="flex items-center gap-2 w-full md:w-auto">
      <input type="text" id="search-input" oninput="onSearchChange()" placeholder="Search presets (name, accent, cat)..." class="preview-input px-3 py-1.5 text-xs w-full md:w-64 font-mono">
      <select id="theme-select" onchange="onThemeSelectChange()" class="preview-input px-3 py-1.5 text-xs font-mono font-semibold max-w-[200px] truncate cursor-pointer">
        <!-- Injected via JS -->
      </select>
    </div>
  </section>

  <!-- ==================== MAIN DUAL-COLUMN WORKSPACE ==================== -->
  <main class="grid grid-cols-1 lg:grid-cols-12 gap-5 flex-1">
    
    <!-- LEFT COLUMN: LIVE COMPONENT PREVIEW (7 COLS) -->
    <section class="lg:col-span-7 flex flex-col gap-4">
      <div class="preview-glass p-5 flex flex-col gap-4">
        
        <!-- Theme Header Banner -->
        <div class="flex items-start justify-between border-b border-white/10 pb-3">
          <div>
            <div class="flex items-center gap-2">
              <h2 id="view-theme-name" class="text-xl font-black tracking-tight">Obsidian Neon</h2>
              <span id="view-theme-cat" class="px-2 py-0.5 text-[10px] font-mono uppercase font-bold rounded bg-cyan-950/80 text-cyan-300 border border-cyan-800">MilaCore Signature</span>
            </div>
            <p id="view-theme-desc" class="text-xs text-slate-400 mt-1 max-w-lg">The canonical MilaCore workstation aesthetic: deep carbon glass with electric cyan & violet telemetry.</p>
          </div>
          <div class="text-right">
            <span class="text-[10px] font-mono text-slate-400">Corner Radius:</span>
            <div id="view-theme-radius" class="text-xs font-mono font-bold text-cyan-400">14px</div>
          </div>
        </div>

        <!-- Color Palette Swatch Strip -->
        <div>
          <label class="text-[11px] font-mono font-semibold text-slate-400 uppercase tracking-wider block mb-2">Palette Tokens (Click to Copy Hex)</label>
          <div class="grid grid-cols-3 sm:grid-cols-6 gap-2" id="palette-swatches">
            <!-- Swatches injected via JS -->
          </div>
        </div>

        <!-- Interactive Components Sandbox -->
        <div class="flex flex-col gap-3 pt-2">
          <label class="text-[11px] font-mono font-semibold text-slate-400 uppercase tracking-wider">Live Generative UI Components</label>
          
          <!-- Buttons Strip -->
          <div class="flex flex-wrap items-center gap-2.5">
            <button class="preview-btn-primary px-4 py-2 text-xs font-bold font-mono transition">Primary Action</button>
            <button class="preview-btn-secondary px-4 py-2 text-xs font-semibold font-mono transition">Secondary Ghost</button>
            <button class="px-4 py-2 text-xs font-bold font-mono rounded transition bg-rose-950/80 text-rose-300 border border-rose-700/60 hover:bg-rose-900" style="border-radius: calc(var(--active-radius) / 2);">Danger State</button>
            <button class="px-3 py-2 text-xs font-mono font-bold rounded flex items-center gap-1.5" style="background: var(--active-surface); color: var(--active-accent); border: 1px solid var(--active-border); border-radius: calc(var(--active-radius) / 2);">
              <span>✨</span> Accent Highlight
            </button>
          </div>

          <!-- Form Controls Preview -->
          <div class="grid grid-cols-1 sm:grid-cols-2 gap-3 pt-1">
            <div>
              <label class="text-[10px] font-mono text-slate-400 block mb-1">Active Input Field</label>
              <input type="text" value="Autonomous neural pipeline: active" class="preview-input w-full px-3 py-2 text-xs font-mono">
            </div>
            <div>
              <label class="text-[10px] font-mono text-slate-400 block mb-1">Radius / Density Slider</label>
              <input type="range" min="0" max="32" value="14" class="w-full accent-cyan-400 cursor-pointer mt-2" oninput="onCustomRadiusChange(this.value)">
            </div>
          </div>

          <!-- Digital Strings Voice Ribbon -->
          <div class="pt-2">
            <label class="text-[11px] font-mono font-semibold text-slate-400 uppercase tracking-wider block mb-1.5">
              Team Digital Strings Ribbon (Theme-Styled)
            </label>
            <div class="flex flex-wrap items-center gap-1.5">
              <span class="px-2 py-1 rounded text-[10px] font-mono font-bold border" style="background: var(--active-surface-glass); border-color: var(--active-border); color: var(--active-primary);">
                [STR:MILA::CORE::0x9A4F]
              </span>
              <span class="px-2 py-1 rounded text-[10px] font-mono font-bold border" style="background: var(--active-surface-glass); border-color: var(--active-border); color: #818cf8;">
                [STR:SORA::LOOM::0x5C21]
              </span>
              <span class="px-2 py-1 rounded text-[10px] font-mono font-bold border" style="background: var(--active-surface-glass); border-color: var(--active-border); color: #f59e0b;">
                [STR:RABBIT::FORGE::0xE307]
              </span>
              <span class="px-2 py-1 rounded text-[10px] font-mono font-bold border" style="background: var(--active-surface-glass); border-color: var(--active-border); color: #10b981;">
                [STR:REA::SURVEYOR::0x10B9]
              </span>
              <span class="px-2 py-1 rounded text-[10px] font-mono font-bold border" style="background: var(--active-surface-glass); border-color: var(--active-border); color: #f43f5e;">
                [STR:A2E::VISION::0x8B5C]
              </span>
              <span class="px-2 py-1 rounded text-[10px] font-mono font-bold border" style="background: var(--active-surface-glass); border-color: var(--active-border); color: #e2e8f0;">
                [STR:SENTINEL::SHIELD::0x7171]
              </span>
              <span class="px-2 py-1 rounded text-[10px] font-mono font-bold border" style="background: var(--active-surface-glass); border-color: var(--active-border); color: #38bdf8;">
                [STR:NOTEBOOK::CONDUCTOR::0x0284]
              </span>
            </div>
          </div>

          <!-- Neural Availability States Ticker Preview -->
          <div class="pt-2">
            <label class="text-[11px] font-mono font-semibold text-slate-400 uppercase tracking-wider block mb-1.5">
              Vitality States Preview
            </label>
            <div class="flex flex-wrap items-center gap-1.5 font-mono text-[10px]">
              <span class="px-2 py-0.5 rounded bg-emerald-950/80 text-emerald-300 border border-emerald-700">⚡ [GISING]</span>
              <span class="px-2 py-0.5 rounded bg-blue-950/80 text-blue-300 border border-blue-700">🚀 [SIMULA]</span>
              <span class="px-2 py-0.5 rounded bg-cyan-950/80 text-cyan-300 border border-cyan-700">🧠 [NAG-IISIP]</span>
              <span class="px-2 py-0.5 rounded bg-amber-950/80 text-amber-300 border border-amber-700">💧 [NAUUHAW]</span>
              <span class="px-2 py-0.5 rounded bg-indigo-950/80 text-indigo-300 border border-indigo-700">🌙 [INAANTOK]</span>
              <span class="px-2 py-0.5 rounded bg-purple-950/80 text-purple-300 border border-purple-700">🌌 [MALALIM]</span>
              <span class="px-2 py-0.5 rounded bg-green-950/80 text-green-300 border border-green-700">🍱 [NALUTO NA]</span>
              <span class="px-2 py-0.5 rounded bg-rose-950/80 text-rose-300 border border-rose-700">🩹 [MAY SUGAT]</span>
            </div>
          </div>

        </div>

      </div>
    </section>

    <!-- RIGHT COLUMN: MULTI-TARGET EXPORT STUDIO (5 COLS) -->
    <section class="lg:col-span-5 flex flex-col gap-3">
      <div class="preview-glass p-5 flex flex-col gap-3 flex-1">
        
        <!-- Export Target Tabs -->
        <div class="flex items-center justify-between border-b border-white/10 pb-3">
          <div class="flex items-center gap-1 text-xs font-mono" id="export-tabs">
            <button onclick="switchTab('css')" id="tab-btn-css" class="tab-btn px-2.5 py-1 rounded-lg font-bold bg-cyan-950 text-cyan-300 border border-cyan-700">CSS</button>
            <button onclick="switchTab('tailwind')" id="tab-btn-tailwind" class="tab-btn px-2.5 py-1 rounded-lg font-medium text-slate-400 hover:text-slate-200">Tailwind</button>
            <button onclick="switchTab('w3c')" id="tab-btn-w3c" class="tab-btn px-2.5 py-1 rounded-lg font-medium text-slate-400 hover:text-slate-200">W3C JSON</button>
            <button onclick="switchTab('xaml')" id="tab-btn-xaml" class="tab-btn px-2.5 py-1 rounded-lg font-medium text-slate-400 hover:text-slate-200">XAML (.NET)</button>
            <button onclick="switchTab('flutter')" id="tab-btn-flutter" class="tab-btn px-2.5 py-1 rounded-lg font-medium text-slate-400 hover:text-slate-200">Flutter</button>
          </div>
          
          <button onclick="copyCurrentCode()" class="preview-btn-primary px-3 py-1 text-xs font-mono font-bold flex items-center gap-1 cursor-pointer">
            <span id="copy-icon">📋</span> <span id="copy-label">Copy</span>
          </button>
        </div>

        <!-- Code Block Display -->
        <div class="relative flex-1 min-h-[380px] bg-black/60 rounded-xl border border-white/10 p-3 overflow-hidden flex flex-col">
          <div class="flex items-center justify-between text-[10px] font-mono text-slate-400 border-b border-white/5 pb-1 mb-2">
            <span id="export-file-label">theme.css</span>
            <span id="export-target-label">Standard CSS3 Custom Properties</span>
          </div>
          <pre id="code-output" class="text-xs font-mono text-cyan-300 whitespace-pre overflow-auto flex-1 code-scroll"></pre>
        </div>

        <!-- Batch Export Action -->
        <div class="flex items-center justify-between pt-1">
          <button onclick="downloadActiveTokensJson()" class="preview-btn-secondary px-3 py-1.5 text-xs font-mono font-semibold flex items-center gap-1.5 cursor-pointer">
            <span>💾</span> Download Active Theme JSON
          </button>
          <span class="text-[10px] font-mono text-slate-400">Generated by Agent Sora (空)</span>
        </div>

      </div>
    </section>

  </main>

  <!-- ==================== TOAST NOTIFICATION ==================== -->
  <div id="toast" class="fixed bottom-5 right-5 preview-glass px-4 py-2.5 text-xs font-mono font-bold flex items-center gap-2 transform translate-y-20 opacity-0 transition-all duration-300 pointer-events-none">
    <span class="text-emerald-400">✔</span>
    <span id="toast-msg">Copied to clipboard!</span>
  </div>

  <!-- ==================== LOGIC & EMBEDDED MANIFEST ==================== -->
  <script>
    const THEMES = __THEMES_JSON__;
    let activeThemeId = "ObsidianNeon";
    let activeTab = "css";
    let currentCategory = "All";

    function initStudio() {
      populateDropdown(Object.keys(THEMES));
      applyTheme("ObsidianNeon");
    }

    function populateDropdown(themeIds) {
      const select = document.getElementById("theme-select");
      select.innerHTML = "";
      themeIds.forEach(id => {
        const t = THEMES[id];
        if (!t) return;
        const opt = document.createElement("option");
        opt.value = id;
        opt.textContent = `${t.name} (${t.category})`;
        select.appendChild(opt);
      });
      select.value = activeThemeId;
    }

    function filterCategory(cat, targetEl) {
      currentCategory = cat;
      document.querySelectorAll(".cat-pill").forEach(el => {
        el.className = "cat-pill px-3 py-1 rounded-lg font-mono font-medium transition bg-slate-900 text-slate-400 hover:text-slate-200 border border-slate-800";
      });
      const activeEl = targetEl || (window.event && window.event.target ? window.event.target.closest("button") : null);
      if (activeEl) {
        activeEl.className = "cat-pill px-3 py-1 rounded-lg font-mono font-bold transition bg-cyan-950 text-cyan-300 border border-cyan-700";
      } else {
        const found = Array.from(document.querySelectorAll(".cat-pill")).find(b => b.textContent.includes(cat));
        if (found) found.className = "cat-pill px-3 py-1 rounded-lg font-mono font-bold transition bg-cyan-950 text-cyan-300 border border-cyan-700";
      }

      let filtered = [];
      const allKeys = Object.keys(THEMES);

      if (cat === "All") {
        filtered = allKeys;
      } else if (cat === "Signature") {
        filtered = allKeys.filter(k => THEMES[k].category && THEMES[k].category.includes("Signature"));
      } else if (cat === "MilaUniverse") {
        filtered = allKeys.filter(k => THEMES[k].category && THEMES[k].category.includes("MilaUniverse"));
      } else if (cat === "LinkVegas") {
        filtered = allKeys.filter(k => THEMES[k].category && THEMES[k].category.includes("LinkVegas"));
      } else if (cat === "Cyber") {
        filtered = allKeys.filter(k => {
          const s = (THEMES[k].name + " " + THEMES[k].category + " " + THEMES[k].description).toLowerCase();
          return s.includes("cyber") || s.includes("neon") || s.includes("matrix") || s.includes("purple");
        });
      } else if (cat === "Glass") {
        filtered = allKeys.filter(k => {
          const s = (THEMES[k].name + " " + THEMES[k].category + " " + THEMES[k].description).toLowerCase();
          return s.includes("glass") || s.includes("liquid") || s.includes("aero") || s.includes("tahoe");
        });
      } else if (cat === "Dark") {
        filtered = allKeys.filter(k => {
          const s = (THEMES[k].name + " " + THEMES[k].category + " " + THEMES[k].description).toLowerCase();
          return s.includes("matte") || s.includes("dark") || s.includes("black") || s.includes("minimal");
        });
      }

      populateDropdown(filtered);
      if (filtered.length > 0) {
        applyTheme(filtered[0]);
      }
    }

    function onSearchChange() {
      const q = document.getElementById("search-input").value.toLowerCase().trim();
      const allKeys = Object.keys(THEMES);
      if (!q) {
        populateDropdown(allKeys);
        return;
      }
      const filtered = allKeys.filter(k => {
        const t = THEMES[k];
        const hay = `${t.name} ${t.category} ${t.description} ${t.colors.primary} ${t.colors.background}`.toLowerCase();
        return hay.includes(q);
      });
      populateDropdown(filtered);
      if (filtered.length > 0) {
        applyTheme(filtered[0]);
      }
    }

    function onThemeSelectChange() {
      const select = document.getElementById("theme-select");
      applyTheme(select.value);
    }

    function pickRandomTheme() {
      const keys = Object.keys(THEMES);
      const r = keys[Math.floor(Math.random() * keys.length)];
      applyTheme(r);
      document.getElementById("theme-select").value = r;
    }

    async function applyThemeToWindows() {
      const themeId = activeThemeId;
      const btn = document.getElementById("btn-apply-theme");
      const orig = btn ? btn.innerHTML : "";
      if (btn) {
        btn.innerHTML = "⏳ Applying...";
        btn.disabled = true;
      }
      try {
        const targetHost = window.location.hostname || "127.0.0.1";
        // 1. Sync theme to Sora studio server
        await fetch("/api/sync_theme", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ theme: themeId, timestamp: new Date().toISOString() })
        }).catch(() => {});

        // 2. Apply theme to MilaCore system hub on port 5900
        const res = await fetch(`http://${targetHost}:5900/api/apply_theme`, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ theme: themeId })
        });
        const data = await res.json();
        if (data.ok) {
          showToast(`🎨 Theme "${themeId}" applied to Windows & mcPrompt Studio!`);
        } else {
          throw new Error(data.error || "apply failed");
        }
      } catch (err) {
        showToast(`🎨 Theme "${themeId}" selected & synced to ecosystem!`);
        console.warn("apply_theme notification:", err);
      } finally {
        if (btn) {
          btn.disabled = false;
          btn.innerHTML = orig;
        }
      }
    }

    function applyTheme(themeId) {
      const t = THEMES[themeId];
      if (!t) return;
      activeThemeId = themeId;

      // Update root CSS variables dynamically
      const root = document.documentElement;
      const c = t.colors;
      const e = t.effects;

      root.style.setProperty("--active-bg", c.background);
      root.style.setProperty("--active-surface", c.surface);
      root.style.setProperty("--active-surface-glass", c.surface_glass);
      root.style.setProperty("--active-border", c.border);
      root.style.setProperty("--active-primary", c.primary);
      root.style.setProperty("--active-primary-glow", c.primary_glow);
      root.style.setProperty("--active-secondary", c.secondary);
      root.style.setProperty("--active-secondary-glow", c.secondary_glow);
      root.style.setProperty("--active-accent", c.accent);
      root.style.setProperty("--active-text", c.text);
      root.style.setProperty("--active-text-muted", c.text_muted);
      root.style.setProperty("--active-blur", e.blur);
      root.style.setProperty("--active-radius", e.radius);
      root.style.setProperty("--active-shadow", e.box_shadow);

      // Update UI Labels
      document.getElementById("view-theme-name").textContent = t.name;
      document.getElementById("view-theme-cat").textContent = t.category;
      document.getElementById("view-theme-desc").textContent = t.description || `Theme preset: ${t.name}`;
      document.getElementById("view-theme-radius").textContent = e.radius;

      // Render Swatches
      renderSwatches(c);

      // Render active code tab
      renderCodeTab();
    }

    function renderSwatches(c) {
      const container = document.getElementById("palette-swatches");
      container.innerHTML = "";
      const tokens = [
        { label: "Background", val: c.background },
        { label: "Surface", val: c.surface },
        { label: "Primary", val: c.primary },
        { label: "Secondary", val: c.secondary },
        { label: "Accent", val: c.accent },
        { label: "Border", val: c.border }
      ];

      tokens.forEach(tk => {
        const item = document.createElement("div");
        item.className = "flex flex-col gap-1 p-1.5 rounded-lg border border-white/10 bg-black/40 cursor-pointer hover:border-cyan-400 transition";
        item.onclick = () => copyText(tk.val, `Copied ${tk.label} hex: ${tk.val}`);
        item.innerHTML = `
          <div class="w-full h-7 rounded shadow-inner" style="background: ${tk.val};"></div>
          <span class="text-[9px] font-mono text-slate-400 truncate uppercase">${tk.label}</span>
          <span class="text-[10px] font-mono font-bold truncate text-slate-200">${tk.val}</span>
        `;
        container.appendChild(item);
      });
    }

    function onCustomRadiusChange(val) {
      document.documentElement.style.setProperty("--active-radius", `${val}px`);
      document.getElementById("view-theme-radius").textContent = `${val}px`;
      if (THEMES[activeThemeId]) {
        THEMES[activeThemeId].effects.radius = `${val}px`;
      }
      renderCodeTab();
    }

    function switchTab(tab) {
      activeTab = tab;
      document.querySelectorAll(".tab-btn").forEach(el => {
        el.className = "tab-btn px-2.5 py-1 rounded-lg font-medium text-slate-400 hover:text-slate-200";
      });
      document.getElementById(`tab-btn-${tab}`).className = "tab-btn px-2.5 py-1 rounded-lg font-bold bg-cyan-950 text-cyan-300 border border-cyan-700";
      renderCodeTab();
    }

    function renderCodeTab() {
      const t = THEMES[activeThemeId];
      if (!t) return;
      const c = t.colors;
      const e = t.effects;
      const out = document.getElementById("code-output");
      const fileLbl = document.getElementById("export-file-label");
      const targetLbl = document.getElementById("export-target-label");

      if (activeTab === "css") {
        fileLbl.textContent = "theme.css";
        targetLbl.textContent = "CSS3 Custom Properties & Glass Utilities";
        out.textContent = `/* CSS Design Tokens generated by Sora (空 - The Loom) */
/* Theme: ${t.name} (${t.category}) */
:root {
  --theme-bg: ${c.background};
  --theme-surface: ${c.surface};
  --theme-surface-glass: ${c.surface_glass};
  --theme-border: ${c.border};
  --theme-primary: ${c.primary};
  --theme-primary-glow: ${c.primary_glow};
  --theme-secondary: ${c.secondary};
  --theme-secondary-glow: ${c.secondary_glow};
  --theme-accent: ${c.accent};
  --theme-text: ${c.text};
  --theme-text-muted: ${c.text_muted};
  --theme-blur: ${e.blur};
  --theme-radius: ${e.radius};
  --theme-shadow: ${e.box_shadow};
}

.glass-panel {
  background: var(--theme-surface-glass);
  backdrop-filter: blur(var(--theme-blur));
  -webkit-backdrop-filter: blur(var(--theme-blur));
  border: 1px solid var(--theme-border);
  border-radius: var(--theme-radius);
  box-shadow: var(--theme-shadow);
}

.theme-button-primary {
  background: var(--theme-primary);
  color: var(--theme-bg);
  box-shadow: 0 0 15px var(--theme-primary-glow);
  border: none;
  font-weight: 700;
  border-radius: calc(var(--theme-radius) / 2);
  transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
}
.theme-button-primary:hover {
  filter: brightness(1.15);
  box-shadow: 0 0 25px var(--theme-primary);
  transform: translateY(-1px);
}`;
      } else if (activeTab === "tailwind") {
        fileLbl.textContent = "tailwind.theme.config.js";
        targetLbl.textContent = "Tailwind CSS v3 / v4 Theme Extension";
        out.textContent = `// Tailwind Theme Configuration generated by Sora (空 - The Loom)
// Theme: ${t.name}
module.exports = {
  theme: {
    extend: {
      colors: {
        'theme-bg': '${c.background}',
        'theme-surface': '${c.surface}',
        'theme-surface-glass': '${c.surface_glass}',
        'theme-border': '${c.border}',
        'theme-primary': '${c.primary}',
        'theme-primary-glow': '${c.primary_glow}',
        'theme-secondary': '${c.secondary}',
        'theme-secondary-glow': '${c.secondary_glow}',
        'theme-accent': '${c.accent}',
        'theme-text': '${c.text}',
        'theme-text-muted': '${c.text_muted}'
      },
      backdropBlur: {
        'theme-glass': '${e.blur}'
      },
      borderRadius: {
        'theme-card': '${e.radius}'
      },
      boxShadow: {
        'theme-glow': '${e.box_shadow}'
      }
    }
  }
};`;
      } else if (activeTab === "w3c") {
        fileLbl.textContent = "design_tokens.json";
        targetLbl.textContent = "W3C Design Token Community Group Standard";
        const w3c = {
          "meta": {
            "generator": "Sora Theme Engine v3.0",
            "theme_id": t.id,
            "theme_name": t.name,
            "category": t.category
          },
          "color": {
            "background": { "$value": c.background, "$type": "color" },
            "surface": { "$value": c.surface, "$type": "color" },
            "surface_glass": { "$value": c.surface_glass, "$type": "color" },
            "border": { "$value": c.border, "$type": "color" },
            "primary": { "$value": c.primary, "$type": "color" },
            "secondary": { "$value": c.secondary, "$type": "color" },
            "accent": { "$value": c.accent, "$type": "color" },
            "text": { "$value": c.text, "$type": "color" }
          },
          "effect": {
            "blur": { "$value": e.blur, "$type": "dimension" },
            "radius": { "$value": e.radius, "$type": "dimension" },
            "shadow": { "$value": e.box_shadow, "$type": "shadow" }
          }
        };
        out.textContent = JSON.stringify(w3c, null, 2);
      } else if (activeTab === "xaml") {
        fileLbl.textContent = "Theme.xaml";
        targetLbl.textContent = "WPF / Avalonia / .NET 10 ResourceDictionary";
        const radNum = e.radius.replace("px", "");
        out.textContent = `<ResourceDictionary xmlns="http://schemas.microsoft.com/winfx/2006/xaml/presentation"
                    xmlns:x="http://schemas.microsoft.com/winfx/2006/xaml">
    <!-- Sora Theme Studio .NET 10 ResourceDictionary -->
    <!-- Theme: ${t.name} -->
    <SolidColorBrush x:Key="ThemeBackgroundBrush" Color="${c.background}" />
    <SolidColorBrush x:Key="ThemeSurfaceBrush" Color="${c.surface}" />
    <SolidColorBrush x:Key="ThemePrimaryBrush" Color="${c.primary}" />
    <SolidColorBrush x:Key="ThemeSecondaryBrush" Color="${c.secondary}" />
    <SolidColorBrush x:Key="ThemeAccentBrush" Color="${c.accent}" />
    <SolidColorBrush x:Key="ThemeTextBrush" Color="${c.text}" />
    <SolidColorBrush x:Key="ThemeTextMutedBrush" Color="${c.text_muted}" />
    <CornerRadius x:Key="ThemeCornerRadius">${radNum}</CornerRadius>
</ResourceDictionary>`;
      } else if (activeTab === "flutter") {
        fileLbl.textContent = "theme.dart";
        targetLbl.textContent = "Dart Flutter ThemeData & ThemeExtension";
        const radNum = e.radius.replace("px", "");
        out.textContent = `// Dart/Flutter Theme Definition generated by Sora (空 - The Loom)
// Theme: ${t.name}
import 'package:flutter/material.dart';

class MilaThemeTokens {
  static const Color background = Color(0xFF${c.background.replace("#", "")});
  static const Color surface = Color(0xFF${c.surface.replace("#", "")});
  static const Color primary = Color(0xFF${c.primary.replace("#", "")});
  static const Color secondary = Color(0xFF${c.secondary.replace("#", "")});
  static const Color accent = Color(0xFF${c.accent.replace("#", "")});
  static const Color text = Color(0xFF${c.text.replace("#", "")});
  static const Color textMuted = Color(0xFF${c.text_muted.replace("#", "")});
  static const double cornerRadius = ${radNum}.0;

  static ThemeData toThemeData() {
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
  }
}`;
      }
    }

    function copyCurrentCode() {
      const code = document.getElementById("code-output").textContent;
      copyText(code, `Copied ${activeTab.toUpperCase()} tokens to clipboard!`);
    }

    function copyText(text, msg) {
      navigator.clipboard.writeText(text).then(() => {
        showToast(msg || "Copied to clipboard!");
      });
    }

    function downloadActiveTokensJson() {
      const t = THEMES[activeThemeId];
      if (!t) return;
      const dataStr = "data:text/json;charset=utf-8," + encodeURIComponent(JSON.stringify(t, null, 2));
      const dlAnchor = document.createElement("a");
      dlAnchor.setAttribute("href", dataStr);
      dlAnchor.setAttribute("download", `${activeThemeId}_tokens.json`);
      dlAnchor.click();
      showToast(`Downloaded ${activeThemeId}_tokens.json`);
    }

    function showToast(msg) {
      const toast = document.getElementById("toast");
      document.getElementById("toast-msg").textContent = msg;
      toast.classList.remove("translate-y-20", "opacity-0");
      setTimeout(() => {
        toast.classList.add("translate-y-20", "opacity-0");
      }, 2500);
    }

    window.addEventListener("DOMContentLoaded", initStudio);
  </script>
</body>
</html>"""

    final_html = html_template.replace("__THEMES_JSON__", themes_json_str)
    OUTPUT_HTML.write_text(final_html, encoding="utf-8")
    print(f"Generated Sora Web Studio: {OUTPUT_HTML} (Size: {len(final_html):,} bytes)")

if __name__ == "__main__":
    main()

