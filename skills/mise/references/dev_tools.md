# Mise - Dev Tools

**Pages:** 10

---

## mise registry ​

**URL:** https://mise.jdx.dev/cli/registry.html

**Contents:**
- mise registry ​
- Arguments ​
  - [NAME] ​
- Flags ​
  - -b --backend <BACKEND> ​
  - --hide-aliased ​
  - -J --json ​

List available tools to install

This command lists the tools available in the registry as shorthand names.

For example, poetry is shorthand for asdf:mise-plugins/mise-poetry.

Show only the specified tool's full name

Show only tools for this backend

Output in JSON format

**Examples:**

Example 1 (yaml):
```yaml
$ mise registry
node    core:node
poetry  asdf:mise-plugins/mise-poetry
ubi     cargo:ubi-cli

$ mise registry poetry
asdf:mise-plugins/mise-poetry
```

---

## Dev Tools ​

**URL:** https://mise.jdx.dev/dev-tools/

**Contents:**
- Dev Tools ​
- How it works ​
  - Tool Resolution Flow ​
  - Environment Integration ​
  - Path Management ​
  - Configuration Hierarchy ​
- Tool Options ​
  - Table Format (Recommended) ​
  - Dotted Notation ​
  - Generic Nested Support ​

Like asdf (or nvm or pyenv but for any language), it manages dev tools like node, python, cmake, terraform, and hundreds more.

mise is a tool that manages installations of programming language runtimes and other tools for local development. For example, it can be used to manage multiple versions of Node.js, Python, Ruby, Go, etc. on the same machine.

Once activated, mise can automatically switch between different versions of tools based on the directory you're in. This means that if you have a project that requires Node.js 18 and another that requires Node.js 22, mise will automatically switch between them as you move between the two projects. See tools available for mise with in the registry.

To know which tool version to use, mise will typically look for a mise.toml file in the current directory and its parents. To get an idea of how tools are specified, here is an example of a mise.toml file:

It's also compatible with asdf .tool-versions files as well as idiomatic version files like .node-version and .ruby-version. See configuration for more details.

When specifying tool versions, you can also refer to environment variables defined in the same file, but note that environment variables from referenced files are not resolved here.

mise is inspired by asdf and can leverage asdf's vast plugin ecosystem under the hood. However, it is much faster than asdf and has a more friendly user experience.

mise manages development tools through a sophisticated but user-friendly system that automatically handles tool installation, version management, and environment setup.

When you enter a directory or run a command, mise follows this process:

mise provides several ways to integrate with your development environment:

Automatic Activation: With mise activate, mise hooks into your shell prompt and automatically updates your environment when you change directories:

On-Demand Execution: Use mise exec to run commands with mise's environment without permanent activation:

Shims: mise can create lightweight wrapper scripts that automatically use the correct tool versions:

mise modifies your PATH environment variable to prioritize the correct tool versions:

This ensures that when you run node, you get the version specified in your project configuration, not a system-wide installation.

mise supports nested configuration that cascades from broad to specific settings:

Each level can override or extend the previous ones, giving you fine-grained control over tool versions across different contexts.

Tool options allow you to customize how tools are installed and configured. They support nested configurations for better organization, particularly useful for platform-specific settings.

The cleanest way to specify nested options is using TOML tables:

You can also use dotted notation for simpler nested configurations:

Any backend can use nested options for organizing complex configurations:

Internally, nested options are flattened to dot notation (e.g., platforms.macos-x64.url, database.host, cache.redis.port) for backend access.

Run a command immediately after a tool finishes installing by adding a postinstall field to that tool's configuration. This is separate from [hooks].postinstall and applies only to when a specific tool is installed.

You can restrict tools to specific operating systems using the os field:

The os field accepts an array of operating system identifiers:

If a tool specifies an os restriction and the current operating system is not in the list, mise will skip installing and using that tool.

mise uses intelligent caching to minimize overhead:

This ensures that mise adds minimal latency to your daily development workflow.

After activating, mise will update env vars like PATH whenever the directory is changed or the prompt is displayed. See the FAQ.

After activating, every time your prompt displays it will call mise hook-env to fetch new environment variables. This should be very fast. It exits early if the directory wasn't changed or mise.toml/.tool-versions files haven't been modified.

mise modifies PATH ahead of time so the runtimes are called directly. This means that calling a tool has zero overhead and commands like which node returns the real path to the binary. Other tools like asdf only support shim files to dynamically locate runtimes when they're called which adds a small delay and can cause issues with some commands. See shims for more information.

Here are some of the most important commands when it comes to working with dev tools. Click the header for each command to go to its reference documentation page to see all available flags/options and more examples.

For some users, mise use might be the only command you need to learn. It will do the following:

mise use node@24 will install the latest version of node-24 and create/update the mise.toml config file in the local directory. Anytime you're in that directory, that version of node will be used.

