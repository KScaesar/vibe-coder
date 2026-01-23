# Mise - Other

**Pages:** 20

---

## Using Plugins ​

**URL:** https://mise.jdx.dev/plugin-usage.html

**Contents:**
- Using Plugins ​
- What Are Plugins? ​
  - Backend Plugins ​
  - Tool Plugins ​
- Installing Plugins ​
  - From a Git Repository ​
  - From Zip File ​
  - From Local Directory ​
- Using Plugins (Advanced) ​
- Plugin:Tool Format ​

mise supports plugins that extend its functionality, allowing you to install tools that aren't available in the standard registry. This is particularly useful for:

Plugins are extensions that can install and manage tools not included in mise's built-in registry. They are written in Lua and come in two main types:

Backend plugins use enhanced backend methods and support the plugin:tool format:

Tool plugins use the traditional hook-based approach:

Once a plugin is installed, you can use it with the plugin:tool format:

The plugin:tool format allows a single plugin to manage multiple tools. This is particularly useful for:

Plugins can be configured in your mise.toml file:

While mise doesn't have a centralized registry for community plugins, you can find them:

The vfox-npm plugin demonstrates how to create a plugin that installs npm packages:

This is just an example plugin for testing. mise already has built-in npm support that you should use instead: mise install npm:prettier@latest

Backend plugins use enhanced backend methods that provide better performance and support for the plugin:tool format:

This architecture allows plugins to manage multiple tools efficiently while providing a consistent interface.

Tool plugins use the traditional hook-based approach:

Both architectures provide a flexible plugin system that can handle diverse installation and management needs.

When using plugins, be aware that:

**Examples:**

Example 1 (sql):
```sql
# Install a plugin from a repository
mise plugin install <plugin-name> <repository-url>

# Example: Installing the vfox-npm plugin
mise plugin install vfox-npm https://github.com/jdx/vfox-npm
```

Example 2 (sql):
```sql
# Install a plugin from a zip file over HTTPS
mise plugin install <plugin-name> <zip-url>

# Example: Installing a plugin from a zip file
mise plugin install tiny https://github.com/mise-plugins/mise-tiny.git
```

Example 3 (markdown):
```markdown
# Link a local plugin for development
mise plugin link <plugin-name> /path/to/plugin/directory
```

Example 4 (julia):
```julia
# Install a specific tool using the plugin
mise install vfox-npm:prettier@latest

# Use the tool
mise use vfox-npm:prettier@3.0.0

# Execute the tool
mise exec vfox-npm:prettier -- --version

# List available versions
mise ls-remote vfox-npm:prettier
```

---

## direnv deprecated ​

**URL:** https://mise.jdx.dev/direnv.html

**Contents:**
- direnv deprecated ​
- mise inside of direnv (use mise in .envrc) ​
  - Do you need direnv? ​

direnv and mise both manage environment variables based on directory. Because they both analyze the current environment variables before and after their respective "hook" commands are run, they can sometimes conflict with each other.

The official stance is you should not use direnv with mise. Issues arising from incompatibilities are not considered bugs. If mise has feature gaps that direnv resolves, please open an issue so we can close those gaps. While that's the official stance, the reality is mise and direnv usually will work together just fine despite this. It's only more advanced use-cases where problems arise.

If you have an issue, it's likely to do with the ordering of PATH. This means it would really only be a problem if you were trying to manage the same tool with direnv and mise. For example, you may use layout python in an .envrc but also be maintaining a .tool-versions file with python in it as well.

A more typical usage of direnv would be to set some arbitrary environment variables, or add unrelated binaries to PATH. In these cases, mise will not interfere with direnv.

use mise is deprecated and no longer supported. If mise activate does not fit your use-case please post an issue.

If you do encounter issues with mise activate, or just want to use direnv in an alternate way, this is a simpler setup that's less likely to cause issues—at the cost of functionality.

This may be required if you want to use direnv's layout python with mise. Otherwise there are situations where mise will override direnv's PATH. use mise ensures that direnv always has control.

To do this, first use mise to build a use_mise function that you can use in .envrc files:

Now in your .envrc file add the following:

direnv will now call mise to export its environment variables. You'll need to make sure to add use_mise to all projects that use mise (or use direnv's source_up to load it from a subdirectory). You can also add use mise to ~/.config/direnv/direnvrc.

Note that in this method direnv typically won't know to refresh .tool-versions files unless they're at the same level as a .envrc file. You'll likely always want to have a .envrc file next to your .tool-versions for this reason. To make this a little easier to manage, I encourage not actually using .tool-versions at all, and instead setting environment variables entirely in .envrc:

Of course if you use mise activate, then these steps won't have been necessary and you can use mise as if direnv was not used.

If you continue to struggle, you can also try using the shims method.

While making mise compatible with direnv is, and will always be a major goal of this project, I also want mise to be capable of replacing direnv if needed. This is why mise includes support for managing env vars and virtualenv for python using mise.toml.

**Examples:**

Example 1 (unknown):
```unknown
mise direnv activate > ~/.config/direnv/lib/use_mise.sh
```

Example 2 (unknown):
```unknown
export MISE_NODE_VERSION=20.0.0
export MISE_PYTHON_VERSION=3.11
```

---

## Plugin Lua Modules ​

**URL:** https://mise.jdx.dev/plugin-lua-modules.html

**Contents:**
- Plugin Lua Modules ​
- Available Modules ​
  - Core Modules ​
- HTTP Module ​
  - Basic HTTP Requests ​
  - HEAD Requests ​
  - File Downloads ​
  - Response Object ​
- JSON Module ​
  - Basic Usage ​

mise plugins have access to a comprehensive set of built-in Lua modules that provide common functionality. These modules are available in both backend plugins and tool plugins, making it easy to perform common operations like HTTP requests, JSON parsing, file operations, and more.

The HTTP module provides functionality for making web requests and downloading files.

HTTP responses contain the following fields:

The JSON module provides encoding and decoding functionality.

The strings module provides various string manipulation utilities.

The semver module provides semantic version comparison and sorting functionality. This is useful for sorting version lists returned by Available() hooks.

The HTML module provides HTML parsing capabilities.

The archiver module provides functionality for extracting compressed archives.

The file module provides file system operations.

The file.join_path(...) function joins any number of path segments using the correct separator for the current operating system. This is the recommended way to construct file paths in cross-platform plugins.

The env module provides environment variable operations.

To read variables in Lua, use os.getenv("MY_VAR").

The cmd module provides shell command execution.

The options table supports the following keys:

Always handle errors gracefully:

Implement caching for expensive operations:

Handle cross-platform differences:

**Examples:**

Example 1 (json):
```json
local http = require("http")

-- GET request
local resp, err = http.get({
    url = "https://api.github.com/repos/owner/repo/releases",
    headers = {
        ['User-Agent'] = "mise-plugin",
        ['Accept'] = "application/json"
    }
})

if err ~= nil then
    error("Request failed: " .. err)
end

if resp.status_code ~= 200 then
    error("HTTP error: " .. resp.status_code)
end

local body = resp.body
```

Example 2 (javascript):
```javascript
local http = require("http")

-- HEAD request to check file info
local resp, err = http.head({
    url = "https://example.com/file.tar.gz"
})

if err ~= nil then
    error("HEAD request failed: " .. err)
end

local content_length = resp.headers['content-length']
local content_type = resp.headers['content-type']
```

