# obsidian-vault — Claude Code Plugin

An LLM-driven Obsidian knowledge base plugin for Claude Code. Operate your knowledge base from **any project directory** — not just when you're inside the vault.

## Features

- **Auto daily logging**: Say "记录一下" → structured entry written to today's note
- **URL ingestion**: Paste a URL → automatically routes to `obsidian:defuddle`
- **Wiki compilation**: Say "总结一下" → raw materials compiled into wiki articles
- **Knowledge Q&A**: Say "查一下wiki" → search and answer from your wiki
- **Health checks**: Say "lint知识库" → find broken links and orphan articles
- **Works everywhere**: SessionStart hook injects vault context into every session

## Requirements

- [Claude Code](https://claude.ai/code) ≥ 2.0
- [obsidian-skills](https://github.com/kepano/obsidian-skills) plugin (`obsidian:defuddle`, `obsidian:obsidian-cli`, etc.)

## Installation

### 1. Register the marketplace

Add to `~/.claude/settings.json`:

```json
"extraKnownMarketplaces": {
  "obsidian-vault-plugin": {
    "source": {
      "source": "github",
      "repo": "donald-ada/obsidian-vault"
    }
  }
}
```

### 2. Enable the plugin

```json
"enabledPlugins": {
  "obsidian-vault@obsidian-vault-plugin": true
}
```

### 3. Run setup

In Claude Code (from any directory):

```
/obsidian-vault:setup
```

Enter your vault path when prompted. Config is saved to `~/.claude/obsidian-vault.conf`.

## Trigger Words

| Say | Action |
|-----|--------|
| "记录一下" / "记一下" | Write to today's daily note |
| "总结一下" / "编译知识库" | Compile raw → wiki |
| "查一下wiki" / "知识库里有" | Q&A against wiki |
| Paste URL | Fetch with defuddle, save to raw/ |
| "lint知识库" / "health check" | Audit wiki for issues |
| "出报告" / "生成报告" | Generate output |

## Vault Structure Expected

```
your-vault/
├── daily/          Daily notes (YYYY-MM-DD.md)
├── wiki/           Compiled knowledge articles
│   └── _index.md   Master index
├── raw/            Source materials
├── output/         Generated reports & slides
├── assets/         Images and media
└── templates/      Note templates
    └── daily-note.md
```

## Configuration

Config file: `~/.claude/obsidian-vault.conf`

```bash
VAULT_PATH="/Users/yourname/Documents/Obsidian Vault"
```

To update: `/obsidian-vault:setup /new/vault/path`

## License

MIT