mise use -g node@24 will do the same but update the global config (~/.config/mise/config.toml) so unless there is a config file in the local directory hierarchy, node-24 will be the default version for the user.

mise install will install but not activate tools—meaning it will download/build/compile the tool into ~/.local/share/mise/installs but you won't be able to use it without "setting" the version in a .mise-toml or .tool-versions file.

If you're coming from asdf, there is no need to also run mise plugin add to first install the plugin, that will be done automatically if needed. Of course, you can manually install plugins if you wish or you want to use a plugin not in the default registry.

There are many ways it can be used:

mise x can be used for one-off commands using specific tools. e.g.: if you want to run a script with python3.12:

Python will be installed if it is not already. mise x will read local/global .mise-toml/.tool-versions files as well, so if you don't want to use mise activate or shims you can use mise by just prefixing commands with mise x --:

If you use this a lot, an alias can be helpful:

Similarly, mise run can be used to execute tasks which will also activate the mise environment with all of your tools.

mise provides several mechanisms to automatically install missing tools or versions as needed. Below, these are grouped by how and when they are triggered, with relevant settings for each. All mechanisms require the global auto_install setting to be enabled (all auto_install settings are enabled by default).

When you run a command like mise x or mise r, mise will automatically install any missing tool versions required to execute the command.

If you type a command in your shell (e.g., node) and it is not found, mise can attempt to auto-install the missing tool version if it knows which tool provides that binary.

Disable auto_install for specific tools by setting auto_install_disable_tools to a list of tool names.

**Examples:**

Example 1 (json):
```json
[tools]
node = '22'
python = '3'
ruby = 'latest'
```

Example 2 (unknown):
```unknown
eval "$(mise activate zsh)"  # In your ~/.zshrc
cd my-project               # Automatically loads mise.toml tools
```

Example 3 (sql):
```sql
mise exec -- node my-script.js  # Runs with tools from mise.toml
```

Example 4 (unknown):
```unknown
mise activate --shims  # Creates shims instead of modifying PATH
```

---

## Shims ​

**URL:** https://mise.jdx.dev/dev-tools/shims.html

**Contents:**
- Shims ​
- Overview of the mise activation methods ​
  - PATH activation ​
  - Shims ​
- How to add mise shims to PATH ​
  - mise reshim ​
- Shims vs PATH ​
  - Env vars and shims ​
  - Hooks and shims ​
  - which ​

There are several ways for the mise context (dev tools, environment variables) to be loaded into your shell:

This page will help you understand the differences between these methods and how to use them. In particular, it will help you decide if you should use shims or mise activate in your shell.

Mise's "PATH" activation method updates environment variables every time the prompt is displayed. In particular, it updates the PATH environment variable, which is used by your shell to search for the programs it can run.

This is the method used when you add the echo 'eval "$(mise activate bash)"' >> ~/.bashrc line to your shell rc file (in this case, for bash).

For example, by default, your PATH variable might look like this:

If using mise activate, mise will automatically add the required tools to PATH.

In this example, the python bin directory was added at the beginning of the PATH, making it available in the current shell session.

While the PATH design of mise works great in most cases, there are some situations where shims are preferable. This is the case when you are not using an interactive shell (for example, when using mise in an IDE or a script).

mise activate --shims does not support all the features of mise activate. See shims vs path for more information.

When using shims, mise places small executables (shims) in a directory that is included in your PATH. You can think of shims as symlinks to the mise binary that intercept commands and load the appropriate context.

By default, the shim directory is located at ~/.local/share/mise/shims. When installing a tool (for example, node), mise will add some entries for every binary provided by this tool in the shims directory (for example, ~/.local/share/mise/shims/node).

To avoid calling ~/.local/share/mise/shims/node, you can add the shims directory to your PATH.

This will effectively make all dev tools available in your current shell session as well as non-interactive environments.

mise activate --shims is a shorthand for adding the shims directory to PATH.

The recommended way to add shims to PATH is to call mise activate --shims in one of your shell initialization file. For example, you can do the following:

In this example, we use mise activate --shims in the non-interactive shell configuration file (like .bash_profile or .zprofile) and mise activate in the interactive shell configuration file (like .bashrc or .zshrc)

mise activate will remove the shims directory from the PATH so it's fine to call mise activate --shims in your shell profile file then later call mise activate in an interactive session.

To force mise to update the content of the shims directory, you can manually call mise reshim.

Note that mise already runs a reshim anytime a tool is installed/updated/removed, so you don't need to use it for those scenarios. It is also done by default when using most tools such as npm.

mise reshim only creates/removes the shims. Some users sometimes use it as a "fix it" button, but it is only necessary if ~/.local/share/mise/shims doesn't contain something it should.

Do not add additional executable in the mise directory, mise will delete them with the next reshim.

The following features are affected when shims are used instead of PATH activation:

