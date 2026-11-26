---
name: ai-coding-agents
description: "Delegate coding tasks to AI agent CLIs — Claude Code (Anthropic), Codex (OpenAI), and OpenCode (provider-agnostic). Covers one-shot execution, background long-running tasks, parallel worktrees, PR creation and review."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [Coding-Agent, Claude, Anthropic, Codex, OpenAI, OpenCode, Code-Review, Refactoring, PTY, Automation, Parallel]
    related_skills: [hermes-agent]
    triggers:
      - "delegate coding"
      - "use Claude Code"
      - "use Codex"
      - "use OpenCode"
      - "coding agent"
      - "autonomous coding"
      - "AI coding agent"
      - "claude code"
      - "openai codex"
      - "opencode"
---

# AI Coding Agents — Hermes Orchestration Guide

Hermes can delegate coding tasks to three autonomous AI agent CLIs. All three can read files, write code, run shell commands, and manage git workflows with minimal supervision. Choose the right tool based on your provider, model preferences, and task type.

## When to Use AI Coding Agent CLIs

Use an AI coding agent CLI when you need to:
- **Implement features or fixes** — hand off a ticket/issue description; the agent autonomously codes, tests, and commits
- **Refactor large codebases** — complex multi-file changes where guiding every edit by hand is impractical
- **Review PRs** — agents can read diffs, check for bugs, security issues, and style problems
- **Parallelize work** — run multiple agents in isolated git worktrees simultaneously, each fixing a different issue
- **Run long-running coding sessions** — delegate in the background and check progress later

### Choosing the Right Agent

| Agent | When to prefer |
|-------|----------------|
| **Claude Code** | Default choice. Best-in-class reasoning, rich feature set (subagents, MCP, hooks, streaming JSON). Requires Anthropic API key or Claude Pro/Max subscription. |
| **Codex** | OpenAI ecosystem. Same core patterns as Claude Code. Use when you have Codex/OpenAI auth configured. |
| **OpenCode** | Provider-agnostic (works with OpenRouter, Anthropic, OpenAI, etc.). Open-source TUI. Use when you want model flexibility or prefer open-source tooling. |

---

## Claude Code

Anthropic's autonomous coding agent CLI. Full reference: https://code.claude.com/docs/en/cli-reference

### Prerequisites

```bash
npm install -g @anthropic-ai/claude-code
claude           # First run: browser OAuth (Pro/Max) or set ANTHROPIC_API_KEY
claude auth login --console   # For API key billing
claude auth status            # Verify login
claude doctor                 # Health check
```

### Mode 1: Print Mode (`-p`) — Preferred for Most Tasks

Print mode runs a one-shot task, returns the result, and exits. No PTY needed. Skips ALL interactive dialogs (no workspace trust, no permission prompts) — ideal for automation.

```
terminal(command="claude -p 'Add error handling to all API calls in src/' --allowedTools 'Read,Edit' --max-turns 10", workdir="/path/to/project", timeout=120)
```

**Structured JSON output:**
```
terminal(command="claude -p 'Analyze auth.py for security issues' --output-format json --max-turns 5", workdir="/project", timeout=120)
```

Returns a JSON object with `result`, `session_id`, `num_turns`, `total_cost_usd`, `stop_reason`.

**Piped input:**
```
terminal(command="git diff HEAD~3 | claude -p 'Summarize these changes' --max-turns 1", timeout=60)
```

**Session continuation:**
```
# Capture session_id from first run, then resume
terminal(command="claude -p 'Continue and add connection pooling' --resume <session_id> --max-turns 5", workdir="/project", timeout=120)
```

### Mode 2: Interactive PTY via tmux — Multi-Turn Sessions

```
terminal(command="tmux new-session -d -s claude-work -x 140 -y 40")
terminal(command="tmux send-keys -t claude-work 'cd /path/to/project && claude' Enter")
terminal(command="sleep 5 && tmux send-keys -t claude-work 'Refactor the auth module to use JWT tokens' Enter")
terminal(command="sleep 15 && tmux capture-pane -t claude-work -p -S -50")
terminal(command="tmux send-keys -t claude-work 'Now add unit tests for the new JWT code' Enter")
terminal(command="tmux send-keys -t claude-work '/exit' Enter")  # Done
```

