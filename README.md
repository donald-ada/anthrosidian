# anthrosidian — Claude Code Plugin

A Claude Code plugin that connects your Obsidian knowledge base to any project session. Write daily logs, compile wiki articles, search your vault, and audit your knowledge base — all without leaving your terminal.

## Features

- **Daily logging**: Capture notes, bug fixes, and insights directly into today's daily note
- **Wiki compilation**: Transform raw source materials into structured wiki articles
- **Knowledge Q&A**: Search and answer questions from your Obsidian wiki
- **Health checks**: Detect broken links, orphan articles, and missing index entries
- **URL ingestion**: Paste a URL to fetch and save content via `obsidian:defuddle`
- **Works everywhere**: SessionStart hook injects vault context into every session, from any project directory

## Skills

| Skill | Trigger Phrases |
|-------|----------------|
| `daily-log` | "log this to my Obsidian knowledge base", "record this in my daily note", "write this to my Obsidian daily log" |
| `compile-wiki` | "compile the wiki", "process raw notes into the knowledge base", "ingest this URL into the knowledge base" |
| `qa-wiki` | "look this up in my Obsidian knowledge base", "search the wiki for X", "what does my knowledge base say about X" |
| `health-check` | "health check the knowledge base", "audit my Obsidian wiki", "find orphan articles in my Obsidian vault", "lint the wiki" |
| `setup` | `/anthrosidian:setup` or "configure the anthrosidian plugin" |

## Requirements

- [Claude Code](https://claude.ai/code) ≥ 2.0
- [obsidian-skills](https://github.com/kepano/obsidian-skills) plugin (`obsidian:defuddle`, `obsidian:obsidian-cli`, etc.)

## Installation

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

Config file: `~/.claude/obsidian-vault.conf`

```bash
VAULT_PATH="/absolute/path/to/your/vault"
```

This file is **required**. Without it, the plugin will not know where your vault is and will prompt you to run setup.

To create or update: `/anthrosidian:setup [vault-path]`

## License

MIT