In general, using PATH (mise activate) instead of shims for interactive situations is recommended.

The way activate works is every time the prompt is displayed, mise-en-place will determine what PATH and other env vars should be and export them. This is why it doesn't work well for non-interactive situations like scripts. The prompt never gets displayed so you have to manually call mise hook-env to get mise to update the env vars. (though there are exceptions, see hook on cd)

A downside of shims is that the environment variables are only loaded when a shim is called. This means if you set an environment variable in mise.toml, it will only be used when a shim is called.

The following example only works under mise activate:

But this will work in either:

Also, mise x|exec and mise r|run can be used to get the environment even if you don't need any mise tools:

In general, tasks are a good way to ensure that the mise environment is always loaded.

The hooks cd, enter, exit, and watch_files only trigger with mise activate. However preinstall and postinstall still work with shims because they don't require shell integration.

which is a command that a lot of users find great value in. Using shims effectively "break" which and cause it to show the location of the shim. A workaround is to use mise which, which will show the actual location. Some users prefer the "cleanliness" of running which node and getting back a real path with a version number inside of it. e.g:

Truthfully, you're probably not going to notice a difference in performance when using shims vs. using mise activate.

If you are calling a shim from within a bash script like this:

You'll pay the mise penalty every time you call it within the loop. However, if you did the same thing but call a subprocess from within a shim (say, node creating a node subprocess), you will not pay a new penalty. This is because when a shim is called, mise sets up the environment with PATH for all tools and those PATH entries will be before the shim directory.

In other words, which is better in terms of performance just depends on how you're calling mise. Really though most users will not notice a few ms lag on their terminal caused by mise activate.

The only difference between these would be that using hook-env you will need to call it again if you change directories but with shims that won't be necessary. The shims directory will be removed by mise activate automatically so you won't need to worry about dealing with shims in your PATH.

There are many ways to load the mise environment that don't require either, chiefly: mise x|exec, mise r|run or mise en.

These will both load all the tools and env vars before executing something. This might be ideal because you don't need to modify your shell rc file at all and the environment is always loaded explicitly. Some might find this is a "clean" way of working.

The obvious downside is that anytime one wants to use mise they need to prefix it with mise exec|run. Though, you can easily alias them to mx|mr.

This is the method Jeff uses

Part of the reason for this is I often need to make sure I'm on my development version of mise. If you work on mise yourself I would recommend working in a similar way and disabling mise activate or shims while you are working on it.

See How I use mise for more information.

For some shells (bash, zsh, fish, xonsh), mise hooks into the cd command, while in others, it only runs when the prompt is displayed. This relies on chpwd in zsh, PROMPT_COMMAND in bash, fish_prompt in fish, and on_chdir in xonsh.

The upside is that it doesn't run as frequently but since mise is written in Rust the cost for executing mise is negligible (a few ms).

If you run a set of commands in a single line like the following:

If using mise activate, in shell without hook on cd, this will use the tools from ~, not from ~/src/proj1 or ~/src/proj2 even after the directory changed.

This is because, in these shells mise runs just before your prompt gets displayed whereas in others, it hooks on cd. Note that shims will always work with the inline example above.

rc files like .zshrc are unusual. It's a script but also runs only for interactive sessions. If you need to access tools provided by mise inside of an rc file you have 2 options:

**Examples:**

Example 1 (bash):
```bash
echo $PATH
/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin
```

Example 2 (bash):
```bash
PATH="$HOME/.local/share/mise/installs/python/3.13.0/bin:/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin"
```

Example 3 (markdown):
```markdown
ls -l ~/.local/share/mise/shims/node
# [...] ~/.local/share/mise/shims/node -> ~/.local/bin/mise
```

Example 4 (markdown):
```markdown
mise use -g node@20
npm install -g prettier@3.1.0

~/.local/share/mise/shims/node -v
# v20.0.0
~/.local/share/mise/shims/prettier -v
# 3.1.0
```

---

## mise.lock Lockfile experimental ​

**URL:** https://mise.jdx.dev/dev-tools/mise-lock.html

**Contents:**
- mise.lock Lockfile experimental ​
- Overview ​
- Enabling Lockfiles ​
- How It Works ​
- File Format ​
  - Platform Information ​
  - Tool Entry Fields ​
  - Platform Keys ​
- Environment-Specific Versions ​
- Local Lockfiles ​

mise.lock is a lockfile that pins exact versions and checksums of tools for reproducible environments. When enabled, mise will automatically maintain this file to ensure consistent tool versions across different machines and deployments.

The lockfile serves similar purposes to package-lock.json in npm or Cargo.lock in Rust:

Lockfiles are controlled by the lockfile setting:

mise.lock is a TOML file with a platform-based format that organizes asset information by platform:

Each platform in a tool's [tools.name.platforms] section uses a key format like "os-arch" (e.g., "linux-x64", "macos-arm64") and can contain:

