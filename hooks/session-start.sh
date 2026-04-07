#!/usr/bin/env bash
# SessionStart hook: load vault config and inject context into every session
# Output: JSON with additionalContext

set -euo pipefail

CONFIG="$HOME/.claude/obsidian-vault.conf"

# Load user config
if [[ -f "$CONFIG" ]]; then
  # shellcheck source=/dev/null
  source "$CONFIG"
fi

VAULT="${VAULT_PATH:-$HOME/Documents/Obsidian Vault}"
TODAY=$(date +%Y-%m-%d)

# Persist vault path for other hooks in this session
if [[ -n "${CLAUDE_ENV_FILE:-}" ]]; then
  printf 'VAULT_PATH="%s"\n' "$VAULT" >> "$CLAUDE_ENV_FILE"
fi

# Build context
CONTEXT="<obsidian-vault>\n\
The user has an Obsidian knowledge base. Use the skills below when the user explicitly asks to interact with it.\n\n\
Vault: ${VAULT}\n\
Today's daily note: ${VAULT}/daily/${TODAY}.md\n\n\
Available skills:\n\
  obsidian-vault:daily-log    — log / record something to today's daily note\n\
  obsidian-vault:compile-wiki — compile raw notes into wiki articles\n\
  obsidian-vault:qa-wiki      — search or look something up in the wiki\n\
  obsidian-vault:health-check — audit and fix wiki quality issues\n\
  obsidian:defuddle           — fetch a URL and save content to raw/\n\n\
Vault structure:\n\
  daily/     daily notes (YYYY-MM-DD.md)\n\
  wiki/      LLM-compiled knowledge articles (owned by Claude)\n\
  raw/       source materials (added by user, read by Claude)\n\
  output/    reports / slides / visualizations\n\
  assets/    media files\n\
  templates/ note templates\n\n\
When the user asks to record, log, or save something to their knowledge base:\n\
  - If it is clear they mean today's daily note, use obsidian-vault:daily-log.\n\
  - If the destination or format is ambiguous, ask one focused clarifying question\n\
    before proceeding (e.g. \"Should I add this to today's daily note, or create a wiki article?\").\n\n\
Full wiki compile rules: ${VAULT}/CLAUDE.md\n\
If vault path is not configured, run: /obsidian-vault:setup\n\
</obsidian-vault>"

# Escape for JSON string
escaped=$(printf '%s' "$CONTEXT" | python3 -c "
import sys, json
print(json.dumps(sys.stdin.read())[1:-1])
" 2>/dev/null)

printf '{"additionalContext": "%s"}\n' "$escaped"
exit 0
