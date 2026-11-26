---
name: web-design
description: "Web design umbrella: high-fidelity HTML artifacts, 54 real design systems, and Google DESIGN.md token spec — route to the right skill."
version: 1.0.0
author: Hermes Agent (curator)
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [web-design, html, css, design-systems, tokens, stripe, linear, vercel, figma, tailwind, ui, visual-design]
    related_skills: [html-design, popular-web-designs, design-md, baoyu-infographic, creative-coding, diagrams]
---

# Web Design Umbrella

Three sibling skills cover the web design space — from building individual high-fidelity HTML artifacts to referencing production design systems to authoring Google's DESIGN.md token spec. Load this umbrella to orient; load the specific skill for execution.

## Skill Map

| Skill | Load when… |
|---|---|
| **html-design** | Building a single high-fidelity HTML/CSS artifact (landing page, dashboard, component, one-off demo) — everything inline in one file, no build step |
| **popular-web-designs** | Referencing an established design system (Stripe, Linear, Vercel, Apple, Airbnb, etc.) as a style source — copying their visual DNA into your own work |
| **design-md** | Authoring, validating, or exporting a Google-style DESIGN.md design token spec file |
| **baoyu-infographic** | Generating a rich single-file HTML infographic with one of 21 layouts × 21 visual styles — data storytelling, visual reports, knowledge cards |

## Routing Guide

**"Build me a landing page / dashboard / UI component"** → **html-design**

**"Style this like Stripe / Linear / Notion / Vercel / Apple"** → **popular-web-designs** (look up that system, then apply via **html-design**)

**"I need a design token spec / DESIGN.md file"** → **design-md**

**Create an infographic / visual data story / knowledge card** → **baoyu-infographic**

**Make generative art or a canvas animation** → NOT this umbrella → load **creative-coding** instead

**"Draw an architecture diagram / flowchart"** → NOT this umbrella → load **diagrams** instead

## Shared Doctrine (applies across all three)

### File-first, no build step

All three skills produce artifacts that must be **self-contained** — no npm, no bundler, no server. Every dependency goes inline or via a stable CDN link. This is non-negotiable for artifacts the user can open directly.

### Visual quality bar

- Dark themes preferred unless the brief specifies light
- Typography: choose one pairing (e.g. Inter + JetBrains Mono) and be consistent
- Spacing: use a consistent scale (4px / 8px grid) — don't mix arbitrary values
- Color: define a palette (2–5 colors) up front; apply consistently throughout
- Motion: use it sparingly and purposefully — no gratuitous transitions

### Verification pattern

After writing any HTML artifact, **always** verify it visually:

```
browser_navigate(url="file:///absolute/path/to/output.html")
browser_vision(question="Does the layout look correct? Any visual artifacts?")
# Iterate until browser_vision confirms quality
```

Never report an artifact as done without visual confirmation.

## When Multiple Skills Are Needed

**"Style this like Linear and build the HTML":**
1. `popular-web-designs` — load the Linear design system reference
2. `html-design` — build the artifact using Linear's visual DNA

**"Create a token spec for our new design system":**
1. `design-md` — author the DESIGN.md token spec
2. `html-design` — prototype the component library from the tokens

## Pitfalls

- **popular-web-designs ≠ a template library** — it's a reference bank of established design system patterns to inform your own work, not copy-paste boilerplate
- **design-md is Google's format** — it produces a DESIGN.md token file, not a component library; validate with the design-md skill's built-in linter before exporting
- **html-design artifacts are one-offs** — for reusable component systems, use a proper framework (but that's outside these skills' scope)
