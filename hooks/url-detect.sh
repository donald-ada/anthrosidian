#!/usr/bin/env bash
# UserPromptSubmit hook: detect URLs and hint at obsidian:defuddle workflow

set -euo pipefail

CONFIG="$HOME/.claude/obsidian-vault.conf"
if [[ -f "$CONFIG" ]]; then
  # shellcheck source=/dev/null
  source "$CONFIG" 2>/dev/null || true
fi
VAULT="${VAULT_PATH:-$HOME/Documents/Obsidian Vault}"

# Read hook input from stdin
input=$(cat)
prompt=$(printf '%s' "$input" \
  | python3 -c "import sys,json; print(json.load(sys.stdin).get('user_prompt',''))" \
  2>/dev/null || echo "")

# Check for http/https URL
if printf '%s' "$prompt" | grep -qE 'https?://[^ ]+'; then
  hint="[obsidian-vault] 检测到 URL。如需保存页面内容，使用 obsidian:defuddle 抓取到 ${VAULT}/raw/，不要直接用 WebFetch 处理文章页面。"
  escaped=$(printf '%s' "$hint" \
    | python3 -c "import sys,json; print(json.dumps(sys.stdin.read())[1:-1])" \
    2>/dev/null)
  printf '{"additionalContext": "%s"}\n' "$escaped"
fi

exit 0
