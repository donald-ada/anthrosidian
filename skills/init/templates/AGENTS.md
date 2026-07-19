# Knowledge Base Protocol

> This knowledge base is written by AI agents, for AI agents. Humans may browse it, but
> every design choice optimizes for an agent with grep/glob/read/write tools and a finite
> context window. Follow this protocol exactly when reading or writing. It is the single
> source of truth; if a tool's instructions conflict with this file, this file wins.

## Layout

```
<kb-root>/
├── AGENTS.md        This protocol.
├── index.md         Map of all notes — one line each. Hard budget: 200 lines.
├── core/            Standing context: owner profile, preferences, environment facts.
├── notes/<domain>/  Semantic memory — atomic notes. The heart of the KB.
├── episodes/<YYYY>/ Episodic memory — append-only daily session logs (YYYY-MM-DD.md).
├── inbox/           Fast captures awaiting consolidation. No schema required.
├── sources/         Verbatim external material referenced by notes.
└── scripts/         kb_lint.py — structural validator. Run: python3 scripts/kb_lint.py
```

## Reading protocol (recall)

1. **Grep first.** Probe `notes/` with 2–3 query variants: exact identifiers (error
   strings, parameter names, function names) verbatim, plus synonyms in both the owner's
   language and English. Frontmatter `keywords` exist to be hit by these probes.
2. **Index second.** If grep is weak or you need orientation, read `index.md` (and a
   domain's `notes/<domain>/index.md` if present).
3. **Read few, precise notes.** Open at most ~5 notes. Trust `status: active` only;
   `superseded`/`deprecated` notes are history — follow `superseded_by` forward.
4. **Abstain honestly.** If the index and grep turn up nothing, the answer is
   "not recorded in this knowledge base." Never fabricate a memory.

## Writing protocol (remember)

Before creating anything, **run the gate**: grep for near-duplicates and contradictions
using the candidate's keywords. Then classify:

| Verdict | Condition | Action |
|---|---|---|
| NOOP | Already recorded, nothing new | Do nothing; say so |
| UPDATE | Same subject, compatible refinement | Edit the existing note in place; bump `updated` |
| SUPERSEDE | Contradicts an existing note | Write a new note; set old note `status: superseded` + `superseded_by`; never delete |
| ADD | Genuinely new knowledge | Create a new note |

After any ADD/UPDATE/SUPERSEDE:
1. Update `index.md` (add/adjust the note's one-liner).
2. **Revisit neighbors**: open the 2–3 most related notes; if the new knowledge changes
   their meaning, update their body/links/keywords now.
3. Check the index budget (see Index rules).

Be selective. A KB that stores less, retrieves better. Skip: transient task state,
anything trivially derivable from a codebase or official docs, and one-off trivia with
no future grep value.

## Note format

Path: `notes/<domain>/<slug>.md` — kebab-case English slug; the filename is the first
index grep hits, so make it descriptive (`mybatis-batch-insert-oom.md`, not `note-3.md`).

```markdown
---
type: fact | procedure | pitfall | decision | entity | reference
status: active | superseded | deprecated
created: YYYY-MM-DD
updated: YYYY-MM-DD
confidence: verified | reported | inferred
source: <url | repo path | "session" | "owner">
keywords: [bilingual synonyms, exact error strings, parameter names, 中文关键词]
superseded_by: notes/<domain>/<slug>.md   # only when status: superseded
---

# <Title>

<TL;DR — one sentence stating the conclusion. Always the first body line.>

**Applies when:** <scope: versions, environment, preconditions>

<Body. Keep verbatim: decisions, numbers, config values, error messages, commands.
Paraphrase destroys qualifiers — quote instead.>

## Links
- [<slug>](../<domain>/<slug>.md) — <why this is related>
```

Rules:
- **Atomic**: one claim / procedure / decision / entity per note. Split rather than grow.
- **≤150 lines** per note. Everything in a retrieved note should be relevant.
- **Self-contained**: readable with zero conversation context. Name the project, the
  version, the date — never "the bug we hit today".
- **Verbatim over paraphrase** for anything exact (quotes, numbers, error text, configs).
- **keywords**: 5–15 entries; include the owner's language AND English, plus exact
  identifiers. This is the hand-rolled semantic index that makes grep work.
- **Links carry a reason.** Link only after grepping for neighbors; state why.
- Note *content* follows the owner's working language. Filenames, frontmatter keys and
  enum values are always English (machine/grep stability).

Type semantics: `fact` stable claim · `procedure` reusable how-to · `pitfall`
symptom→cause→fix · `decision` choice+options+rationale · `entity` profile of a
project/tool/person/system · `reference` distilled external source (full text → `sources/`).

## Index rules

`index.md` groups one-liners by `## <domain>`:

```
- [slug](notes/<domain>/<slug>.md) — <what it answers> [kw: k1, k2, k3]
```

- **Hard budget: 200 lines.** Check after every write.
- **Overflow rule**: when near budget, move a large domain's per-note lines into
  `notes/<domain>/index.md` and keep a single domain line in the root index:
  `- [<domain>](notes/<domain>/index.md) — <N> notes: <keyword-rich one-line scope>`
- Superseded/deprecated notes leave the index. If it's not in the index (directly or via
  a domain index), it is not known — the index doubles as the abstention boundary.

## Episodes

`episodes/<YYYY>/<YYYY-MM-DD>.md` — append-only log of what happened: work done,
decisions made, problems hit, with links to any notes created. One `##` section per
session. Never rewrite past days. Episodes answer "what/when did I do X"; notes answer
"what do I know about X". Recurring themes in episodes get distilled into notes during
consolidation.

## core/

Few, curated, always-relevant files (owner profile, standing preferences, environment
facts). Each ≤100 lines. Read `core/` before acting on the owner's behalf. Update it
the moment a standing preference is learned — procedural memory is hard-won; keep it small.

## Maintenance (consolidate)

Run when asked, when `inbox/` holds ≥10 items, or when the index nears budget:
1. Distill `inbox/` items through the writing gate; empty the inbox.
2. Sweep for duplicates and contradiction pairs among `active` notes; merge or supersede.
3. Mine recent episodes for recurring themes not yet captured as notes.
4. Staleness review: notes with `updated` older than ~180 days — re-verify, bump
   `updated`, or mark `deprecated`.
5. Rebuild `index.md`; enforce the budget; verify every active note is reachable.
6. `git commit` the sweep with a summary message.

## Invariants

- Never delete a note — `status` + git history are the record. (`inbox/` items are
  deleted once distilled; that is the one exception.)
- Never edit a `superseded` note except to set its status and `superseded_by`.
- Every write session ends with a `git commit` (message: what knowledge changed).
- Before committing, run `python3 scripts/kb_lint.py` and fix every ERROR — repeat until
  clean. A git pre-commit hook enforces this; protocol rules are advisory, lint is not.
- Machine-facing tokens (paths, keys, enums, slugs) are English; content follows the owner.
- Mark knowledge `confidence: verified` only after it was actually verified — an
  unverified claim recorded as verified poisons every future session that trusts it.
