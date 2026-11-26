---
name: creative-coding
description: "Creative coding umbrella: generative art, animation, ASCII, real-time visuals — route to the right tool and apply shared delivery patterns."
version: 1.0.0
author: Hermes Agent (curator)
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [creative-coding, generative-art, animation, ascii, canvas, p5js, manim, touchdesigner, ascii-art, ascii-video, pretext, visualization, browser-artifact]
    related_skills: [p5js, pretext, ascii-art, ascii-video, manim-video, touchdesigner-mcp, diagrams, html-design, baoyu-infographic]
---

# Creative Coding Umbrella

Six sibling skills cover the creative coding space. This umbrella provides routing logic, shared delivery patterns, and aesthetic doctrine that applies across all of them.

## Skill Map

| Skill | Medium | Output | Load when… |
|---|---|---|---|
| **p5js** | Browser canvas (JS) | Single-file HTML artifact | Generative art, interactive sketches, WebGL/shaders, data viz, 2D/3D animations in browser |
| **pretext** | Browser canvas (JS, @chenglou/pretext) | Single-file HTML artifact | DOM-free text-as-geometry, kinetic typography, text-layout experiments |
| **ascii-art** | Terminal / raster→text | Text / PNG | Convert images to ASCII; standalone text art from prompts; cowsay/figlet |
| **ascii-video** | Terminal / ffmpeg | MP4 or GIF | ASCII-ified video or audio visualization; animate ASCII frames over time |
| **manim-video** | Python (Manim CE) | MP4 | Mathematical / algorithmic animations in 3Blue1Brown style; precise rendered video |
| **touchdesigner-mcp** | TouchDesigner (via MCP) | Real-time visual / video | Live visuals, audio-reactive VJ sets, GLSL shaders, installations; requires TD running |

## Routing Guide

**"Make generative art / an interactive sketch"** → **p5js**

**"Animate text / kinetic typography / text layout"** → **pretext**

**"Convert this image/screenshot to ASCII"** or **"draw me ASCII art of X"** → **ascii-art**

**"Make an ASCII animation" / "ASCII music visualizer"** → **ascii-video**

**"Explain this algorithm visually" / "make a 3Blue1Brown-style animation"** → **manim-video**

**"Build a live visual / audio-reactive VJ set / TouchDesigner network"** → **touchdesigner-mcp**

**Ambiguous prompt (e.g. "animate X")** → prefer **p5js** for browser-first delivery; escalate to **manim-video** when precise math rendering matters, **touchdesigner-mcp** when real-time interactivity is required.

**"Draw a system diagram / architecture diagram / flowchart"** → **NOT this umbrella** → load **diagrams** instead (dark-themed SVG HTML diagrams + Excalidraw JSON). That skill is in the same `creative` category but is for technical diagrams, not generative art.

**"Build a high-fidelity UI / style it like Stripe or Linear / author a DESIGN.md token spec"** → **NOT this umbrella** → load **web-design** instead (covers `html-design`, `popular-web-designs`, `design-md`).

## Shared Delivery Pattern (p5js, pretext, html-based skills)

These skills all deliver a **single self-contained HTML file**:

```
write_file("output.html", "<html>...")
browser_navigate(url="file:///absolute/path/to/output.html")
browser_vision(question="Does the animation run correctly? Any visual issues?")
# Iterate until browser_vision confirms it looks right
```

Rules:
- **No build step** — embed all CSS and JS inline or via stable CDN `<script>` tags
- **Verify before reporting done** — always run `browser_navigate` + `browser_vision`; never say "done" without visual confirmation
- **First render must be excellent** — if the user sees it first in a browser, it must be good from the first load
- **Go beyond the reference vocabulary** — don't just reproduce the example from the skill docs; apply it creatively to the user's actual request

## Shared Aesthetic Doctrine

These principles apply across all visual creative coding output unless the user specifies otherwise:

1. **Dark backgrounds by default** — rich dark (#0a0a0a, #111, deep navy) unless the brief says light
2. **Intentional color palette** — 2-4 colors maximum; define them up front; use them consistently
3. **Motion serves meaning** — every animation should communicate something (rhythm, structure, transformation, data); pure decoration is noise
4. **Density is a choice** — sparse and dense are both valid; pick one deliberately
5. **First frame matters** — even animated work should look considered if paused on frame 0

## Output Format by Skill

| Skill | Primary output | Delivery |
|---|---|---|
| p5js | HTML file | `write_file` → `browser_navigate` → `browser_vision` |
| pretext | HTML file | `write_file` → `browser_navigate` → `browser_vision` |
| ascii-art | Text / PNG | Terminal output or `write_file` |
| ascii-video | MP4 / GIF | `terminal` ffmpeg pipeline → share path |
| manim-video | MP4 | `terminal` manim render → share path |
| touchdesigner-mcp | Real-time / MP4 | MCP tools → `td_get_screenshot` / `MovieFileOut` |

## Pitfalls

- **p5js vs pretext confusion**: p5js is for graphics/canvas. pretext is specifically for text-as-geometry layout — don't use p5js when the user wants text-layout kinetics.
- **ascii-art vs ascii-video**: ascii-art is for static images; ascii-video handles temporal/animated ASCII output.
- **manim is slow**: Manim renders are CPU-bound and take 30s–5min. Set expectations and use `background=True` for long scenes.
- **TouchDesigner requires a running instance**: The MCP skill cannot start TD. If it's not running, tell the user.
- **Don't claim browser verification without doing it**: Run `browser_navigate` + `browser_vision` before reporting.
