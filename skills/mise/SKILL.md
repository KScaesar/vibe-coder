---
name: mise
description: mise cli 適合需要頻繁切換工具版本與多語言環境的情境。它可以選擇將工具版本、環境變數與任務定義集中於單一設定檔，進入目錄即可自動生效，並在執行任務時套用正確的版本與設定，減少手動操作與環境不一致問題，提升整體開發體驗。
---

# Mise Skill

Mise is a comprehensive tool for managing development environments. It handles tool version management, environment variable configuration, and task execution, replacing multiple single-purpose tools with a unified experience.

install:

```sh
curl https://mise.run | sudo MISE_INSTALL_PATH=/usr/local/bin/mise sh
```

## Getting Started

Based on [Getting Started](references/getting_started.md).

Mise allows you to run tools without installing them globally or recursively.

### Core Concepts

- **Exec (`mise x`)**: Run a tool in an ephemeral environment.
  ```bash
  mise exec node@20 -- node app.js
  ```
- **Use (`mise use`)**: Install and pin a tool version for the current directory.
  ```bash
  mise use node@20
  ```
- **Run (`mise run`)**: Execute tasks defined in `mise.toml`.
- **Activate**: Integrate mise with your shell to automatically load tools and env vars when entering directories.

### Common Commands

- `mise ls`: List installed tools.
- `mise install`: Install tools defined in config.
- `mise doctor`: Diagnose issues.
- `mise upgrade`: Upgrade tool versions.

## Environments

Based on [Environments](references/environments.md).

Mise manages environment variables via `mise.toml` or `[env]` sections.

### Features

- **Project Structure**: Define env vars per project in `mise.toml`.
- **Dynamic Values**: Use templates like `{{config_root}}` or `{{env.HOME}}`.
- **Secrets**: Encrypt sensitive variables using `mise set --age-encrypt`.
- **Loading from Files**: Load `.env` files using `env._.file`.
  ```toml
  [env]
  _.file = ".env"
  NODE_ENV = "production"
  ```
- **Redaction**: Mark variables as sensitive to prevent leakage in logs.

## Dev Tools

Based on [Dev Tools](references/dev_tools.md).

Mise is a polyglot tool version manager, supporting hundreds of languages and tools via a registry and plugins.

### Key Capabilities

- **Backends**: Supports multiple backends (core, asdf, cargo, npm, go, etc.).
- **Shims**: Use shims for IDE integration or non-interactive shells.
- **Lockfiles**: Use `mise.lock` for reproducible tool versions across teams (Experimental).
- **Tool Stubs**: Generate executable stubs for tools to avoid full installation overhead until needed.

### Configuration

Tools are defined in the `[tools]` section of `mise.toml`:

```toml
[tools]
node = "20"
python = "3.11"
terraform = "1.5"
```

## Tasks

Based on [Tasks](references/tasks.md).

Mise includes a task runner similar to `make` or `npm scripts` but language-agnostic.

### Task Definitions

Tasks can be defined in `mise.toml` or as standalone scripts in `mise-tasks/`.

```toml
[tasks.build]
description = "Build the project"
run = "cargo build"
depends = ["lint"]
sources = ["src/**/*.rs"]
outputs = ["target/debug/app"]
```

### Features

- **Dependencies**: Define task execution order (`depends`, `depends_post`).
- **Parallelism**: Runs independent tasks in parallel.
- **Caching**: Skip tasks if sources haven't changed.
- **Watch**: Re-run tasks on file changes (`mise watch`).
- **Arguments**: Pass arguments to tasks using the usage spec.

## IDE Integration & Shell Configuration

Understanding the difference between interactive and non-interactive shells is key to configuring IDEs correctly.

### 1. Interactive Shells (Terminal)

This is your standard terminal usage where you type commands.

- **Mechanism**: Uses shell hooks to dynamically load environments.
- **Config File**: `~/.zshrc` (Zsh) or `~/.bashrc` (Bash).
- **Setup**:
  ```bash
  eval "$(mise activate zsh)"
  ```

### 2. Non-Interactive Shells (IDEs, Scripts, GUI Apps)

IDEs and background processes often run in non-interactive mode and do not load `.zshrc`. Using `activate` here will often fail.

- **Mechanism**: Uses Shims (executables that intercept commands) to route to the correct tool version.
- **Config File**: `~/.zprofile` (Zsh) or `~/.profile` (Bash).
- **Setup**:
  Add the shims directory to your PATH _before_ system paths.
  ```sh
  # ~/.zprofile
  eval "$(mise activate zsh --shims)"

  # ~/.bash_profile or ~/.bash_login or ~/.profile
  eval "$(mise activate bash --shims)"
  ```

### Summary Comparison

| Feature     | Interactive Terminal | IDE / Scripts / Non-Interactive |
| :---------- | :------------------- | :------------------------------ |
| Method      | `mise activate`      | Shims / `mise exec`             |
| Config File | `~/.zshrc`           | `~/.zprofile` / `~/.profile`    |
| Mechanism   | Shell Hooks (Prompt) | System PATH intercept           |

### 3. IDE Specific Recommendations

- **VS Code**:
  - **Best Practice**: Install the official Mise extension (publisher: `jdx`). It handles the environment injection automatically.

- **JetBrains (IntelliJ, PyCharm)**:
  - **Option A**: Install the Mise plugin.
  - **Option B**: Manually set the Project SDK/Interpreter path to the shim executable found in `~/.local/share/mise/shims/`.

## Other Reference Materials

For more detailed information, refer to the detailed markdown files in the `references/` directory:

- [getting_started.md](references/getting_started.md): Installation, basic usage, IDE integration, and troubleshooting.
- [environments.md](references/environments.md): Managing environment variables, secrets, and configuration files.
- [dev_tools.md](references/dev_tools.md): Tool version management, backends, shims, and lockfiles.
- [tasks.md](references/tasks.md): Definition and execution of tasks, dependencies, and file watching.
- [advanced.md](references/advanced.md): Advanced configuration, cookbooks for specific languages (Node.js, C++, etc.), and CI/CD tips.
- [cli.md](references/cli.md): Complete reference for all CLI commands and flags. Try `mise [COMMAND] -h` first.
- [plugins.md](references/plugins.md): CLI reference for managing plugins (install, update, uninstall).
- [other.md](references/other.md): Plugin architecture, guide to creating custom plugins, and direnv migration/deprecation.
- [index.md](references/index.md): Documentation index.
