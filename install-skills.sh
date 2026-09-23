#!/bin/bash
# 暫時解法：先手動建立目標目錄，避免 npx skills add -g 發生 "not linked" 錯誤

# =============================================================================
# 設定與常數
# =============================================================================

# 為了相容 macOS 預設的 Bash 3.2 (不支援 declare -A 關聯陣列)，改用兩個對應陣列
AGENTS=(
  "antigravity"
  "claude-code"
  "codex"
  "opencode"
  "junie"
)

AGENT_ARGS=$(printf " -a %s" "${AGENTS[@]}")

# 各 Agent 的 skill 安裝目錄 (與 AGENTS 順序一一對應)
# shellcheck disable=SC2088 # 這裡刻意保留 ~，下方用 eval echo 展開為家目錄路徑
PATHS=(
  "~/.gemini/antigravity/skills/" # antigravity (npm skills@1.7.0 的 globalSkillsDir 定義，非官方文件寫的 ~/.gemini/config/skills/)
  "~/.claude/skills/"             # claude-code
  "~/.codex/skills/"              # codex
  "~/.config/opencode/skills/"    # opencode
  "~/.junie/skills/"              # junie
)

# 各 Agent 的 Global 規則目標路徑 (與 AGENTS/PATHS 順序一一對應)
# shellcheck disable=SC2088 # 這裡刻意保留 ~，下方用 eval echo 展開為家目錄路徑
RULE_TARGETS=(
  "~/.gemini/GEMINI.md"          # antigravity
  "~/.claude/CLAUDE.md"          # claude-code
  "~/.codex/AGENTS.md"           # codex
  "~/.config/opencode/AGENTS.md" # opencode
  "~/.junie/AGENTS.md"           # junie
)

# agents.md 規範定義的全域標準位置 (https://agentsstandard.com/)，非個別 agent 專屬，故獨立於上面的 1:1 陣列外
UNIVERSAL_RULE_TARGET=~/.agents/AGENTS.md

# npx skills add --copy 對於「universal agent」(codex/opencode/antigravity，
# 其 skillsDir 定義為 .agents/skills) 實際上永遠只會複製到這個通用目錄，
# 不會真的落地到各自的專屬目錄，所以需要 sync_skills_to_agents() 額外補一次複製。
UNIVERSAL_SKILLS_DIR=~/.agents/skills

# 本地 skills 黑名單: 掃描 ./skills/ 時跳過這些項目
SKILL_BLACKLIST=(
  "youtube-download"
  "atlas-schema"
  "bun-uptrace"
)

# =============================================================================
# 函數 (依 main 的執行順序排列)
# =============================================================================

# -----------------------------------------------------------------------------
# Function: create_agent_skill_dirs
# 意圖: 依序檢查並建立所有 agent 專屬的 skill 目錄，避免 npx skills add -g 發生 "not linked" 錯誤。
# -----------------------------------------------------------------------------
create_agent_skill_dirs() {
  echo "[*] Creating agent specific skill directories..."
  for i in "${!AGENTS[@]}"; do
    # 利用 eval 展開波浪號 (~) 為家目錄路徑
    eval mkdir -p "${PATHS[$i]}"
  done
  echo "[*] Directories are ready."
}

# -----------------------------------------------------------------------------
# Function: prompt_install_scope
# 意圖: 讓使用者選擇要安裝的 skill 範圍 (remote / local / all)，必須明確選擇，不提供預設值；輸入錯誤直接失敗結束。
# -----------------------------------------------------------------------------
prompt_install_scope() {
  local choice
  echo "請選擇要安裝的 skill 範圍："
  echo "  1) Remote skills (來自 GitHub 的公開 skills)"
  echo "  2) Local skills (本專案 ./skills/ 底下的 skills)"
  echo "  3) 全部安裝"
  read -r -p "輸入選項 [1/2/3]: " choice

  case "$choice" in
    1)
      install_remote_skills
      ;;
    2)
      install_local_skills
      ;;
    3)
      install_remote_skills
      install_local_skills
      ;;
    *)
      echo "[!] 無法辨識的選項 \"$choice\"，安裝中止。" >&2
      exit 1
      ;;
  esac
}

