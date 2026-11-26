---
name: debugging
description: "Universal debugging: 4-phase root-cause methodology (any language), Python pdb/debugpy, Node.js --inspect/CDP."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [debugging, troubleshooting, root-cause, python, pdb, debugpy, nodejs, node-inspect, cdp, breakpoints, dap, post-mortem, investigation]
    related_skills: [test-driven-development, plan, systematic-debugging]
    triggers:
      - debug
      - test failing
      - bug
      - breakpoint
      - Python debugging
      - Node.js debugging
      - root cause
      - pdb
      - debugpy
      - node inspect
      - step through
      - stack trace
---

# Debugging

Universal debugging skill covering the methodology for ANY language/stack, plus language-specific tooling for Python and Node.js.

**Start here:** [Universal Debugging Methodology](#universal-debugging-methodology) → then jump to the language-specific section as needed.

---

## Universal Debugging Methodology

Random fixes waste time and create new bugs. Quick patches mask underlying issues.

**Core principle:** ALWAYS find root cause before attempting fixes. Symptom fixes are failure.

### The Iron Law

```
NO FIXES WITHOUT ROOT CAUSE INVESTIGATION FIRST
```

If you haven't completed Phase 1, you cannot propose fixes.

### When to Use

Use for ANY technical issue:
- Test failures
- Bugs in production
- Unexpected behavior
- Performance problems
- Build failures
- Integration issues

**Use this ESPECIALLY when:**
- Under time pressure (emergencies make guessing tempting)
- "Just one quick fix" seems obvious
- You've already tried multiple fixes
- Previous fix didn't work
- You don't fully understand the issue

**Don't skip when:**
- Issue seems simple (simple bugs have root causes too)
- You're in a hurry (rushing guarantees rework)
- Someone wants it fixed NOW (systematic is faster than thrashing)

### The Four Phases

You MUST complete each phase before proceeding to the next.

---

#### Phase 1: Root Cause Investigation

**BEFORE attempting ANY fix:**

##### 1. Read Error Messages Carefully

- Don't skip past errors or warnings
- They often contain the exact solution
- Read stack traces completely
- Note line numbers, file paths, error codes

**Action:** Use `read_file` on the relevant source files. Use `search_files` to find the error string in the codebase.

##### 2. Reproduce Consistently

- Can you trigger it reliably?
- What are the exact steps?
- Does it happen every time?
- If not reproducible → gather more data, don't guess

**Action:** Use the `terminal` tool to run the failing test or trigger the bug:

```bash
# Run specific failing test
pytest tests/test_module.py::test_name -v

# Run with verbose output
pytest tests/test_module.py -v --tb=long
```

##### 3. Check Recent Changes

- What changed that could cause this?
- Git diff, recent commits
- New dependencies, config changes

**Action:**

```bash
# Recent commits
git log --oneline -10

# Uncommitted changes
git diff

# Changes in specific file
git log -p --follow src/problematic_file.py | head -100
```

##### 4. Gather Evidence in Multi-Component Systems

**WHEN system has multiple components (API → service → database, CI → build → deploy):**

**BEFORE proposing fixes, add diagnostic instrumentation:**

For EACH component boundary:
- Log what data enters the component
- Log what data exits the component
- Verify environment/config propagation
- Check state at each layer

Run once to gather evidence showing WHERE it breaks.
THEN analyze evidence to identify the failing component.
THEN investigate that specific component.

##### 5. Trace Data Flow

**WHEN error is deep in the call stack:**

- Where does the bad value originate?
- What called this function with the bad value?
- Keep tracing upstream until you find the source
- Fix at the source, not at the symptom

**Action:** Use `search_files` to trace references:

```python
# Find where the function is called
search_files("function_name(", path="src/", file_glob="*.py")

# Find where the variable is set
search_files("variable_name\\s*=", path="src/", file_glob="*.py")
```

##### Phase 1 Completion Checklist

- [ ] Error messages fully read and understood
- [ ] Issue reproduced consistently
- [ ] Recent changes identified and reviewed
- [ ] Evidence gathered (logs, state, data flow)
- [ ] Problem isolated to specific component/code
- [ ] Root cause hypothesis formed

**STOP:** Do not proceed to Phase 2 until you understand WHY it's happening.

---

#### Phase 2: Pattern Analysis

**Find the pattern before fixing:**

##### 1. Find Working Examples

- Locate similar working code in the same codebase
- What works that's similar to what's broken?

**Action:** Use `search_files` to find comparable patterns:

```python
search_files("similar_pattern", path="src/", file_glob="*.py")
```

##### 2. Compare Against References

- If implementing a pattern, read the reference implementation COMPLETELY
- Don't skim — read every line
- Understand the pattern fully before applying

##### 3. Identify Differences

- What's different between working and broken?
- List every difference, however small
- Don't assume "that can't matter"

##### 4. Understand Dependencies

- What other components does this need?
- What settings, config, environment?
- What assumptions does it make?

---

#### Phase 3: Hypothesis and Testing

**Scientific method:**

##### 1. Form a Single Hypothesis

- State clearly: "I think X is the root cause because Y"
- Write it down
- Be specific, not vague

##### 2. Test Minimally

- Make the SMALLEST possible change to test the hypothesis
- One variable at a time
- Don't fix multiple things at once

##### 3. Verify Before Continuing

- Did it work? → Phase 4
- Didn't work? → Form NEW hypothesis
- DON'T add more fixes on top

##### 4. When You Don't Know

- Say "I don't understand X"
- Don't pretend to know
- Ask the user for help
- Research more

---

#### Phase 4: Implementation

**Fix the root cause, not the symptom:**

##### 1. Create Failing Test Case

- Simplest possible reproduction
- Automated test if possible
- MUST have before fixing
- Use the `test-driven-development` skill

##### 2. Implement Single Fix

- Address the root cause identified
- ONE change at a time
- No "while I'm here" improvements
- No bundled refactoring

##### 3. Verify Fix

```bash
# Run the specific regression test
pytest tests/test_module.py::test_regression -v

# Run full suite — no regressions
pytest tests/ -q
```

##### 4. If Fix Doesn't Work — The Rule of Three

- **STOP.**
- Count: How many fixes have you tried?
- If < 3: Return to Phase 1, re-analyze with new information
- **If ≥ 3: STOP and question the architecture (step 5 below)**
- DON'T attempt Fix #4 without architectural discussion

##### 5. If 3+ Fixes Failed: Question Architecture

**Pattern indicating an architectural problem:**
- Each fix reveals new shared state/coupling in a different place
- Fixes require "massive refactoring" to implement
- Each fix creates new symptoms elsewhere

**STOP and question fundamentals:**
- Is this pattern fundamentally sound?
- Are we "sticking with it through sheer inertia"?
- Should we refactor the architecture vs. continue fixing symptoms?

**Discuss with the user before attempting more fixes.**

This is NOT a failed hypothesis — this is a wrong architecture.

---

### Red Flags — STOP and Follow Process

If you catch yourself thinking:
- "Quick fix for now, investigate later"
- "Just try changing X and see if it works"
- "Add multiple changes, run tests"
- "Skip the test, I'll manually verify"
- "It's probably X, let me fix that"
- "I don't fully understand but this might work"
- "Pattern says X but I'll adapt it differently"
- "Here are the main problems: [lists fixes without investigation]"
- Proposing solutions before tracing data flow
- **"One more fix attempt" (when already tried 2+)**
- **Each fix reveals a new problem in a different place**

**ALL of these mean: STOP. Return to Phase 1.**

**If 3+ fixes failed:** Question the architecture (Phase 4 step 5).

### Common Rationalizations

| Excuse | Reality |
|--------|---------|
| "Issue is simple, don't need process" | Simple issues have root causes too. Process is fast for simple bugs. |
| "Emergency, no time for process" | Systematic debugging is FASTER than guess-and-check thrashing. |
| "Just try this first, then investigate" | First fix sets the pattern. Do it right from the start. |
| "I'll write test after confirming fix works" | Untested fixes don't stick. Test first proves it. |
| "Multiple fixes at once saves time" | Can't isolate what worked. Causes new bugs. |
| "Reference too long, I'll adapt the pattern" | Partial understanding guarantees bugs. Read it completely. |
| "I see the problem, let me fix it" | Seeing symptoms ≠ understanding root cause. |
| "One more fix attempt" (after 2+ failures) | 3+ failures = architectural problem. Question the pattern, don't fix again. |

### Quick Reference

| Phase | Key Activities | Success Criteria |
|-------|---------------|------------------|
| **1. Root Cause** | Read errors, reproduce, check changes, gather evidence, trace data flow | Understand WHAT and WHY |
| **2. Pattern** | Find working examples, compare, identify differences | Know what's different |
| **3. Hypothesis** | Form theory, test minimally, one variable at a time | Confirmed or new hypothesis |
| **4. Implementation** | Create regression test, fix root cause, verify | Bug resolved, all tests pass |

### Hermes Agent Integration

Use these Hermes tools during Phase 1:

- **`search_files`** — Find error strings, trace function calls, locate patterns
- **`read_file`** — Read source code with line numbers for precise analysis
- **`terminal`** — Run tests, check git history, reproduce bugs
- **`web_search`/`web_extract`** — Research error messages, library docs

For complex multi-component debugging, dispatch investigation subagents:

```python
delegate_task(
    goal="Investigate why [specific test/behavior] fails",
    context="""
    Follow the debugging skill methodology:
    1. Read the error message carefully
    2. Reproduce the issue
    3. Trace the data flow to find root cause
    4. Report findings — do NOT fix yet

    Error: [paste full error]
    File: [path to failing code]
    Test command: [exact command]
    """,
    toolsets=['terminal', 'file']
)
```

### Real-World Impact

From debugging sessions:
- Systematic approach: 15-30 minutes to fix
- Random fixes approach: 2-3 hours of thrashing
- First-time fix rate: 95% vs 40%
- New bugs introduced: Near zero vs common

**No shortcuts. No guessing. Systematic always wins.**

---

## Python Debugging

Three tools, picked by situation:

| Tool | When |
|---|---|
| **`breakpoint()` + pdb** | Local, interactive, simplest. Add `breakpoint()` in the source, run normally, get a REPL at that line. |
| **`python -m pdb`** | Launch an existing script under pdb with no source edits. Useful for quick poking. |
| **`debugpy`** | Remote / headless / "attach to already-running process." Talks DAP, scriptable from terminal, works for long-lived processes (gateway, daemon, PTY children). |

**Start with `breakpoint()`.** It's the cheapest thing that works.

### When to Use Python Debugging

- A test fails and the traceback doesn't reveal why a value is wrong
- You need to step through a function and watch a collection mutate
- A long-running process (hermes gateway, tui_gateway) misbehaves and you can't restart it
- Post-mortem: an exception fired in prod-ish code and you want to inspect locals at the crash site
- A subprocess / child (Python `_SlashWorker`, PTY bridge worker) is the actual bug site

**Don't use for:** things `print()` / `logging.debug` solve in under a minute, or things `pytest -vv --tb=long --showlocals` already reveals.

### pdb Quick Reference

Inside any pdb prompt (`(Pdb)`):

| Command | Action |
|---|---|
| `h` / `h cmd` | help |
| `n` | next line (step over) |
| `s` | step into |
| `r` | return from current function |
| `c` | continue |
| `unt N` | continue until line N |
| `j N` | jump to line N (same function only) |
| `l` / `ll` | list source around current line / full function |
| `w` | where (stack trace) |
| `u` / `d` | move up / down in the stack |
| `a` | print args of the current function |
| `p expr` / `pp expr` | print / pretty-print expression |
| `display expr` | auto-print expr on every stop |
| `b file:line` | set breakpoint |
| `b func` | break on function entry |
| `b file:line, cond` | conditional breakpoint |
| `cl N` | clear breakpoint N |
| `tbreak file:line` | one-shot breakpoint |
| `!stmt` | execute arbitrary Python (assignments included) |
| `interact` | drop into full Python REPL in current scope (Ctrl+D to exit) |
| `q` | quit |

The `interact` command is the most powerful — you can import anything, inspect complex objects, even call methods that mutate state. Locals are read-only by default; use `!x = 42` from the `(Pdb)` prompt to mutate.

### Python Recipe 1: Local breakpoint

Easiest. Edit the file:

```python
def compute(x, y):
    result = some_helper(x)
    breakpoint()           # <-- drops into pdb here
    return result + y
```

Run the code normally. You land at the `breakpoint()` line with full access to locals.

**Don't forget to remove `breakpoint()` before committing.** Use `git diff` or a pre-commit grep:
```bash
rg -n 'breakpoint\(\)' --type py
```

### Python Recipe 2: Launch a script under pdb (no source edits)

```bash
python -m pdb path/to/script.py arg1 arg2
# Lands at first line of script
(Pdb) b path/to/script.py:42
(Pdb) c
```

### Python Recipe 3: Debug a pytest test

```bash
# Drop to pdb on failure (or on any raised exception):
scripts/run_tests.sh tests/path/to/test_file.py::test_name --pdb

# Drop to pdb at the START of the test:
scripts/run_tests.sh tests/path/to/test_file.py::test_name --trace

# Show locals in tracebacks without pdb:
scripts/run_tests.sh tests/path/to/test_file.py --showlocals --tb=long
```

Note: `scripts/run_tests.sh` uses xdist (`-n 4`) by default, and pdb does NOT work under xdist. Add `-p no:xdist` or run a single test with `-n 0`:

```bash
scripts/run_tests.sh tests/foo_test.py::test_bar --pdb -p no:xdist
# or
source .venv/bin/activate
python -m pytest tests/foo_test.py::test_bar --pdb
```

This bypasses the hermetic-env guarantees — fine for debugging, but re-run under the wrapper to confirm before pushing.

### Python Recipe 4: Post-mortem on any exception

```python
import pdb, sys
try:
    run_the_thing()
except Exception:
    pdb.post_mortem(sys.exc_info()[2])
```

Or wrap a whole script:

```bash
python -m pdb -c continue script.py
# When it crashes, pdb catches it and you're in the frame of the exception
```

Or set a global hook in a repl/jupyter:

```python
import sys
def excepthook(etype, value, tb):
    import pdb; pdb.post_mortem(tb)
sys.excepthook = excepthook
```

### Python Recipe 5: Remote debug with debugpy (attach to running process)

For long-lived processes: Hermes gateway, tui_gateway, a daemon, a process that's already misbehaving and can't be restarted clean.

#### Setup

```bash
source /home/bb/hermes-agent/.venv/bin/activate
pip install debugpy
```

#### Pattern A: Source-edit — process waits for debugger at launch

Add near the top of the entry point:

```python
import debugpy
debugpy.listen(("127.0.0.1", 5678))
print("debugpy listening on 5678, waiting for client...", flush=True)
debugpy.wait_for_client()
debugpy.breakpoint()       # optional: pause immediately once attached
```

Start the process; it blocks on `wait_for_client()`.

#### Pattern B: No source edit — launch with `-m debugpy`

```bash
python -m debugpy --listen 127.0.0.1:5678 --wait-for-client your_script.py arg1
```

Equivalent for module entry:

```bash
python -m debugpy --listen 127.0.0.1:5678 --wait-for-client -m your.module
```

#### Pattern C: Attach to an already-running process

```bash
python -m debugpy --listen 127.0.0.1:5678 --pid <pid>
# debugpy injects itself into the process. Then attach a client as below.
```

Some kernels/security configs block the ptrace-based injection (`/proc/sys/kernel/yama/ptrace_scope`). Fix with:
```bash
echo 0 | sudo tee /proc/sys/kernel/yama/ptrace_scope
```

#### Connecting a client from the terminal

**Option 1: VS Code / Cursor / Zed `launch.json`:**

```json
{
  "name": "Attach to Hermes",
  "type": "debugpy",
  "request": "attach",
  "connect": { "host": "127.0.0.1", "port": 5678 },
  "justMyCode": false,
  "pathMappings": [
    { "localRoot": "${workspaceFolder}", "remoteRoot": "/home/bb/hermes-agent" }
  ]
}
```

**Option 2: `remote-pdb` (usually the best terminal choice):**

```bash
pip install remote-pdb
```

In your code:
```python
from remote_pdb import set_trace
set_trace(host="127.0.0.1", port=4444)   # blocks until connection
```

Then from the terminal:
```bash
nc 127.0.0.1 4444
# You get a (Pdb) prompt exactly as if debugging locally.
```

`remote-pdb` is the cleanest agent-friendly choice when `debugpy`'s DAP protocol is overkill. Use `debugpy` only when you actually need IDE integration.

### Debugging Hermes-specific Python Processes

**Tests:** Always add `-p no:xdist` or run single tests without xdist.

**`run_agent.py` / CLI — one-shot:** Add `breakpoint()` near the suspect line, then run `hermes` normally.

**`tui_gateway` subprocess (spawned by `hermes --tui`):**

```python
# Option A: tui_gateway/server.py near the top of serve()
import debugpy
debugpy.listen(("127.0.0.1", 5678))
debugpy.wait_for_client()
```

```python
# Option B: Use remote-pdb at a specific handler
from remote_pdb import set_trace
set_trace(host="127.0.0.1", port=4444)
```
Trigger the matching slash command from the TUI, then `nc 127.0.0.1 4444` in another terminal.

**`_SlashWorker` subprocess:** Same pattern — `remote-pdb` with `set_trace()` inside the worker's `exec` path.

**Gateway (`gateway/run.py`):** Long-lived. Use `remote-pdb` at a handler, or `debugpy` with `--wait-for-client` if restarting the gateway anyway.

### Python Common Pitfalls

1. **pdb under pytest-xdist silently does nothing.** You won't see the prompt, the test just hangs. Always use `-p no:xdist` or `-n 0`.

2. **`breakpoint()` in CI / non-TTY contexts hangs the process.** Safe locally; never commit it. Add a pre-commit grep as a safety net.

3. **`PYTHONBREAKPOINT=0`** disables all `breakpoint()` calls. Check the env if your breakpoint isn't hitting:
   ```bash
   echo $PYTHONBREAKPOINT
   ```

4. **`debugpy.listen` blocks only if you also call `wait_for_client()`.** Without it, execution continues and your first breakpoint may fire before the client is attached.

5. **Attach to PID fails on hardened kernels.** `ptrace_scope=1` (Ubuntu default) allows only same-user ptrace of child processes. Workaround: `echo 0 > /proc/sys/kernel/yama/ptrace_scope` (needs root) or launch under `debugpy` from the start.

6. **Threads.** `pdb` only debugs the current thread. For multithreaded code, use `debugpy` (thread-aware DAP) or set `threading.settrace()` per thread.

7. **asyncio.** `pdb` works in coroutines but `await` inside pdb requires Python 3.13+ or `await` from `interact` mode on older versions.

8. **`scripts/run_tests.sh` strips credentials and sets `HOME=<tmpdir>`.** If your bug depends on user config or real API keys, it won't reproduce under the wrapper. Debug with raw `pytest` first to repro.

9. **Forking / multiprocessing.** pdb does not follow forks. Each child needs its own `breakpoint()` or `set_trace()`. For Hermes subagents, debug one process at a time.

### Python Verification Checklist

- [ ] After `pip install debugpy`, confirm: `python -c "import debugpy; print(debugpy.__version__)"`
- [ ] For remote debug, confirm the port is actually listening: `ss -tlnp | grep 5678`
- [ ] First breakpoint actually hits (if it doesn't, you likely have `PYTHONBREAKPOINT=0`, you're under xdist, or execution finished before attach)
- [ ] `where` / `w` shows the expected call stack
- [ ] Post-debug cleanup: no stray `breakpoint()` / `set_trace()` in committed code
  ```bash
  rg -n 'breakpoint\(\)|set_trace\(|debugpy\.listen' --type py
  ```

### Python One-Shot Recipes

**"Why is this dict missing a key?"**
```python
# add above the KeyError site
breakpoint()
# then in pdb:
(Pdb) pp d
(Pdb) pp list(d.keys())
(Pdb) w                # how did we get here
```

**"This test passes in isolation but fails in the suite."**
```bash
scripts/run_tests.sh tests/the_test.py --pdb -p no:xdist
# But if it only fails WITH other tests:
source .venv/bin/activate
python -m pytest tests/ -x --pdb -p no:xdist
# Now it pdb-traps at the exact failing test after state accumulated.
```

**"My async handler deadlocks."**
```python
# Add at handler entry
import remote_pdb; remote_pdb.set_trace(host="127.0.0.1", port=4444)
```
Trigger the handler. `nc 127.0.0.1 4444`, then `w` to see the suspended frame, `!import asyncio; asyncio.all_tasks()` to see what else is pending.

**"Post-mortem on a crash in an Ink child process / subprocess."**
```bash
PYTHONFAULTHANDLER=1 python -m pdb -c continue path/to/entrypoint.py
# On crash, pdb lands at the frame of the exception with full locals
```

---

## Node.js Debugging

When `console.log` isn't enough, drive Node's built-in V8 inspector programmatically from the terminal. You get real breakpoints, step in/over/out, call-stack walking, local/closure scope dumps, and arbitrary expression evaluation in the paused frame.

Two tools, pick one:

- **`node inspect`** — built-in, zero install, CLI REPL. Best for quick poking.
- **`ndb` / CDP via `chrome-remote-interface`** — scriptable from Node/Python; best when you want to automate many breakpoints, collect state across runs, or debug non-interactively from an agent loop.

**Prefer `node inspect` first.** It's always available and the REPL is fast.

### When to Use Node.js Debugging

- A Node test fails and you need to see intermediate state
- ui-tui crashes or behaves wrong and you want to inspect React/Ink state pre-render
- tui_gateway child processes (`_SlashWorker`, PTY bridge workers) misbehave
- You need to inspect a value in a closure that `console.log` can't reach without patching
- Perf: attach to a running process to capture a CPU profile or heap snapshot

**Don't use for:** things `console.log` solves in under a minute.

### Quick Reference: `node inspect` REPL

Launch paused on first line:

```bash
node inspect path/to/script.js
# or with tsx
node --inspect-brk $(which tsx) path/to/script.ts
```

The `debug>` prompt accepts:

| Command | Action |
|---|---|
| `c` or `cont` | continue |
| `n` or `next` | step over |
| `s` or `step` | step into |
| `o` or `out` | step out |
| `pause` | pause running code |
| `sb('file.js', 42)` | set breakpoint at file.js line 42 |
| `sb(42)` | set breakpoint at line 42 of current file |
| `sb('functionName')` | break when function is called |
| `cb('file.js', 42)` | clear breakpoint |
| `breakpoints` | list all breakpoints |
| `bt` | backtrace (call stack) |
| `list(5)` | show 5 lines of source around current position |
| `watch('expr')` | evaluate expr on every pause |
| `watchers` | show watched expressions |
| `repl` | drop into REPL in current scope (Ctrl+C to exit REPL) |
| `exec expr` | evaluate expression once |
| `restart` | restart script |
| `kill` | kill the script |
| `.exit` | quit debugger |

**In the `repl` sub-mode:** type any JS expression, including access to locals/closure variables. `Ctrl+C` exits back to `debug>`.

### Attaching to a Running Node Process

When the process is already running (e.g. a long-lived dev server or the TUI gateway):

```bash
# 1. Send SIGUSR1 to enable the inspector on an existing process
kill -SIGUSR1 <pid>
# Node prints: Debugger listening on ws://127.0.0.1:9229/<uuid>

# 2. Attach the debugger CLI
node inspect -p <pid>
# or by URL
node inspect ws://127.0.0.1:9229/<uuid>
```

To start a process with the inspector from the beginning:

```bash
node --inspect script.js           # listen on 127.0.0.1:9229, keep running
node --inspect-brk script.js       # listen AND pause on first line
node --inspect=0.0.0.0:9230 script.js   # custom host:port
```

For TypeScript via tsx:

```bash
node --inspect-brk --import tsx script.ts
# or older tsx
node --inspect-brk -r tsx/cjs script.ts
```

### Programmatic CDP (scripting from terminal)

When you want to automate — set many breakpoints, capture scope state, script a repro — use `chrome-remote-interface`:

```bash
npm i -g chrome-remote-interface        # or project-local
# Start your target:
node --inspect-brk=9229 target.js &
```

Driver script (save as `/tmp/cdp-debug.js`):

```javascript
const CDP = require('chrome-remote-interface');

(async () => {
  const client = await CDP({ port: 9229 });
  const { Debugger, Runtime } = client;

  Debugger.paused(async ({ callFrames, reason }) => {
    const top = callFrames[0];
    console.log(`PAUSED: ${reason} @ ${top.url}:${top.location.lineNumber + 1}`);

    // Walk scopes for locals
    for (const scope of top.scopeChain) {
      if (scope.type === 'local' || scope.type === 'closure') {
        const { result } = await Runtime.getProperties({
          objectId: scope.object.objectId,
          ownProperties: true,
        });
        for (const p of result) {
          console.log(`  ${scope.type}.${p.name} =`, p.value?.value ?? p.value?.description);
        }
      }
    }

    // Evaluate an expression in the paused frame
    const { result } = await Debugger.evaluateOnCallFrame({
      callFrameId: top.callFrameId,
      expression: 'typeof state !== "undefined" ? JSON.stringify(state) : "n/a"',
    });
    console.log('state =', result.value ?? result.description);

    await Debugger.resume();
  });

  await Runtime.enable();
  await Debugger.enable();

  // Set a breakpoint by URL regex + line
  await Debugger.setBreakpointByUrl({
    urlRegex: '.*app\\.tsx$',
    lineNumber: 119,       // 0-indexed
    columnNumber: 0,
  });

  await Runtime.runIfWaitingForDebugger();
})();
```

Run it:

```bash
node /tmp/cdp-debug.js
```

Hermes-specific note: `chrome-remote-interface` is NOT in `ui-tui/package.json`. Install to a throwaway location:

```bash
mkdir -p /tmp/cdp-tools && cd /tmp/cdp-tools && npm i chrome-remote-interface
NODE_PATH=/tmp/cdp-tools/node_modules node /tmp/cdp-debug.js
```

### Debugging Hermes ui-tui

The TUI is built with Ink + tsx. Two common scenarios:

#### Debugging a single Ink component under dev

```bash
cd /home/bb/hermes-agent/ui-tui
npm run build    # produce dist/ once so transpile isn't needed on first load
node --inspect-brk dist/entry.js
# In another terminal:
node inspect -p <node pid>
```

Then inside `debug>`:

```
sb('dist/app.js', 220)     # or wherever the suspect render is
cont
```

When it pauses, `repl` → inspect `props`, state refs, `useInput` handler values, etc.

#### Debugging a running `hermes --tui`

```bash
# 1. Launch TUI
hermes --tui &
TUI_PID=$(pgrep -f 'ui-tui/dist/entry' | head -1)

# 2. Enable inspector on that Node PID
kill -SIGUSR1 "$TUI_PID"

# 3. Find the WS URL
curl -s http://127.0.0.1:9229/json/list | jq -r '.[0].webSocketDebuggerUrl'

# 4. Attach
node inspect ws://127.0.0.1:9229/<uuid>
```

#### Debugging `_SlashWorker` / PTY child processes

Those are Python, not Node — use the Python Debugging section above for them. Only Node portions (Ink UI, tui_gateway client, tsx-run tests under `ui-tui/`) use this section.

### Running Vitest Tests Under the Debugger

```bash
cd /home/bb/hermes-agent/ui-tui
# Run a single test file paused on entry
node --inspect-brk ./node_modules/vitest/vitest.mjs run --no-file-parallelism src/app/foo.test.tsx
```

In another terminal: `node inspect -p <pid>`, then `sb('src/app/foo.tsx', 42)`, `cont`.

Use `--no-file-parallelism` (vitest) or `--runInBand` (jest) so only one worker exists — debugging a pool is painful.

### Heap Snapshots & CPU Profiles (Non-interactive)

```javascript
// CPU profile for 5 seconds
await client.Profiler.enable();
await client.Profiler.start();
await new Promise(r => setTimeout(r, 5000));
const { profile } = await client.Profiler.stop();
require('fs').writeFileSync('/tmp/cpu.cpuprofile', JSON.stringify(profile));
// Open /tmp/cpu.cpuprofile in Chrome DevTools → Performance tab
```

```javascript
// Heap snapshot
await client.HeapProfiler.enable();
const chunks = [];
client.HeapProfiler.addHeapSnapshotChunk(({ chunk }) => chunks.push(chunk));
await client.HeapProfiler.takeHeapSnapshot({ reportProgress: false });
require('fs').writeFileSync('/tmp/heap.heapsnapshot', chunks.join(''));
```

### Node.js Common Pitfalls

1. **Wrong line numbers in TS source.** Breakpoints hit the emitted JS, not the `.ts`. Either (a) break in the built `dist/*.js`, or (b) enable sourcemaps (`node --enable-source-maps`) and use `sb('src/app.tsx', N)` — but only with CDP clients that follow sourcemaps. `node inspect` CLI does not.

2. **`--inspect` vs `--inspect-brk`.** `--inspect` starts the inspector but doesn't pause; your script races past your first breakpoint if you attach too late. Use `--inspect-brk` when you need to set breakpoints before any code runs.

3. **Port collisions.** Default is `9229`. If multiple Node processes are inspecting, pass `--inspect=0` (random port) and read the actual URL from `/json/list`:
   ```bash
   curl -s http://127.0.0.1:9229/json/list   # lists all inspectable targets on the host
   ```

4. **Child processes.** `--inspect` on a parent does NOT inspect its children. Use `NODE_OPTIONS='--inspect-brk' node parent.js` to propagate to every child; be aware they all need unique ports (Node auto-increments when `NODE_OPTIONS='--inspect'` is inherited).

5. **Background kills.** If you `Ctrl+C` out of `node inspect` while the target is paused, the target stays paused. Either `cont` first, or `kill` the target explicitly.

6. **Running `node inspect` through an agent terminal.** It's a PTY-friendly REPL. In Hermes, launch it with `terminal(pty=true)` or `background=true` + `process(action='submit', data='...')`. Non-PTY foreground mode will work for one-shot commands but not for interactive stepping.

7. **Security.** `--inspect=0.0.0.0:9229` exposes arbitrary code execution. Always bind to `127.0.0.1` (the default) unless you have an isolated network.

### Node.js Verification Checklist

After setting up a debug session, verify:

- [ ] `curl -s http://127.0.0.1:9229/json/list` returns exactly the target you expect
- [ ] First breakpoint actually hits (if it doesn't, you likely missed `--inspect-brk` or attached after execution completed)
- [ ] Source listing at pause shows the right file (mismatch = sourcemap issue, see pitfall 1)
- [ ] `exec process.pid` in `repl` returns the PID you meant to attach to

### Node.js One-Shot Recipes

**"Why is this variable undefined at line X?"**
```bash
node --inspect-brk script.js &
node inspect -p $!
# debug>
sb('script.js', X)
cont
# paused. Now:
repl
> myVariable
> Object.keys(this)
```

**"What's the call path into this function?"**
```
debug> sb('suspectFn')
debug> cont
# paused on entry
debug> bt
```

**"This async chain hangs — where?"**
```
# Start with --inspect (no -brk), let it run to the hang, then:
debug> pause
debug> bt
# Now you see the stuck frame
```
