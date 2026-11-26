---
name: software-development
description: "Software development umbrella: spike experiments, TDD, debugging, and code quality — route to the right skill and apply shared engineering doctrine."
version: 1.0.0
author: Hermes Agent (curator)
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [software-development, tdd, testing, debugging, code-quality, spike, engineering, pre-commit, linting]
    related_skills: [spike, test-driven-development, debugging, code-quality, plan]
---

# Software Development Umbrella

Four sibling skills cover the software development lifecycle — from quick throwaway experiments through disciplined test-first development to systematic debugging and automated quality gates. Load this umbrella to orient; load the specific skill for execution.

## Skill Map

| Skill | Phase | Load when… |
|---|---|---|
| **spike** | Exploration | Validate a risky idea or unknown API with a throwaway experiment BEFORE writing production code; time-boxed, discardable |
| **test-driven-development** | Development | Write a failing test first, then make it pass; strict RED→GREEN→REFACTOR cycle; use for all non-trivial production code |
| **debugging** | Investigation | Systematic root-cause investigation of a bug, failure, or unexpected behaviour; 4-phase methodology |
| **code-quality** | Maintenance | Pre-commit hooks, linting, type-checking, formatting, CI integration; enforce quality gates across the codebase |

## Routing Guide

**"I don't know if this API/library/approach will work"** → **spike** first, then build for real

**"Build this feature / implement this function"** → **test-driven-development** (write tests first)

**"This is broken and I don't know why"** → **debugging**

**"Set up linting / pre-commit / CI quality gates"** → **code-quality**

**"I need to plan a larger change"** → **plan** (separate skill for actionable markdown planning)

**Ambiguous "fix this bug"** → start with **debugging** to find root cause, then apply **test-driven-development** to fix it with a regression test

## Shared Engineering Doctrine

### Don't skip the spike
If there's uncertainty about whether an approach works (new library, undocumented API, unfamiliar pattern), a 30-minute spike is always faster than a 3-day failed implementation. The spike's only deliverable is a decision: *go/no-go and which approach.*

### Test first, always
For production code: write the failing test before touching the implementation. This is not optional. A test written after the fact is documentation, not a safety net.

### Root-cause before fix
Never apply a fix before understanding the root cause. A fix without root-cause understanding creates two bugs: the original one (still latent) and the new one introduced by the blind patch.

### Quality gates belong in CI
Code quality checks (linting, type errors, test failures) must run automatically on every commit. Manual checks are skipped under pressure. Automate them once, enforce them always.

## Typical Workflows

**New feature with uncertainty:**
1. `spike` — validate the risky parts in isolation
2. `test-driven-development` — build the real thing test-first

**Bug report lands:**
1. `debugging` — reproduce, isolate, find root cause
2. `test-driven-development` — write a failing regression test first, then fix

**Onboarding to a new codebase:**
1. `code-quality` — understand and enable the existing quality gates
2. `test-driven-development` — use as the development pattern for contributions

## Pitfalls

- **Spiking forever** — a spike has a time box (30–60 min). If it grows into a full implementation, you've already shipped without tests
- **TDD on trivial code** — don't write tests for `return x + 1`. TDD is for logic that can break, has edge cases, or will be modified
- **Debugging by adding print statements** — print-driven debugging is fine as a first pass, but the `debugging` skill's 4-phase methodology scales to hard problems; use it when the first pass fails
- **Code quality as a one-time setup** — quality gates only work if they block merges; enforce them in CI, not just locally
