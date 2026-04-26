---
name: review-work
description: This skill should be used when the user asks to "review my work", "summarize what I did this week/month", "generate a weekly/monthly report", "what have I been working on", or in Chinese asks to "回顾我的工作", "本周/本月做了什么", "做个周报/月报", or wants to aggregate completed tasks and noteworthy problems from daily notes across a time range or filtered by project/topic.
---

# Work Review Workflow

Aggregate `Tasks` and noteworthy `Problems` from daily notes across a time range and produce a structured retrospective.

This is the **review** counterpart to `qa-wiki`. They serve different needs:
- `qa-wiki` answers "how did I solve X?" by searching the curated wiki.
- `review` answers "what have I been working on?" by aggregating raw daily notes.
Do not mix them — keep wiki retrieval and daily aggregation as separate pipelines.

**Output language:** the report content (titles, narrative, project names, identifiers) follows the user's working language in this conversation. Field labels and section headings stay English for consistency with `daily-log`. The English placeholders in this skill are documentation only.

## Determine Vault Path

Read `VAULT_PATH` from `~/.claude/obsidian-vault.conf`.
If missing, stop and tell the user: "Vault path is not configured. Please run `/anthrosidian:setup`."

## Resolve Time Range

Parse the range from the user's argument. Default = **current ISO week (Mon–Sun, including today)** if no argument given.

| Argument                     | Range                                            |
| ---------------------------- | ------------------------------------------------ |
| (empty) / `week`             | Current ISO week, Mon–Sun including today        |
| `last-week`                  | Previous ISO week                                |
| `month`                      | Current calendar month                           |
| `last-month`                 | Previous calendar month                          |
| `YYYY-MM`                    | All days in that calendar month                  |
| `YYYY-MM-DD..YYYY-MM-DD`     | Explicit start..end (inclusive)                  |
| `last N days`                | The last N calendar days including today         |
| `project=<name>` (modifier)  | Filter to entries mentioning this project name   |

Combine modifier with range: `month project=baolong-mobileSource`. If only `project=` is given without a time range, default scope to **last 60 days**.

Resolve "today" from the system clock. Convert all relative phrases ("this week", "本月") to absolute `YYYY-MM-DD..YYYY-MM-DD` before reading files — store the resolved range in the report header.

## Collect Daily Notes

List `<VAULT>/daily/*.md`. Match filenames against the resolved range (filename is the date). Read all matching files in one pass — do not stop early.

Note any **gaps** (days within the range with no log file) and surface them in the Stats section.

## Extract Signal

From each daily note, pull:
- **Tasks**: every `- [x] ...` line under `## Tasks`.
- **Problem headings**: every `### <title>` under `## Problems & Solutions` (title only — do not copy multi-line bodies).
- **Wiki links**: every `[[wiki/...]]` reference (signals which problems escalated to permanent knowledge that day).
- **Project hint**: scan task lines and `Context:` fields for project names (e.g. `baolong-mobileSource`, `anthrosidian`, repository names, module prefixes). The first matching token in a task line wins as that task's project tag.

If `project=<name>` modifier was set, drop tasks and problems whose detected project does not match.

## Group, Summarize, De-duplicate

**Primary grouping = project**, secondary = **topic** (refactor / bugfix / feature / docs / infra / research / other).

Topic heuristic — match the task wording:
- "重构 / refactor / 改造" → **refactor**
- "修复 / fix / bug / 修正" → **bugfix**
- "新增 / add / implement / 实现 / 创建" → **feature**
- "文档 / docs / README / SKILL.md / 注释" → **docs**
- "部署 / 配置 / pom / 依赖 / CI / 版本 / bump / release" → **infra**
- "调研 / research / 探索 / 评估" → **research**
- everything else → **other**

Within each `(project, topic)` bucket: collapse near-duplicates (same outcome on consecutive days = one line with date range), preserve concrete identifiers, order by date.

## Output Format

Write the report to `<VAULT>/output/review-<range-slug>.md` and also show it inline.

Range slug examples:
- ISO week → `review-2026-W17.md`
- Month → `review-2026-04.md`
- Explicit dates → `review-2026-04-01_2026-04-26.md`
- With project filter → suffix `-<project>` (e.g. `review-2026-04-baolong-mobileSource.md`)

Template:

```markdown
---
tags: [review]
range: <human-readable range, e.g. "2026 ISO week 17 (04-20 – 04-26)">
generated: <YYYY-MM-DD>
---

# Work Review · <human-readable range>

## Snapshot
- Daily notes: N
- Tasks completed: N
- Problems documented: N
- Wiki articles touched: N

## By Project

### <project name> (N tasks)

#### Refactor
- `<YYYY-MM-DD>` — <task line, identifier-preserving>
- ...

#### Bugfix
- ...

(omit empty topic buckets within a project)

### <next project> (N tasks)
...

## Problems Worth Revisiting
- [[YYYY-MM-DD#<problem title>]] — <one-line "why it's worth re-reading">
- ...

## Loose Threads
- <item> — <source: [[YYYY-MM-DD]]>
- ...

## Stats
- Top topics: <topic-1>, <topic-2>, <topic-3>
- Most active project: <name>
- Days without a log in range: <list of YYYY-MM-DD>
```

## Filtering Rules

**Problems Worth Revisiting** — include a problem heading only if **at least one** holds:
- It links to a wiki article (`[[wiki/...]]` in the body).
- The same problem heading (or near-duplicate) appears in 2+ daily notes within the range.
- Its title contains markers of non-routine difficulty: "scope creep", "regression", "race", "edge case", "incident", "踩坑", "线上", "事故".

Skip routine problems. The point of this section is to surface entries the user should re-read, not to dump every P&S.

**Loose Threads** — include only:
- Unchecked `- [ ]` checkboxes in the range.
- Lines containing `TODO`, `FIXME`, `待办`, `待跟进`, `pending`.

If a section has zero qualifying items, omit the section entirely.

## Hard Rules

- **No fluff.** No "great progress this week" or motivational summaries. The report is a scannable index.
- **Preserve identifiers verbatim** (function names, file names, error codes, version numbers) — they are the searchable hooks for future grep.
- **Cite, do not quote.** Link back via `[[YYYY-MM-DD#problem title]]` rather than copying body paragraphs.
- **Read every matched daily note**, even if early ones look thin. Skipping any breaks the aggregation contract.
- **Do not invent.** If a project, topic, or stat cannot be derived from the daily notes, leave it empty rather than fabricate.

## Diff Mode (optional)

If the user asks for a comparison ("vs last week" / "对比上周" / "compared to last month"), resolve both ranges, run extraction twice, and produce a third section:

```markdown
## Diff vs <previous range>
- New projects: <list>
- Dropped projects: <list>
- Recurring problems: <problem titles appearing in both periods — these are candidates for deeper investigation or wiki article upgrade>
```