Each tool entry ([[tools.name]]) can contain:

The platform key format is generally os-arch but can be customized by backends:

When using environment-specific configuration files (e.g., mise.test.toml), tools from those files are tagged with an env field in the lockfile:

When you run MISE_ENV=test mise use tiny@2, the lockfile will include:

Resolution priority: When resolving versions, mise checks in order:

This allows different environments to use different tool versions while sharing the same lockfile.

Tools defined in mise.local.toml (which is typically gitignored) use a separate mise.local.lock file. This keeps local tool configurations separate from the committed lockfile.

Use mise lock --local to update the local lockfile for all platforms:

The locked setting enforces that all tools have pre-resolved URLs in the lockfile before installation. This prevents API calls to GitHub, aqua registry, etc., ensuring fully reproducible installations.

When enabled, mise install will fail if a tool doesn't have a URL for the current platform in the lockfile. To fix this, first populate the lockfile with URLs:

This is useful for CI environments where you want to guarantee reproducible builds without any external API dependencies.

When you want to update tool versions:

Backend support for lockfile features varies:

If checksums become invalid or you need to regenerate them:

When merging branches with different lockfiles:

Since lockfiles are still experimental, enable them with:

**Examples:**

Example 1 (json):
```json
# Enable lockfiles globally
mise settings lockfile=true

# Or set in mise.toml
[settings]
lockfile = true
```

Example 2 (json):
```json
# Example mise.lock
[[tools.node]]
version = "20.11.0"
backend = "core:node"

[tools.node.platforms.linux-x64]
checksum = "sha256:a6c213b7a2c3b8b9c0aaf8d7f5b3a5c8d4e2f4a5b6c7d8e9f0a1b2c3d4e5f6a7"
size = 23456789
url = "https://nodejs.org/dist/v20.11.0/node-v20.11.0-linux-x64.tar.xz"

[[tools.python]]
version = "3.11.7"
backend = "core:python"

[tools.python.platforms.linux-x64]
checksum = "sha256:def456..."
size = 12345678

# Tool with backend-specific options
[[tools.ripgrep]]
version = "14.1.1"
backend = "aqua:BurntSushi/ripgrep"
options = { exe = "rg" }

[tools.ripgrep.platforms.linux-x64]
checksum = "sha256:4cf9f2741e6c465ffdb7c26f38056a59e2a2544b51f7cc128ef28337eeae4d8e"
size = 1234567

# Environment-specific version (only used when MISE_ENV=test)
[[tools.tiny]]
version = "2.1.0"
env = ["test"]
```

Example 3 (json):
```json
# mise.test.toml
[tools]
tiny = "2"
```

Example 4 (json):
```json
[[tools.tiny]]
version = "2.1.0"
env = ["test"]
```

---

## Registry ​

**URL:** https://mise.jdx.dev/registry.html

**Contents:**
- Registry ​
- Backends ​
  - Backends Priority ​
  - Environment Variable Overrides ​
- Tools ​

List of all tools aliased by default in mise.

You can use these shorthands with mise use. This allows you to use a tool without needing to know the full name. For example, to use the aws-cli tool, you can do the following:

If a tool is not available in the registry, you can install it by its full name. github and aqua give you for example access to almost all programs available on GitHub.

In addition to built-in core tools, mise supports a variety of backends to install tools.

In general, the preferred backend to use for new tools is the following:

New vfox and asdf tools are almost never accepted for supply-chain security reasons.

Each tool can define its own priority if it has more than one backend it supports. If you would like to disable a backend, you can do so with the following command:

This will disable the asdf backend. See Aliases for a way to set a default backend for a tool. Note that the asdf backend is disabled by default on Windows.

You can also specify the full name for a tool using mise use aqua:1password/cli if you want to use a specific backend.

You can override the backend for any tool using environment variables with the pattern MISE_BACKENDS_<TOOL>. This takes the highest priority and overrides any registry or alias configuration:

The tool name in the environment variable should be in SHOUTY_SNAKE_CASE (uppercase with underscores). For example, my-tool becomes MISE_BACKENDS_MY_TOOL.

Source: https://github.com/jdx/mise/blob/main/registry.toml

Note that mise registry can be used to list all tools in the registry. mise use without any arguments will show a tui to select a tool to install.

**Examples:**

Example 1 (unknown):
```unknown
mise use aws-cli
```

Example 2 (unknown):
```unknown
mise use aqua:aws/aws-cli
```

Example 3 (unknown):
```unknown
mise settings disable_backends=asdf
```

Example 4 (markdown):
```markdown
# Use vfox backend for php
export MISE_BACKENDS_PHP='vfox:mise-plugins/vfox-php'
mise install php@latest
```

---

## Tool Stubs ​

**URL:** https://mise.jdx.dev/dev-tools/tool-stubs.html

