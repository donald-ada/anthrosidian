---
name: daily-log
description: This skill should be used when the user says "记录一下", "记一下", "写进日志", or asks to log a problem, solution, or technical note into their Obsidian daily note. Provides the structured entry workflow.
---

# Daily Development Log Workflow

Write structured problem/solution entries into today's Obsidian daily note.

## Determine Vault Path

Read from `~/.claude/obsidian-vault.conf` (key: `VAULT_PATH`).
Fallback: `~/Documents/Obsidian Vault`.

## Daily Note Path

`<VAULT>/daily/<YYYY-MM-DD>.md` (today's date)

## If Daily Note Doesn't Exist

Create it with this template (use `obsidian:obsidian-cli` or write directly):

```markdown
---
tags: [daily]
date: YYYY-MM-DD
---

# YYYY-MM-DD

## 任务
- [ ] 

## 问题 & 解决方案

## 技术笔记
```

## Entry Format

Append under `## 问题 & 解决方案`:

```markdown
### <问题标题>
**Context:** 在哪个项目/场景下
**Problem:** 出了什么问题 / 遇到了什么
**Solution:** 如何解决的
**Why it works:** 原理简述（1-2句）
```

Append reusable insights under `## 技术笔记`.

## After Writing

If the insight is reusable beyond today's specific code (patterns, API quirks, tool behaviors), offer to file it into `wiki/<topic>/` as a standalone article.
Link from daily note: `→ [[wiki/<topic>/<article-name>]]`
