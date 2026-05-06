# anthrosidian — Claude Code / Codex Plugin

A Claude Code and Codex plugin that connects your Obsidian knowledge base to any project session. Write daily logs, compile wiki articles, search your vault, and audit your knowledge base — all without leaving your terminal.

## Features

- **Daily logging**: Capture notes, bug fixes, and insights directly into today's daily note
- **Wiki compilation**: Transform raw source materials into structured wiki articles
- **Knowledge Q&A**: Search and answer questions from your Obsidian wiki
- **Health checks**: Detect broken links, orphan articles, and missing index entries
- **URL ingestion**: Paste a URL to fetch and save content into `raw/` with the bundled Anthrosidian helper
- **Works everywhere**: SessionStart hook injects vault context into every session, from any project directory
- **Dual plugin support**: Claude Code metadata lives in `.claude-plugin/`; Codex metadata lives in `.codex-plugin/`

## Skills

| Skill | Trigger Phrases |
|-------|----------------|
| `daily-log` | "log this to my Obsidian knowledge base", "record this in my daily note", "write this to my Obsidian daily log" |
| `compile-wiki` | "compile the wiki", "process raw notes into the knowledge base", "ingest this URL into the knowledge base" |
| `qa-wiki` | "look this up in my Obsidian knowledge base", "search the wiki for X", "what does my knowledge base say about X" |
| `health-check` | "health check the knowledge base", "audit my Obsidian wiki", "find orphan articles in my Obsidian vault", "lint the wiki" |
| `setup` | `/anthrosidian:setup` or "configure the anthrosidian plugin" |

## Requirements

- [Claude Code](https://claude.ai/code) ≥ 2.0 or Codex with local plugin support
- Python 3 for the bundled URL ingestion helper

Anthrosidian does not require any separate Obsidian skill package.

## Installation

### Claude Code

### 1. Add the marketplace and install the plugin

In Claude Code, run:

```
/plugin marketplace add donald-ada/anthrosidian
```

### 2. Run setup

```
/anthrosidian:setup
```

Enter your vault path when prompted. Config is saved to `~/.claude/obsidian-vault.conf`.

> **Required**: The plugin will not activate without this config file. If the file is missing, each session will prompt you to run `/anthrosidian:setup`.

### Codex

The Codex plugin manifest is `.codex-plugin/plugin.json`. It reuses the same `skills/` and `hooks/` files as Claude Code, with platform-specific config paths handled inside the shared workflows.

Configure the vault from Codex with:

```
anthrosidian:setup
```

Codex config is saved to `~/.codex/obsidian-vault.conf`.

## Vault Structure

```
your-vault/
├── daily/          Daily notes (YYYY-MM-DD.md)
├── wiki/           Compiled knowledge articles
│   └── _index.md   Master index
├── raw/            Source materials
├── output/         Generated reports
├── assets/         Images and media
└── templates/
    └── daily-note.md
```

## Configuration

Claude Code config file: `~/.claude/obsidian-vault.conf`

Codex config file: `~/.codex/obsidian-vault.conf`

```bash
VAULT_PATH="/absolute/path/to/your/vault"
```

This file is **required**. Without it, the plugin will not know where your vault is and will prompt you to run setup.

To create or update in Claude Code: `/anthrosidian:setup [vault-path]`

To create or update in Codex: `anthrosidian:setup [vault-path]`

## License

MIT
