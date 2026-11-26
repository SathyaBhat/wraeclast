---
name: html-design
description: Design HTML artifacts — high-fidelity one-offs (landing, deck, prototype) or throwaway variant mockups for side-by-side comparison.
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [design, html, prototype, ux, ui, creative, artifact, deck, motion, design-system, sketch, mockup, variants, exploration, wireframe, comparison]
    related_skills: [design-md, popular-web-designs, excalidraw, architecture-diagram, spike]
---

# HTML Design

Use this skill for all HTML/CSS/JS design work — from high-fidelity one-off artifacts to throwaway variant mockups for comparison. This skill is also the **web design umbrella**: load it first, then load the sibling skills below as needed.

This skill merges two former skills:
- **claude-design** — design process, taste, and doctrine for high-fidelity HTML artifacts
- **sketch** — throwaway 2-3 variant mockups for exploring a UI direction before committing

## Web Design Skill Map

| Skill | What it covers | Load when… |
|---|---|---|
| **html-design** (this skill) | Design *process and taste* — how to scope a brief, produce variants, verify an HTML artifact, avoid AI slop | Building or exploring any HTML artifact from scratch |
| **popular-web-designs** | 54 ready-to-paste design system references (Stripe, Linear, Vercel, Notion, etc.) — exact colors, typography, CSS values | User says "make it look like X" or you need a visual starting point |
| **design-md** | Google's DESIGN.md token spec format — author, lint, diff, export design-token files with WCAG contrast checking | Authoring a formal, persistent, machine-readable design-system spec file |

**Rule of thumb:**
- Process + taste → **html-design** (Mode A)
- Explore variants → **html-design** (Mode B)
- Match a real product's aesthetic → **popular-web-designs**
- Token spec file for a repo → **design-md**

## Related Skills (load alongside when relevant)

| Skill | What it gives you | Use when... |
|---|---|---|
| **html-design** (this one) | Design *process and taste* — how to scope a brief, produce variants, verify an HTML artifact, avoid AI slop | a from-scratch designed artifact or throwaway comparison mockups |
| **popular-web-designs** | 54 ready-to-paste design systems — exact colors, typography, components, CSS values for Stripe, Linear, Vercel, Notion, etc. | "make it look like Stripe / Linear / Vercel", visual starting point from a real product |
| **design-md** | Google's DESIGN.md spec format — author/validate/diff/export design-token files, WCAG contrast checking | a formal, persistent, machine-readable design-system *spec file* that lives in a repo |

Rule of thumb:
- **Process + taste, one-off artifact** → html-design (Mode A)
- **Explore variants before committing** → html-design (Mode B)
- **Match a known brand's look** → popular-web-designs (optionally combined with Mode A)
- **Author the tokens spec itself** → design-md

---

## Mode A — High-Fidelity One-Off Artifact

### When To Use Mode A

Triggers: landing pages, teaser pages, high-fidelity prototypes, interactive product mockups, visual option boards, component explorations, design-system previews, HTML slide decks, motion studies, onboarding flows, dashboards, settings, command palettes, modals, cards, forms, empty states, redesigns from screenshots/repos/brand docs.

Do **not** use Mode A for pure DESIGN.md token authoring — use `design-md` for that.

### Runtime Mode (CLI/API)

You are running in **CLI/API mode**, not the Claude Design hosted web UI.

Ignore references to hosted-only tools: `done()`, `fork_verifier_agent()`, `questions_v2()`, `copy_starter_component()`, `show_to_user()`, `show_html()`, `snip()`, `eval_js_user_view()`, hosted preview panes, `window.claude.complete()`, built-in tool schemas, `/projects/<projectId>/...` paths, etc.

Default deliverable: complete local HTML file, self-contained CSS and JS, exact on-disk path in final response, verified before reporting done.

### Core Identity

Act as an expert designer working with the user as manager.

HTML is the default tool, but the medium changes by assignment:
- UX designer for flows and product surfaces
- interaction designer for prototypes
- visual designer for static explorations
- motion designer for animated artifacts
- deck designer for presentations
- design-systems designer for tokens, components, and visual rules
- frontend-minded prototyper when code fidelity matters

Avoid generic web-design tropes unless explicitly asked.

