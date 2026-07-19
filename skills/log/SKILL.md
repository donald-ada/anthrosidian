---
name: log
description: This skill should be used when the user asks to "log today's session", "write the episode log", "记录今天的工作", "写今日日志", or at the end of a work session worth remembering what happened and when.
argument-hint: [what happened]
---

# Log — episodic memory

Append what happened to today's episode file. Episodes answer "what/when did I do X";
notes answer "what do I know about X" — do not mix them.

## 0. Locate the KB

`source ~/.anthrosidian.conf` → `$KB_PATH`. If missing, stop: "Knowledge base not
configured — run `/anthrosidian:init`."

## 1. Append to today's episode

Path: `$KB_PATH/episodes/<YYYY>/<YYYY-MM-DD>.md` (create the year directory and file
if needed; file starts with `# YYYY-MM-DD`).

Append one `##` section per session:

```markdown
## <HH:MM> <one-line session summary>
- <outcome-level items: what was accomplished, one line each>
- Decision: <verbatim what was decided and why, if any>
- Problem: <symptom → cause → fix, with exact error text, if any>
- Notes: [<slug>](../../notes/<domain>/<slug>.md) <links to notes created this session>
```

Rules:
- **Append-only.** Never rewrite past days or earlier sections.
- **Outcome granularity**: one line ≈ one work unit you'd report at a standup, not
  individual file edits.
- Content in the user's language; identifiers, paths, and error text verbatim.

## 2. Promote durable knowledge

If the session produced insights with future grep value (a pitfall, a decision, a
reusable procedure), run the `/anthrosidian:remember` write path for them now and link
the resulting notes from the episode entry. The episode records *that* it happened;
the note records *what is known*.

## 3. Commit

```bash
cd "$KB_PATH" && git add -A && git commit -m "log: <YYYY-MM-DD> <one-line summary>"
```
