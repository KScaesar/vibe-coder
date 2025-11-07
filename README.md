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