**Reading TUI status:**
- `❯` at bottom = waiting for input (done or asking a question)
- `●` lines = actively using tools

### PTY Dialog Handling (Interactive Mode Only)

Claude Code presents up to two dialogs on first launch:

**Dialog 1: Workspace Trust** — press `Enter` (default is "Yes, I trust this folder")

**Dialog 2: `--dangerously-skip-permissions` warning** — default is "No, exit" (WRONG). Must navigate down first:
```
tmux send-keys -t <session> Down && sleep 0.3 && tmux send-keys -t <session> Enter
```

> Tip: Print mode (`-p`) skips both dialogs entirely. Prefer it for automation.

### Key CLI Flags (Claude Code)

| Flag | Effect |
|------|--------|
| `-p` / `--print` | Non-interactive one-shot mode |
| `--max-turns <n>` | Limit agentic loops (print mode only) |
| `--max-budget-usd <n>` | Cap spend in dollars (min ~$0.05) |
| `--dangerously-skip-permissions` | Auto-approve all tool use |
| `--allowedTools <tools>` | Whitelist specific tools (e.g., `Read,Edit`) |
| `--output-format json` | Structured result JSON |
| `--output-format stream-json` | Streaming JSON events |
| `--model <alias>` | `sonnet`, `opus`, `haiku`, or full model name |
| `--effort <level>` | `low`, `medium`, `high`, `max`, `auto` |
| `-w, --worktree [name]` | Run in an isolated git worktree |
| `--from-pr <number>` | Resume session linked to a GitHub PR |
| `--bare` | Skip hooks, plugins, MCP (fastest for CI/scripting) |
| `--continue` / `-c` | Resume most recent conversation in current dir |

### Parallel Claude Code Instances

```
terminal(command="tmux new-session -d -s task1 -x 140 -y 40 && tmux send-keys -t task1 'cd ~/project && claude -p \"Fix the auth bug in src/auth.py\" --allowedTools \"Read,Edit\" --max-turns 10' Enter")
terminal(command="tmux new-session -d -s task2 -x 140 -y 40 && tmux send-keys -t task2 'cd ~/project && claude -p \"Write integration tests for the API endpoints\" --allowedTools \"Read,Write,Bash\" --max-turns 15' Enter")
# Monitor all
terminal(command="sleep 30 && for s in task1 task2; do echo '=== '$s' ==='; tmux capture-pane -t $s -p -S -5; done")
# Cleanup
terminal(command="tmux kill-session -t task1 && tmux kill-session -t task2")
```

Or use Claude's built-in worktree + tmux support:
```
terminal(command="claude -w feature-x --tmux", workdir="/path/to/repo")
```

### PR Review (Claude Code)

**Quick review via print mode:**
```
terminal(command="cd /path/to/repo && git diff main...feature-branch | claude -p 'Review this diff for bugs, security issues, and style problems.' --max-turns 1", timeout=60)
```

**From PR number:**
```
terminal(command="claude -p 'Review this PR thoroughly' --from-pr 42 --max-turns 10", workdir="/path/to/repo", timeout=120)
```

### Claude Code Pitfalls

1. **Interactive mode requires tmux** — Claude Code is a full TUI app; tmux gives `capture-pane` for monitoring
2. **`--dangerously-skip-permissions` dialog defaults to "No, exit"** — send Down then Enter; print mode skips this
3. **`--max-budget-usd` minimum ~$0.05** — system prompt cache alone costs this
4. **`--max-turns` is print-mode only** — ignored in interactive sessions
5. **Session resumption requires same directory** — `--continue` finds the most recent session for cwd
6. **`--bare` skips OAuth** — requires `ANTHROPIC_API_KEY`
7. **Context degradation above 70% window** — use `/compact` or `/clear` proactively
8. **Clean up tmux sessions** — `tmux kill-session -t <name>` when done

---

## Codex

OpenAI's autonomous coding agent CLI. Full reference: https://github.com/openai/codex

### Prerequisites

```bash
npm install -g @openai/codex
# Auth: OPENAI_API_KEY env var, or run `codex` once for OAuth login
# Must run inside a git repository
```

> Auth note: A CLI OAuth session may live under `~/.codex/auth.json`. Missing `OPENAI_API_KEY` alone doesn't mean auth is absent.

