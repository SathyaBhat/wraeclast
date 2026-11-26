---
name: diagrams
description: "Diagrams umbrella: dark-themed SVG architecture HTML diagrams + hand-drawn Excalidraw JSON diagrams."
version: 1.0.0
author: Hermes Agent
license: MIT
dependencies: []
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [diagrams, architecture, SVG, HTML, Excalidraw, flowcharts, visualization, infrastructure, cloud]
    related_skills: [concept-diagrams]
    absorbs: [architecture-diagram, excalidraw]
---

# Diagrams Skill

Two diagram modes in one skill:

| Mode | When to use | Output |
|------|------------|--------|
| **SVG Architecture (HTML)** | Dark-themed tech/infra/cloud system diagrams | `.html` file, browser-ready |
| **Excalidraw (JSON)** | Hand-drawn feel: flowcharts, arch maps, sequence diagrams | `.excalidraw` file, drag onto excalidraw.com |

---

## SVG Architecture Diagrams (HTML output)

Generate professional, dark-themed technical architecture diagrams as standalone HTML files with inline SVG graphics. No external tools, no API keys, no rendering libraries — just write the HTML file and open it in a browser.

Based on [Cocoon AI's architecture-diagram-generator](https://github.com/Cocoon-AI/architecture-diagram-generator) (MIT).

### Scope

**Best suited for:**
- Software system architecture (frontend / backend / database layers)
- Cloud infrastructure (VPC, regions, subnets, managed services)
- Microservice / service-mesh topology
- Database + API map, deployment diagrams
- Anything with a tech-infra subject that fits a dark, grid-backed aesthetic

**Look elsewhere for:**
- Physics, chemistry, math, biology, or other scientific subjects
- Physical objects (vehicles, hardware, anatomy, cross-sections)
- Floor plans, narrative journeys, educational / textbook-style visuals
- Hand-drawn whiteboard sketches → use **Excalidraw mode** below

### Workflow

1. User describes their system architecture (components, connections, technologies)
2. Generate the HTML file following the design system below
3. Save with `write_file` to a `.html` file (e.g. `~/architecture-diagram.html`)
4. User opens in any browser — works offline, no dependencies

**Output location:** Save to user-specified path, or default to `./[project-name]-architecture.html`

**Preview:**
```bash
# macOS
open ./my-architecture.html
# Linux
xdg-open ./my-architecture.html
```

### Design System & Visual Language

#### Color Palette (Semantic Mapping)

| Component Type | Fill (rgba) | Stroke (Hex) |
| :--- | :--- | :--- |
| **Frontend** | `rgba(8, 51, 68, 0.4)` | `#22d3ee` (cyan-400) |
| **Backend** | `rgba(6, 78, 59, 0.4)` | `#34d399` (emerald-400) |
| **Database** | `rgba(76, 29, 149, 0.4)` | `#a78bfa` (violet-400) |
| **AWS/Cloud** | `rgba(120, 53, 15, 0.3)` | `#fbbf24` (amber-400) |
| **Security** | `rgba(136, 19, 55, 0.4)` | `#fb7185` (rose-400) |
| **Message Bus** | `rgba(251, 146, 60, 0.3)` | `#fb923c` (orange-400) |
| **External** | `rgba(30, 41, 59, 0.5)` | `#94a3b8` (slate-400) |

#### Typography & Background
- **Font:** JetBrains Mono (Monospace), loaded from Google Fonts
- **Sizes:** 12px (Names), 9px (Sublabels), 8px (Annotations), 7px (Tiny labels)
- **Background:** Slate-950 (`#020617`) with a subtle 40px grid pattern

```svg
<!-- Background Grid Pattern -->
<pattern id="grid" width="40" height="40" patternUnits="userSpaceOnUse">
  <path d="M 40 0 L 0 0 0 40" fill="none" stroke="#1e293b" stroke-width="0.5"/>
</pattern>
```

### Technical Implementation Details

#### Component Rendering
Components are rounded rectangles (`rx="6"`) with 1.5px strokes. To prevent arrows from showing through semi-transparent fills, use a **double-rect masking technique**:
1. Draw an opaque background rect (`#0f172a`)
2. Draw the semi-transparent styled rect on top

#### Connection Rules
- **Z-Order:** Draw arrows *early* in the SVG (after the grid) so they render behind component boxes
- **Arrowheads:** Defined via SVG markers
- **Security Flows:** Use dashed lines in rose color (`#fb7185`)
- **Boundaries:**
  - *Security Groups:* Dashed (`4,4`), rose color
  - *Regions:* Large dashed (`8,4`), amber color, `rx="12"`

#### Spacing & Layout Logic
- **Standard Height:** 60px (Services); 80-120px (Large components)
- **Vertical Gap:** Minimum 40px between components
- **Message Buses:** Must be placed *in the gap* between services, not overlapping them
- **Legend Placement:** **CRITICAL.** Must be placed outside all boundary boxes. Calculate the lowest Y-coordinate of all boundaries and place the legend at least 20px below it.

### Document Structure

The generated HTML file follows a four-part layout:
1. **Header:** Title with a pulsing dot indicator and subtitle
2. **Main SVG:** The diagram contained within a rounded border card
3. **Summary Cards:** A grid of three cards below the diagram for high-level details
4. **Footer:** Minimal metadata

### Info Card Pattern
```html
<div class="card">
  <div class="card-header">
    <div class="card-dot cyan"></div>
    <h3>Title</h3>
  </div>
  <ul>
    <li>• Item one</li>
    <li>• Item two</li>
  </ul>
</div>
```

### Output Requirements
- **Single File:** One self-contained `.html` file
- **No External Dependencies:** All CSS and SVG must be inline (except Google Fonts)
- **No JavaScript:** Use pure CSS for any animations (like pulsing dots)
- **Compatibility:** Must render correctly in any modern web browser

### Template Reference

Load the full HTML template for the exact structure, CSS, and SVG component examples:

```
skill_view(name="diagrams", file_path="templates/template.html")
```

The template contains working examples of every component type (frontend, backend, database, cloud, security), arrow styles (standard, dashed, curved), security groups, region boundaries, and the legend — use it as your structural reference when generating diagrams.

---

## Excalidraw Hand-Drawn Diagrams

Create diagrams by writing standard Excalidraw element JSON and saving as `.excalidraw` files. These files can be drag-and-dropped onto [excalidraw.com](https://excalidraw.com) for viewing and editing. No accounts, no API keys, no rendering libraries — just JSON.

### When to use

Generate `.excalidraw` files for architecture diagrams, flowcharts, sequence diagrams, concept maps, and more. Files can be opened at excalidraw.com or uploaded for shareable links.

### Workflow

1. **Load this skill** (you already did)
2. **Write the elements JSON** — an array of Excalidraw element objects
3. **Save the file** using `write_file` to create a `.excalidraw` file
4. **Optionally upload** for a shareable link using `scripts/upload.py` via `terminal`

#### Saving a Diagram

Wrap your elements array in the standard `.excalidraw` envelope and save with `write_file`:

```json
{
  "type": "excalidraw",
  "version": 2,
  "source": "hermes-agent",
  "elements": [ ...your elements array here... ],
  "appState": {
    "viewBackgroundColor": "#ffffff"
  }
}
```

Save to any path, e.g. `~/diagrams/my_diagram.excalidraw`.

#### Uploading for a Shareable Link

Run the upload script (located in this skill's `scripts/` directory) via terminal:

```bash
python skills/creative/diagrams/scripts/upload.py ~/diagrams/my_diagram.excalidraw
```

This uploads to excalidraw.com (no account needed) and prints a shareable URL. Requires the `cryptography` pip package (`pip install cryptography`).

---

### Element Format Reference

#### Required Fields (all elements)
`type`, `id` (unique string), `x`, `y`, `width`, `height`

#### Defaults (skip these — they're applied automatically)
- `strokeColor`: `"#1e1e1e"`
- `backgroundColor`: `"transparent"`
- `fillStyle`: `"solid"`
- `strokeWidth`: `2`
- `roughness`: `1` (hand-drawn look)
- `opacity`: `100`

Canvas background is white.

#### Element Types

**Rectangle**:
```json
{ "type": "rectangle", "id": "r1", "x": 100, "y": 100, "width": 200, "height": 100 }
```
- `roundness: { "type": 3 }` for rounded corners
- `backgroundColor: "#a5d8ff"`, `fillStyle: "solid"` for filled

**Ellipse**:
```json
{ "type": "ellipse", "id": "e1", "x": 100, "y": 100, "width": 150, "height": 150 }
```

**Diamond**:
```json
{ "type": "diamond", "id": "d1", "x": 100, "y": 100, "width": 150, "height": 150 }
```

**Labeled shape (container binding)** — create a text element bound to the shape:

> **WARNING:** Do NOT use `"label": { "text": "..." }` on shapes. This is NOT a valid
> Excalidraw property and will be silently ignored, producing blank shapes. You MUST
> use the container binding approach below.

The shape needs `boundElements` listing the text, and the text needs `containerId` pointing back:
```json
{ "type": "rectangle", "id": "r1", "x": 100, "y": 100, "width": 200, "height": 80,
  "roundness": { "type": 3 }, "backgroundColor": "#a5d8ff", "fillStyle": "solid",
  "boundElements": [{ "id": "t_r1", "type": "text" }] },
{ "type": "text", "id": "t_r1", "x": 105, "y": 110, "width": 190, "height": 25,
  "text": "Hello", "fontSize": 20, "fontFamily": 1, "strokeColor": "#1e1e1e",
  "textAlign": "center", "verticalAlign": "middle",
  "containerId": "r1", "originalText": "Hello", "autoResize": true }
```
- Works on rectangle, ellipse, diamond
- Text is auto-centered by Excalidraw when `containerId` is set
- The text `x`/`y`/`width`/`height` are approximate — Excalidraw recalculates them on load
- `originalText` should match `text`
- Always include `fontFamily: 1` (Virgil/hand-drawn font)

**Labeled arrow** — same container binding approach:
```json
{ "type": "arrow", "id": "a1", "x": 300, "y": 150, "width": 200, "height": 0,
  "points": [[0,0],[200,0]], "endArrowhead": "arrow",
  "boundElements": [{ "id": "t_a1", "type": "text" }] },
{ "type": "text", "id": "t_a1", "x": 370, "y": 130, "width": 60, "height": 20,
  "text": "connects", "fontSize": 16, "fontFamily": 1, "strokeColor": "#1e1e1e",
  "textAlign": "center", "verticalAlign": "middle",
  "containerId": "a1", "originalText": "connects", "autoResize": true }
```

**Standalone text** (titles and annotations only — no container):
```json
{ "type": "text", "id": "t1", "x": 150, "y": 138, "text": "Hello", "fontSize": 20,
  "fontFamily": 1, "strokeColor": "#1e1e1e", "originalText": "Hello", "autoResize": true }
```
- `x` is the LEFT edge. To center at position `cx`: `x = cx - (text.length * fontSize * 0.5) / 2`
- Do NOT rely on `textAlign` or `width` for positioning

**Arrow**:
```json
{ "type": "arrow", "id": "a1", "x": 300, "y": 150, "width": 200, "height": 0,
  "points": [[0,0],[200,0]], "endArrowhead": "arrow" }
```
- `points`: `[dx, dy]` offsets from element `x`, `y`
- `endArrowhead`: `null` | `"arrow"` | `"bar"` | `"dot"` | `"triangle"`
- `strokeStyle`: `"solid"` (default) | `"dashed"` | `"dotted"`

#### Arrow Bindings (connect arrows to shapes)

```json
{
  "type": "arrow", "id": "a1", "x": 300, "y": 150, "width": 150, "height": 0,
  "points": [[0,0],[150,0]], "endArrowhead": "arrow",
  "startBinding": { "elementId": "r1", "fixedPoint": [1, 0.5] },
  "endBinding": { "elementId": "r2", "fixedPoint": [0, 0.5] }
}
```

`fixedPoint` coordinates: `top=[0.5,0]`, `bottom=[0.5,1]`, `left=[0,0.5]`, `right=[1,0.5]`

#### Drawing Order (z-order)
- Array order = z-order (first = back, last = front)
- Emit progressively: background zones → shape → its bound text → its arrows → next shape
- BAD: all rectangles, then all texts, then all arrows
- GOOD: bg_zone → shape1 → text_for_shape1 → arrow1 → arrow_label_text → shape2 → text_for_shape2 → ...
- Always place the bound text element immediately after its container shape

#### Sizing Guidelines

**Font sizes:**
- Minimum `fontSize`: **16** for body text, labels, descriptions
- Minimum `fontSize`: **20** for titles and headings
- Minimum `fontSize`: **14** for secondary annotations only (sparingly)
- NEVER use `fontSize` below 14

**Element sizes:**
- Minimum shape size: 120x60 for labeled rectangles/ellipses
- Leave 20-30px gaps between elements minimum
- Prefer fewer, larger elements over many tiny ones

### Color Palette

See `references/excalidraw-colors.md` for full color tables. Quick reference:

| Use | Fill Color | Hex |
|-----|-----------|-----|
| Primary / Input | Light Blue | `#a5d8ff` |
| Success / Output | Light Green | `#b2f2bb` |
| Warning / External | Light Orange | `#ffd8a8` |
| Processing / Special | Light Purple | `#d0bfff` |
| Error / Critical | Light Red | `#ffc9c9` |
| Notes / Decisions | Light Yellow | `#fff3bf` |
| Storage / Data | Light Teal | `#c3fae8` |

### Tips
- Use the color palette consistently across the diagram
- **Text contrast is CRITICAL** — never use light gray on white backgrounds. Minimum text color on white: `#757575`
- Do NOT use emoji in text — they don't render in Excalidraw's font
- For dark mode diagrams, see `references/excalidraw-dark-mode.md`
- For larger examples, see `references/excalidraw-examples.md`