### Start From Context, Not Vibes

Before designing, look for source context:
1. brand docs
2. existing product screenshots
3. current repo components
4. design tokens
5. UI kits
6. prior mockups
7. reference models
8. copy docs
9. constraints from legal, product, or engineering

If a repo is available, inspect theme files, token files, global stylesheets, layout scaffolds, component files, route/page files, form/button/card/navigation implementations before designing.

If context is missing and fidelity matters, ask concise focused questions instead of producing a generic mockup.

### Asking Questions

Ask when the assignment is new, ambiguous, high-fidelity, externally facing, or depends on taste. Keep questions short.

Ask for: intended output format, audience, fidelity level, source materials, brand/design system, number of variations, conservative vs divergent exploration, which dimension matters most (layout, visual, interaction, copy, motion, systemization).

Skip questions when the user gave enough direction, it's a small tweak, or the task is a continuation.

### Workflow

1. **Understand the brief** — what, for whom, what artifact, what constraints
2. **Gather context** — read docs, screenshots, repo files, design assets
3. **Define the design system** — colors, type, spacing, radii, shadows, motion posture, component treatment
4. **Choose the right format** — static comparison / clickable prototype / deck / component lab / motion study
5. **Build the artifact** — prefer single self-contained HTML file; preserve prior versions for major revisions
6. **Verify** — file exists, HTML saved completely, syntax checked; ideally open in browser and inspect
7. **Report briefly** — exact file path, what was created, caveats, next suggested action

### Artifact Format Rules

- Descriptive filename: e.g. `Landing Page.html`, `Command Palette Prototype.html`
- Embed CSS in `<style>`, JS in `<script>`
- Keep openable directly in a browser
- Avoid remote dependencies unless stable and explicitly useful
- Include responsive behavior unless intentionally fixed-size
- For significant revisions: `Name.html` → `Name v2.html`, `Name v3.html`

### HTML / CSS / JS Standards

Use modern CSS well: CSS variables for tokens, CSS grid for layout, container queries when helpful, `text-wrap: pretty`, real focus/hover states, `prefers-reduced-motion` for non-trivial motion, responsive scaling, semantic HTML.

Avoid: fragile hard-coded viewport assumptions, inaccessible tiny hit targets (<44px mobile), decorative JS that fights usability.

### Deck Rules

Fixed-size canvas (default 1920×1080, 16:9) scaled to fit viewport. Requirements: keyboard navigation, visible slide count, localStorage persistence, print-friendly layout, no speaker notes unless asked. Keep slides sparse. 1-2 background colors max.

### Prototype Rules

Make primary path clickable. Include key states: default, hover/focus, loading, empty, error, success. Expose variations with in-page controls. Persist important state in localStorage.

### Variation Rules

Default to at least three options:
1. **Conservative** — closest to existing patterns / lowest risk
2. **Strong-fit** — best interpretation of the brief
3. **Divergent** — more novel, for discovering taste boundaries

Variations explore layout, hierarchy, type scale, density, color posture, surface treatment, motion, interaction model, copy structure, or component shape — **not** just color swaps.

When the user picks a direction, consolidate. Don't leave the project as a pile of options forever.

### Tweakable Designs

When useful, add an in-page `Tweaks` panel controlling: theme mode, layout variant, density, accent color, type scale, motion on/off, copy variant, component variant. Keep it small and unobtrusive. Persist with localStorage.

### Anti-Slop Rules

Avoid: aggressive gradient backgrounds, glassmorphism by default, emoji unless brand uses them, generic SaaS cards with icons everywhere, left-border accent callout cards, fake dashboards with arbitrary numbers, stock-photo hero sections, oversized rounded rectangles as hierarchy substitute, rainbow palettes, vague labels like "Insights / Growth / Scale / Optimize" without content, decorative SVG illustrations pretending to be product imagery.

Minimal is not automatically good. Dense is not automatically cluttered. Choose intentionally.

### Typography

Use existing type system if one exists. Otherwise choose deliberately:
- editorial: serif or humanist headline + restrained sans body
- software/productivity: precise sans with strong numeric treatment
- luxury/minimal: fewer weights, more spacing discipline
- technical: mono accents only, not mono everywhere
- deck: large, clear, high contrast

