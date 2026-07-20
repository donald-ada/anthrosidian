---
name: recall
description: This skill should be used when the user asks "what do I know about X", "check my knowledge base", "look this up in the KB", "知识库里有没有", "查一下知识库", "我之前是怎么解决的", or when a task touches a problem the knowledge base may already answer.
argument-hint: [question]
---

# Recall — the read path

Answer from the KB with citations, or state honestly that the KB does not know.
`$KB_PATH/AGENTS.md` § Reading protocol is the authority.

## 0. Locate the KB

`source ~/.anthrosidian.conf` → `$KB_PATH`. If missing, stop: "Knowledge base not
configured — run `/anthrosidian:init`."

## 1. Grep first

Probe `$KB_PATH/notes/` with 2–3 query variants:
- exact identifiers verbatim (error strings, function/parameter names, versions)
- synonyms in the user's language AND English (frontmatter `keywords` are built for this)

```bash
grep -ril -e "<probe1>" -e "<probe2>" "$KB_PATH/notes/"
```

If the question is temporal ("when did I…", "what did I do last week"), grep
`$KB_PATH/episodes/` instead — filenames are `YYYY-MM-DD.md`, so date-range globbing works.

## 2. Index second

If grep is weak or the question is broad, read `$KB_PATH/index.md` (and a domain's
`notes/<domain>/index.md` if present) to orient, then read the matching notes.

## 3. Read few, precise notes

- Open at most ~5 notes. Near-miss notes are context poison — prefer fewer, tighter hits.
- Trust `status: active` only. If a hit is `superseded`, follow `superseded_by` forward
  and answer from the current note (mention the history only if relevant).
- A note's TL;DR (first body line) is enough to judge relevance — skim before committing.

## 4. Answer

- Answer in the user's language, citing each supporting note by path.
- Preserve verbatim anything the notes quote verbatim (commands, configs, numbers).
- Surface the note's `confidence` and `updated` date when the user is about to act on it
  and the note is old or unverified.

## 5. Abstain honestly

If grep and index turn up nothing relevant: say "这个知识库里没有记录" / "not recorded
in the knowledge base" — and offer to research and `/anthrosidian:remember` the answer.
Never blend general knowledge into a KB answer without labeling which is which.
