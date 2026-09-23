#!/bin/bash
# 暫時解法：先手動建立目標目錄，避免 npx skills add -g 發生 "not linked" 錯誤

# 1. 為了相容 macOS 預設的 Bash 3.2 (不支援 declare -A 關聯陣列)，改用兩個對應陣列
AGENTS=(
  "antigravity"
  "claude-code"
  "codex"
  "opencode"
  "junie"
)

AGENT_ARGS=$(printf " -a %s" "${AGENTS[@]}")

PATHS=(
  "~/.claude/skills/"
  "~/.codex/skills"
  "~/.gemini/config/skills/"
  "~/.config/opencode/skills"
  "~/.junie/skills"
)

# 2. 依序檢查並建立所有專屬的目錄
echo "[*] Creating agent specific skill directories..."
for i in "${!AGENTS[@]}"; do
  # 利用 eval 展開波浪號 (~) 為家目錄路徑
  eval mkdir -p "${PATHS[$i]}"
done
echo "[*] Directories are ready."

npx skills add vercel-labs/skills $AGENT_ARGS -y -g --copy
npx skills add anthropics/skills --skill skill-creator $AGENT_ARGS -y -g --copy
npx skills add vercel-labs/agent-browser --skill agent-browser $AGENT_ARGS -y -g --copy
mise use -g npm:agent-browser
npx skills add upstash/context7 --skill context7-cli $AGENT_ARGS -y -g --copy
mise use -g npm:ctx7
# npx skills add Ben8t/math-spec-driven-skill $AGENT_ARGS -y -g --copy
npx skills add multica-ai/andrej-karpathy-skills $AGENT_ARGS -y -g --copy

# npx skills add obra/superpowers --skill using-git-worktrees $AGENT_ARGS -y -g --copy
# npx skills add obra/superpowers --skill receiving-code-review $AGENT_ARGS -y -g --copy
npx skills add obra/superpowers --skill brainstorming $AGENT_ARGS -y -g --copy
npx skills add obra/superpowers --skill writing-plans $AGENT_ARGS -y -g --copy

npx skills add mattpocock/skills --skill grill-me $AGENT_ARGS -y -g --copy
npx skills add mattpocock/skills --skill grill-with-docs $AGENT_ARGS -y -g --copy
npx skills add mattpocock/skills --skill domain-modeling $AGENT_ARGS -y -g --copy

# -----------------------------------------------------------------------------
# 本地 skills: 掃描 ./skills/ 底下所有目錄自動安裝，黑名單內的項目跳過。
# 新增 skill 只要建目錄即可，不需再回來改這份清單。
# -----------------------------------------------------------------------------
SKILL_BLACKLIST=(
  "youtube-download"
  "atlas-schema"
  "bun-uptrace"
)

is_blacklisted() {
  local name="$1"
  local item
  for item in "${SKILL_BLACKLIST[@]}"; do
    if [ "$item" = "$name" ]; then
      return 0
    fi
  done
  return 1
}

LOCAL_SKILLS_DIR="$(dirname "$0")/skills"
echo "[*] Installing local skills from $LOCAL_SKILLS_DIR ..."
for skill_path in "$LOCAL_SKILLS_DIR"/*/; do
  [ -d "$skill_path" ] || continue
  skill_path="${skill_path%/}"
  skill_name=$(basename "$skill_path")

  if [ ! -f "$skill_path/SKILL.md" ]; then
    echo "    [!] Skip $skill_name (no SKILL.md)"
    continue
  fi

  if is_blacklisted "$skill_name"; then
    echo "    [-] Skip $skill_name (blacklisted)"
    continue
  fi

  echo "    [+] Install $skill_name"
  npx skills add "$skill_path" $AGENT_ARGS -y -g --copy
done

# -----------------------------------------------------------------------------
# Function: sync_skills_to_agents
# 意圖: 確保所有安裝在通用目錄 (~/.agents/skills) 的技能，都能實體複製到各個 agent 的專屬目錄。
# 說明: 這是為了解決部分 LLM CLI 無法正確解析軟連結 (symlink) 導致無法觸發斜線指令的問題。
# -----------------------------------------------------------------------------
sync_skills_to_agents() {
  echo "[*] Ensuring all skills are explicitly copied..."
  local UNIVERSAL_DIR=~/.agents/skills

  if [ -d "$UNIVERSAL_DIR" ]; then
    for skill_path in "$UNIVERSAL_DIR"/*; do
      if [ -d "$skill_path" ]; then
        local skill_name=$(basename "$skill_path")
        for i in "${!AGENTS[@]}"; do
          local dir_path=$(eval echo "${PATHS[$i]}")

          # 先清除可能存在的舊版拷貝或無效的軟連結
          rm -rf "$dir_path/$skill_name"

          # 強制將技能實體複製到各個 agent 的目錄中
          cp -R "$skill_path" "$dir_path/$skill_name"
        done
      fi
    done
  fi
}

# -----------------------------------------------------------------------------
# Function: sync_global_rules
# 意圖: 將專案的 AGENTS.md 同步複製到各個 agent 的 Global 規則路徑
# -----------------------------------------------------------------------------
sync_global_rules() {
  echo "[*] Syncing global AGENTS.md to agents..."
  local SOURCE_RULE="$(dirname "$0")/AGENTS.md"

  if [ ! -f "$SOURCE_RULE" ]; then
    echo "[!] Source rule file $SOURCE_RULE not found, skipping."
    return
  fi

  # 定義各 Agent 的 Global 規則目標路徑
  local RULE_TARGETS=(
    "~/.claude/CLAUDE.md"
    "~/.codex/AGENTS.md"
    "~/.gemini/GEMINI.md"
    "~/.config/opencode/AGENTS.md"
    "~/.junie/AGENTS.md"
  )

  for target in "${RULE_TARGETS[@]}"; do
    local expanded_target=$(eval echo "$target")
    mkdir -p "$(dirname "$expanded_target")"
    cp "$SOURCE_RULE" "$expanded_target"
    echo "    -> Synced to $target"
  done
}

# 執行同步複製
sync_skills_to_agents
sync_global_rules

echo "[*] All done!"

