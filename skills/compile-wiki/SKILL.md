---
name: compile-wiki
description: This skill should be used when the user asks to "compile the wiki", "process raw notes into the knowledge base", "turn raw sources into wiki articles in my Obsidian vault", "ingest this URL into the knowledge base", or wants to transform unstructured material in raw/ into structured wiki articles in the Obsidian knowledge base.
---

# Wiki Compilation Workflow

Compile raw source materials in `raw/` into structured wiki articles in `wiki/`.

## Determine Vault Path

Read `VAULT_PATH` from the active agent config:
- Codex: `~/.codex/obsidian-vault.conf`
- Claude Code: `~/.claude/obsidian-vault.conf`

If only one config file exists, use that one. If missing, stop and tell the user:
"Vault path is not configured. Please run `anthrosidian:setup` in Codex or `/anthrosidian:setup` in Claude Code."

## Step 1: Ingest (if URL provided)

Use the bundled helper; do not rely on external Obsidian skill packages:

```bash
python3 <plugin-root>/skills/compile-wiki/scripts/ingest_url.py --vault "$VAULT_PATH" "<url>"
```

If the active environment cannot resolve `<plugin-root>`, locate this `SKILL.md` file and use the adjacent `scripts/ingest_url.py` path. The helper saves the page as `raw/<title>.md` with source metadata.

Network and IO errors must be reported with the URL/path and the original error. Do not silently skip a failed fetch, and do not fabricate a raw note if the page could not be read.

## Step 2: Read and Extract

Read the raw source thoroughly. Extract:
- Key concepts and definitions
- Facts, data points, and examples
- Relationships between ideas
- Practical patterns and gotchas

## Step 3: Create or Update Wiki Articles

Write Markdown files directly in the vault using the rules below.
For article format and naming conventions, see: `references/wiki-rules.md`

- One concept per article (prefer many small articles over few large ones)
- Save to `wiki/<topic>/<article-name>.md`
- Use `[[wikilinks]]` for cross-references between articles
- Use `![[embeds]]` for images in `assets/`
- Add YAML frontmatter: `tags`, `aliases`, `source`, `created`, `updated`
  - `aliases:` lists alternate names the article can be reached by — synonyms, abbreviations, error messages, or older naming the user might remember. Obsidian resolves `[[alias]]` wikilinks to the canonical article when listed here. Aim for 3-8 aliases.

## Step 4: Update Topic Index

Each topic directory must have `wiki/<topic>/_index.md`. Create it if it doesn't exist.

Use a **three-column table** (see `references/wiki-rules.md` for exact format):

| 文章 | 摘要 | 关键词 |
|------|------|--------|
| [[wiki/topic/article\|Title]] | 2-3 sentence summary of the problem, solution, and key gotchas | keyword1, param-name, error-term, synonym |

**The Keywords column must be comprehensive** — include parameter names, function/class names, error messages, synonyms, and alternate phrasings. This is the primary way agents navigate to the right article without opening every file.

## Step 5: Update Master Index

`wiki/_index.md` — links to each topic's `_index.md` (NOT to individual articles).

**Required on every update:**
- Link target must be `[[wiki/<topic>/_index\|<Topic>]]`, never a direct article link
- Description should name specific sub-topics covered, not just the domain name
- Sync the `updated:` field in the YAML frontmatter to today's date
- Keep article count in sync
