---
name: research
description: "Research umbrella: discover papers, monitor feeds, build knowledge wikis, write papers — route to the right skill."
version: 1.0.0
author: Hermes Agent (curator)
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [research, arxiv, papers, academic, wiki, knowledge-base, rss, blog-monitoring, writing, literature-review]
    related_skills: [research-discovery, llm-wiki, research-paper-writing]
---

# Research Umbrella

Three sibling skills cover the full research lifecycle — from discovering papers and monitoring feeds, to building a persistent knowledge base, to writing and publishing academic work. Load this umbrella to orient; load the specific skill for execution.

## Skill Map

| Skill | Phase | Load when… |
|---|---|---|
| **research-discovery** | Discovery | Search arXiv, get citations from Semantic Scholar, generate BibTeX, monitor blogs/RSS feeds via blogwatcher-cli |
| **llm-wiki** | Synthesis | Build or query a Karpathy-style interlinked markdown knowledge base; synthesize findings from multiple sources into a navigable wiki |
| **research-paper-writing** | Production | Draft, outline, revise, and format an academic paper; structure sections; write abstracts and introductions |

## Research Workflow

**Typical flow for a research task:**

```
1. research-discovery  →  find the right papers, assess citation impact, monitor fields
2. llm-wiki            →  ingest findings, build a navigable knowledge base, track summaries
3. research-paper-writing → draft the paper, structure arguments, write from the knowledge base
```

**Quick lookup / single paper:** load only `research-discovery`

**Domain synthesis / literature review:** load `research-discovery` + `llm-wiki`

**Writing a paper:** load all three, or `llm-wiki` + `research-paper-writing` if discovery is done

## Key Capabilities by Skill

### research-discovery
- arXiv API search (no key needed): title, author, abstract, category, date filters
- Semantic Scholar: citation counts, reference lists, related-paper recommendations, author profiles
- BibTeX generation from arXiv IDs
- blogwatcher-cli: add/scan RSS/Atom feeds, track unread articles, import OPML
- Helper script: `scripts/search_arxiv.py` (stdlib only)

### llm-wiki
- Karpathy-style interlinked markdown knowledge base at `~/.hermes/wiki/` (or custom path)
- Commands: `wiki search`, `wiki add`, `wiki link`, `wiki show`, `wiki export`
- Good for accumulating and cross-linking research notes across sessions

### research-paper-writing
- Academic writing guidance: section structure, argumentation, abstract/intro patterns
- Revision and editing workflows
- Formatting for common venues (arXiv, NeurIPS, ICML, etc.)

## Pitfalls

- **arXiv rate limiting**: ~1 req/3s without auth. Use the helper script for bursts; it respects the rate limit.
- **Withdrawn papers**: check `<summary>` for "withdrawn"/"retracted" before treating as valid; arXiv keeps them indexed.
- **LLM-wiki vs direct notes**: llm-wiki adds value when you're synthesizing many sources with cross-links; for a single paper summary, a plain `write_file` note may be faster.
- **BibTeX version drift**: use versioned arXiv IDs (e.g. `1706.03762v7`) in citations to prevent changes over time.