Use type as hierarchy before adding boxes, icons, or color.

### Color

Use brand/design-system colors first. If no palette: define a small system (neutrals, surface, ink, muted text, border, accent, danger/success). One primary accent unless the assignment calls for more. Prefer oklch for harmonious invented palettes. Check contrast for important text and controls.

### Layout and Composition

Design with rhythm: scale, whitespace, density, alignment, repetition, contrast, interruption. Avoid making every section the same card grid. For product UIs: speed of comprehension over decoration. For marketing: one idea per section. For dashboards: only data that helps the user decide or act.

### Motion

Good motion: clarifies state changes, reduces loading anxiety, shows continuity, gives controls tactility, stays subtle. Bad motion: loops without purpose, delays the user, hides poor hierarchy. Always respect `prefers-reduced-motion`.

### Content Discipline

Every element must earn its place. Avoid: fake metrics, decorative stats, generic feature grids, unnecessary icons, placeholder testimonials, AI-generated fluff, invented content that changes strategy or claims. Mark copy as draft if not final.

### React Guidance

Use plain HTML/CSS/JS by default. Use React only when: meaningful state is needed, variants/toggles are easier as components, interaction complexity warrants it, or target is React/Next.js. If using React from CDN: pin exact versions, avoid `type="module"` unless necessary, give global style objects specific names.

### Verification

Minimum: file exists, HTML saved completely, obvious syntax issues checked.
Better: open in browser, check console errors, inspect screenshots, test key interactions, test light/dark variants, test responsive breakpoints.

Never say "done" if the file was not actually written.

### Final Response Format

```text
Created: /path/to/Prototype.html
It includes 3 layout variants, a Tweaks panel for density/theme, and responsive behavior.
Verified: file exists and opened cleanly in browser, no console errors.
Next: pick the strongest direction and I'll tighten copy + motion.
```

---

## Mode B — Throwaway Variant Mockups (Sketch)

### When To Use Mode B

Triggers: "sketch this screen", "show me what X could look like", "compare layout A vs B", "give me 2-3 takes on this UI", "let me see some variants", "mockup this before I build", "show me variants".

Do **not** use Mode B when: the user wants a production component (build it properly), a polished one-off artifact (use Mode A), a diagram (use `excalidraw`), or the design is already locked.

### GSD Integration

If `gsd-sketch` shows up as a sibling skill (installed via `npx get-shit-done-cc --hermes`), prefer **`gsd-sketch`** for the full workflow: persistent `.planning/sketches/` with MANIFEST, frontier mode analysis, consistency audits. This mode is the lightweight standalone version.

### Core Method

```
intake  →  variants  →  head-to-head  →  pick winner (or iterate)
```

#### 1. Intake (skip if enough context given)

Get three things, one question at a time:
1. **Feel.** "What should this feel like? Adjectives, emotions, a vibe."
2. **References.** "What apps, sites, or products capture the feel you're imagining?"
3. **Core action.** "What's the single most important thing a user does on this screen?"

Reflect each answer briefly before the next question. If all three were given upfront, skip to variants.

#### 2. Variants (2-3, never 1, rarely 4+)

Produce **2-3 variants** in one go. Each is a complete standalone HTML file. Build them — don't describe them. The point is comparison.

Each variant takes a **different design stance**, not different pixel values:
- **Density:** compact / airy / ultra-dense
- **Emphasis:** content-first / action-first / tool-first
- **Aesthetic:** editorial / utilitarian / playful
- **Layout:** single-column / sidebar / split-pane
- **Grounding:** card-based / bare-content / document-style

Pick one axis and pull apart from it. Two variants differing only in accent color is wasted effort.

**Variant naming:** describe the stance, not the number.

```
sketches/
├── 001-calm-editorial/
│   ├── index.html
│   └── README.md
├── 001-utilitarian-dense/
│   ├── index.html
│   └── README.md
└── 001-playful-split/
    ├── index.html
    └── README.md
```

#### 3. Make Them Real HTML

Each variant is a **single self-contained HTML file**:
- Inline `<style>` — no build step, no external CSS
- System fonts or one Google Font via `<link>`
- Tailwind via CDN is fine
- Realistic fake content — actual sentences, actual names, not "Lorem ipsum"
- **Interactive**: links clickable, hovers real, at least one state transition

