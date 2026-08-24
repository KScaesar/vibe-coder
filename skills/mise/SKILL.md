---
name: mise
description: Manage development environments, runtime toolchains (Node.js, Python, Go, Java, etc.), environment variables, secrets, and cross-platform task automation using Mise. Trigger this skill whenever the user asks to install or switch language tool versions, configure environment variables or .env files, manage global/local developer toolchains, or set up development environments.
---

# Mise Skill

Mise is a polyglot tool version manager and development environment orchestrator. It manages toolchains (Node, Go, Python, Java, etc.), environment variables, and task runners.

## Universal Constraint: Explicit Version Pinning (NEVER use `@latest`)

- **Strict Prohibition**: NEVER use `mise use <tool>@latest`, `mise install <tool>@latest`, or `@latest` in configuration files (`mise.toml`, `config.toml`).
- **Rationale**: `@latest` forces dynamic remote registry queries on every command, causing DNS resolution timeouts in sandboxed/offline environments and breaking build reproducibility.
- **Workflow to Install Latest**:
  ```bash
  mise use -g <tool>@$(mise latest <tool>)
  ```
  *(Resolves the latest version once and writes the concrete version string, e.g. `go = "1.24.0"`, into the active configuration).*

---

## Pre-Installation Check & Intent Clarification

Whenever the user asks to install, upgrade, use, or switch a tool (Node, Go, Python, usage, npm CLIs, etc.):

- **Mandatory Pre-Check**: Run [scripts/check_tool.sh](scripts/check_tool.sh) `<tool> [target_version]` **BEFORE** executing any installation, upgrade, or version change.
- **Do NOT Guess or Execute Directly**: Do not run `mise use` or `mise upgrade` without first executing the script.

```bash
bash scripts/check_tool.sh <tool> [target_version]
```

### Deterministic Gatekeeper & `ask_question` Enforcement

- **Exit Code 0 (`ALREADY_ACTIVE` / `NEW_INSTALL`)**:
  - Safe to proceed or no action needed. If scope (Project vs Global `-g`) is ambiguous for new installs, clarify with the user.
- **Exit Code 2 (`REQUIRES_USER_DECISION` / `VERSION_CHANGE`)**:
  - **🛑 STRICT PROHIBITION**: NEVER execute `mise use` or `mise upgrade` directly in the same turn.
  - **MANDATORY TOOL GATE**: The Agent **MUST IMMEDIATELY invoke the `ask_question` tool** using the questions and options provided in `ask_question_payload` from the script's JSON output.
  - **Human-In-The-Loop Execution**: Only execute the command after the user selects an option via `ask_question`:
    1. **Scenario 1 (Upgrade Existing Version)**: `mise upgrade <tool> --bump`
    2. **Scenario 2 (Coexistence & Global Switch)**: `mise use -g <tool>@<target_version>`
    3. **Scenario 3 (Project-local Switch)**: `mise use <tool>@<target_version>`

---

## AI Agent Execution Patterns

In non-interactive subshells (`bash -c`), `cd` does not trigger shell prompt hooks. Follow the sequential workflow below to select and apply the correct execution pattern:

- **Session Consistency**: Once the execution pattern is determined, stick with it consistently for all subsequent commands without re-running the diagnostic.
- **When NOT to Run**: Do NOT re-run `scripts/check_env.sh` before routine commands once the pattern is established.

### Step 1: Discover Environment First (`scripts/check_env.sh`)

- **Mandatory Discovery**: Run [scripts/check_env.sh](scripts/check_env.sh) **once** at the start of a session or when first discovering an environment.
- **Do NOT Guess**: Do not arbitrarily assume Pattern 1 or Pattern 2 before running the diagnostic script.
- **Follow Action Directive**: Inspect the `[Agent Action Directive]` output from the script and adopt the recommended pattern.

### Step 2: Apply the Detected Pattern

#### Pattern 1: Shims (Recommended — Clean Native Commands)

Adopted when `check_env.sh` reports `Pattern 1 is ACTIVE`.

- **Host Setup (One-time)**: Split activation across shell rc files so
  non-interactive/agent subshells inherit shims without relying on the
  prompt hook:
  ```bash
  # ~/.zprofile (non-interactive / login shell — read once, inherited by subshells)
  eval "$(mise activate zsh --shims)"

  # ~/.zshrc (interactive shell — place LAST, after any other PATH exports)
  eval "$(mise activate zsh)"
  ```
  Do NOT put `--shims` in `~/.zshrc`/`~/.bashrc` — that loses `mise activate`'s
  full feature set (env vars from `mise.toml`, `cd`/`enter`/`exit`/`watch_files`
  hooks) for interactive human sessions.
- **Agent Command Execution**: Directly execute clean native commands, e.g.
  `go build ./...`, `node app.js`, `uv run pytest` — no `mise exec --` prefix needed.
- **Mechanism**: The shim executable (e.g. `~/.local/share/mise/shims/go`) automatically detects `./mise.toml` at runtime and dispatches to the correct version.

