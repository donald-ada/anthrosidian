---
name: qa-wiki
description: This skill should be used when the user asks "查一下wiki", "知识库里有没有", "帮我查", or any question that should be answered from the Obsidian knowledge base. Provides the search and Q&A workflow.
---

# Wiki Q&A Workflow

Answer questions by searching and reading the Obsidian wiki.

## Process

1. **Orient**: Read `wiki/_index.md` to understand available topics

2. **Navigate**: Read relevant topic indexes (`wiki/<topic>/_index.md`) to find related articles

3. **Read**: Read the articles needed to answer the question

4. **Answer**: Provide the answer, citing sources with `[[wikilinks]]`

5. **Save** (if requested): Write the answer to `output/` or file it into the wiki

## If No Relevant Articles Found

- Search `raw/` for uncompiled source materials that might contain the answer
- Offer to compile raw material into a new wiki article
- Suggest using web search + `obsidian:defuddle` to ingest new sources on the topic
