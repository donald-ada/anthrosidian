#!/usr/bin/env bash
# SessionStart hook: inject a minimal pointer to the knowledge base.
# Deliberately tiny — the KB is retrieved just-in-time, never preloaded.

set -euo pipefail

CONFIG="$HOME/.anthrosidian.conf"

if [[ -z "${KB_PATH:-}" && -f "$CONFIG" ]]; then
  # shellcheck source=/dev/null
  source "$CONFIG"
fi

if [[ -z "${KB_PATH:-}" ]]; then
  CONTEXT="<anthrosidian>
Knowledge base plugin installed but not configured. If the user wants a personal
AI-first knowledge base, run /anthrosidian:init. Otherwise ignore this.
</anthrosidian>"
elif [[ ! -d "$KB_PATH" ]]; then
  CONTEXT="<anthrosidian>
Knowledge base configured at ${KB_PATH} but the directory does not exist.
Fix ${CONFIG} or run /anthrosidian:init.
</anthrosidian>"
else
  NOTE_COUNT=$(grep -rl "^status: active" "$KB_PATH/notes" 2>/dev/null | wc -l | tr -d ' ')
  CONTEXT="<anthrosidian>
The user has a personal knowledge base at: ${KB_PATH} (${NOTE_COUNT} notes; protocol: ${KB_PATH}/AGENTS.md)
It is written by and for AI agents. Use it just-in-time — do not preload it:
- Before solving a problem the user may have hit before, grep it first (/anthrosidian:recall).
- When a session yields a durable insight, decision, or pitfall, offer to save it (/anthrosidian:remember).
- /anthrosidian:log appends today's episode; /anthrosidian:consolidate runs maintenance.
Read ${KB_PATH}/core/ before acting on standing preferences of the user.
</anthrosidian>"
fi

escaped=$(printf '%s' "$CONTEXT" | python3 -c "
import sys, json
print(json.dumps(sys.stdin.read())[1:-1])
" 2>/dev/null)

printf '{"hookSpecificOutput":{"hookEventName":"SessionStart","additionalContext":"%s"}}\n' "$escaped"
exit 0
