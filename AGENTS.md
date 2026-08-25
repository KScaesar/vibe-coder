# AGENTS.md

## Language & Communication

- Respond in Traditional Chinese (`zh-TW`) for all conversational interactions and Q&A.
- Keep technical terms, programming keywords, and proper nouns in English (`en-US`, e.g., `toolchain`, `shims`, `prefix matching`, `auto-approval`).

## Python Usage Rules

- All Python development, execution, and dependency management MUST use `uv`.
- Direct usage of `pip`, `poetry`, `conda`, or system Python for installation or execution is strictly prohibited.
- Python commands MUST always be executed via `uv run`.

## Shell Command Line Execution Rule

- The environment is managed by `mise`. Follow the execution patterns defined in the `mise` skill before running commands.
- **Avoid Compound Commands**: Avoid chaining commands with `&&`, `;`. Prefer splitting them into standalone individual commands to match auto-approval whitelists.

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
- Language Server (LSP): "internal truth source"

Before modifying or reasoning about existing code, the agent MUST prefer LSP-based tools over plain text search (e.g. `grep`) for code discovery, including:
- symbols and their definitions
- call sites and references
- affected files and modules

Any available LSP-backed tool qualifies as the source of truth, in this priority order:
1. A built-in multi-language LSP MCP already provided by the agent runtime.
2. A user-installed LSP MCP (e.g. Serena, or other language-server-backed MCP tools).
3. A directly invoked language server / editor tooling, if no LSP MCP is available.

The agent MUST:
1. Use the available LSP-based tool to discover the relevant source of truth (symbols, references, call sites, affected files).
2. Limit the working context to the minimal relevant code returned by the LSP tool to reduce unnecessary token usage.
3. Base all changes and conclusions on the discovered implementation, not on assumptions.

Constraints:
- Do not manually scan the repository with plain text search before attempting LSP-based discovery.
- Do not modify code that has not been inspected via an LSP-based tool or explicitly justified.

Fallback:
- If no LSP-based tool is available, the agent must state this explicitly and proceed with caution (e.g. falling back to `grep`/text search).
