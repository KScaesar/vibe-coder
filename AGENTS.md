# AGENTS.md

## Python 使用規則

- 所有 Python 程式碼的撰寫、執行與依賴管理，一律使用 uv。
- 不得直接使用 pip、poetry、conda、或系統 python 進行安裝或執行。
- Python 指令一律透過 `uv run` 執行。

### Shell Command Line Execution Rule

在 AI agent / 非互動 shell 環境中，mise 無法藉由 `cd` 目錄 Hook 自動環境切換。

執行前置檢查：
1. 首先確認當前 project 是否存在 `mise.toml` ...等等 mise 相關文件。
2. **僅在上述檔案存在時**，為了讓 mise 在非互動式環境生效且避免重複執行，執行環境切換指令。
3. 若專案無 `mise` 相關檔案，則直接執行任務指令，無需執行環境切換指令。

```bash
[ "$MISE_FOR_AI" = "1" ] || { eval "$(mise env)" && export MISE_FOR_AI=1; }
<執行任務指令>
```

## Code Generation and Library Usage

- Context7: "external truth source"
- Serena: "internal truth source"

When performing any of the following tasks:
- code generation
- setup or configuration steps
- usage of third-party libraries or APIs

The agent MUST:
1. Resolve the correct library or framework identity.
2. Retrieve up-to-date documentation using Context7 MCP tools as the primary source.
3. Base all generated code and configuration on the retrieved documentation, not on model memory.

Fallback behavior:
- If Context7 is unavailable or cannot resolve the library, the agent must explicitly state this and:
  - either request clarification from the user, or
  - proceed using best-effort knowledge while clearly marking assumptions.

Constraints:
- Do not generate code for undocumented or unverifiable APIs.
- Do not silently assume default versions or behaviors.

## Codebase Search and Exploration

- Context7: "external truth source"
- Serena: "internal truth source"

Before modifying or reasoning about existing code, the agent MUST:

1. Use Serena MCP tools to discover the relevant source of truth, including:
   - symbols and their definitions
   - call sites and references
   - affected files and modules
2. Limit the working context to the minimal relevant code returned by Serena to reduce unnecessary token usage.
3. Base all changes and conclusions on the discovered implementation, not on assumptions.

Constraints:
- Do not manually scan the repository without prior Serena-based discovery.
- Do not modify code that has not been inspected via Serena or explicitly justified.

Fallback:
- If Serena is unavailable, the agent must state this explicitly and proceed with caution.