**Contents:**
- Tool Stubs ​
- Overview ​
- Tool (non-http) Stubs ​
- Configuration Fields ​
  - Optional Fields ​
- HTTP Stubs ​
  - Platform-Specific Binary Paths ​
- Generating Tool Stubs (http) ​
  - Basic Generation ​
  - Platform-Specific Generation ​

Tool stubs allow you to create executable files with embedded TOML configuration for tool execution. They provide a convenient way to define tool versions, backends, and execution parameters directly within executable scripts. They are also a good way to have some tools in mise lazy-load since the tools are only fetched when called and not when calling something like mise install.

This feature is inspired by dotslash, which pioneered the concept of executable files with embedded configuration for portable tool execution.

A tool stub is an executable file that begins with a shebang line pointing to mise tool-stub and contains TOML configuration specifying which tool to execute and how to execute it. When the stub is run, mise automatically installs the specified tool version (if needed) and executes it with the provided arguments.

Tool stubs can use any mise backend but because they default to http—and http backend tools have things like urls and don't require a version—the http stubs look a bit different than non-http stubs.

Tool stubs are particularly useful for adding less-commonly used tools to your mise setup. Since tools are only installed when their stub is first executed, you can define many tools without the overhead of installing them all upfront. This is perfect for specialized tools, testing utilities, or project-specific binaries that you might not use every day.

The -S flag tells env to split the command line on spaces, allowing multiple arguments to be passed to the interpreter. This is necessary because shebangs on Unix systems traditionally only support a single argument after the interpreter path. Using env -S mise tool-stub allows the shebang to work correctly by splitting it into env → mise → tool-stub.

Tool stub configuration is essentially a subset of what can be done in mise.toml [tools] sections, with the addition of a tool field to specify which tool to use. All the same options available for tool configuration in mise.toml are supported in tool stubs.

For multi-platform tarballs:

For platform-specific tarballs:

Different platforms may have different binary structures or names. You can specify platform-specific bin fields when the binary path differs between platforms:

The tool stub generator automatically detects when platforms have different binary paths and will generate platform-specific bin fields when needed, or use a global bin field when all platforms have the same binary structure.

tool stubs default to the HTTP backend if no tool field is specified and a url field is present. See the HTTP backend documentation for full details on configuring HTTP-based tools.

While you can manually create tool stubs with TOML configuration, mise provides a mise generate tool-stub command to automatically create stubs for HTTP-based tools.

When using platform-specific URLs, the tool stub generator will append new platforms to existing stub files rather than overwriting them. This allows you to incrementally build cross-platform tool stubs by running the command multiple times with different platforms.

Generate a tool stub for a tool distributed via HTTP:

For tools with different URLs per platform, you can generate all platforms at once:

Auto-Platform Detection: If the URL contains platform information, you can omit the platform prefix and let mise auto-detect it:

Or build them incrementally by adding platforms one at a time:

The generator will preserve existing configuration and merge new platforms into the [platforms] table. If you specify a platform that already exists, its URL will be updated.

The generator automatically detects and extracts various archive formats:

Running the generation command produces an executable stub like:

The generator automatically:

Make the stub executable and run it directly:

Execute using the mise tool-stub command—useful for testing if something isn't working right:

Tool stubs implement intelligent caching which reduces the overhead mise has when running stubs:

Cached stubs have ~4ms of overhead.

For basic use cases, you can quickly create simple tool stubs using the mise x command as an alternative to writing TOML configuration manually:

This approach is ideal for simple tool execution without the need for custom options, environment variables, or platform-specific settings. For more complex configurations, use the full TOML configuration format described above.

**Examples:**

Example 1 (markdown):
```markdown
#!/usr/bin/env -S mise tool-stub
# Optional comment describing the tool

version = "1.0.0"
tool = "python"
bin = "python"
```

Example 2 (unknown):
```unknown
#!/usr/bin/env -S mise tool-stub
url = "https://example.com/releases/1.0.0/tool-linux-x64.tar.gz"
```

Example 3 (json):
```json
#!/usr/bin/env -S mise tool-stub
[platforms.linux-x64]
url = "https://example.com/releases/1.0.0/tool-linux-x64.tar.gz"

[platforms.darwin-arm64]
url = "https://example.com/releases/1.0.0/tool-macos-arm64.tar.gz"
```

Example 4 (json):
```json
#!/usr/bin/env -S mise tool-stub
# Global bin field used when platforms have the same structure
bin = "bin/tool"

[platforms.linux-x64]
url = "https://example.com/tool-linux.tar.gz"
# Uses global bin field: "bin/tool"

[platforms.windows-x64]
url = "https://example.com/tool-windows.zip"
bin = "tool.exe"  # Platform-specific binary for Windows
```

---

## Tool Aliases ​

**URL:** https://mise.jdx.dev/dev-tools/aliases.html

