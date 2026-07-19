# anthrosidian — an AI-first knowledge base, operated by agents

A Claude Code / Codex plugin that turns a plain **markdown + git** directory into a
personal knowledge base whose **sole consumer is an AI agent**. Humans may browse it;
every design decision optimizes for an agent with grep/glob/read/write tools and a
finite context window.

v2 is a ground-up redesign. The old Obsidian-centric wiki (daily-log / compile-wiki /
qa-wiki / health-check) is gone.

## Design principles (first principles, research-backed)

The consumer is an LLM agent. Its real constraints dictate everything:

| Constraint | Design response |
|---|---|
| Finite, expensive context window | Progressive disclosure: tiny session hook → 200-line index → atomic notes ≤150 lines. Nothing is preloaded; everything is fetched just-in-time. |
| Tools are grep/glob/read, not a GUI | Grep-first retrieval; descriptive kebab-case filenames; bilingual `keywords` frontmatter (synonyms + verbatim error strings) as a hand-rolled semantic index. No Obsidian-specific features. |
| No memory across sessions | The KB is self-describing: its `AGENTS.md` protocol lives *inside* the KB, so any agent — with or without this plugin — can operate it correctly. |
| Reads notes with zero conversation context | Every note is self-contained: TL;DR first line, "Applies when" scope, provenance, confidence, dates. |
| Good at write-time synthesis, bad at read-time digestion | Distill at write time. Verbatim quotes for decisions/numbers/errors (paraphrase silently destroys qualifiers). Raw material goes to `sources/`. |
| Knowledge goes stale and contradicts itself | Deterministic supersession: `status: active/superseded/deprecated` + `superseded_by` links. Never delete — git is the history. Freshness is a grep filter, not an LLM judgment call. |
| Memory bloat degrades retrieval | A selectivity gate at write time (store less, retrieve better), hard index budget enforced on every write, and a periodic consolidation ("sleep") phase. |

Memory types are separated because their lifecycles differ:
**semantic** (`notes/` — atomic facts, procedures, pitfalls, decisions, entities,
references), **episodic** (`episodes/` — append-only daily logs), **procedural**
(`core/` — few, curated, standing preferences).

## Operations

| Skill | What it does |
|---|---|
| `/anthrosidian:init` | Scaffold the KB (protocol, index, directories), `git init`, save `~/.anthrosidian.conf` |
| `/anthrosidian:remember` | Write path: selectivity gate → grep for duplicates/contradictions → ADD / UPDATE / SUPERSEDE / NOOP → index + neighbor updates → commit. Fast mode drops raw captures into `inbox/`. |
| `/anthrosidian:recall` | Read path: grep-first (bilingual probes), index second, read ≤5 active notes, answer with citations — or abstain honestly ("not recorded"). |
| `/anthrosidian:log` | Append today's episode (append-only, outcome-granularity), promote durable insights to notes. |
| `/anthrosidian:consolidate` | Sleep phase: distill inbox, dedup/merge, arbitrate contradictions, mine episodes for recurring themes, staleness sweep, rebuild index, commit. |

A `SessionStart` hook injects a ~10-line pointer (KB path, note count, when to recall/
remember) into every session — the KB itself is never preloaded.

## KB layout

```
<kb-root>/
├── AGENTS.md        The protocol — single source of truth, readable by any agent
├── index.md         One line per note, hard budget 200 lines (overflow → domain indexes)
├── core/            Standing context: owner profile, preferences (≤100 lines each)
├── notes/<domain>/  Atomic notes with typed frontmatter (the semantic memory)
├── episodes/<YYYY>/ Append-only daily logs (the episodic memory)
├── inbox/           Fast captures awaiting consolidation
└── sources/         Verbatim external material
```

Note frontmatter: `type`, `status`, `created`/`updated`, `confidence`
(verified/reported/inferred), `source`, `keywords`, `superseded_by`.

## Installation

```
/plugin marketplace add donald-ada/anthrosidian
/anthrosidian:init ~/kb
```

Config is one shared file for both Claude Code and Codex: `~/.anthrosidian.conf`
(`KB_PATH="/absolute/path"`). The Codex manifest is `.codex-plugin/plugin.json`,
reusing the same skills and hooks.

## Requirements

- Claude Code ≥ 2.0 or Codex with local plugin support
- git (the KB's audit trail), python3 (hook JSON escaping)

## License

MIT
