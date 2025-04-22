# vibe-coder

AI 協作開發起手式框架，與任意 LLM 模型（如 gemini, chatgpt, claude 等）結合，使用對話驅動專案設計與開發。  
包含常見的 prompt snippets，能快速啟動新專案並進行高效開發。  

- 快速啟動新專案並建立 llm 協作上下文。
- 作為 ai 接力式開發流程框架。
- 支援各種 llm 模型（gemini, chatgpt, claude, mistral 等）。
- 可應用於各種開發模式（api、web、資料處理等）。

![Vibe Coding 語意生成歷程](https://github.com/user-attachments/assets/1881a3f7-2f57-485d-b11c-c063cde114c7)

## 📁 目錄結構

```
vibe-coder/
├── prd.md
├── plan.md
├── tsd.md
├── README.md
└── .prompts/
    ├── prd.md
    ├── plan.md
    └── tsd.md
```

## 🔁 專案流程：llm-driven dev flow

### 1. 撰寫 Product Requirements Document (`prd.md`)
- 與 llm 腦力激盪，整理產品構想與功能需求。
- 產出 `prd.md`，包含：
  - 專案目標
  - 功能清單
  - 非功能需求（如 sla、安全性）
  - 使用者故事（可選）

### 2. 撰寫 Technical Specifications Document (`tsd.md`)
- 與 llm 共編，目的是讓開發者 5 分鐘內快速上手。
- 建議內容：
  - 專案簡介
  - 架構設計（可附圖或文字說明）
  - 資料夾結構與用途（如 `tree -L 2`）
  - 開發環境設定與啟動流程
  - 常見開發任務與指令範例

### 3. 架構設計與任務分解 (`plan.md`)
- 與 llm 討論技術架構與開發方向（前後端分離、資料流設計等）
- create checkboxes for "Next Steps"
- 請 llm 將 prd 拆解為具體的開發任務（ticket）：
  - 第一張為建立 skeleton（初始化專案）
  - 其餘每張為單一功能
- 建議 ticket 格式為 yaml，方便追蹤與管理：

```yaml
- title: "建立專案 skeleton"
  description: "初始化 repo，安裝必要套件與框架"
  files: ["README.md", "src/", "Dockerfile"]
  est_hours: 2
```

## 📦 常見 prompt snippets

```
# prd 起手式
請協助我整理以下構想為一份清楚的 prd 文件...

# plan 起手式
以下是 prd，請幫我拆解為實作任務，每張任務用 yaml 格式撰寫...

# tsd 起手式
請幫我撰寫一份 tsd.md，讓其他開發者能快速理解並加入開發...
```
