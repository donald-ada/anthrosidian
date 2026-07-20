---
name: consolidate
description: This skill should be used when the user asks to "consolidate the knowledge base", "clean up the KB", "process the inbox", "整理知识库", "巩固记忆", "清理收件箱", or periodically when inbox items pile up or the index nears its budget.
---

# Consolidate — the sleep phase

Offline maintenance of the KB: distill, dedup, resolve contradictions, sweep staleness,
rebuild the index. Never run this inline with task work. `$KB_PATH/AGENTS.md`
§ Maintenance is the authority.

## 0. Locate the KB

`source ~/.anthrosidian.conf` → `$KB_PATH`. If missing, stop: "Knowledge base not
configured — run `/anthrosidian:init`."

## 1. Distill the inbox

For each file in `$KB_PATH/inbox/`: run the full write gate from
`/anthrosidian:remember` (NOOP / UPDATE / SUPERSEDE / ADD), then delete the inbox file
— the one place deletion is allowed, because the knowledge now lives in `notes/`.
Oversized raw material goes to `sources/` with a `reference` note pointing at it.

## 2. Dedup and contradiction sweep

Across `status: active` notes (grep frontmatter, compare titles/keywords per domain):
- Near-duplicates → merge into the stronger note; supersede the weaker one.
- Contradiction pairs (same subject, incompatible claims) → decide which is current
  (prefer newer + higher confidence + verified over inferred); supersede the loser.
  If genuinely undecidable, keep both active but cross-link them with a warning line —
  and flag it in the report for the user to arbitrate.

## 3. Mine episodes

Scan recent `episodes/` (since the last consolidation commit): recurring problems or
themes appearing across ≥3 days that have no note yet are promotion candidates — run
them through the write gate.

## 4. Staleness review

Notes with `updated` older than ~180 days: re-verify if cheaply possible (grep the
relevant repo, check the tool's current docs); otherwise downgrade `confidence` or set
`status: deprecated`. Never silently trust old knowledge — and never delete it.

## 5. Rebuild the index and validate

Regenerate `index.md` from the actual `notes/` tree: every active note reachable
(directly or via a domain index), superseded/deprecated notes removed, budget ≤200
lines enforced via the overflow rule. Then run the validator loop:

```bash
cd "$KB_PATH" && python3 scripts/kb_lint.py
```

Fix every ERROR and re-run until clean; address WARNs where cheap (core files over
budget, oversized notes). Lint checks structure only — the semantic judgments in
steps 1–4 remain yours.

## 6. Commit and report

```bash
cd "$KB_PATH" && git add -A && git commit -m "consolidate: <inbox N, merged N, superseded N, deprecated N>"
```

Report in the user's language: counts per step, contradictions needing arbitration,
and anything deprecated. No fluff — the report is a changelog, not an essay.
