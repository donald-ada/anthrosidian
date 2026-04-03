---
name: health-check
description: This skill should be used when the user says "lint知识库", "health check", "检查wiki", or asks to audit the Obsidian knowledge base for broken links, orphan articles, stale content, or structural issues.
---

# Wiki Health Check Workflow

Audit the Obsidian knowledge base for structural issues.

## Checks to Perform

1. **Broken wikilinks** — Find `[[links]]` pointing to non-existent articles
   - Read all wiki articles, extract all `[[wikilinks]]`, verify each target exists

2. **Orphan articles** — Articles not linked from any index or other article
   - Check that every article appears in its topic's `_index.md`
   - Check that every topic appears in `wiki/_index.md`

3. **Stale articles** — Source material in `raw/` updated after wiki article was last modified
   - Compare `updated` frontmatter date against raw source file modification time

4. **Index completeness** — Every article in `wiki/<topic>/` appears in `wiki/<topic>/_index.md`

5. **Data inconsistencies** — Conflicting facts across articles on the same topic

## Output Format

Report findings as:
- **Critical** (broken links, missing indexes) — must fix
- **Warnings** (orphans, stale) — should fix  
- **Suggestions** (missing article candidates, topic gaps, research opportunities)

Offer to fix issues automatically when possible.