**Contents:**
- Tool Aliases ​
- Aliased Backends ​
- Aliased Versions ​
- Templates ​

[alias] has been renamed to [tool_alias] to distinguish it from [shell_alias]. The old [alias] key still works but is deprecated.

For shell command aliases (like alias ll='ls -la'), see Shell Aliases.

Tools can be aliased so that something like node which normally maps to core:node can be changed to something like asdf:company/our-custom-node instead.

mise supports aliasing the versions of runtimes. One use-case for this is to define aliases for LTS versions of runtimes. For example, you may want to specify lts-hydrogen as the version for node@20.x so you can use set it with node lts-hydrogen in mise.toml/.tool-versions.

User aliases can be created by adding a tool_alias.<PLUGIN> section to ~/.config/mise/config.toml:

Plugins can also provide aliases via a bin/list-aliases script. Here is an example showing node.js versions:

Because this is mise-specific functionality not currently used by asdf it isn't likely to be in any plugin currently, but plugin authors can add this script without impacting asdf users.

Alias values can be templates, see Templates for details.

**Examples:**

Example 1 (json):
```json
[tool_alias]
node = 'asdf:company/our-custom-node' # shorthand for https://github.com/company/our-custom-node
erlang = 'asdf:https://github.com/company/our-custom-erlang'
```

Example 2 (json):
```json
[tool_alias.node.versions]
my_custom_20 = '20'
```

Example 3 (bash):
```bash
#!/usr/bin/env bash

echo "lts-hydrogen 18"
echo "lts-gallium 16"
echo "lts-fermium 14"
```

Example 4 (json):
```json
[tool_alias.node.versions]
current = "{{exec(command='node --version')}}"
```

---

## Prepare experimental ​

**URL:** https://mise.jdx.dev/dev-tools/prepare.html

**Contents:**
- Prepare experimental ​
- Quick Start ​
- Configuration ​
- Built-in Providers ​
- Custom Providers ​
  - Provider Options ​
- Freshness Checking ​
- Auto-Prepare ​
- Staleness Warnings ​
- CLI Usage ​

The mise prepare command ensures project dependencies are ready by checking if lockfiles are newer than installed outputs (e.g., package-lock.json vs node_modules/) and running install commands if needed.

Configure prepare providers in mise.toml:

mise includes built-in providers for common package managers:

Built-in providers are only active when explicitly configured in mise.toml and their lockfile exists.

Create custom providers for project-specific build steps:

mise uses modification time (mtime) comparison to determine if outputs are stale:

When auto = true is set on a provider, it will automatically run before:

This ensures dependencies are always up-to-date before running tasks or commands.

To skip auto-prepare for a single invocation:

When using mise activate, mise will warn you if any auto-enabled providers have stale dependencies:

This can be disabled with:

Prepare providers run in parallel, respecting the jobs setting for concurrency limits. This speeds up preparation when multiple providers need to run (e.g., both npm and pip).

Running mise prep will check all four providers and run any that are stale, in parallel.

**Examples:**

Example 1 (markdown):
```markdown
# Enable experimental features
export MISE_EXPERIMENTAL=1

# Run all applicable prepare steps
mise prepare

# Or use the alias
mise prep
```

Example 2 (go):
```go
# Built-in npm provider (auto-detects lockfile)
[prepare.npm]
auto = true  # Auto-run before mise x/run

# Built-in providers for other package managers
[prepare.yarn]
[prepare.pnpm]
[prepare.bun]
[prepare.go]
[prepare.pip]
[prepare.poetry]
[prepare.uv]
[prepare.bundler]
[prepare.composer]

# Custom provider
[prepare.codegen]
auto = true
sources = ["schema/*.graphql"]
outputs = ["src/generated/"]
run = "npm run codegen"

# Disable specific providers
[prepare]
disable = ["npm"]
```

Example 3 (json):
```json
[prepare.codegen]
sources = ["schema/*.graphql", "codegen.yml"]
outputs = ["src/generated/"]
run = "npm run codegen"
description = "Generate GraphQL types"

[prepare.prisma]
sources = ["prisma/schema.prisma"]
outputs = ["node_modules/.prisma/"]
run = "npx prisma generate"
```

Example 4 (unknown):
```unknown
mise run --no-prepare build
mise x --no-prepare -- npm test
```

---

## Comparison to asdf ​

**URL:** https://mise.jdx.dev/dev-tools/comparison-to-asdf.html

**Contents:**
- Comparison to asdf ​
- Migrate from asdf to mise ​
- asdf in go (0.16+) ​
- Supply chain security ​
- UX ​
- Performance ​
- Windows support ​
- Security ​
- Command Compatibility ​
- Extra backends ​

mise can be used as a drop-in replacement for asdf. It supports the same .tool-versions files that you may have used with asdf and can use asdf plugins through the asdf backend.

