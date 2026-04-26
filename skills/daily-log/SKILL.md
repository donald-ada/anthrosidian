---
name: daily-log
description: This skill should be used when the user asks to "log this to my Obsidian knowledge base", "record this in my daily note", "save this problem and solution to my knowledge base", "write this to my Obsidian daily log", or wants to capture a technical note, bug fix, insight, or solved problem into their Obsidian vault's daily note.
---

# Daily Development Log Workflow

Write structured problem/solution entries into today's Obsidian daily note.

## Determine Vault Path

Read `VAULT_PATH` from `~/.claude/obsidian-vault.conf`.
If the file is missing or `VAULT_PATH` is not set, stop and tell the user:
"Vault path is not configured. Please run `/anthrosidian:setup` to set it up."

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

## Tasks
- [ ] 

## Problems & Solutions

## Technical Notes
```

## Entry Format

**Output language:** write the actual log content in the user's working language (the language they wrote/spoke in this conversation). The English placeholders and examples in this skill are documentation only — do not mimic their language. Field labels (`Context:` / `Symptom:` / `Cause:` / `Solution:` / `Why it works:`) stay in English to keep grep compatibility with historical notes; everything else (titles, narrative, identifiers used in prose) follows the user's language.

### Tasks section

Append completed work items under `## Tasks` as checked checkboxes:

```markdown
- [x] <one line — the high-level outcome, not the steps>
```

**Granularity rule (important):** one task ≈ one commit, or one work unit you'd report in a single sentence at a standup. **Do not list individual operations** — deleting a file, adding a dependency, removing an import, registering a config entry are *steps*, not *tasks*.

**Aggregation:** if multiple actions served the same goal (one refactor, one feature, one bugfix), collapse them into a single line that names the outcome.

**Anti-pattern (avoid — one refactor exploded into a step-by-step log):**
```
- [x] Delete <SomeClass>.java
- [x] Remove unused import in <Config>.java
- [x] Add <library> dependency to pom.xml
- [x] Register <datasource> in application.properties
- [x] Create <ModuleA>Mapper + XML
- [x] Create <ModuleB>Mapper + XML
- [x] Wire <ModuleA>Mapper into <ServiceA>
- [x] Wire <ModuleB>Mapper into <ServiceB>
```

**Preferred (same work, aggregated):**
```
- [x] Migrate <module-group> writes from <old store> to <new store> via <mechanism>
- [x] Fix <component> connection config (host/credentials)
```

**Source:** things the user *actually finished* in this conversation (features, bugfixes, refactors, docs, reviews). Skip abandoned attempts, pure discussion, or in-progress exploration.

### Problems & Solutions section

Append under `## Problems & Solutions`. **The key information must be scannable** — use bullets, one sentence per line. Do not write long paragraphs.

```markdown
### <Problem Title — one line stating what the problem is>
- **Context:** <project / module, one line>
- **Symptom:** <what was observed, one line — not a list of causes>
- **Cause:** <why it happened, one line>
- **Solution:** <how it was fixed, one line — name the API / command / file>
- **Why it works:** <why the fix is correct, one line — omit if Cause + Solution already make it obvious>
```

**Field split (key change):** the old format used a single `Problem` field, which kept growing into "what happened + why + impact 1) 2) 3)" walls of text. The new format forces a split into `Symptom` (what was seen) and `Cause` (why), one line each. This is the core fix for the wall-of-text problem.

**Rules:**
- Each bullet stays on one line (≤ 80 chars). If it overflows, split into multiple problems or move detail into `## Technical Notes`.
- **Symptom ≠ Cause ≠ Impact.** Symptom = what was seen / what triggered. Cause = why. Do not stuff a numbered impact list into Symptom.
- Include concrete identifiers (function names, field names, error codes, config keys) so future-you can grep for them.
- Distinct problems get distinct entries — never merge unrelated issues under one heading.

**Anti-pattern (avoid — symptom, cause, and impact all crammed into one paragraph):**
```
**Problem:** Old <Component> used <mechanism> to do <thing>, which caused: 1) <impact A>; 2) <impact B>; 3) <impact C>.
```

**Preferred (one sentence per field):**
```
- **Symptom:** <one observable fact>
- **Cause:** <one causal explanation>
- **Solution:** <one fix, naming the concrete change>
- **Why it works:** <one sentence on the underlying mechanism>
```

### Technical Notes section

Append reusable insights under `## Technical Notes` as a short bullet list. No long paragraphs.

## After Writing

If the insight is reusable beyond today's specific code (patterns, API quirks, tool behaviors), offer to file it into `wiki/<topic>/` as a standalone article.
Link from daily note: `→ [[wiki/<topic>/<article-name>]]`

## When Adding a Wiki Article

After creating `wiki/<topic>/<article-name>.md`, **always** update `wiki/_index.md`:

1. **Link format**: Use Obsidian wikilink, not Markdown link:
   ```
   | [[wiki/topic/article-name\|topic]] | N | Description |
   ```
2. **Sync frontmatter**: Update `updated:` in the YAML frontmatter to today's date.
3. **Sync article count**: Increment the Articles column and the Stats section.

These three steps are mandatory — skip any one and the index becomes stale.