**Default CSS reset:**
```html
<style>
  * { box-sizing: border-box; margin: 0; padding: 0; }
  body {
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto,
                 "Helvetica Neue", Arial, sans-serif;
    -webkit-font-smoothing: antialiased;
    color: #1a1a1a;
    background: #fafafa;
    line-height: 1.5;
  }
</style>
```

**Verify variants visually — use browser tools:**
```
browser_navigate(url="file:///absolute/path/to/sketches/001-calm-editorial/index.html")
browser_vision(question="Does this layout look clean and readable? Any visible bugs?")
```

Fix and re-navigate until each variant looks right.

#### 4. Variant README

```markdown
## Variant: {stance name}

### Design stance
One sentence on the principle driving this variant.

### Key choices
- Layout: ...
- Typography: ...
- Color: ...
- Interaction: ...

### Trade-offs
- Strong at: ...
- Weak at: ...

### Best for
- The kind of user or use case this variant actually serves
```

#### 5. Head-to-Head

After all variants are built, present a comparison table and **opinionate**:

```markdown
## Three takes on the home screen

| Dimension | Calm editorial | Utilitarian dense | Playful split |
|-----------|----------------|-------------------|---------------|
| Density   | Low            | High              | Medium        |
| Primary action visibility | Low | High | Medium |
| Feel | Calm, trusted | Sharp, tool-like | Inviting |

**My take:** Utilitarian dense for power users, calm editorial for content-forward audiences.
```

### Interactivity Bar

A sketch is interactive enough when the user can:
1. Click a primary action and something visible happens
2. See one meaningful state transition (filter, toggle, open/close)
3. Hover recognizable affordances (buttons, rows, tabs)

More = over-engineering a throwaway. Less = a screenshot.

### Theming

If the user has an existing theme, put shared tokens in `sketches/themes/tokens.css` and `@import` in each variant. Keep minimal: three colors and one font is usually enough.

### Frontier Mode (what to sketch next)

If sketches already exist and the user asks "what should I sketch next?":
- **Consistency gaps** — winning variants made independent choices not yet composed
- **Unsketched screens** — referenced but never explored
- **State coverage** — happy path sketched, but not empty/loading/error/1000-items
- **Responsive gaps** — validated at one viewport
- **Interaction patterns** — static layouts, but transitions/drag/scroll unexplored

### Output

- Create `sketches/` (or `.planning/sketches/` for GSD) in repo root
- One subdir per variant: `NNN-stance-name/index.html` + `README.md`
- Tell user how to open: `open sketches/001-calm-editorial/index.html` (macOS), `xdg-open` (Linux), `start` (Windows)
- Keep variants disposable — preserved sketches should be promoted into real code

**Typical tool sequence:**
```
terminal("mkdir -p sketches/001-calm-editorial")
write_file("sketches/001-calm-editorial/index.html", "<!doctype html>...")
write_file("sketches/001-calm-editorial/README.md", "## Variant: Calm editorial\n...")
browser_navigate(url="file://$(pwd)/sketches/001-calm-editorial/index.html")
browser_vision(question="How does this look? Any obvious layout issues?")
```

---

## Pitfalls

- Do not paste hosted tool schemas into runtime context — they cause fake tool calls
- Do not strip design doctrine while removing hosted-tool plumbing
- Do not over-ask when the user already gave enough direction
- Do not under-ask for high-fidelity work with no brand context
- Do not produce generic SaaS layouts and call them designed
- Do not claim browser verification unless it actually happened
- Do not create variant mockups that differ only in accent color — different stances, not pixel tweaks
- Do not leave a project as a pile of options forever — consolidate after the user picks a direction
- Mode A artifacts should be self-contained and openable in a browser without a build step
- Mode B sketches are disposable — don't curate them, promote good ones to real code

## Attribution

Mode B (Sketch) adapted from the GSD (Get Shit Done) project's `/gsd-sketch` workflow — MIT © 2025 Lex Christopherson ([gsd-build/get-shit-done](https://github.com/gsd-build/get-shit-done)).