It will not, however, reuse existing asdf directories (so you'll need to either reinstall them or move them), and 100% compatibility is not a design goal. That said, if you're coming from asdf-bash (0.15 and below), mise actually has fewer breaking changes than asdf-go (0.16 and above) despite 100% compatibility not being a design goal of mise.

Casual users coming from asdf have generally found mise to just be a faster, easier to use asdf.

Make sure you have a look at environments and tasks which are major portions of mise that have no asdf equivalent.

If you're moving from asdf to mise, please review #how-do-i-migrate-from-asdf for guidance.

asdf has gone through a rewrite in go. Because this is quite new as of this writing (2025-01-01), I'm going to keep information about 0.16+ asdf versions (which I call "asdf-go" vs "asdf-bash") in this section and the rest of this doc will apply to asdf-bash (0.15 and below).

In terms of performance, mise is still faster than the go asdf, however the difference is much closer. asdf is likely fast enough that the difference in overhead between asdf-go and mise may not even be enough to notice for you—after all there are plenty of people still using asdf-bash that claim they don't even notice how slow it is (don't ask me how):

I don't think performance is a good enough reason to switch though now that asdf-go is a thing. It's a reason, but it's a minor one. The improved security in mise, better DX, and lack of reliance on shims are all more important than performance.

Given they went through the trouble of rewriting asdf—that's also an indication they want to keep working on it (which is awesome that they're doing that btw). This does mean that some of what's written here may go out of date if they address some of the problems with asdf.

asdf plugins are not secure. This is explained in SECURITY.md, but the quick explanation is that asdf plugins involve shell code which can essentially do anything on your machine. It's dangerous code. What's worse is asdf plugins are rarely written by the tool vendor (who you need to trust anyway to use the tool), which means for every asdf plugin you use you'll be trusting a random developer to not go rogue and to not get hacked themselves and publish changes to a plugin with an exploit.

mise still uses asdf plugins for some tools, but we're actively reducing that count as well as moving things into the mise-plugins org. It looks like asdf has a similar model with their asdf-community org, but it isn't. asdf gives plugin authors commit access to their plugin in asdf-community when they move it in, which I feel like defeats the purpose of having a dedicated org in the first place. By the end of 2025 I would like for there to no longer be any asdf plugins in the registry that aren't owned by me.

I've also been adopting extra security verification steps when vendors offer that ability such as gpg verification on node installs, and native Cosign/SLSA/Minisign/GitHub attestation verification for aqua tools.

Some commands are the same in asdf but others have been changed. Everything that's possible in asdf should be possible in mise but may use slightly different syntax. mise has more forgiving commands, such as using fuzzy-matching, e.g.: mise install node@20. While in asdf you can run asdf install node latest:20, you can't use latest:20 in a .tool-versions file or many other places. In mise you can use fuzzy-matching everywhere.

asdf requires several steps to install a new runtime if the plugin isn't installed, e.g.:

In mise this can all be done in a single step which installs the plugin, installs the runtime, and sets the version:

If you have an existing .tool-versions file, or .mise.toml, you can install all plugins and runtimes with a single command:

I've found asdf to be particularly rigid and difficult to learn. It also made strange decisions like having asdf list all but asdf latest --all (why is one a flag and one a positional argument?). mise makes heavy use of aliases so you don't need to remember if it's mise plugin add node or mise plugin install node. If I can guess what you meant, then I'll try to get mise to respond in the right way.

That said, there are a lot of great things about asdf. It's the best multi-runtime manager out there and I've really been impressed with the plugin system. Most of the design decisions the authors made were very good. I really just have 2 complaints: the shims and the fact it's written in Bash.

asdf made (what I consider) a poor design decision to use shims that go between a call to a runtime and the runtime itself. e.g.: when you call node it will call an asdf shim file ~/.asdf/shims/node, which then calls asdf exec, which then calls the correct version of node.

These shims have terrible performance, adding ~120ms to every runtime call. mise activate does not use shims and instead updates PATH so that it doesn't have any overhead when simply calling binaries. These shims are the main reason that I wrote this. Note that in the demo GIF at the top of this README that mise isn't actually used when calling node -v for this reason. The performance is identical to running node without using mise.

I don't think it's possible for asdf to fix these issues. The author of asdf did a great writeup of performance problems. asdf is written in bash which certainly makes it challenging to be performant, however I think the real problem is the shim design. I don't think it's possible to fix that without a complete rewrite.

mise does call an internal command mise hook-env every time the directory has changed, but because it's written in Rust, this is very quick—taking ~10ms on my machine. 4ms if there are no changes, 14ms if it's a full reload.

tl;dr: asdf adds overhead (~120ms) when calling a runtime, mise adds a small amount of overhead (~ 5ms) when the prompt loads.

asdf does not run on Windows at all. With mise, tools using non-asdf backends can support Windows. Of course, this means the tool vendor must provide Windows binaries but if they do, and the backend isn't asdf, the tool should work on Windows.

