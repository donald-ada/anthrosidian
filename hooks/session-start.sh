#!/usr/bin/env bash
# SessionStart hook: load vault config and inject context into every session
# Output: JSON with additionalContext

set -euo pipefail

if [[ -n "${CODEX_PLUGIN_ROOT:-}" || -n "${CODEX_ENV_FILE:-}" ]]; then
  PLATFORM="Codex"
  CONFIG="$HOME/.codex/obsidian-vault.conf"
  SETUP_COMMAND="anthrosidian:setup"
else
  PLATFORM="Claude Code"
  CONFIG="$HOME/.claude/obsidian-vault.conf"
  SETUP_COMMAND="/anthrosidian:setup"
fi

# Load user config
if [[ -f "$CONFIG" ]]; then
  # shellcheck source=/dev/null
  source "$CONFIG"
fi

TODAY=$(date +%Y-%m-%d)

# Require explicit config — no default path fallback
if [[ -z "${VAULT_PATH:-}" ]]; then
  CONTEXT="<anthrosidian>\n\
anthrosidian plugin is installed but vault path is not configured.\n\
Run ${SETUP_COMMAND} to set your vault path and create ${CONFIG}.\n\
</anthrosidian>"
else
  VAULT="$VAULT_PATH"

  # Persist vault path for other hooks in this session
  if [[ -n "${CODEX_ENV_FILE:-}" ]]; then
    printf 'VAULT_PATH="%s"\n' "$VAULT" >> "$CODEX_ENV_FILE"
  elif [[ -n "${CLAUDE_ENV_FILE:-}" ]]; then
    printf 'VAULT_PATH="%s"\n' "$VAULT" >> "$CLAUDE_ENV_FILE"
  fi

  CONTEXT="<anthrosidian>\n\
The user has an Obsidian knowledge base connected to ${PLATFORM}. Use the skills below when the user explicitly asks to interact with it.\n\n\
Vault: ${VAULT}\n\
Today's daily note: ${VAULT}/daily/${TODAY:0:4}/${TODAY}.md\n\n\
Available skills:\n\
  anthrosidian:daily-log    — log / record something to today's daily note\n\
  anthrosidian:compile-wiki — ingest URLs, compile raw notes, and update wiki articles\n\
  anthrosidian:qa-wiki      — search or look something up in the wiki\n\
  anthrosidian:health-check — audit and fix wiki quality issues\n\n\
Vault structure:\n\
  daily/     daily notes (YYYY-MM-DD.md)\n\
  wiki/      LLM-compiled knowledge articles (owned by Claude)\n\
  raw/       source materials (added by user, read by Claude)\n\
  output/    reports / slides / visualizations\n\
  assets/    media files\n\
  templates/ note templates\n\n\
When the user asks to record, log, or save something to their knowledge base:\n\
  - If it is clear they mean today's daily note, use anthrosidian:daily-log.\n\
  - If the destination or format is ambiguous, ask one focused clarifying question\n\
    before proceeding (e.g. \"Should I add this to today's daily note, or create a wiki article?\").\n\n\
Full wiki compile rules: check ${VAULT}/AGENTS.md or ${VAULT}/CLAUDE.md when present\n\
To update vault path: ${SETUP_COMMAND} [new-path]\n\
</anthrosidian>"
fi

# Escape for JSON string
escaped=$(printf '%s' "$CONTEXT" | python3 -c "
import sys, json
print(json.dumps(sys.stdin.read())[1:-1])
" 2>/dev/null)

printf '{"additionalContext": "%s"}\n' "$escaped"
exit 0