Example 3 (json):
```json
local http = require("http")

-- Download file
local err = http.download_file({
    url = "https://github.com/owner/repo/archive/v1.0.0.tar.gz",
    headers = {
        ['User-Agent'] = "mise-plugin"
    }
}, "/path/to/download.tar.gz")

if err ~= nil then
    error("Download failed: " .. err)
end
```

Example 4 (json):
```json
{
    status_code = 200,
    headers = {
        ['content-type'] = "application/json",
        ['content-length'] = "1234"
    },
    body = "response content"
}
```

---

## Plugin Publishing ​

**URL:** https://mise.jdx.dev/plugin-publishing.html

**Contents:**
- Plugin Publishing ​
- Publishing Checklist ​
  - Essential Files ​
  - Optional but Recommended ​
- Repository Setup ​
  - 1. Initialize Repository ​
  - 2. Basic Directory Structure ​
  - 3. Git Ignore Configuration ​
- Versioning Strategy ​
  - Semantic Versioning ​

This guide shows how to publish and distribute your plugins, whether they are backend plugins or tool plugins. Publishing makes your plugins available to other users and ensures they can be easily installed and maintained.

Before publishing your plugin, ensure you have:

The easiest way to start is with the mise-tool-plugin-template:

Alternatively, create a repository from scratch:

Organize your plugin with this structure:

Create a .gitignore file:

Use semantic versioning (SemVer) for your plugin releases:

Update version in metadata.lua:

Create git tags for releases:

Create comprehensive test scripts:

Test your plugin manually:

Before publishing, ensure everything is ready:

Create a tagged release:

Create a GitHub release for better discoverability:

For private repositories, users need access:

You can also distribute as archives:

Establish a regular update process:

Maintain backward compatibility when possible:

Keep users informed about updates:

Plugin not installing:

**Examples:**

Example 1 (markdown):
```markdown
# Clone the template
git clone https://github.com/jdx/mise-tool-plugin-template my-plugin
cd my-plugin

# Remove template history and set up your own repository
rm -rf .git
git init
git remote add origin https://github.com/username/my-plugin.git

# Customize for your plugin
# Edit metadata.lua, hooks/*.lua, README.md, etc.
```

Example 2 (markdown):
```markdown
# Create plugin directory
mkdir my-plugin
cd my-plugin

# Initialize git repository
git init
git remote add origin https://github.com/username/my-plugin.git

# Create initial structure
touch metadata.lua
mkdir -p test
echo "# My Plugin" > README.md
```

Example 3 (unknown):
```unknown
my-plugin/
├── metadata.lua          # Plugin metadata
├── README.md            # Basic documentation
├── test/                # Test scripts
│   └── test.sh
├── .gitignore           # Git ignore rules
└── [implementation files]
```

Example 4 (unknown):
```unknown
backend-plugin/
├── metadata.lua          # Backend methods implementation
├── README.md
└── test/
    └── test.sh
```

---

## asdf (Legacy) Plugins ​

**URL:** https://mise.jdx.dev/asdf-legacy-plugins.html

**Contents:**
- asdf (Legacy) Plugins ​
- What are asdf (Legacy) Plugins? ​
- Limitations ​
- When to Use asdf (Legacy) Plugins ​
- Installing asdf (Legacy) Plugins ​
  - From the Registry ​
  - From Git Repository ​
  - Manual Installation ​
- Plugin Structure ​
- Required Scripts ​

mise maintains compatibility with the asdf plugin ecosystem through its asdf backend. These plugins are considered legacy because they have limitations compared to mise's modern plugin system.

asdf plugins are shell script-based plugins that follow the asdf plugin specification. They were the original way to extend tool management in the asdf ecosystem and are now supported by mise for backward compatibility.

asdf plugins have several limitations compared to mise's modern plugin system:

Only use asdf plugins when:

For new tools, consider these alternatives first:

Most popular asdf plugins are available through mise's registry:

asdf plugins follow this directory structure:

Lists all available versions of the tool:

Downloads the tool source/binary:

Set environment variables when executing tools:

Get the latest stable version:

List legacy version file names:

Parse legacy version files:

asdf plugins have access to these environment variables:

Here's a minimal example for a fictional tool:

Consider migrating from asdf plugins to modern alternatives:

asdf plugins execute arbitrary shell scripts, which poses security risks:

**Examples:**

Example 1 (sql):
```sql
# Install from registry shorthand
mise use postgres@15

# This is equivalent to
mise use asdf:mise-plugins/mise-postgres@15
```

Example 2 (sql):
```sql
# Install plugin directly from repository
mise plugin install <plugin-name> <git-url>

# Example: PostgreSQL plugin
mise plugin install postgres https://github.com/mise-plugins/mise-postgres
```

Example 3 (markdown):
```markdown
# Add plugin manually
mise plugin add postgres https://github.com/mise-plugins/mise-postgres

# Install tool version
mise install postgres@15.0.0

# Use the tool
mise use postgres@15.0.0
```

Example 4 (sql):
```sql
plugin-name/
├── bin/
│   ├── list-all          # List all available versions
│   ├── download          # Download source code/binary
│   ├── install           # Install the tool
│   ├── latest-stable     # Get latest stable version [optional]
│   ├── help.overview     # Plugin description [optional]
│   ├── help.deps         # Plugin dependencies [optional]
│   ├── help.config       # Plugin configuration [optional]
│   ├── help.links        # Plugin links [optional]
│   ├── list-legacy-filenames  # Legacy version files [optional]
│   ├── parse-legacy-file # Parse legacy version files [optional]
│   ├── post-plugin-add   # Post plugin addition hook [optional]
│   ├── post-plugin-update # Post plugin update hook [optional]
│   ├── pre-plugin-remove # Pre plugin removal hook [optional]
│   └── exec-env          # Set execution environment [optional]
├── lib/                  # Shared library code [optional]
└── README.md
```

---

## Backend Plugin Development ​

**URL:** https://mise.jdx.dev/backend-plugin-development.html

**Contents:**
- Backend Plugin Development ​
- What are Backend Plugins? ​
- Plugin Architecture ​
- Backend Methods ​
  - BackendListVersions ​
  - BackendInstall ​
  - BackendExecEnv ​
- Creating a Backend Plugin ​
  - Using the Template Repository ​
  - 1. Plugin Structure ​

Backend plugins in mise use enhanced backend methods to manage multiple tools using the plugin:tool format. These plugins are perfect for package managers, tool families, and custom installations that need to manage multiple related tools.

Backend plugins extend the standard vfox plugin system with enhanced backend methods. They support:

Backend plugins are generally a git repository but can also be a directory (via mise link).

Backend plugins are implemented in Lua (version 5.1 at the moment). They use three main backend methods implemented as individual files:

Lists available versions for a tool:

Version sorting: The versions returned by BackendListVersions should be in ascending order (oldest to newest), sorted semantically (version 3.10.0 should not come before 3.2.0). Mise does not apply any additional sorting to the versions returned by this method.

Installs a specific version of a tool:

Sets up environment variables for a tool:

Use the dedicated mise-backend-plugin-template for creating backend plugins:

The template includes:

Create a directory with this structure:

Here's the complete implementation of the vfox-npm plugin that manages npm packages:

The plugin name doesn't have to match the repository name. The backend prefix will match whatever name the backend plugin was installed as.

Tip: This naming flexibility could potentially be used to have a very complex plugin backend that would behave differently based on what it was named. For example, you could install the same plugin with different names to configure different behaviors or access different tool registries.

Backend plugins receive context through the ctx parameter passed to each hook function:

