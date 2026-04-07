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
你维护一个 Obsidian 知识库，从任何项目目录皆可操作。\n\n\
Vault: ${VAULT}\n\
今日日志: ${VAULT}/daily/${TODAY}.md\n\n\
触发词（识别后立即执行，无需用户指定 skill）:\n\
  \"记录一下\" / \"记一下\"         → 写入今日 daily note\n\
  \"总结一下\" / \"编译知识库\"     → wiki 编译工作流\n\
  \"查一下wiki\" / \"知识库里有\"   → Q&A 工作流\n\
  粘贴 URL                          → obsidian:defuddle 抓取存到 raw/\n\
  \"lint知识库\" / \"health check\"  → wiki 健康检查\n\
  \"出报告\" / \"生成报告\"           → 输出到 output/\n\n\
Vault 结构:\n\
  daily/     今日日志 (YYYY-MM-DD.md)\n\
  wiki/      LLM 编译知识文章（Claude 完全拥有）\n\
  raw/       源材料（用户放入，Claude 读取）\n\
  output/    报告/幻灯片/可视化\n\
  assets/    媒体文件\n\
  templates/ 笔记模板\n\n\
Skill 路由:\n\
  URL 抓取  → obsidian:defuddle\n\
  读写搜索  → obsidian:obsidian-cli\n\
  MD 格式   → obsidian:obsidian-markdown\n\
  知识图谱  → obsidian:json-canvas\n\
  数据视图  → obsidian:obsidian-bases\n\n\
Daily note 格式:\n\
  ### <标题>\n\
  **Context:** 项目/场景\n\
  **Problem:** 问题描述\n\
  **Solution:** 解决方案\n\
  **Why it works:** 原理简释\n\n\
完整 wiki 编译规则: ${VAULT}/CLAUDE.md\n\
如未配置 vault 路径，运行: /obsidian-vault:setup\n\
</obsidian-vault>"

# Escape for JSON string
escaped=$(printf '%s' "$CONTEXT" | python3 -c "
import sys, json
print(json.dumps(sys.stdin.read())[1:-1])
" 2>/dev/null)

printf '{"additionalContext": "%s"}\n' "$escaped"
exit 0
