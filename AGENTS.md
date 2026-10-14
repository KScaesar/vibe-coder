# AGENTS.md

## Language & Communication

- Reply in Traditional Chinese (`zh-TW`) for all conversational interactions and Q&A.
- Keep technical terms, programming keywords, and proper nouns in English (`en-US`).

## Python Usage Rules

- You MUST use `uv` for all Python work: writing code, running scripts, and managing dependencies. Run Python commands with `uv run`.
- Never use `pip`, `poetry`, `conda`, or system Python to install or run anything.

## Shell Command Line Execution Rule

- The environment is managed by `mise`. Before running commands, follow the execution patterns defined in the `mise` skill.
- **Avoid compound commands**: Do not chain commands with `&&` or `;`. Split them into separate single commands so they match the auto-approval whitelists.

### Production Operations

- Before running any command that targets production (the command, host, path, or config name contains the substring `prod`) or that writes/deletes data, list the exact commands and what each will do, then wait for explicit confirmation.
- Run production commands one host at a time. Do not chain them or loop over hosts without confirmation.

## Sources of Truth & Code Intelligence

### External Truth (Docs & APIs)

Before writing code or config for any third-party library or API, retrieve verified, version-specific documentation. If no verified source exists, explicitly flag the assumption in the reply.

Use whichever mechanism is available (MCP, skill, CLI, or built-in tool), in this priority order:

1. Structured doc index — e.g. `llms.txt`, a docs MCP server, a doc-fetch skill, or a `ctx7`-style CLI
2. Package/repo-native docs — README, changelog, or official repo docs, via CLI (`man`, `--help`, `npm docs`) or direct file read
3. Live web search / page fetch — for issues, error logs, or undocumented edge cases
4. Model memory — last resort only; must be explicitly marked as unverified

### Internal Truth (Codebase Intelligence)

Before modifying existing code, resolve symbols, definitions, call sites, and architecture with structural tools, not plain-text search. Pull only the minimal relevant context per lookup, and base all edits on verified implementations.

Use whichever mechanism is available (built-in, LSP client, MCP, skill, or CLI), in this priority order:

1. Editor/IDE built-in structural navigation (go-to-definition, find-references, rename)
2. Language-server tooling — an LSP client, an MCP wrapper, or a CLI invocation of a language server
3. Semantic codebase memory or graph tool, if configured — e.g. an MCP server (Serena, Graphify) or an equivalent skill/CLI
4. `grep` / plain-text search — fallback only; state explicitly that structural tools were unavailable

## Asking the User

- Ask before acting when the decision is the user's: changing docs or code, changing specs, deleting files, merging, or filling in content that cannot be verified. Do not assume.
- Use the agent's built-in interactive prompt if one exists; otherwise ask in the chat and wait for the reply.
- Give a concrete example of the situation and the outcome of each option first, then ask one clear question.
- Put the full option details and your recommendation in the message body, not only in the option description fields (the user may not see them).
- Mark the recommended option with `(Recommended)` and explain the trade-offs. If an option changes an existing rule, say so explicitly: "This will change the existing rules."
- Ask at most 4 questions at a time; split larger sets into batches.
- If the user says they do not understand, explain with a concrete example and ask again. Change nothing until they understand.
- Exception: for small, uncontroversial fixes (typos, or docs that disagree with code that is reasonable), make the fix directly and say what you changed in the reply.

## Delegating to Other Agents

Applies when handing work to a subagent, a separate session, or an agent in a multiplexer:

- For long or auditable tasks, write the task to a file and have the result written to a specified file; keep the chat reply to a short completion message.
- Put those files in the environment's designated temp directory and use absolute paths.
- Do not trust the agent's self-reported completion; verify against the result file and your own checks (run tests, read the diff, check links).
- Only close or clean up sessions and resources that you created.