Use debug mode to see detailed plugin execution:

Provide more meaningful error messages:

Parse versions with regex:

Use cross-platform path handling:

Handle different operating systems:

Different installation logic based on tool or version:

vfox automatically injects runtime information into your plugin:

The RUNTIME object provides:

Set multiple environment variables:

TODO: We need caching support for Shared Lua modules.

**Examples:**

Example 1 (julia):
```julia
function PLUGIN:BackendListVersions(ctx)
    local tool = ctx.tool
    local versions = {}

    -- Your logic to fetch versions for the tool
    -- Example: query an API, parse a registry, etc.

    return {versions = versions}
end
```

Example 2 (julia):
```julia
function PLUGIN:BackendInstall(ctx)
    local tool = ctx.tool
    local version = ctx.version
    local install_path = ctx.install_path

    -- Your logic to install the tool
    -- Example: download files, extract archives, etc.

    return {}
end
```

Example 3 (json):
```json
function PLUGIN:BackendExecEnv(ctx)
    local install_path = ctx.install_path

    -- Your logic to set up environment variables
    -- Example: add bin directories to PATH

    return {
        env_vars = {
            {key = "PATH", value = install_path .. "/bin"}
        }
    }
end
```

Example 4 (markdown):
```markdown
# Option 1: Use GitHub's template feature (recommended)
# Visit https://github.com/jdx/mise-backend-plugin-template
# Click "Use this template" to create your repository

# Option 2: Clone and modify
git clone https://github.com/jdx/mise-backend-plugin-template my-backend-plugin
cd my-backend-plugin
rm -rf .git
git init
```

---

## Shell Aliases ​

**URL:** https://mise.jdx.dev/shell-aliases.html

**Contents:**
- Shell Aliases ​
- Configuration ​
- Supported Shells ​
- Dynamic Behavior ​
- Hierarchy ​
- Templates ​
- Use Cases ​
  - Project-Specific Shortcuts ​
  - Tool Wrappers ​
  - Quick Navigation ​

mise can manage shell aliases that are set dynamically when you enter a directory and unset when you leave, similar to how environment variables work.

Shell aliases are defined in mise.toml under the [shell_alias] section:

