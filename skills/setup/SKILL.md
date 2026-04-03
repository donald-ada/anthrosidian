---
name: setup
description: This skill should be used when the user runs /obsidian-vault:setup, wants to configure the obsidian-vault plugin, or asks to set up their vault path. Use to initialize or update plugin configuration.
argument-hint: [vault-path]
allowed-tools: [Bash]
---

# Obsidian Vault Plugin Setup

Configure the obsidian-vault plugin by recording the vault path.

## Configuration File

The plugin reads vault settings from: `~/.claude/obsidian-vault.conf`

Format:
```
VAULT_PATH="/absolute/path/to/your/vault"
```

## Setup Process

1. **Determine vault path**
   - If `$ARGUMENTS` is non-empty, use it directly as the vault path
   - Otherwise ask the user: "请输入你的 Obsidian vault 完整路径（例如 /Users/yourname/Documents/My Vault）："

2. **Validate** the path exists:
   ```bash
   test -d "<vault-path>" && echo OK || echo NOT_FOUND
   ```
   - If NOT_FOUND, warn the user and ask to confirm or enter a different path

3. **Write config**:
   ```bash
   printf 'VAULT_PATH="%s"\n' "<vault-path>" > ~/.claude/obsidian-vault.conf
   ```

4. **Confirm success** with a summary:
   - Config saved to `~/.claude/obsidian-vault.conf`
   - Today's daily note path: `<vault-path>/daily/YYYY-MM-DD.md`
   - Active trigger words: "记录一下", URL paste, "查一下wiki", "编译知识库", "出报告"
   - To reconfigure: `/obsidian-vault:setup [new-path]`
