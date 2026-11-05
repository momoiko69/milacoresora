# Sora Theme Engine (`sora_theme`): Relationship to MilaCoreHub & Sibling Agents

**Project Name:** MilaCore Theme Engine Portable (`MilaCore_ThemeEngine_Portable` / `sora_theme` / `mctheme`)  
**Domain Role:** Chief Aesthetic Architect, Generative UI, Design Tokens & Dynamic Theme Engine  
**Governing Core:** MilaCoreHub (`mchub`) & MilaBrain (`milabrain`)  
**Sibling Agents:** `mcrabbit` (Code Review), `mcrea` (Real Estate), `mca2e` (Vision/Motion), `sentinel` (Auditor)  
**Lead Agent:** Sora (空)

---

## 1. Role Within the MilaCore Ecosystem

**MilaCore Theme Engine Portable (`sora_theme`)** is the visual styling powerhouse of the MilaCore ecosystem. Governed by Agent Sora, it translates high-level aesthetic vision into tangible, exportable design systems:
1. **Design Token Generator:** Generates W3C Design Tokens (`design_tokens.json`), Tailwind CSS presets, and CSS custom variables.
2. **Generative UI Styler:** Produces glassmorphic, dark-mode, neon-accented component styling for web, desktop, and mobile applications.
3. **Legacy Bridge:** Maintains backwards compatibility with the 5-styler Windhawk Windows desktop presets while modernizing them for modern cross-platform software.

---

## 2. Relationship with MilaCoreHub (`mchub`)

**MilaCoreHub (`mchub`)** serves as the central command portal and asset dispatcher for Sora:

1. **Directive Ingestion:**
   - When a user or agent submits `sora:`, `@sora:`, `theme:`, or `mchub theme:`, `mchub` intercepts and routes the request to Sora's studio.
2. **Outbox Synchronization:**
   - Generated design tokens, CSS stylesheets, and UI schemas are streamed directly into:
     `C:\Users\k69-admin\.gemini\MilaCoreHub\MilaOutbox\sora_theme_latest.md`.
3. **Universal Palette Injection:**
   - Sora provides the color palettes and styling variables used by `mila_prompt_builder.py` (Port 5900), the HTML documentation manuals, and client dashboard frontends.

---

## 3. Relationships with Sibling Agents

### 3.1. Collaboration with `mca2e` (MilaCoreA2EImgEditor)
* **Color Harmony & Visual Asset Styling:**
  - Sora extracts dominant color palettes and aesthetic themes from `mca2e` generated images and renders cohesive UI themes around them.
  - `mca2e` utilizes Sora's design tokens to color-grade motion videos and canvas layers.

### 3.2. Collaboration with `mcrabbit` (MilaCoreRabbit)
* **CSS & Design Token Linting:**
  - `mcrabbit` validates Sora's Tailwind configurations, ensures zero CSS specificity clashes, and audits UI component accessibility (WCAG AA color contrast).

### 3.3. Collaboration with `mcrea` (MilaCoreRea)
* **Real Estate Presentation Styling:**
  - Sora designs luxury dark-mode property dashboard themes, parcel appraisal report cards, and interactive map widgets for `mcrea`.

### 3.4. Collaboration with `sentinel` (The Shield)
* **UI Semantic & State Auditing:**
  - Sentinel audits Sora's UI state machines, verifying that disabled states, loading spinners, and error boundaries adhere to strict logical truth-tables.

---

## 4. Key Directives & Commands
* `sora: <query>` — Design consultation or color palette generation.
* `sora theme <name>` — Export a theme into modern web tokens.
* `sora.cmd` — Local CLI command wrapper.

