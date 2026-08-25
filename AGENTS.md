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

## Sources of Truth & Code Intelligence

### External Truth (Docs & APIs)

Before generating code or config for any third-party library/API, retrieve verified,
version-specific documentation. Never rely on model memory alone. If no verified
source exists, explicitly flag the assumption in the response.

Priority order (via whichever mechanism is available: MCP, skill, CLI, or built-in tool):
1. Structured doc index — e.g. `llms.txt`, a docs MCP server, a doc-fetch skill,
   or a `ctx7`-style CLI
2. Package/repo-native docs — README, changelog, official repo docs, via CLI
   (`man`, `--help`, `npm docs`) or direct file read
3. Live web search / page fetch — for issues, error logs, or undocumented edge
   cases, via web-search MCP, skill, or built-in browsing tool
4. Model memory — last resort only, must be explicitly marked as unverified

### Internal Truth (Codebase Intelligence)

Before modifying existing code, resolve symbols, definitions, call sites, and
architecture structurally — not via plain-text search. Pull only the minimal
relevant context per lookup to conserve tokens, and base all edits on verified
implementations.

Priority order (via whichever mechanism is available: built-in, LSP client, MCP,
skill, or CLI):
1. Editor/IDE built-in structural navigation (go-to-definition, find-references, rename)
2. Language-server tooling — LSP client, MCP wrapper, or CLI invocation of a
   language server
3. Semantic codebase memory or graph tool, if configured — e.g. an MCP server
   (Serena, Graphify) or an equivalent skill/CLI
4. `grep` / plain-text search — fallback only, with an explicit notice that
   structural tools were unavailable
