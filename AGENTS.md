# AGENTS.md

## Tools

- Context7: "external truth source"
- Serena: "internal truth source"

## Python 使用規則

- 所有 Python 程式碼的撰寫、執行與依賴管理，一律使用 uv。
- 不得直接使用 pip、poetry、conda、或系統 python 進行安裝或執行。
- Python 指令一律透過 `uv run` 執行。

### Toolchain Execution Rule (mise)

在 AI agent / 非互動 shell 環境中，禁止依賴自動環境切換。

所有語言指令必須透過 `mise exec` 執行。

標準格式：
```
mise exec -- <tool> <command...>
```

範例（Go 測試）：
```
mise exec -- go test ./...
```

規則：
* 禁止直接執行 `go / node / python`
* 禁止使用 activate / source / 自動切換

## Code Generation and Library Usage

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