### One-Shot Tasks

```
terminal(command="codex exec 'Add dark mode toggle to settings'", workdir="~/project", pty=true)
```

For scratch work (Codex needs a git repo):
```
terminal(command="cd $(mktemp -d) && git init && codex exec 'Build a snake game in Python'", pty=true)
```

### Background Mode (Long Tasks)

```
terminal(command="codex exec --full-auto 'Refactor the auth module'", workdir="~/project", background=true, pty=true)
# Returns session_id

process(action="poll", session_id="<id>")
process(action="log", session_id="<id>")
process(action="submit", session_id="<id>", data="yes")  # If Codex asks a question
process(action="kill", session_id="<id>")
```

### Key Flags (Codex)

| Flag | Effect |
|------|--------|
| `exec "prompt"` | One-shot execution, exits when done |
| `--full-auto` | Sandboxed, auto-approves file changes in workspace |
| `--yolo` | No sandbox, no approvals (fastest, most dangerous) |
| `--sandbox danger-full-access` | No bubblewrap sandbox (use in gateway/container contexts) |

### Hermes Gateway Sandbox Caveat

When invoking Codex from a Hermes gateway/service context (e.g., Telegram-driven agent sessions), bubblewrap/user-namespace sandboxing may fail with errors like `setting up uid map: Permission denied`. In that context, prefer:

```
codex exec --sandbox danger-full-access "<task>"
```

Use process boundaries as the safety layer: explicit `workdir`, clean git status before launch, narrow task prompts, `git diff` review, and targeted tests before committing.

### PR Reviews (Codex)

```
terminal(command="REVIEW=$(mktemp -d) && git clone https://github.com/user/repo.git $REVIEW && cd $REVIEW && gh pr checkout 42 && codex review --base origin/main", pty=true)
```

### Parallel Issue Fixing with Worktrees (Codex)

```
terminal(command="git worktree add -b fix/issue-78 /tmp/issue-78 main", workdir="~/project")
terminal(command="git worktree add -b fix/issue-99 /tmp/issue-99 main", workdir="~/project")

terminal(command="codex --yolo exec 'Fix issue #78: <description>. Commit when done.'", workdir="/tmp/issue-78", background=true, pty=true)
terminal(command="codex --yolo exec 'Fix issue #99: <description>. Commit when done.'", workdir="/tmp/issue-99", background=true, pty=true)

process(action="list")

# After completion, push and create PRs
terminal(command="cd /tmp/issue-78 && git push -u origin fix/issue-78")
terminal(command="gh pr create --repo user/repo --head fix/issue-78 --title 'fix: ...' --body '...'")

# Cleanup
terminal(command="git worktree remove /tmp/issue-78", workdir="~/project")
```

### Codex Rules

1. **Always use `pty=true`** — Codex is an interactive terminal app and hangs without a PTY
2. **Git repo required** — use `mktemp -d && git init` for scratch work
3. **Use `exec` for one-shots** — runs and exits cleanly
4. **`--full-auto` for building** — auto-approves changes within sandbox
5. **Background for long tasks** — use `background=true` and monitor with `process` tool
6. **Parallel is fine** — run multiple Codex processes at once for batch work

---

## OpenCode

Provider-agnostic, open-source AI coding agent with a TUI and CLI. Full reference: https://opencode.ai

### Prerequisites

```bash
npm i -g opencode-ai@latest   # or: brew install anomalyco/tap/opencode
opencode auth login            # Or set provider env vars (OPENROUTER_API_KEY, etc.)
opencode auth list             # Verify at least one provider is configured
```

**Binary resolution check** (if behavior differs between terminal and Hermes):
```
terminal(command="which -a opencode")
terminal(command="opencode --version")
# If needed, pin the binary:
terminal(command="$HOME/.opencode/bin/opencode run '...'", workdir="~/project", pty=true)
```

### One-Shot Tasks (`opencode run`)

```
terminal(command="opencode run 'Add retry logic to API calls and update tests'", workdir="~/project")
```

With context files:
```
terminal(command="opencode run 'Review this config for security issues' -f config.yaml -f .env.example", workdir="~/project")
```

With model thinking visible:
```
terminal(command="opencode run 'Debug why tests fail in CI' --thinking", workdir="~/project")
```

