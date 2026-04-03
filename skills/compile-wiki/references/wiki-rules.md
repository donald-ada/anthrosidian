# Wiki Article Rules

## Article Format

```markdown
---
tags: [topic-tag]
source: "[[raw/source-file]]"
created: YYYY-MM-DD
updated: YYYY-MM-DD
---

# Article Title

Content with [[wikilinks]] to related concepts.

## See Also
- [[related-article-1]]
- [[related-article-2]]
```

## Conventions

- **Language**: Chinese for all wiki content unless source is English-only
- **File naming**: Chinese titles are fine; use hyphens for multi-word English names
- **Granularity**: One concept per article — prefer many small articles over few large ones
- **Source linking**: Always link back to raw source via `source` frontmatter
- **Callouts**: Use Obsidian callouts (`> [!note]`, `> [!warning]`) for emphasis
- **References**: When moving content between directories, update all references

## Index Format

Topic index (`wiki/<topic>/_index.md`):
```markdown
# <Topic Name>

- [[article-name]] — one-sentence description
- [[another-article]] — one-sentence description
```

Master index (`wiki/_index.md`):
```markdown
# Knowledge Base Index

| Topic | Articles | Summary |
|-------|---------|--------|
| [[topic/_index\|Topic Name]] | N | One-line description |
```