#### Pattern 2: Explicit Execution (`mise exec --` / `mise x --`)

Adopted as fallback when `check_env.sh` reports Pattern 1 is not configured.

- **Agent Command Execution**:
  Use `mise exec --` (or `mise x --`) as a single binary prefix:
  ```bash
  mise exec -- go build ./...
  mise x -- uv run pytest
  ```
- **Mechanism**: Loads local `./mise.toml` tools and environment variables for the command.

---

### Troubleshooting & Sandbox Execution

- **Network Resolution Timeout**: Pass `MISE_OFFLINE=1` (e.g. `MISE_OFFLINE=1 mise reshim`) to prevent network queries.
- **Sandbox Filesystem Protection**: Run global setup (`mise reshim`) with host execution permissions (`BypassSandbox: true`).
- **Agent Rule**: If `mise` encounters network/DNS hangs, proactively ask the user for clarification before proceeding.

---

## Getting Started

Based on [Getting Started](references/getting_started.md).

### Core Concepts

- **Exec (`mise x`)**: Run a tool in an ephemeral environment.
  ```bash
  mise exec node@22 -- node app.js
  ```
- **Use (`mise use`)**: Install and configure tool versions.
  - **Project / Current Config**: `mise use node@22` (updates the configuration file where `node` is defined, or creates `./mise.toml`).
  - **Global Explicit (`-g`)**: `mise use -g go@$(mise latest go)` (writes to global configuration).
  - **Backend Packages**: `mise use -g npm:agent-browser@$(mise latest npm:agent-browser)`.
  - **Pin Exact**: `mise use --pin node@22.14.0`.
- **Upgrade (`mise upgrade`)**: Automatically upgrade tools to newer versions and bump configuration in-place.
- **Run (`mise run`)**: Execute tasks defined in `mise.toml`.
- **Activate**: Integrate mise with your shell.

### Common Commands

- `mise ls`: List installed tools and active versions.
- `mise upgrade`: Automatically upgrade outdated tools (`mise upgrade <tool> --bump`).
- `mise use`: Set active tool version in project or global config (`mise use <tool>@<version>`).
- `mise doctor`: Diagnose environment and configuration issues.

---

## Environments

Based on [Environments](references/environments.md).

Mise manages environment variables via `mise.toml` `[env]` sections:
```toml
[env]
_.file = ".env"
NODE_ENV = "production"
```

---

## Dev Tools & Multiple Backends

Based on [Dev Tools](references/dev_tools.md).

Define tools in `mise.toml`:
Mise is a polyglot manager supporting runtimes and CLI tools via multiple package ecosystems (backends):

### Supported Backend Prefixes
- **Core / Plugins**: Direct language runtimes (e.g. `node@22.14.0`, `go@1.24.0`, `python@3.12.0`).
- **NPM (`npm:<package>`)**: JavaScript/Node CLIs (e.g. `npm:agent-browser`, `npm:@google/gemini-cli`).
- **Cargo (`cargo:<crate>`)**: Rust binary crates (e.g. `cargo:ripgrep`, `cargo:eza`).
- **Pipx (`pipx:<package>`)**: Python standalone applications (e.g. `pipx:black`, `pipx:ruff`).
- **Aqua (`aqua:<repo>`)**: Direct prebuilt GitHub releases (e.g. `aqua:duckdb/duckdb`).
- **Ubi (`ubi:<repo>`)**: Universal binary installer from GitHub releases (e.g. `ubi:BurntSushi/ripgrep`).

### Usage Examples
```bash
# Install NPM-based CLI:
mise use -g npm:agent-browser@$(mise latest npm:agent-browser)

# Install Cargo-based CLI:
mise use -g cargo:ripgrep@14.1.0

# Install Aqua prebuilt binary:
mise use -g aqua:duckdb/duckdb@1.4.5
```

### Configuration (`mise.toml` / `~/.config/mise/config.toml`)
```toml
[tools]
node = "22.14.0"
python = "3.12.0"
go = "1.24.0"
"npm:agent-browser" = "0.22.2"
"npm:@google/gemini-cli" = "0.1.5"
"aqua:duckdb/duckdb" = "1.4.5"
```

For more details on backend configuration, lockfiles, and registries, see [references/dev_tools.md](references/dev_tools.md).

---

## Tasks

Based on [Tasks](references/tasks.md).

Define task pipelines in `mise.toml`:
```toml
[tasks.build]
description = "Build the project"
run = "cargo build"
depends = ["lint"]
```

---

## IDE Integration

- **VS Code**: Install official `Mise` extension (`jdx`).
- **JetBrains**: Set SDK/Interpreter to the shim in `~/.local/share/mise/shims/`.

---

## Reference Materials

- [getting_started.md](references/getting_started.md)
- [environments.md](references/environments.md)
- [dev_tools.md](references/dev_tools.md)
- [tasks.md](references/tasks.md)
- [advanced.md](references/advanced.md)
- [cli.md](references/cli.md)