Force a specific model:
```
terminal(command="opencode run 'Refactor auth module' --model openrouter/anthropic/claude-sonnet-4", workdir="~/project")
```

> `opencode run` does NOT need `pty=true` — it's non-interactive.

### Interactive TUI Sessions (Background)

```
terminal(command="opencode", workdir="~/project", background=true, pty=true)
# Returns session_id

process(action="submit", session_id="<id>", data="Implement OAuth refresh flow and add tests")
process(action="poll", session_id="<id>")
process(action="log", session_id="<id>")
process(action="submit", session_id="<id>", data="Now add error handling for token expiry")

# Exit: Ctrl+C (NOT /exit — that opens agent selector)
process(action="write", session_id="<id>", data="\x03")
# Or: process(action="kill", session_id="<id>")
```

### Key Flags (OpenCode)

| Flag | Effect |
|------|--------|
| `run 'prompt'` | One-shot execution and exit |
| `--continue` / `-c` | Continue last OpenCode session |
| `--session <id>` / `-s` | Continue a specific session |
| `--agent <name>` | Choose agent: `build` or `plan` |
| `--model provider/model` | Force specific model |
| `--format json` | Machine-readable output/events |
| `--file <path>` / `-f` | Attach file(s) to the message |
| `--thinking` | Show model thinking blocks |
| `--variant <level>` | Reasoning effort: `high`, `max`, `minimal` |

### PR Review (OpenCode)

Built-in PR command:
```
terminal(command="opencode pr 42", workdir="~/project", pty=true)
```

Or review in a temporary clone:
```
terminal(command="REVIEW=$(mktemp -d) && git clone https://github.com/user/repo.git $REVIEW && cd $REVIEW && opencode run 'Review this PR vs main. Report bugs, security risks, test gaps, and style issues.' -f $(git diff origin/main --name-only | head -20 | tr '\n' ' ')", pty=true)
```

### Parallel Work Pattern (OpenCode)

Use separate workdirs/worktrees to avoid collisions:

```
terminal(command="opencode run 'Fix issue #101 and commit'", workdir="/tmp/issue-101", background=true, pty=true)
terminal(command="opencode run 'Add parser regression tests and commit'", workdir="/tmp/issue-102", background=true, pty=true)
process(action="list")
```

### Session & Cost Management (OpenCode)

```
terminal(command="opencode session list")
terminal(command="opencode stats")
terminal(command="opencode stats --days 7 --models anthropic/claude-sonnet-4")
```

### TUI Keybindings (OpenCode)

| Key | Action |
|-----|--------|
| `Enter` | Submit message (press twice if needed) |
| `Tab` | Switch between agents (build/plan) |
| `Ctrl+P` | Open command palette |
| `Ctrl+X L` | Switch session |
| `Ctrl+X M` | Switch model |
| `Ctrl+X N` | New session |
| `Ctrl+C` | Exit OpenCode |

### OpenCode Pitfalls

1. **Interactive TUI requires `pty=true`** — `opencode run` does NOT need pty
2. **`/exit` is NOT a valid command** — it opens an agent selector; use Ctrl+C (`\x03`) instead
3. **PATH mismatch** — different shell environments may pick different binaries; use `which -a opencode` to check
4. **Enter may need pressing twice** in the TUI (once to finalize text, once to send)
5. **Don't share one workdir** across parallel OpenCode sessions
6. **Check logs before killing stuck sessions**: `process(action="log", session_id="<id>")`

---

## Universal Rules (All Agents)

1. **Prefer non-interactive / one-shot modes for automation** — cleaner, no dialog handling, structured output
2. **Set a workdir** — always scope the agent to the right project directory
3. **Limit agentic loops** — use `--max-turns` (Claude Code/Codex) or bounded prompts (OpenCode) to prevent runaway
4. **Monitor long-running tasks** — use `tmux capture-pane` (Claude Code) or `process(action="poll"|"log")` (all)
5. **Parallel is fine** — run multiple agents simultaneously in isolated git worktrees
6. **Clean up** — kill tmux sessions or process sessions when done; avoid resource leaks
7. **Report results** — after completion, summarize what changed, test results, and any remaining risks
8. **Don't interfere prematurely** — agents may do multi-step work; check progress before killing