# -----------------------------------------------------------------------------
# Function: install_remote_skills
# 意圖: 安裝所有來自遠端 GitHub repo 的 skills (含相依的 mise 工具)。
# -----------------------------------------------------------------------------
# shellcheck disable=SC2086 # $AGENT_ARGS 刻意不加引號，用來展開成多個 -a <agent> 參數
install_remote_skills() {
  echo "[*] Installing remote skills..."

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
}

# -----------------------------------------------------------------------------
# Function: install_local_skills
# 意圖: 掃描 ./skills/ 底下所有目錄自動安裝，黑名單內的項目跳過。
# 新增 skill 只要建目錄即可，不需再回來改這份清單。
# -----------------------------------------------------------------------------
install_local_skills() {
  local LOCAL_SKILLS_DIR
  LOCAL_SKILLS_DIR="$(dirname "$0")/skills"
  echo "[*] Installing local skills from $LOCAL_SKILLS_DIR ..."
  for skill_path in "$LOCAL_SKILLS_DIR"/*/; do
    [ -d "$skill_path" ] || continue
    skill_path="${skill_path%/}"
    local skill_name
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
    # shellcheck disable=SC2086 # $AGENT_ARGS 刻意不加引號，用來展開成多個 -a <agent> 參數
    npx skills add "$skill_path" $AGENT_ARGS -y -g --copy
  done
}

# -----------------------------------------------------------------------------
# Function: is_blacklisted
# 意圖: 判斷指定的 skill 名稱是否在 SKILL_BLACKLIST 裡 (供 install_local_skills 使用)。
# -----------------------------------------------------------------------------
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

# -----------------------------------------------------------------------------
# Function: sync_skills_to_agents
# 意圖: 確保所有安裝在通用目錄 ($UNIVERSAL_SKILLS_DIR) 的技能，都能實體複製到各個 agent 的專屬目錄。
# 說明: npx skills add --copy 對 codex/opencode/antigravity 這類 universal agent 不會真的
#       複製到專屬目錄 (一律導回通用目錄)，所以這裡強制補一次複製，見 vercel-labs/skills#1805。
# -----------------------------------------------------------------------------
sync_skills_to_agents() {
  echo "[*] Ensuring all skills are explicitly copied..."

  if [ -d "$UNIVERSAL_SKILLS_DIR" ]; then
    for skill_path in "$UNIVERSAL_SKILLS_DIR"/*; do
      if [ -d "$skill_path" ]; then
        local skill_name
        skill_name=$(basename "$skill_path")
        for i in "${!AGENTS[@]}"; do
          local dir_path
          dir_path=$(eval echo "${PATHS[$i]}")

          # 先清除可能存在的舊版拷貝或無效的軟連結
          rm -rf "${dir_path:?}/${skill_name:?}"

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
  local SOURCE_RULE
  SOURCE_RULE="$(dirname "$0")/AGENTS.md"

  if [ ! -f "$SOURCE_RULE" ]; then
    echo "[!] Source rule file $SOURCE_RULE not found, skipping."
    return
  fi

  for target in "${RULE_TARGETS[@]}"; do
    local expanded_target
    expanded_target=$(eval echo "$target")
    mkdir -p "$(dirname "$expanded_target")"
    cp "$SOURCE_RULE" "$expanded_target"
    echo "    -> Synced to $target"
  done

  mkdir -p "$(dirname "$UNIVERSAL_RULE_TARGET")"
  cp "$SOURCE_RULE" "$UNIVERSAL_RULE_TARGET"
  echo "    -> Synced to $UNIVERSAL_RULE_TARGET"
}

# -----------------------------------------------------------------------------
# Function: main
# 意圖: 主要流程 - 建立目錄 -> 依使用者選擇安裝 skills -> 同步 Global 規則。
# -----------------------------------------------------------------------------
main() {
  create_agent_skill_dirs
  prompt_install_scope
  sync_skills_to_agents
  sync_global_rules
  echo "[*] All done!"
}

main
