---
name: init
description: This skill should be used when the user runs /anthrosidian:init, asks to "create my knowledge base", "initialize the KB", "set up anthrosidian", "初始化知识库", "创建知识库", or wants to configure where their AI-first knowledge base lives.
argument-hint: [kb-path]
---

# Initialize the Knowledge Base

Create (or connect to) an AI-first knowledge base and record its location.

## 1. Resolve the KB path

- If `$ARGUMENTS` is non-empty, use it as the KB root path.
- Otherwise ask: "Where should the knowledge base live? (absolute path, e.g. ~/kb)"
- Expand `~` to `$HOME`. The directory may or may not exist yet.

## 2. Write config

Shared across Claude Code and Codex — one home-level file, no platform detection:

```bash
printf 'KB_PATH="%s"\n' "<absolute-kb-path>" > ~/.anthrosidian.conf
```

## 3. Scaffold the KB (skip pieces that already exist)

```bash
mkdir -p "$KB_PATH"/{core,notes,episodes,inbox,sources}
```

Then, only for files that do not already exist:
- Copy `templates/AGENTS.md` (adjacent to this SKILL.md) to `$KB_PATH/AGENTS.md` **verbatim** — it is the protocol every future session follows.
- Copy `templates/index.md` to `$KB_PATH/index.md`.
- Copy `templates/owner.md` to `$KB_PATH/core/owner.md`, then fill in what is already known from this conversation (working language, projects, environment). Ask nothing; leave unknown fields blank.

If `$KB_PATH/AGENTS.md` already exists, do NOT overwrite it — the KB's own protocol wins. Just report that an existing KB was connected.

## 4. Version control

```bash
cd "$KB_PATH" && git rev-parse --git-dir 2>/dev/null || git init
git add -A && git commit -m "init knowledge base" 2>/dev/null || true
```

Git is the KB's audit trail and recovery memory — every future write session commits.

## 5. Confirm

Report: config path, KB root, the five directories, and the available operations:
- `/anthrosidian:remember` — distill knowledge into the KB (write gate)
- `/anthrosidian:recall` — answer from the KB (grep-first, cite or abstain)
- `/anthrosidian:log` — append today's episode
- `/anthrosidian:consolidate` — dedup, distill inbox, staleness sweep

Suggest reading `$KB_PATH/AGENTS.md` once — it is short and defines everything.