asdf plugins are insecure. They typically are written by individuals with no ties to the vendors that provide the underlying tool. Where possible, mise does not use asdf plugins and instead uses backends like aqua and ubi which do not require separate plugins.

Aqua tools include native Cosign/SLSA/Minisign/GitHub attestation verification built into mise. See SECURITY for more information.

In nearly all places you can use the exact syntax that works in asdf, however this likely won't show up in the help or CLI reference. If you're coming from asdf and comfortable with that way of working you can almost always use the same syntax with mise, e.g.:

UPDATE (2025-01-01): asdf-go (0.16+) actually got rid of asdf global|local entirely in favor of asdf set which we can't support since we already have a command named mise set. mise command compatibility will likely not be as good with asdf-go 0.16+.

It's not recommended though. You almost always want to modify config files and install things so mise use node@20 saves an extra command. Also, the "@" in the command is preferred since it allows you to install multiple tools at once: mise use|install node@20 node@18. Also, there are edge cases where it's not possible—or at least very challenging—for us to definitively know which syntax is being used and so we default to mise-style. While there aren't many of these, asdf-compatibility is done as a "best-effort" in order to make transitioning from asdf feel familiar for those users who can rely on their muscle memory. Ensuring asdf-syntax works with everything is not a design goal.

mise has support for backends other than asdf plugins. For example you can install CLIs directly from cargo and npm:

**Examples:**

Example 1 (json):
```json
asdf plugin add node
asdf install node latest:20
asdf local node latest:20
```

Example 2 (python):
```python
mise use node@20
```

Example 3 (unknown):
```unknown
mise install
```

Example 4 (unknown):
```unknown
mise install node 20.0.0
mise local node 20.0.0
```

---

## Backend Architecture ​

**URL:** https://mise.jdx.dev/dev-tools/backend_architecture.html

**Contents:**
- Backend Architecture ​
- What are Backends? ​
- The Backend Trait System ​
- Backend Types ​
  - Core Tools ​
  - Language Package Managers ​
  - Universal Installers ​
    - aqua - Comprehensive Package Manager ​
    - ubi - Universal Binary Installer (Deprecated) ​
  - Plugin Systems ​

Understanding how mise's backend system works can help you choose the right backend for your tools and troubleshoot issues when they arise. Most users don't need to explicitly choose backends since the mise registry defines smart defaults, but understanding the system helps when you need specific tools or want to optimize performance.

Backends are mise's way of supporting different tool installation methods. Each backend knows how to:

Think of backends as "adapters" that let mise work with different package managers and installation systems.

All backends implement a common interface (called a "trait" in Rust), which means they all provide the same basic functionality:

This design allows mise to treat all backends uniformly while each backend handles the specifics of its installation method.

Built directly into mise, written in Rust for performance and reliability:

Core tools like Node.js and Java are implemented as backends even though they represent single tools. This consistent backend architecture allows mise to handle all tools uniformly, whether they're complex ecosystems or individual tools.

Leverage existing language ecosystems:

Registry-based package manager with strong security features:

The ubi backend is deprecated. Use the github backend instead.

Zero-configuration installer that works with any GitHub/GitLab repository following standard conventions:

Support for external plugin ecosystems:

When you specify a tool, mise determines the backend using this priority:

The mise registry defines a priority order for which backend to use for each tool, so typically end-users don't need to know which backend to choose unless they want tools not available in the registry or want to override the default selection.

You can override the backend for any tool using the MISE_BACKENDS_<TOOL> environment variable pattern. The tool name is converted to SHOUTY_SNAKE_CASE (uppercase with underscores replacing hyphens).

The registry (mise registry) maps short names to full backend specifications with a preferred priority order:

Core tools should generally always be used when available, as they provide the best performance and integration with mise.

Some backends have dependencies on others:

mise automatically handles these dependencies, installing Node.js before npm tools, pipx before pipx tools, etc.

Some backends support additional configuration:

**Examples:**

Example 1 (rust):
```rust
pub trait Backend {
    async fn list_remote_versions(&self) -> Result<Vec<String>>;
    async fn install_version(&self, ctx: &InstallContext, tv: &ToolVersion) -> Result<()>;
    async fn uninstall_version(&self, tv: &ToolVersion) -> Result<()>;
    // ... other methods
}
```

Example 2 (markdown):
```markdown
# Use vfox backend for php
export MISE_BACKENDS_PHP='vfox:mise-plugins/vfox-php'
mise install php@latest
```

Example 3 (json):
```json
# ~/.config/mise/config.toml
[tool_alias]
go = "core:go"                    # Use core backend
terraform = "aqua:hashicorp/terraform"  # Use aqua backend
```

Example 4 (json):
```json
# ~/.config/mise/config.toml
[settings]
disable_backends = ["asdf", "vfox"] # Don't use these backends
```

---
