---
name: remember
description: This skill should be used when the user asks to "remember this", "save this to my knowledge base", "record this insight", "把这个记到知识库", "记住这个", "存进知识库", or when a session produced a durable insight, decision, pitfall, or fact worth keeping for future AI sessions.
argument-hint: [what to remember]
---

# Remember — the write path

Distill knowledge from this session into the KB. The KB's own `AGENTS.md` (§ Writing
protocol, § Note format) is the authority; this skill is the operating procedure.

## 0. Locate the KB

`source ~/.anthrosidian.conf` → `$KB_PATH`. If missing, stop: "Knowledge base not
configured — run `/anthrosidian:init`." Read `$KB_PATH/AGENTS.md` if this session has
not read it yet.

## 1. Extract candidates

From `$ARGUMENTS` and the conversation, list candidate knowledge units — each atomic
(one claim / procedure / pitfall / decision / entity / reference). For each, draft:
title, type, 5–15 bilingual keywords (exact error strings and identifiers verbatim),
and a one-sentence TL;DR.

**Selectivity gate first**: drop candidates that are transient task state, derivable
from a codebase/official docs, or one-off trivia with no future grep value. Storing
less retrieves better. If nothing survives, say so and stop.

## 2. Run the write gate (per candidate)

Grep `$KB_PATH/notes/` with the candidate's keywords (2–3 probe variants). Classify:

- **NOOP** — already recorded → report, skip.
- **UPDATE** — same subject, compatible refinement → edit existing note, bump `updated`.
- **SUPERSEDE** — contradicts an existing note → write new note; set the old note's
  `status: superseded` and `superseded_by:`; never delete.
- **ADD** — genuinely new → create `notes/<domain>/<slug>.md` per the AGENTS.md schema.

Pick the domain by grepping existing domains first; create a new domain directory only
when nothing fits.

## 3. After writing

1. Update `$KB_PATH/index.md` — one line per touched note, under its `## <domain>`.
   Remove the `(no notes yet)` placeholder on the first ever write.
2. **Neighbor revisit**: open the 2–3 most related notes; update their links/keywords
   if the new knowledge changes their context.
3. **Budget check**: if `index.md` exceeds ~180 lines, apply the overflow rule from
   AGENTS.md (spill the largest domain into `notes/<domain>/index.md`).
4. **Validator loop, then commit**:
   ```bash
   cd "$KB_PATH" && python3 scripts/kb_lint.py
   ```
   Fix every ERROR and re-run until clean (the pre-commit hook blocks invalid commits
   anyway). Then:
   ```bash
   git add -A && git commit -m "remember: <one-line summary>"
   ```

## Fast capture mode

If the user is mid-task and just wants it saved ("先记下来"), or the material needs
research before distilling: write a raw dump to
`$KB_PATH/inbox/YYYY-MM-DD-<slug>.md` (no schema required), commit, and note that
`/anthrosidian:consolidate` will distill it later. Never leave knowledge only in the
conversation — context dies, files survive.

## Report

End with: verdict per candidate (ADD/UPDATE/SUPERSEDE/NOOP + path), index status, and
the commit hash. Content language follows the user; paths/slugs/frontmatter in English.
