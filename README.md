# vibe-coder

```
cp -r ~/vibe-coder/prompts $(pwd)/
```

AI 協作開發起手式框架，與任意 LLM 模型（如 gemini, chatgpt, claude 等）結合，使用對話驅動專案設計與開發。  
包含常見的 prompt snippets，能快速啟動新專案並進行高效開發。

- 快速啟動新專案並建立 llm 協作上下文。
- 作為 ai 接力式開發流程框架。
- 支援各種 llm 模型（gemini, chatgpt, claude, mistral 等）。
- 可應用於各種開發模式（api、web、資料處理等）。

## Shortcut Commands

- create git commit message

```
gemini --yolo -p "/commit detail=true"
```

- create code review report

```
gemini --yolo -p "/review old={xx} new={yy} detail=true"
```

## Manager Skills

[vercel-labs/skills](https://github.com/vercel-labs/skills) 是一個用於管理 AI Agent Skills 的工具，支援 `claude-code`, `cursor`, `gemini` 等。

### ⚠️ 已知問題 (Known Issue)

> 目前 `npx skills add -g` 在安裝 agent 專屬技能時有一個 Bug ([Issue #537](https://github.com/vercel-labs/skills/issues/537))：
> 官方 CLI 在建立 symlink（軟連結）前，**不會自動建立目標目錄**（如 `~/.gemini/skills/`）。如果該目錄原本不存在，安裝雖然會顯示成功並放在 `~/.agents/skills/`，但對特定 agent 來說會處於 `not linked` 狀態，導致在 LLM CLI 輸入 `/` 時無法觸發。

### 解決方案 (Workaround)

作為暫時解法，我們已經將處理腳本獨立出來。
在進行全域安裝前，請直接執行專案中的腳本來主動建立各目錄與安裝 skills：

```bash
./install-skills.sh
```
