#!/bin/bash
# 暫時解法：先手動建立目標目錄，避免 npx skills add -g 發生 "not linked" 錯誤

# 1. 為了相容 macOS 預設的 Bash 3.2 (不支援 declare -A 關聯陣列)，改用兩個對應陣列
AGENTS=(
  "antigravity"
  "gemini-cli"
  "codex"
  "opencode"
  "junie"
)

PATHS=(
  "~/.gemini/antigravity/skills"
  "~/.gemini/skills"
  "~/.codex/skills"
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

AGENT_ARGS=$(printf " -a %s" "${AGENTS[@]}")
npx skills add vercel-labs/skills $AGENT_ARGS -y -g --copy
npx skills add anthropics/skills --skill skill-creator $AGENT_ARGS -y -g --copy
npx skills add vercel-labs/agent-browser --skill agent-browser $AGENT_ARGS -y -g --copy
mise use -g npm:agent-browser
npx skills add upstash/context7 --skill context7-cli $AGENT_ARGS -y -g --copy
mise use -g npm:ctx7
npx skills add Ben8t/math-spec-driven-skill $AGENT_ARGS -y -g --copy

# npx skills add obra/superpowers --skill using-git-worktrees $AGENT_ARGS -y -g --copy
# npx skills add obra/superpowers --skill receiving-code-review $AGENT_ARGS -y -g --copy
npx skills add obra/superpowers --skill brainstorming $AGENT_ARGS -y -g --copy
npx skills add obra/superpowers --skill writing-plans $AGENT_ARGS -y -g --copy

# npx skills add ./skills/youtube-download $AGENT_ARGS -y -g --copy
npx skills add ./skills/mise $AGENT_ARGS -y -g --copy
npx skills add ./skills/git-commit $AGENT_ARGS -y -g --copy
npx skills add ./skills/git-worktree-design $AGENT_ARGS -y -g --copy

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

# 執行同步複製
sync_skills_to_agents

echo "[*] All done!"