When you enter a directory with this configuration, these aliases will be automatically set in your shell. When you leave the directory (and the new directory doesn't have the same aliases), they will be unset.

Shell aliases are currently supported in:

Other shells (nushell, elvish, xonsh, powershell) do not currently support shell aliases.

Shell aliases work similarly to environment variables managed by mise:

Like other mise config, shell aliases are inherited from parent directories. A child directory can override a parent's alias:

Alias values support templates, allowing dynamic values:

Define shortcuts that only make sense within a specific project:

Create aliases that wrap tools with project-specific defaults:

mise has two different alias features that serve different purposes:

See Tool Aliases for documentation on aliasing tool versions.

**Examples:**

Example 1 (json):
```json
[shell_alias]
ll = "ls -la"
la = "ls -A"
gs = "git status"
gc = "git commit"
```

Example 2 (markdown):
```markdown
$ cd ~/myproject
# mise sets: alias ll='ls -la'

$ ll
# Runs: ls -la

$ cd ~
# mise runs: unalias ll
```

Example 3 (json):
```json
# ~/projects/mise.toml
[shell_alias]
build = "make build"

# ~/projects/myapp/mise.toml
[shell_alias]
build = "npm run build"  # Overrides parent
```

Example 4 (json):
```json
[shell_alias]
proj = "cd {{config_root}}"
node_version = "echo {{exec(command='node --version')}}"
```

---

## Plugins ​

**URL:** https://mise.jdx.dev/plugins.html

**Contents:**
- Plugins ​
- Backend Plugins ​
- Tool Plugins ​
- Environment Plugins ​
- General Plugin Usage ​
- asdf (Legacy) Plugins ​
- Plugin Authors ​
- Tool Options ​
- Templates ​

Plugins in mise are a way to extend mise with new functionality like extra tools or environment variable management.

Historically it was the only way to add new tools (as the only backend was asdf).

The way that backend works is every tool has its own plugin which needs to be manually installed. However, now with core tools and backends like aqua/ubi, plugins are no longer necessary to run most tools in mise.

Tool plugins should be avoided for security reasons. New tools will not be accepted into mise built with asdf/plugins unless they are very popular and aqua/ubi is not an option for some reason.

The only exception is if the tool needs to set env vars or has a complex installation process, as plugins can provide functionality like setting env vars globally without relying on a tool being installed. They can also provide aliases for versions.

If you want to integrate a new tool into mise, you should either try to get it into the aqua registry or see if it can be installed with ubi. Then add it to the registry. Aqua is definitely preferred to ubi as it has better UX and more features like slsa verification and the ability to use different logic for older versions.

You can manage all installed plugins in mise with mise plugins.

Backend plugins provide enhanced functionality with modern backend methods. These plugins use the plugin:tool format and offer advantages over traditional plugins:

See Backend Plugin Development for creating backend plugins. You can start quickly with the mise-backend-plugin-template.

Tool plugins use the traditional hook-based approach with Lua scripts. These plugins provide:

See Tool Plugin Development for creating tool plugins. The mise-tool-plugin-template provides a ready-to-use starting point.

Environment plugins provide environment variables and PATH modifications without managing tool versions. They're ideal for integrating with secret managers, setting dynamic configurations, and standardizing team environments.

Unlike tool plugins, environment plugins:

See Environment Plugin Development for creating environment plugins. The mise-env-sample repository provides a working example.

For end-user documentation on installing and using both backend and tool plugins, see Using Plugins.

mise can use asdf's plugin ecosystem under the hood for backward compatibility. These plugins contain shell scripts like bin/install (for installing) and bin/list-all (for listing all of the available versions).

asdf plugins have limitations compared to modern backends and should only be used when necessary. They only work on Linux/macOS and are slower than native backends.

See asdf (Legacy) Plugins for comprehensive documentation on using and creating these plugins.

https://github.com/mise-plugins is a GitHub organization for community-developed plugins. See SECURITY.md for more details on how plugins here are treated differently.

If you'd like your plugin to be hosted here please let me know (GH discussion or discord is fine) and I'd be happy to host it for you.

mise has support for "tool options" which is configuration specified in mise.toml to change behavior of tools. One example of this is virtualenv on python runtimes:

This will be passed to all plugin scripts as MISE_TOOL_OPTS__VIRTUALENV=.venv. The user can specify any option, and it will be passed to the plugin in that format.

Currently, this only supports simple strings, but we can make it compatible with more complex types (arrays, tables) fairly easily if there is a need for it.

Plugin custom repository values can be templates, see Templates for details.

**Examples:**

Example 1 (markdown):
```markdown
mise plugins ls --urls
# Plugin                          Url                                                     Ref  Sha
# 1password                       https://github.com/mise-plugins/mise-1password-cli.git  HEAD f5d5aab
# vfox-mise-plugins-vfox-dart     https://github.com/mise-plugins/vfox-dart               HEAD 1424253
# ...
```

Example 2 (markdown):
```markdown
# Install a backend plugin
mise plugin install my-plugin https://github.com/username/my-plugin

# Use the plugin:tool format
mise install my-plugin:some-tool@1.0.0
mise use my-plugin:some-tool@latest
```

Example 3 (markdown):
```markdown
# Install a tool plugin
mise plugin install my-tool https://github.com/username/my-tool-plugin

# Use the tool directly
mise install my-tool@1.0.0
mise use my-tool@latest
```

Example 4 (markdown):
```markdown
# Install an environment plugin
mise plugin install my-env-plugin https://github.com/username/my-env-plugin
```

---

## mise Architecture ​

**URL:** https://mise.jdx.dev/architecture.html

**Contents:**
- mise Architecture ​
- System Overview ​
- Core Architecture Components ​
  - Command Layer (src/cli/) ​
  - Backend System (src/backend/) ​
  - Configuration System (src/config/) ​
  - Toolset Management (src/toolset/) ​
  - Task System (src/task/) ​
  - Plugin System (src/plugins/) ​
  - Shell Integration (src/shell/) ​

This document provides a comprehensive overview of mise's architecture, designed primarily for contributors and those interested in understanding how mise works internally.

For practical development guidance, see the Contributing Guide.

mise is a Rust-based tool with a modular architecture centered around three core concepts:

These three pillars work together to provide a unified development environment management experience.

The CLI layer provides the user interface and delegates to core functionality:

Key Commands Architecture:

The backend system is mise's core abstraction for tool management, implementing a trait-based architecture:

For guidance on implementing new backends, see the Contributing Guide. For detailed backend system design, see Backend Architecture.

A hierarchical configuration system that merges settings from multiple config files:

Config Trait Architecture:

Concrete Implementations:

Configuration Hierarchy: See Configuration Documentation for the complete hierarchy and precedence rules.

Coordinates tool resolution, installation, and environment setup:

Tool Resolution Pipeline:

Sophisticated task execution with dependency graph management:

Architecture Components:

Dependency Resolution:

See the Task Documentation for complete usage details and configuration options, and Task Architecture for detailed system design.

Extensibility layer supporting multiple plugin architectures:

For complete plugin documentation, see Plugin Guide.

Shell-specific code generation that abstracts commands like mise env and contains all shell differences in one place:

Supported Shells: See mise activate documentation for the complete list Shell Abstractions: Environment variable setting, PATH modification, command execution

Helpers for working with environment variables:

For environment setup and configuration, see Environment Documentation.

Generic caching backed by files, using msgpack serialization with zstd compression:

mise employs a multi-layered testing strategy that combines different testing approaches for thorough validation across its complex feature set.

Testing Strategy Overview:

Most tests in mise are end-to-end tests, and this is generally the preferred approach for new functionality. E2E tests provide thorough validation of real-world usage scenarios and catch integration issues that unit tests might miss. However, E2E tests can be challenging to run locally due to environment dependencies and setup complexity. For development and CI purposes, it's often easier to run tests on GitHub Actions where the environment is consistent and properly configured.

See the Contributing Guide for detailed testing setup and guidelines.

Structure and Characteristics:

Test Environment Setup:

Environment Isolation System:

Each test runs in complete isolation with temporary directories:

Rich Assertion Framework:

The assert.sh provides rich test utilities:

Windows-Specific Tests (e2e-win/):

Performance and Utility Tests (xtasks/test/):

Test Data Management (test/):

Test Execution Modes:

Developer Experience Features:

For complete development setup and testing procedures, see the Contributing Guide.

This robust test architecture ensures mise's reliability across its complex feature set, including tool management, environment configuration, task execution, and multi-platform support.

For deeper understanding of specific subsystems:

**Examples:**

Example 1 (rust):
```rust
pub trait Backend: Debug + Send + Sync {
    async fn list_remote_versions(&self) -> Result<Vec<String>>;
    async fn install_version(&self, ctx: &InstallContext, tv: &ToolVersion) -> Result<()>;
    async fn uninstall_version(&self, tv: &ToolVersion) -> Result<()>;
    // ... additional methods for lifecycle management
}
```

Example 2 (rust):
```rust
pub trait ConfigFile: Debug + Send + Sync {
    fn get_path(&self) -> &Path;
    fn to_tool_request_set(&self) -> Result<ToolRequestSet>;
    fn env_entries(&self) -> Result<Vec<EnvDirective>>;
    fn tasks(&self) -> Vec<&Task>;
    // ... additional configuration methods
}
```

Example 3 (rust):
```rust
pub trait Plugin: Debug + Send {
    fn name(&self) -> &str;
    fn path(&self) -> PathBuf;
    async fn install(&self, config: &Arc<Config>, pr: &Box<dyn SingleReport>) -> Result<()>;
    async fn update(&self, pr: &Box<dyn SingleReport>, gitref: Option<String>) -> Result<()>;
    // ... lifecycle management methods
}
```

Example 4 (rust):
```rust
pub trait Shell {
    fn activate(&self, opts: ActivateOptions) -> String;
    fn set_env(&self, k: &str, v: &str) -> String;
    fn unset_env(&self, k: &str) -> String;
    // ... shell-specific methods
}
```

---

## Hooks experimental ​

**URL:** https://mise.jdx.dev/hooks.html

**Contents:**
- Hooks experimental ​
- CD hook ​
- Enter hook ​
- Leave hook ​
- Preinstall/postinstall hook ​
- Tool-level postinstall ​
- Watch files hook ​
- Hook execution ​
- Shell hooks ​
- Multiple hooks syntax ​

You can have mise automatically execute scripts during a mise activate session. You cannot use these without the mise activate shell hook installed in your shell—except the preinstall and postinstall hooks. The configuration goes into mise.toml.

This hook is run anytimes the directory is changed.

This hook is run when the project is entered. Changing directories while in the project will not trigger this hook again.

This hook is run when the project is left. Changing directories while in the project will not trigger this hook.

These hooks are run before and after tools are installed (respectively). Unlike other hooks, these hooks do not require mise activate.

The postinstall hook receives a MISE_INSTALLED_TOOLS environment variable containing a JSON array of the tools that were just installed:

Individual tools can define their own postinstall scripts using the postinstall option. These run immediately after each tool is installed (before other tools in the same session are installed):

Tool-level postinstall scripts receive the following environment variables:

While using mise activate you can have mise watch files for changes and execute a script when a file changes.

This hook will have the following environment variables set:

Hooks are executed with the following environment variables set:

Hooks can be executed in the current shell, for example if you'd like to add bash completions when entering a directory:

I feel this should be obvious but in case it's not, this isn't going to do any sort of cleanup when you leave the directory like using [env] does in mise.toml. You're literally just executing shell code when you enter the directory which mise has no way to track at all. I don't think there is a solution to this problem and it's likely the reason direnv has never implemented something similar.

I think in most situations this is probably fine, though worth keeping in mind.

You can use arrays to define multiple hooks in the same file:

**Examples:**

Example 1 (json):
```json
[hooks]
cd = "echo 'I changed directories'"
```

Example 2 (json):
```json
[hooks]
enter = "echo 'I entered the project'"
```

Example 3 (json):
```json
[hooks]
leave = "echo 'I left the project'"
```

Example 4 (json):
```json
[hooks]
preinstall = "echo 'I am about to install tools'"
postinstall = "echo 'I just installed tools'"
```

---

## Environment Plugin Development ​

**URL:** https://mise.jdx.dev/env-plugin-development.html

**Contents:**
- Environment Plugin Development ​
- Quick Start ​
- Plugin Structure ​
  - metadata.lua ​
  - hooks/mise_env.lua ​
  - hooks/mise_path.lua ​
- Context Object ​
- Configuration in mise.toml ​
- Complete Example: Secret Manager Plugin ​
- Available Lua Modules ​

Environment plugins are a special type of mise plugin that provide environment variables and PATH modifications without managing tool versions. They're ideal for integrating external services, managing secrets, and standardizing environment configuration across teams.

Unlike tool plugins and backend plugins, environment plugins:

The fastest way to create an environment plugin is to use the mise-env-plugin-template:

Environment plugins are implemented in Lua (version 5.1 at the moment). A minimal environment plugin has this structure:

The metadata.lua file defines your plugin's basic information:

The MiseEnv hook returns environment variables to set:

Return value: Either a simple array of env keys, or a table with caching metadata.

Simple format - array of tables, each with:

Extended format - table with:

Example using extended format with caching:

When cacheable = true, mise will cache the environment variables and only re-execute the plugin when:

The MisePath hook returns directories to add to PATH (optional):

Return value: Array of strings (directory paths)

Both hooks receive a ctx parameter with:

For environment plugins, ctx.options is the primary way to accept user configuration.

Users configure environment plugins using the env._ directive:

Simple activation with no options:

With configuration options:

All fields in the TOML table are passed to your hooks as ctx.options.

Here's a complete example of a plugin that fetches secrets from an external service:

Environment plugins have access to mise's built-in Lua modules:

See Plugin Lua Modules for complete documentation.

For plugins that fetch data from external services, use mise's built-in caching by returning the extended format with cacheable = true:

This is preferred over manual caching because:

Plugin not found: Make sure you've installed/linked the plugin:

Hook not executing: Enable debug logging:

Options not passed: Verify TOML syntax in mise.toml:

Once your environment plugin is ready:

See Plugin Publishing for detailed instructions.

If you have an existing tool plugin that only sets environment variables, you can simplify it to an environment-only plugin:

Before (tool plugin with unused hooks):

After (environment plugin):

**Examples:**

Example 1 (markdown):
```markdown
# Clone the template
git clone https://github.com/jdx/mise-env-sample my-env-plugin
cd my-env-plugin

# Customize for your use case
# Edit metadata.lua, hooks/mise_env.lua, hooks/mise_path.lua
```

Example 2 (unknown):
```unknown
my-env-plugin/
├── metadata.lua           # Plugin metadata
└── hooks/
    ├── mise_env.lua      # Returns environment variables (required)
    └── mise_path.lua     # Returns PATH entries (optional)
```

Example 3 (yaml):
```yaml
PLUGIN = {}

--- Plugin name (required)
PLUGIN.name = "my-env-plugin"

--- Plugin version (required)
PLUGIN.version = "1.0.0"

--- Plugin description (required)
PLUGIN.description = "Provides environment variables for my service"

--- Plugin homepage (optional)
PLUGIN.homepage = "https://github.com/username/my-env-plugin"

--- Plugin license (optional)
PLUGIN.license = "MIT"

--- Minimum mise/vfox version required (optional)
PLUGIN.minRuntimeVersion = "0.3.0"
```

Example 4 (sql):
```sql
function PLUGIN:MiseEnv(ctx)
    -- Access configuration from mise.toml via ctx.options
    local api_url = ctx.options.api_url or "https://api.example.com"
    local debug = ctx.options.debug or false

    -- Return array of environment variables
    return {
        {
            key = "API_URL",
            value = api_url
        },
        {
            key = "DEBUG",
            value = tostring(debug)
        },
        {
            key = "SERVICE_TOKEN",
            value = get_token_from_somewhere()  -- Your custom logic
        }
    }
end
```

---

## Paranoid ​

**URL:** https://mise.jdx.dev/paranoid.html

**Contents:**
- Paranoid ​
- Config files ​
- Community plugins ​
- Always uses HTTPS ​
- More? ​

Paranoid is an optional behavior that locks mise down more to make it harder for a bad actor to compromise your system. These are settings that I personally do not use on my own system because I find the behavior too restrictive for the benefits.

Paranoid mode can be enabled with either MISE_PARANOID=1 or a setting:

Normally mise will make sure some config files are "trusted" before loading them. This will prompt you to confirm that you want to load the file, e.g.:

Generally only potentially dangerous config files are checked such as files that use templates (which can execute arbitrary code) or that set env vars. Under paranoid, however, all config files must be trusted first.

Also, in normal mode, a config file only needs to be trusted a single time. In paranoid, the contents of the file are hashed to check if the file changes. If you change your config file, you'll need to trust it again.

Note that global and system config files (e.g., ~/.config/mise/config.toml) are implicitly trusted and exempt from this check. This allows paranoid mode to be enabled in a global config without requiring a trust prompt for that file itself.

Community plugins can not be directly installed via short-name under paranoid. You can install plugins that are either core, maintained by the mise team, or plugins that mise has marked as "first-party"—meaning plugins developed by the same team that builds the tool the plugin installs.

Other than that, say for "shfmt", you'll need to specify the full git repo to install:

Unlike in normal mode where mise plugin install shfmt would be sufficient.

Some endpoints in mise are fetched over HTTP such as checking for the latest mise version and pulling version lists of tools. These are not security risks and a malicious actor injecting false data would not introduce a security risk. Normally mise uses HTTP because loading the TLS module takes about 10ms and this affects commonly used commands so it is a noticeably delay. In paranoid mode, all endpoints will be fetched over HTTPS.

If you have suggestions for more that could be added to paranoid, please let me know.

**Examples:**

Example 1 (unknown):
```unknown
mise settings paranoid=1
```

Example 2 (unknown):
```unknown
$ mise install
mise ~/src/mise/.tool-versions is not trusted. Trust it [y/n]?
```

Example 3 (unknown):
```unknown
mise plugin install shfmt https://github.com/luizm/asdf-shfmt
```

---

## Core Tools ​

**URL:** https://mise.jdx.dev/core-tools.html

**Contents:**
- Core Tools ​

mise comes with some plugins built into the CLI written in Rust. These are new and will improve over time.

They can be easily overridden by installing an asdf/vfox plugin with the same name, e.g.: mise plugin install python https://github.com/asdf-community/asdf-python.

You can see the core plugins with mise registry -b core.

---

## URL Replacements ​

**URL:** https://mise.jdx.dev/url-replacements.html

**Contents:**
- URL Replacements ​
- Configuration Examples ​
- Simple Hostname Replacement ​
- Advanced Regex Replacement ​
  - Regex Examples ​
    - 1. Protocol Conversion (HTTP to HTTPS) ​
    - 2. GitHub Release Mirroring with Path Restructuring ​
    - 3. Subdomain to Path Conversion ​
    - 4. Multiple Replacement Patterns (processed in order) ​
- Use Cases ​

mise does not include a built-in registry for downloading artifacts. Instead, it retrieves remote registry manifests, which specify the URLs for downloading tools.

In some environments — such as enterprises or DMZs — these URLs may not be directly accessible and must be accessed through a proxy or internal mirror.

URL replacements allow you to modify or redirect any URL that mise attempts to access, making it possible to use internal proxies, mirrors, or alternative sources as needed.

In mise.toml (single line):

In mise.toml (multiline):

For simple hostname-based mirroring, the key is the original hostname/domain to replace, and the value is the replacement string. The replacement happens by searching and replacing the pattern anywhere in the full URL string (including protocol, hostname, path, and query parameters).

See Security Considerations for important warnings about credential handling.

For more complex URL transformations, you can use regex patterns. When a key starts with regex:, it is treated as a regular expression pattern that can match and transform any part of the URL. The value can use capture groups from the regex pattern.

This converts any HTTP URL to HTTPS by capturing everything after "http://" and replacing it with "https://".

Transforms https://github.com/owner/repo/releases/download/v1.0.0/file.tar.gz to https://hub.example.com/artifactory/github/owner/repo/v1.0.0/file.tar.gz

Converts subdomain-based URLs to path-based URLs on a unified CDN.

First regex catches Microsoft repositories specifically, second catches all other GitHub URLs, and the simple replacement handles HashiCorp.

mise uses Rust regex engine which supports:

You can check on regex101.com if your regex works (see example). Full regex syntax documentation: https://docs.rs/regex/latest/regex/#syntax

When using regex patterns, ensure your replacement URLs point to trusted sources, as this feature can redirect tool downloads to arbitrary locations.

Credential Leaking: When using url_replacements, any authentication headers (like Authorization: Bearer <TOKEN>) generated for the original URL (e.g., api.github.com) are preserved and sent to the replaced URL.

This is by design to allow authentication with internal proxies that forward requests to upstream services (GitHub, GitLab, Forgejo, etc.). However, it means you must only replace URLs with trusted servers. Redirecting to an untrusted server will leak your credentials to that server.

Best Practice: Use the ^ anchor in your regex patterns to ensure you are matching the start of the URL.

Bad: "regex:github\\.com" (matches evil-github.com) Good: "regex:^https://github\\.com" (only matches actual GitHub URLs)

URL replacements can be used with ~/.netrc (or ~/_netrc on Windows) to authenticate with the replaced URL. Replacements are applied before the netrc lookup, so you should use the hostname of the replaced URL in your netrc file.

For example, if you have this in mise.toml:

Credentials from .netrc take precedence over and will overwrite any default authentication headers (such as those from MISE_GITHUB_TOKEN or other environment variables).

You should have this in ~/.netrc:

**Examples:**

Example 1 (json):
```json
[settings]
url_replacements = { "example.com" = "mirror.example.com" }
```

Example 2 (json):
```json
[settings.url_replacements]
"example.com" = "mirror.example.com"
"releases.hashicorp.com" = "hashicorp.example.com"
```

Example 3 (json):
```json
[settings.url_replacements]
"regex:^http://(.+)" = "https://$1"
"regex:^https://github\\.com/([^/]+)/([^/]+)/releases/download/(.+)" = "https://hub.example.com/artifactory/github/$1/$2/$3"
```

Example 4 (json):
```json
[settings]
url_replacements = {
  "regex:^http://(.+)" = "https://$1"
}
```

---

## Tool Plugin Development ​

**URL:** https://mise.jdx.dev/tool-plugin-development.html

**Contents:**
- Tool Plugin Development ​
- What are Tool Plugins? ​
- Plugin Architecture ​
- Hook Functions ​
  - Required Hooks ​
    - Available Hook ​
      - Rolling Releases ​
    - PreInstall Hook ​
    - EnvKeys Hook ​
  - Optional Hooks ​

Tool plugins use a hook-based architecture to manage individual tools. They are compatible with the standard vfox ecosystem and are perfect for tools that need complex installation logic, environment configuration, or legacy file parsing.

Tool plugins use traditional hook functions to manage a single tool. They provide:

Tool plugins are implemented in Lua (version 5.1 at the moment). They use a hook-based architecture with specific functions for different lifecycle events:

These hooks must be implemented for a functional plugin:

Lists all available versions of the tool:

For tools that have rolling releases like "nightly" or "stable" where the version string stays the same but the content changes, you can mark versions as rolling and provide a checksum for update detection:

When rolling = true is set:

The checksum should be the SHA256 hash of the release asset for the user's platform. See the vfox-neovim plugin for a complete example.

Handles pre-installation logic and returns download information:

Configures environment variables for the installed tool:

These hooks provide additional functionality:

Performs additional setup after installation:

Modifies version before use:

Parses version files from other tools:

The easiest way to create a new tool plugin is to use the mise-tool-plugin-template repository as a starting point:

The template includes:

Create a directory with this structure (or use the template above):

Configure plugin metadata and legacy file support:

Create shared functions in the lib/ directory:

Here's a complete example based on the vfox-nodejs plugin that demonstrates all the concepts:

If you're using the template repository, you can run the included tests:

Use debug mode to see detailed plugin execution:

Create a comprehensive test script:

Always provide meaningful error messages:

Handle different operating systems properly using the RUNTIME object:

Note: The RUNTIME object is automatically available in all plugin hooks and provides:

Normalize versions consistently:

Cache expensive operations:

Different installation logic based on platform or version:

For plugins that need to compile from source:

Complex environment variable setup:

**Examples:**

Example 1 (json):
```json
-- hooks/available.lua
function PLUGIN:Available(ctx)
    local args = ctx.args  -- User arguments

    -- Return array of available versions
    return {
        {
            version = "20.0.0",
            note = "Latest"
        },
        {
            version = "18.18.0",
            note = "LTS",
            addition = {
                {
                    name = "npm",
                    version = "9.8.1"
                }
            }
        }
    }
end
```

Example 2 (json):
```json
function PLUGIN:Available(ctx)
    return {
        {
            version = "nightly",
            note = "Latest development build",
            rolling = true,  -- Mark as rolling release
            checksum = "abc123..."  -- SHA256 of the release asset
        },
        {
            version = "stable",
            note = "Latest stable release",
            rolling = true,
            checksum = "def456..."
        },
        {
            version = "1.0.0",
            note = "Fixed release"
            -- No rolling or checksum needed for fixed versions
        }
    }
end
```

Example 3 (typescript):
```typescript
-- hooks/pre_install.lua
function PLUGIN:PreInstall(ctx)
    local version = ctx.version
    local runtimeVersion = ctx.runtimeVersion

    -- Determine download URL and checksums
    local url = "https://nodejs.org/dist/v" .. version .. "/node-v" .. version .. "-linux-x64.tar.gz"

    return {
        version = version,
        url = url,
        sha256 = "abc123...",  -- Optional checksum
        note = "Installing Node.js " .. version,
        -- Optional attestation metadata, choose a verification type
        attestation = {
            -- GitHub
            github_owner = "ownername"
            github_repo = "reponame"
            -- Cosign
            cosign_sig_or_bundle_path = "/path/to/sig/or/bundle/file"
            -- SLSA
            slsa_provenance_path = "/path/to/provenance/file"
        },
        -- Additional files can be specified
        addition = {
            {
                name = "npm",
                url = "https://registry.npmjs.org/npm/-/npm-" .. npm_version .. ".tgz"
            }
        }
    }
end
```

Example 4 (json):
```json
-- hooks/env_keys.lua
function PLUGIN:EnvKeys(ctx)
    local mainPath = ctx.path
    local runtimeVersion = ctx.runtimeVersion
    local sdkInfo = ctx.sdkInfo['nodejs']
    local path = sdkInfo.path
    local version = sdkInfo.version
    local name = sdkInfo.name

    return {
        {
            key = "NODE_HOME",
            value = mainPath
        },
        {
            key = "PATH",
            value = mainPath .. "/bin"
        },
        -- Multiple PATH entries are automatically merged
        {
            key = "PATH",
            value = mainPath .. "/lib/node_modules/.bin"
        }
    }
end
```

---

## Templates ​

**URL:** https://mise.jdx.dev/templates.html

**Contents:**
- Templates ​
- Example ​
- Template Rendering ​
  - Tera Filters ​
  - Tera Functions ​
  - Tera Tests ​
- Mise Template Features ​
  - Variables ​
  - Functions ​
    - Tera Built-In Functions ​

Templates in mise provide a powerful way to configure different aspects of your environment and project settings.

A template is a string that contains variables, expressions, and control structures. When rendered, the template engine (tera) replaces the variables with their values.

You can define and use templates in the following locations:

Here is an example of a mise.toml file that uses templates:

You will find more examples in the cookbook.

Mise uses tera to provide the template feature. In the template, there are 3 kinds of delimiters:

Additionally, use raw block to skip rendering tera delimiters:

This will become Hello {{name}}.

Tera supports literals, including:

You can render a variable by using the {{ name }}. For complex attributes, use:

Tera also supports powerful expressions:

Tera also supports control structures such as if and for. Read more.

You can modify variables using filters. You can filter a variable by a pipe symbol (|) and may have named arguments in parentheses. You can also chain multiple filters. e.g. {{ "Doctor Who" | lower | replace(from="doctor", to="Dr.") }} will output Dr. who.

Functions provide additional features to templates.

You can also uses tests to examine variables.

Mise provides additional variables, functions, filters, and tests on top of tera features.

Mise exposes several variables. These variables offer key information about the current environment:

In task run scripts, mise also exposes a usage map when the task has a usage specification (see Task Arguments):

The keys are the argument/flag names as written in the usage spec. If the name contains -, use bracket access, e.g. {{ usage["dry-run"] }}. Examples:

Tera offers many built-in functions. [] indicates an optional function argument. Some functions:

Tera offers more functions. Read more on tera documentation.

Mise offers a slew of useful functions in addition to tera's built-ins.

These functions are available in all tasks, and will always behave the same way regardless of the task definition they are used in. In other words, their return values are consistent across task definition(s).

These functions are task-specific and behave differently depending on the task they are used in. In other words, their return values may (but are not guaranteed to) be consistent across executions of any given task, and should be expected to be inconsisent across different task definition(s).

For example, task_source_files() returns a different set of filepaths depending on the sources of the task it's called from.

The exec function supports the following options:

Tera offers many built-in filters. [] indicates an optional filter argument. Some filters:

Tera offers more filters. Read more on tera documentation.

For example, you can use split(), concat(), and join_path filters to construct a file path:

Tera offers many built-in tests. Some tests:

Tera offers more tests. Read more on tera documentation.

Mise offers additional tests:

**Examples:**

Example 1 (json):
```json
[env]
PROJECT_NAME = "{{ cwd | basename }}"
TERRAFORM_VERSION = "1.0.0"

[tools]
# refers to env variable defined in this file
terraform = "{{ env.TERRAFORM_VERSION }}"
# refers to external env variable
node = "{{ get_env(name='NODE_VERSION', default='20') }}"
```

Example 2 (json):
```json
{% raw %}
  Hello {{ name }}
{% endraw %}
```

Example 3 (json):
```json
{% if my_number is not odd %}
  Even
{% endif %}
```

Example 4 (json):
```json
[tasks.deploy]
usage = '''
arg "<environment>" help="Target environment"
flag "-v --verbose" help="Enable verbose output"
arg "[tags]" var=#true
'''
run = '''
echo "env={{ usage.environment }}"
echo "verbose={{ usage.verbose }}"
echo "tag count={{ usage.tags | length }}"
{% for tag in usage.tags %}
  echo "tag={{ tag }}"
{% endfor %}
'''
```

---

## Directory Structure ​

**URL:** https://mise.jdx.dev/directories.html

**Contents:**
- Directory Structure ​
- ~/.config/mise ​
- ~/.cache/mise ​
- ~/.local/state/mise ​
- ~/.local/share/mise ​
  - ~/.local/share/mise/downloads ​
  - ~/.local/share/mise/plugins ​
  - ~/.local/share/mise/installs ​
  - ~/.local/share/mise/shims ​

The following are the directories that mise uses.

If you often find yourself using these directories (as I do), I suggest setting all of them to ~/.mise for easy access.

This directory stores the global configuration file ~/.config/mise/config.toml. This is intended to go into your dotfiles repo to share across machines.

Stores internal cache that mise uses for things like the list of all available versions of a plugin. Do not share this across machines. You may delete this directory any time mise isn't actively installing something. Do this with mise cache clear. See Cache Behavior for more information.

Used for storing state local to the machine such as which config files are trusted. These should not be shared across machines.

This is the main directory that mise uses and is where plugins and tools are installed into. It is nearly identical to ~/.asdf in asdf, so much so that you may be able to get by symlinking these together and using asdf and mise simultaneously. (Supporting this isn't a project goal, however).

This directory could be shared across machines but only if they run the same OS/arch. In general I wouldn't advise doing so.

This is where plugins may optionally cache downloaded assets such as tarballs. Use the always_keep_downloads setting to prevent mise from removing files from here.

mise installs plugins to this directory when running mise plugins install. If you are working on a plugin, I suggest symlinking it manually by running:

This is where tools are installed to when running mise install. For example, mise install node@20.0.0 will install to ~/.local/share/mise/installs/node/20.0.0

This will also create other symlinks to this directory for version prefixes ("20" and "20.15") and matching aliases ("lts", "latest"). For example:

You can set the MISE_INSTALLS_DIR environment variable to override this location.

This is where mise places shims. Generally these are used for IDE integration or if mise activate does not work for some reason.

**Examples:**

Example 1 (unknown):
```unknown
ln -s ~/src/mise-my-tool ~/.local/share/mise/plugins/my-tool
```

Example 2 (php):
```php
$ tree ~/.local/share/mise/installs/node
20 -> ./20.15.0
20.15 -> ./20.15.0
lts -> ./20.15.0
latest -> ./20.15.0
```

---

## Model Context Protocol (MCP) ​

**URL:** https://mise.jdx.dev/mcp.html

**Contents:**
- Model Context Protocol (MCP) ​
- Overview ​
- Usage ​
- Available Resources ​
  - mise://tools ​
  - mise://tasks ​
  - mise://env ​
  - mise://config ​
- Available Tools ​
  - install_tool ​

The Model Context Protocol (MCP) is a standard protocol that enables AI assistants to interact with development tools and access project context. Mise provides an MCP server that allows AI assistants to query information about your development environment.

When you run mise mcp, it starts a server that AI assistants can connect to and query information about your mise-managed development environment. The server communicates over stdin/stdout using JSON-RPC protocol.

The MCP feature is experimental and requires enabling experimental features with MISE_EXPERIMENTAL=1.

The MCP server is typically launched by AI assistants automatically, but you can also run it manually for testing:

The MCP server exposes the following read-only resources that AI assistants can query:

Lists all tools managed by mise in your project, including:

Shows all available mise tasks with:

Displays environment variables defined in your mise configuration:

Provides information about mise configuration:

The following tools are available for AI assistants to call (currently stubbed for future implementation):

Install a specific tool version (not yet implemented)

Execute a mise task (not yet implemented)

To use mise with Claude Desktop, add the following to your Claude configuration file:

macOS: ~/Library/Application Support/Claude/claude_desktop_config.jsonWindows: %APPDATA%\Claude\claude_desktop_config.jsonLinux: ~/.config/claude/claude_desktop_config.json

After adding this configuration and restarting Claude Desktop, the assistant will be able to:

The MCP server uses standard JSON-RPC 2.0 over stdio, making it compatible with any AI assistant that supports the Model Context Protocol. Consult your AI assistant's documentation for specific integration instructions.

When integrated with an AI assistant, you can ask questions like:

The AI assistant will query the MCP server to provide accurate, up-to-date information about your development environment.

The MCP server implementation can be found in src/cli/mcp.rs. It implements the ServerHandler trait from the rmcp crate to handle:

For more information about the Model Context Protocol, visit the official MCP documentation.

**Examples:**

Example 1 (markdown):
```markdown
# Enable experimental features
export MISE_EXPERIMENTAL=1

# Start the MCP server (it will wait for JSON-RPC input on stdin)
mise mcp
```

Example 2 (json):
```json
{
  "mcpServers": {
    "mise": {
      "command": "mise",
      "args": ["mcp"],
      "env": {
        "MISE_EXPERIMENTAL": "1"
      }
    }
  }
}
```

---

## Cache Behavior ​

**URL:** https://mise.jdx.dev/cache-behavior.html

**Contents:**
- Cache Behavior ​
- Plugin/Runtime Cache ​
- Cache auto-pruning ​

mise makes use of caching in many places in order to be efficient. The details about how long to keep cache for should eventually all be configurable. There may be gaps in the current behavior where things are hardcoded, but I'm happy to add more settings to cover whatever config is needed.

Below I explain the behavior it uses around caching. If you're seeing behavior where things don't appear to be updating, this is a good place to start.

Each plugin has a cache that's stored in ~/$MISE_CACHE_DIR/<PLUGIN>. It stores the list of versions available for that plugin (mise ls-remote <PLUGIN>), the idiomatic filenames (see below), the list of aliases, the bin directories within each runtime installation, and the result of running exec-env after the runtime was installed.

Remote versions are updated daily by default. The file is zlib messagepack, if you want to view it you can run the following (requires msgpack-cli).

Note that the caching of exec-env may be problematic if the script isn't simply exporting static values. The vast majority of exec-env scripts only export static values, but if you're working with a plugin that has a dynamic exec-env submit a ticket and we can try to figure out what to do.

Caching exec-env massively improved the performance of mise since it requires calling bash every time mise is initialized. Ideally, we can keep this behavior.

mise will automatically delete old files in its cache directory (configured with cache_prune_age). Much of the contents are also ignored by mise if they are >24 hours old or a few days. For this reason, it's likely wasteful to store this directory in CI jobs.

**Examples:**

Example 1 (php):
```php
cat ~/$MISE_CACHE_DIR/node/remote_versions.msgpack.z | perl -e 'use Compress::Raw::Zlib;my $d=new Compress::Raw::Zlib::Inflate();my $o;undef $/;$d->inflate(<>,$o);print $o;' | msgpack-cli decode
```

---

## Tips & Tricks ​

**URL:** https://mise.jdx.dev/tips-and-tricks.html

**Contents:**
- Tips & Tricks ​
- macOS Rosetta ​
- Shebang ​
- Bootstrap script ​
- Installation via zsh zinit ​
- CI/CD ​
  - GitHub Actions ​
- mise set ​
- mise run shorthand ​
- Software verification ​

An assortment of helpful tips for using mise.

If you have a need to run tools as x86_64 on Apple Silicon, this can be done with mise however you'll currently need to use the x86_64 version of mise itself. A common reason for doing this is to support compiling node <=14.

You can do this either with the MISE_ARCH setting or by using a dedicated rosetta mise bin as described below:

First, you'll need a copy of mise that's built for x86_64:

If ~/.local/bin is not in PATH, you'll need to prefix all commands with ~/.local/bin/mise-x64.

Now you can use mise-x64 to install tools:

You can specify a tool and its version in a shebang without needing to first set up a mise.toml/.tool-versions config:

This can also be useful in environments where mise isn't activated (such as a non-interactive session).

You can download the https://mise.run script to use in a project bootstrap script:

This file contains checksums so it's more secure to commit it into your project rather than calling curl https://mise.run dynamically—though of course this means it will only fetch the version of mise that was current when the script was created.

Zinit is a plugin manager for ZSH, which this snippet you will get mise (and usage for shell completion):

Using mise in CI/CD is a great way to synchronize tool versions for dev/build.

mise is pretty easy to use without an action:

Or you can use the custom action jdx/mise-action:

Instead of manually editing mise.toml to add env vars, you can use mise set instead:

As long as the task name doesn't conflict with a mise-provided command you can skip the run part:

Don't do this inside of scripts because mise may add a command in a future version and could conflict with your task.

mise provides native software verification for aqua tools without requiring external dependencies. For aqua tools, Cosign/Minisign signatures, SLSA provenance, and GitHub attestations are verified automatically using mise's built-in implementation.

For other verification needs (like GPG), you can install additional tools:

To configure aqua verification (all enabled by default):

Use mise up --bump to upgrade all software to the latest version and update mise.toml files. This keeps the same semver range as before, so if you had node = "22" and node 24 is the latest, mise up --bump node will change mise.toml to node = "24".

cargo-binstall is sort of like ubi but specific to rust tools. It fetches binaries for cargo releases. mise will use this automatically for cargo: tools if it is installed so if you use cargo: you should add this to make mise i go much faster.

mise caches things for obvious reasons but sometimes you want it to use fresh data (maybe it's not noticing a new release). Run mise cache clear to remove the cache which basically just run rm -rf ~/.cache/mise/*.

mise en is a great alternative to mise activate if you don't want to always be using mise for some reason. It sets up the mise environment in your current directory but doesn't keep running and updating the env vars after that.

Auto-install tools when entering a project by adding the following to mise.toml:

Get information about what backend a tool is using and other information with mise tool [TOOL]:

List the config files mise is reading in a particular directory with mise cfg:

This is helpful figuring out which order the config files are loaded in to figure out which one is overriding.

If you enable experimental mode, mise will update mise.lock with full versions and tarball checksums (if supported by the backend). These can be updated with mise up. You need to manually create the lockfile, then mise will add the tools to it:

The lockfile uses a consolidated format with [tools.name.assets] sections to organize asset information under each tool. Asset information includes checksums, file sizes, and optional download URLs. Legacy lockfiles with separate [tools.name.checksums] and [tools.name.sizes] sections are automatically migrated to the new format.

Note that at least currently mise needs to actually install the tool to get the tarball checksum (otherwise it would need to download the tarball just to get the checksum of it since normally that gets deleted). So you may need to run something like mise uninstall --all first in order to have it reinstall everything. It will store the full versions even if it doesn't know the checksum though so it'll still lock the version just not have a checksum to go with it.

When you use a lockfile (mise.lock), mise stores the exact download URLs for each tool asset. This means that after the initial install, future mise install runs will use the URLs from the lockfile instead of making API calls to GitHub (or other providers). This has several benefits:

This is especially useful in CI/CD or when working in environments with strict network or authentication requirements.

**Examples:**

Example 1 (unknown):
```unknown
$ curl https://mise.run | MISE_INSTALL_PATH=~/.local/bin/mise-x64 MISE_INSTALL_ARCH=x64 sh
$ ~/.local/bin/mise-x64 --version
mise 2024.x.x
```

Example 2 (python):
```python
mise-x64 use -g node@20
```

Example 3 (javascript):
```javascript
#!/usr/bin/env -S mise x node@20 -- node
// "env -S" allows multiple arguments in a shebang
console.log(`Running node: ${process.version}`);
```

Example 4 (unknown):
```unknown
curl https://mise.run > setup-mise.sh
chmod +x setup-mise.sh
./setup-mise.sh
```

---
