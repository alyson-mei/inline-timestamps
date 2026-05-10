# Inline Timestamps

A lightweight file watcher that handles inline time tracking in plain text and Markdown files.

Write a command, save the file — timestamps are inserted automatically. Sessions are tracked, 
deltas computed, and a statistics block appended to the bottom of the file on every save.

Designed for daily journaling in Obsidian, but works with any plain text workflow.

## Status

MVP. Experimental but usable. Core workflow is stable, edge cases and extended features are in progress. 

### Known limitations and issues

- Linux only (for now)
- Sometimes you need to reload the app, this mostly happens after certain system events
- Cursor behavior is unstable in most editors, which is an inherent limitation of external file watching via Python

## Installation & Running

Python 3.10+ and pip required.

1. Clone the repo:
```bash
git clone https://github.com/alyson-mei/inline-timestamps
cd inline-timestamps
```

2. Install:
```bash
make install
```
The install sets up an `its` alias for your shell. The alias name can be changed in `Makefile` via `ALIAS_NAME`. To proceed without restarting, run `source ~/.bashrc` (or `~/.zshrc`).

3. Configure `config.yaml`:
```yaml
watch:
  - path: "/your/notes/folder"
    recursive: true        # include subfolders
  - path: "/your/other/folder"
    recursive: false       # top-level only
suffixes:
  - ".md"                  # file types to watch
  - ".txt"
ts_format: "FULL"          # FULL: HH:MM:SS, SHORT: HH:MM
stats_separator: "\n---"   # separator before the stats block
```

4. Run:
```bash
its
```

## Workflow

### Single: Stamping a timestamp

Type `\ts` anywhere in a file and save — it gets replaced with the current time.

### Double: Tracking a session

`\td` opens a live session — the start time is stamped immediately, the end time is frozen until you close it:

```
\td  →  10:32:11 -> \ts \stopwatch
```

`\ts` is protected by `\stopwatch` and won't be replaced on save. To close, append `\` to the marker:

```
10:32:11 -> \ts \stopwatch\  →  10:32:11 -> 10:45:03
```

### Instant: Quick session

`\ti` is for sessions where you won't updated the file's content before closing — start time is stamped immediately, end time is left as `\ts` and gets replaced on the next save. In Obsidian, Space + Ctrl+S is enough to close it.

```
\ti  →  10:32:11 -> \ts  →  (next save)  →  10:32:11 -> 10:32:58
```

### Statistics

On every save, a statistics block is appended (or updated) at the bottom of the file:

```
---
# Statistics

- Total: 2 hrs 42 min
  - Coding: 45 min
  - Math: 1 hrs 30 min 
  - Other: 27 min
```

Sessions are grouped by category — the nearest label line above a timestamp pair with less indentation.