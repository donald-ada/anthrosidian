---
name: compile-wiki
description: This skill should be used when the user says "总结一下", "编译知识库", "把raw里的内容编进wiki", or asks to turn raw source materials into structured wiki articles. Provides the full wiki compilation workflow.
---

# Wiki Compilation Workflow

Compile raw source materials in `raw/` into structured wiki articles in `wiki/`.

## Step 1: Ingest (if URL provided)

Use `obsidian:defuddle` to fetch the URL, save as `raw/<title>.md`.

## Step 2: Read and Extract

Read the raw source thoroughly. Extract:
- Key concepts and definitions
- Facts, data points, and examples
- Relationships between ideas
- Practical patterns and gotchas

## Step 3: Create or Update Wiki Articles

Use `obsidian:obsidian-markdown` for correct formatting.
For article format and naming conventions, see: `references/wiki-rules.md`

- One concept per article (prefer many small articles over few large ones)
- Save to `wiki/<topic>/<article-name>.md`
- Use `[[wikilinks]]` for cross-references between articles
- Use `![[embeds]]` for images in `assets/`
- Add YAML frontmatter: `tags`, `source`, `created`, `updated`

## Step 4: Update Topic Index

Each topic directory has `wiki/<topic>/_index.md`:
- Add the new article with title + one-sentence description
- Keep concise: title + one sentence per entry

## Step 5: Update Master Index

`wiki/_index.md` — lists all topic areas with article counts and one-line summaries.
Regenerate whenever articles are added, removed, or significantly changed.
