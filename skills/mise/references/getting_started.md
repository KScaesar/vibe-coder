# Mise - Getting Started

**Pages:** 8

---

## Demo ​

**URL:** https://mise.jdx.dev/demo.html

**Contents:**
- Demo ​
- Transcript ​

The following demo shows:

mise exec <tool> -- <command> allows you to run any tools with mise

node is only available in the mise environment, not globally

Here is another example where we run terraform with mise exec

mise exec is great for running one-off commands, however it can be convenient to activate mise. When activated, mise will automatically update your PATH to include the tools you have installed, making them available directly.

We will start by installing node@lts and make it the global default

Note that we get back the path to the real node here, not a shim.

We can also install other tools with mise. For example, we will install terraform, jq, and go

Let's enter a project directory where we will set up node@23

As expected, node -v is now v23.x

We will leave this directory. The node version will revert to the global LTS version

**Examples:**

Example 1 (markdown):
```markdown
mise exec node@24 -- node -v
# mise node@24.x.x ✓ installed
# v24.x.x
```

Example 2 (markdown):
```markdown
node -v
# bash: node: command not found
```

Example 3 (markdown):
```markdown
mise exec terraform -- terraform -v
# mise terraform@1.11.3 ✓ installed
# Terraform v1.11.3
```

Example 4 (markdown):
```markdown
mise use --global node@lts
# v22.14.0
```

---

## Troubleshooting ​

**URL:** https://mise.jdx.dev/troubleshooting.html

**Contents:**
- Troubleshooting ​
- mise activate doesn't work in ~/.profile, ~/.bash_profile, ~/.zprofile ​
- mise is failing or not working right ​
- The wrong version of a tool is being used ​
- New version of a tool is not available ​
- Windows problems ​
  - Path limits ​
- mise isn't working when calling from tmux or another shell initialization script ​
- Is mise secure? ​
- 403 Forbidden when installing a tool ​

mise activate should only be used in rc files. These are the interactive ones used when a real user is using the terminal. (As opposed to being executed by an IDE or something). The prompt isn't displayed in non-interactive environments so PATH won't be modified.

For non-interactive setups, consider using shims instead which will route calls to the correct directory by looking at PWD every time they're executed. You can also call mise exec instead of expecting things to be directly on PATH. You can also run mise env in a non-interactive shell, however that will only setup the global tools. It won't modify the environment variables when entering into a different project.

mise activate --shims does not support all the features of mise activate. See shims vs path for more info.

Also see the shebang example for a way to make scripts call mise to get the runtime. That is another way to use mise without activation.

First try setting MISE_DEBUG=1 or MISE_TRACE=1 and see if that gives you more information. You can also set MISE_LOG_FILE_LEVEL=debug MISE_LOG_FILE=/path/to/logfile to write logs to a file.

If something is happening with the activate hook, you can try disabling it and calling eval "$(mise hook-env)" manually. It can also be helpful to use mise env which will just output environment variables that would be set. Also consider using shims which can be more compatible.

If runtime installation isn't working right, try using the --raw flag which will install things in series and connect stdin/stdout/stderr directly to the terminal. If a plugin is trying to interact with you for some reason this will make it work.

Of course check the version of mise with mise --version and make sure it is the latest. Use mise self-update to update it. mise cache clean can be used to wipe the internal cache and mise implode can be used to remove everything except config.

Lastly, there is mise doctor which will show diagnostic information and any warnings about issues detected with your setup. If you submit a bug report, please include the output of mise doctor.

Likely this means that mise isn't first in PATH—using shims or mise activate. You can verify if this is the case by calling which -a, for example, if node@20.0.0 is being used but mise specifies node@24.0.0, first make sure that mise has this version installed and active by running mise ls node. It should not say missing and have the correct "Requested" version:

If node -v isn't showing the right version, make sure mise is activated by running mise doctor. It should not have a "problem" listed about mise not being activated. Lastly, run which -a node. If the directory listed is not a mise directory, then mise is not first in PATH. Whichever node is being run first needs to have its directory set before mise is. Typically this means setting PATH for mise shims at the end of bashrc/zshrc.

If using mise activate, you have another option of enabling MISE_ACTIVATE_AGGRESSIVE=1 which will have mise always prepend its tools to be first in PATH. If you're using something that also modifies paths dynamically like mise activate does, this may not work because the other tool may be modifying PATH after mise does.

If nothing else, you can run things with mise x -- to ensure that the correct version is being used.

There are 2 places that versions are cached so a brand new release might not appear right away.

The first is that the mise CLI caches versions for. The cache can be cleared with mise cache clear.

The second uses the https://mise-versions.jdx.dev host as a centralized place to list all of the versions of most plugins. This is intended to speed up mise and also get around GitHub rate limits when querying for new versions. Check that repo for your plugin to see if it has an updated version. This service can be disabled by setting MISE_USE_VERSIONS_HOST=0.

mise-versions itself also struggles with rate limits but you can help it to fetch more frequently by authenticating with its GitHub app. It does not require any permissions since it simply fetches public repository information. The more people do this, the quicker mise will be able to fetch new versions of tools.

Very basic support for windows is currently available, however because Windows can't support asdf plugins, they must use core and vfox only—which means only a handful of tools are available on Windows.

If you have many tools defined in your mise.toml hierarchy, then it is possible that mise x will produce a Path environment variable that is too long for certain tools to handle, most notably, cmd.exe. This will affect mise tools that invoke cmd.exe (like npm install).

You have a few options:

You can run the following command to test whether you have hit the cmd.exe Path limitation:

mise activate will not update PATH until the shell prompt is displayed. So if you need to access a tool provided by mise before the prompt is displayed you can either add the shims to your PATH e.g.

Or you can manually call hook-env:

For more information, see What does mise activate do?

Providing a secure supply chain is incredibly important. mise already provides a more secure experience when compared to asdf. Security-oriented evaluations and contributions are welcome. We also urge users to look after the plugins they use, and urge plugin authors to look after the users they serve.

For more details see SECURITY.md.

You may get an error like one of the following:

This can happen if the tool is hosted on GitHub, and you've hit the API rate limit. This is especially common running mise in a CI environment like GitHub Actions. If you don't have a GITHUB_TOKEN set, the rate limit is quite low. You can fix this by creating a GitHub token (which needs no scopes) by going to https://github.com/settings/tokens/new and setting it as an environment variable. You can use any of the following (in order of preference):

If you are expecting mise to automatically install a tool when you run a command that is not found (using the not_found_auto_install feature), be aware of an important limitation:

mise can only auto-install missing versions of tools that already have at least one version installed.

This is because mise does not have a way of knowing which binaries a tool provides unless there is already an installed (even inactive) version of that tool. If you have never installed any version of a tool, mise cannot determine which tool is responsible for a given binary name, and so it cannot auto-install it on demand.

**Examples:**

Example 1 (unknown):
```unknown
$ mise ls node
Plugin  Version  Config Source       Requested
node    24.0.0  ~/.mise/config.toml  24.0.0
```

Example 2 (yaml):
```yaml
# Path is within limits
❯ mise x -- cmd.exe /d /s /c "where.exe where"
C:\Windows\System32\where.exe
# Path exceeds cmd.exe limits
❯ mise x -- cmd.exe /d /s /c "where.exe where"
'where.exe' is not recognized as an internal or external command,
operable program or batch file.
mise ERROR command failed: exit code 1
mise ERROR Run with --verbose or MISE_VERBOSE=1 for more information
```

Example 3 (bash):
```bash
export PATH="$HOME/.local/share/mise/shims:$PATH"
python --version # will work after adding shims to PATH
```

Example 4 (unknown):
```unknown
eval "$(mise activate bash)"
eval "$(mise hook-env)"
python --version # will work only after calling hook-env explicitly
```

---

## Installing Mise ​

**URL:** https://mise.jdx.dev/installing-mise.html

**Contents:**
- Installing Mise ​
- Installation Methods ​
  - https://mise.run ​
    - Shell-specific installation + activation ​
  - apk ​
  - apt ​
  - pacman ​
  - Cargo ​
  - dnf ​
    - Fedora 41+, RHEL 9+, CentOS Stream 9+ ​

If you are new to mise, follow the Getting Started guide first.

This page lists various ways to install mise on your system.

Which methods auto-update?

Package managers (apt, dnf, brew, pacman, etc.) update mise when you update system packages. Other methods can be updated with mise self-update.

Note that it isn't necessary for mise to be on PATH. If you run the activate script in your shell's rc file, mise will automatically add itself to PATH.

For a more streamlined setup, you can use shell-specific endpoints that will install mise and automatically configure activation in your shell's configuration file:

These shell-specific installers will:

If you want to verify the install script hasn't been tampered with:

As long as you don't change the version with MISE_VERSION, the install script will be pinned to whatever the latest version was when it was downloaded with checksums inside the file. This makes downloading the file and putting it into a project a great way to ensure that anyone installing with that script fetches the exact same mise bin.

If you need something else, compile it with cargo install mise (see below).

mise lives in the community repository.

For installation on Ubuntu/Debian:

Build from source with Cargo:

Do it faster with cargo-binstall:

Build from the latest commit in main:

mise is available on npm as a precompiled binary. This isn't a Node.js package—just distributed via npm. This is useful for JS projects that want to setup mise via package.json or npx.

Use npx if you just want to test it out for a single command without fully installing:

Download the latest release from GitHub.

For the Nix package manager, at release 24.05 or later:

You can also import the package directly using mise-flake.packages.${system}.mise. It supports all default Nix systems.

NixOS compiles from source by default

For precompiled binaries, enable nix-ld and disable all_compile.

This is the recommended way to install mise on Windows. It will automatically add your shims to PATH.

chocolatey version is currently outdated.

Download the latest release from GitHub and add the binary to your PATH.

If your shell does not support mise activate, you would want to edit PATH to include the shims directory (by default: %LOCALAPPDATA%\mise\shims).

For homebrew and possibly other installs mise is automatically activated so this is not necessary.

See MISE_FISH_AUTO_ACTIVATE=1 for more information.

See about_Profiles docs to find your actual profile location. You will need to first create the parent directory if it does not exist.

Nu does not support eval Install Mise by appending env.nu and config.nu:

If you prefer to keep your dotfiles clean you can save it to a different directory then update $env.NU_LIB_DIRS:

Since .xsh files are not compiled you may shave a bit off startup time by using a pure Python import: add the code below to, for example, ~/.config/xonsh/mise.py config file and import mise it in ~/.config/xonsh/rc.xsh:

Or continue to use rc.xsh/.xonshrc:

Given that mise replaces both shell env $PATH and OS environ PATH, watch out that your configs don't have these two set differently (might throw os.environ['PATH'] = xonsh.built_ins.XSH.env.get_detyped('PATH') at the end of a config to make sure they match)

Add following to your rc.elv:

Optionally alias mise to mise:mise for seamless integration of mise {activate,deactivate,shell}:

Adding a new shell is not hard at all since very little shell code is in this project. See here for how the others are implemented. If your shell isn't currently supported I'd be happy to help you get yours integrated.

Some installation methods automatically install autocompletion scripts.

The mise completion command can generate autocompletion scripts for your shell. This requires usage to be installed. If you don't have it, install it with:

Then, run the following commands to install the completion script for your shell:

Then source your shell's rc file or restart your shell.

If you encounter issues after installation, run:

This will diagnose common problems with your mise setup. See mise doctor for more information.

Use mise implode to uninstall mise. This will remove the mise binary and all of its data. Use mise implode --help for more information.

Alternatively, manually remove the following directories to fully clean up:

**Examples:**

Example 1 (unknown):
```unknown
curl https://mise.run | sh
```

Example 2 (unknown):
```unknown
curl https://mise.run | MISE_INSTALL_PATH=/usr/local/bin/mise sh
```

Example 3 (markdown):
```markdown
curl https://mise.run/zsh | sh
# Installs mise and adds activation to ~/.zshrc
```

Example 4 (markdown):
```markdown
curl https://mise.run/bash | sh
# Installs mise and adds activation to ~/.bashrc
```

---

## IDE Integration ​

**URL:** https://mise.jdx.dev/ide-integration.html

**Contents:**
- IDE Integration ​
- Adding shims to PATH in your default shell profile ​
- IDE Plugins ​
- Vim ​
- Neovim ​
- emacs ​
  - Traditional shims way ​
  - Use with package mise.el ​
- JetBrains Editors (IntelliJ, RustRover, PyCharm, WebStorm, RubyMine, GoLand, etc) ​
  - IntelliJ Plugin ​

Code editors and IDEs work differently than interactive shells.

Usually, they will either inherit the environment from your current shell (this is the case if you start it from a terminal like nvim . or code .) or will have their own way to set up the environment.

Once you have launched the IDE, it won't reload the environment variables or the PATH provided by mise if you update your mise configuration files. Therefore, we cannot rely on the default mise activate method to automatically set up the editor.

There are a few ways to make mise work with your editor:

IDEs work better with shims than they do environment variable modifications. The simplest way is to add the mise shim directory to PATH.

For IntelliJ and VSCode—and likely others, you can modify your default shell's login (aka "profile") script. Your default shell can be found with:

You can change your default shell with chsh -s /path/to/shell but you may need to first add it to /etc/shells. Once you know the right one, modify the appropriate file:

Do not use /bin/bash or /usr/bin/bash on macOS. bash is complicated, decades old, and mise isn't able to use as many features. Unless you consider yourself an expert on bash and know why I (and Apple for that matter) admonish using bash, just use zsh on macOS.

On Linux this is read when logging into the machine, so changing it requires logging out and back in for it to work. See #vscode below for how to get VSCode to read the login file.

This assumes that mise is on PATH. If it is not, you'll need to use the absolute path ( e.g.: eval "$($HOME/.local/bin/mise activate zsh --shims)").

Here is an example showing that VSCode will use node provided by mise:

As mentioned above, using shims doesn't work with all mise features. For example, arbitrary env vars in [env] will only be set if a shim is executed. For this we need tighter integration with the IDE and/or a custom plugin.

Here are some community plugins that have been developed to work with mise:

For a better Treesitter and LSP integration, check out the neovim cookbook.

https://github.com/eki3z/mise.el

A GNU Emacs library which uses the mise tool to determine per-directory/project environment variables and then set those environment variables on a per-buffer basis.

https://github.com/134130/intellij-mise

This plugin can automatically configure the IDE to use the tools provided by mise. It has also some support for running mise tasks and loading environment variables in the run configurations.

Some JetBrains IDEs (or language plugins) have direct support for mise. This allows you to select the SDK version from the IDE settings. Example for Java:

Some plugins cannot find SDK installed by mise yet but might have support for asdf. In that case, a workaround is to symlink the mise tool directory which has same layout as asdf:

Then they should show up on in Project Settings:

Or in the case of node (possibly other languages), it's under "Languages & Frameworks":

Unlike Linux, macOS does not read the login shell profile (~/.profile, or ~/.zprofile) when logging into the machine. You'll likely want to add this setting to VSCode config in order to have it load your shims:

You can also use ["--login", "--interactive"] if you want to include ~/.zshrc.

There is a VSCode plugin which can configure other extensions for you, without having to modify your shell profile to add the shims to PATH.

In addition, it provides additional features such as:

https://github.com/hverlin/mise-vscode/ (Documentation)

While modifying your default shell profile is likely the easiest solution, you can also set the tools in launch.json:

Xcode projects can run system commands from script build phases and schemes. Since Xcode sandboxes the execution of the script using the tool /usr/bin/sandbox-exec, don't expect Mise and the automatically-activated tools to work out of the box. First, you'll need to add $(SRCROOT)/mise.toml to the list of Input files. This is necessary for Xcode to allow reads to that file. Then, you can use mise activate to activate the tools you need:

**Examples:**

Example 1 (bash):
```bash
dscl . -read /Users/$USER UserShell
```

Example 2 (bash):
```bash
getent passwd $USER | cut -d: -f7
```

Example 3 (markdown):
```markdown
# ~/.zprofile
eval "$(mise activate zsh --shims)"
```

Example 4 (markdown):
```markdown
# ~/.bash_profile or ~/.bash_login or ~/.profile
eval "$(mise activate bash --shims)"
```

---

## Getting Started ​

**URL:** https://mise.jdx.dev/getting-started.html

**Contents:**
- Getting Started ​
- 1. Install mise CLI ​
- 2. mise exec and run ​
- 3. Activate mise optional ​
- 4. Use tools from backends (npm, pipx, core, aqua, github) ​
- 5. Setting environment variables ​
- 6. Run a task ​
- 7. Next steps ​
  - Set up autocompletion ​
  - GitHub API rate limiting ​

This will show you how to install mise and get started with it. This is a suitable way when using an interactive shell like bash, zsh, or fish.

See installing mise for other ways to install mise (macport, apt, yum, nix, etc.).

By default, mise will be installed to ~/.local/bin (this is simply a suggestion. mise can be installed anywhere). You can verify the installation by running:

mise respects MISE_DATA_DIR and XDG_DATA_HOME if you'd like to change these locations.

Once mise is installed, you can immediately start using it. mise can be used to install and run tools, launch tasks, and manage environment variables.

The most essential feature mise provides is the ability to run tools with specific versions. A simple way to run a shell command with a given tool is to use mise x|exec. For example, here is how you can start a Python 3 interactive shell (REPL):

In the examples below, use ~/.local/bin/mise (or the absolute path to mise) if mise is not already on PATH

mise x|exec is a powerful way to load the current mise context (tools & environment variables) without modifying your shell session or running ad-hoc commands with mise tools set. Installing tools is as simple as running mise u|use.

Another useful command is mise r|run which allows you to run a mise task or a script with the mise context.

You can set a shell alias in your shell's rc file like alias x="mise x --" to save some keystrokes.

While using mise x|exec is useful, for interactive shells, you might prefer to activate mise to automatically load the mise context (tools and environment variables) in your shell session. Another option is to use shims.

For interactive shells, mise activate is recommended. In non-interactive sessions, like CI/CD, IDEs, and scripts, using shims might work best. You can also not use any and call mise exec/run directly instead. See this guide for more information.

Here is how you can activate mise depending on your shell and the installation method:

Make sure you restart your shell session after modifying your rc file in order for it to take effect. You can run mise dr|doctor to verify that mise is correctly installed and activated.

Now that mise is activated or its shims have been added to PATH, node is also available directly! (without using mise exec):

Note that when you ran mise use --global node@24, mise updated the global mise configuration.

Backends are ecosystems or package managers that mise uses to install tools. With mise use, you can install multiple tools from each backend.

For example, to install claude-code with the npm backend:

Install black with the pipx backend:

mise can also install tools directly from github with the github backend:

See Backends for more ecosystems and details.

You can set environment variables in mise.toml which will be set if mise is activated or if mise x|exec is used in a directory:

You can define simple tasks in mise.toml and run them with mise run:

mise tasks will automatically install all of the tools from mise.toml before running the task.

See tasks for more information on how to define and use tasks.

Follow the walkthrough for more examples on how to use mise.

See autocompletion to learn how to set up autocompletion for your shell.

Many tools in mise require the use of the GitHub API. Unauthenticated requests to the GitHub API are often rate limited. If you see 4xx errors while using mise, you can set MISE_GITHUB_TOKEN or GITHUB_TOKEN to a token generated from here which will likely fix the issue. The token does not require any scopes.

**Examples:**

Example 1 (unknown):
```unknown
curl https://mise.run | sh
```

Example 2 (markdown):
```markdown
~/.local/bin/mise --version
# mise 2024.x.x
```

Example 3 (markdown):
```markdown
mise exec python@3 -- python
# this will download and install Python if it is not already installed
# Python 3.13.2
# >>> ...
```

Example 4 (markdown):
```markdown
mise exec node@24 -- node -v
# v24.x.x
```

---

## Walkthrough ​

**URL:** https://mise.jdx.dev/walkthrough.html

**Contents:**
- Walkthrough ​
- Installing Dev Tools ​
- mise.toml Configuration ​
- Dev Tool Backends ​
- Upgrading Dev Tools ​
- Setting Environment Variables ​
- Tasks ​
- Common Commands ​
- Final Thoughts ​

Once you've completed the Getting Started guide, you're ready to start using mise. This document offers a quick overview on some initial things you may want to try out.

The main command for working with tools in mise is mise u|use. This does 2 main things:

Both of these are required to use a tool. If you simply install a tool via mise install, it won't be available in your shell. It must also be added to mise.toml—which is why I promote using mise use since it does both.

You use it like so (note that mise must be activated for this example to work):

And you'll also note that you now have a mise.toml file with the following content:

Use mise.toml to share your tool configurations with others. This file should be committed to version control and contains the common toolset needed for your project.

For tools or settings you want to keep private, use mise.local.toml. This file should be added to .gitignore and is perfect for personal preferences or configurations.

mise supports nested configuration files that cascade from broad to specific settings:

mise will use all the parent directories together to determine the set of tools—overriding configuration as it goes lower in the hierarchy.

Use mise config ls to see the configuration files currently used by mise.

In general, it's preferred to use loose versions like this in mise so that other people working on a project don't have to worry about the exact version of a tool you're using. If you'd like to pin the version to enforce a specific version, use mise use --pin or the lockfile setting.

If you leave out the version, then mise will default to node@latest.

Tools are installed with a variety of backends like asdf, ubi, or vfox. See registry for the full list of shorthands like node you can use.

You can also use other backends like npm or cargo which can install any package from their respective registries:

Upgrading tool versions can be done with mise up|upgrade. By default, it will respect the version prefix in mise.toml. If a lockfile exists, mise will update mise.lock to the latest version of the tool with the prefix from mise.toml.

So if you have node = "24" in mise.toml, then mise upgrade node will upgrade to the latest version of node 24.

If you'd like to upgrade to the latest version of node, you can use mise upgrade --bump node. It will set the version at the same specificity as the current version, so if you have node = "24", but use mise upgrade --bump node to update to node@26, then it will set node = "26" in mise.toml.

See Dev Tools for more information on working with tools.

mise can also be used to set environment variables for your project. You can set environment variables with the CLI:

Or by directly modifying mise.toml:

Some examples on where this can be used:

You can also modify PATH with mise.toml. This example makes CLIs installed with npm available:

This will add ./node_modules/.bin to the PATH for the project—with "." here referring to the directory the mise.toml file is in so if you enter a subdirectory, it will still work.

See Environments for more information on working with environment variables.

Tasks are defined in a project to execute commands.

You can define tasks in a mise.toml:

Or in a mise-tasks directory as a standalone file, such as mise-tasks/build:

Tasks are executed with mise r|run:

mise run sets up the "mise environment" before running the task (tools and environment variables). So if you'd rather not activate mise in your shell, you can use mise run to run tasks, and it will have the tools in PATH and the environment variables from mise.toml set.

mise is paired with usage which provides lots of features for documenting and running tasks.

Here is an example of a task with usage spec:

This task can be run like so:

To get the autocompletion working, set up mise autocompletions.

See Tasks for more information on working with tasks.

Since there are a lot of commands available in mise, here are what I consider the most important:

Dev tools, env vars, and tasks work together to make managing your development environment easier—especially when working with others. The goal is to have a consistent UX to interface with projects regardless of the programming languages or tools used on it.

**Examples:**

Example 1 (markdown):
```markdown
mkdir example-project && cd example-project
mise use node@24
node -v
# v24.x.x
```

Example 2 (json):
```json
[tools]
node = "24"
```

Example 3 (python):
```python
mise use npm:@antfu/ni
mise use cargo:starship
```

Example 4 (bash):
```bash
mise set MY_VAR=123
echo $MY_VAR
# 123
```

---

## Glossary ​

**URL:** https://mise.jdx.dev/glossary.html

**Contents:**
- Glossary ​
- Core Concepts ​
- Backends ​
- Shell Integration ​
- Configuration ​
- Environment Variables ​
- Hooks ​
- Tasks ​
- Directories & Environment ​
- Other Terms ​

This glossary defines key terms and concepts used throughout the mise documentation.

Activation : The process of loading mise's context (tools, environment variables, PATH modifications) into your shell session. Typically done via eval "$(mise activate bash)" in your shell rc file. See Installing mise for setup instructions.

Backend : A package manager or ecosystem that mise uses to install and manage tools. Each backend knows how to fetch, install, and manage tools from its respective source. See Backends below and Backend Architecture for details.

Core Tools : Built-in tool implementations written in Rust that ship with mise. These provide first-class support for popular languages like Node.js, Python, Ruby, Go, and others. See Core tools for the full list.

mise.toml : The primary configuration file for mise projects. Contains tool versions, environment variables, tasks, and hooks. See Configuration for the full specification.

mise.local.toml : A user-local configuration file that overrides mise.toml. Typically added to .gitignore for personal settings that shouldn't be shared with the team.

Plugin : An extension that adds functionality to mise, such as managing additional tools or setting up environment variables. See Plugins for an overview.

Registry : The collection of tool aliases that map user-friendly short names to their full backend specifications. For example, aws-cli maps to aqua:aws/aws-cli. See Registry.

Tool : A development tool or runtime that mise can install and manage, such as node, python, terraform, or jq.

Tool Request : A user's specification for a tool version, which may be fuzzy or use aliases. Examples: node@18, python@latest, go@1.21. These get resolved to concrete Tool Versions.

Tool Version : A concrete, resolved version of a tool. For example, node@18 (tool request) might resolve to node@18.19.0 (tool version).

Toolset : An immutable collection of resolved tools for a specific context, containing all the Tool Versions that should be active for a directory or project.

mise supports multiple backends for installing tools from different sources:

aqua : Backend using the aqua-proj registry. Supports SLSA provenance verification and provides access to thousands of tools. See aqua backend.

asdf : Legacy backend compatible with asdf shell-script plugins. Linux and macOS only. Slower than native backends but provides access to the asdf plugin ecosystem. See asdf backend.

cargo : Installs Rust tools by compiling them with cargo install. See cargo backend.

conda : Installs packages from Conda repositories. See conda backend.

dotnet : Installs .NET tools. See dotnet backend.

gem : Installs Ruby gems as tools. See gem backend.

github : Installs tools directly from GitHub releases. See github backend.

gitlab : Installs tools directly from GitLab releases. See gitlab backend.

go : Installs Go tools using go install. See go backend.

http : Installs tools from arbitrary HTTP/HTTPS URLs. See http backend.

npm : Installs Node.js packages and CLI tools from the npm registry. See npm backend.

pipx : Installs Python CLI tools in isolated environments using pipx. See pipx backend.

spm : Installs tools via Swift Package Manager. See spm backend.

ubi : Universal Binary Installer for tools distributed as single binaries. See ubi backend.

vfox : Backend compatible with VersionFox plugins. See vfox backend.

hook-env : The mise hook-env command that exports environment changes for shell integration. Called automatically by the shell hook installed via mise activate.

PATH Activation : The default method of shell integration where mise updates the PATH environment variable at each prompt to include the appropriate tool binaries.

Reshim : The process of updating the shims directory after tools are installed or removed. Run mise reshim if shims get out of sync.

Shims : Small executable scripts that intercept tool commands and delegate to mise, which loads the appropriate tool context before execution. An alternative to PATH activation. See Shims.

config_root : The canonical project root directory that mise uses when resolving relative paths in configuration files. Set via the MISE_PROJECT_ROOT environment variable or detected automatically.

Configuration Environments : Environment-specific configuration files like mise.dev.toml or mise.prod.toml, activated via the MISE_ENV environment variable. See Configuration Environments.

Configuration Hierarchy : The system where mise.toml files at different levels (system, global, project) are merged together, with files closer to the current directory taking precedence over parent directories.

Settings : Global mise configuration options stored in ~/.config/mise/settings.toml that define behavior across all projects. See Settings.

Templates : Dynamic values in configuration using Tera template syntax, like {{env.HOME}} or {{arch()}}. See Templates.

env._ directives : Special environment configuration directives for advanced setup:

Lazy Evaluation : Environment variables configured with tools = true that can access tool-provided environment variables. These are evaluated after tools are loaded.

Redaction : Marking sensitive environment variables with redact = true to hide their values from mise output and logs.

Hooks : Scripts that automatically execute during mise activation at specific events. An experimental feature. See Hooks.

cd hook : Runs whenever you change directories while mise is active.

enter hook : Runs when entering a directory where a mise.toml becomes active.

leave hook : Runs when leaving a directory where a mise.toml was active.

postinstall hook : Runs after a tool is successfully installed.

preinstall hook : Runs before a tool installation begins.

watch_files hook : Runs when specified files change. Requires mise activate for file watching.

Dependency Graph : A Directed Acyclic Graph (DAG) used internally to resolve task execution order based on dependencies.

File Tasks : Tasks defined as standalone executable scripts in directories like mise-tasks/ or .mise/tasks/. See File Tasks.

Task : A reusable command defined in mise.toml or as a standalone script that executes within the mise environment. See Tasks.

Task Dependencies : Relationships between tasks defined via depends (run before), depends_post (run after), or wait_for (wait but don't trigger). See Task Configuration.

TOML Tasks : Tasks defined directly in the [tasks] section of mise.toml files. See TOML Tasks.

MISE_CACHE_DIR : Directory where mise caches downloaded files and metadata. Defaults to ~/.cache/mise on Linux, ~/Library/Caches/mise on macOS.

MISE_DATA_DIR : Directory where mise stores installed tools and other persistent data. Defaults to ~/.local/share/mise.

MISE_PROJECT_ROOT : Environment variable automatically set to the root directory of the current project (where the mise.toml is located).

Aliases : Alternative names for tool versions, allowing shortcuts like lts for Node.js LTS versions. See Tool Aliases.

direnv : An external tool for environment management that mise can work alongside. See direnv integration.

mise-en-place : French culinary phrase meaning "everything in its place" - the philosophy behind mise. Chefs prepare all ingredients before cooking; developers should have all tools ready before coding.

mise.lock : A lockfile that records exact resolved versions for reproducible environments across machines and CI. See mise.lock.

Tool Options : Configuration in mise.toml that changes tool behavior, such as setting a Python virtualenv path or Node.js corepack preferences.

---

## Configuration ​

**URL:** https://mise.jdx.dev/configuration.html

**Contents:**
- Configuration ​
- mise.toml ​
- Configuration Hierarchy ​
  - How Configuration Merging Works ​
  - Configuration Resolution Process ​
  - Visual Configuration Hierarchy ​
  - Merge Behavior by Section ​
  - Target File for Write Operations ​
  - [tools] - Dev tools ​
  - [env] - Arbitrary Environment Variables ​

Learn how to configure mise for your project with mise.toml files, environment variables, and various configuration options to manage your development environment.

mise.toml is the config file for mise. They can be at any of the following file paths (in order of precedence, top overrides configuration of lower paths):

Run mise cfg to figure out what order mise is loading files on your particular setup. This is often a lot easier than figuring out mise's rules.

mise uses a sophisticated hierarchical configuration system that merges settings from multiple sources. Understanding this hierarchy helps you organize your development environments effectively.

These files recurse upwards, so if you have a ~/src/work/myproj/mise.toml file, what is defined there will override anything set in ~/src/work/mise.toml or ~/.config/mise.toml. The config contents are merged together.

When mise needs configuration, it follows this process:

Different configuration sections merge in different ways:

Tools ([tools]): Additive with overrides

Environment Variables ([env]): Additive with overrides

Tasks ([tasks]): Completely replaced per task

Settings ([settings]): Additive with overrides

Run mise config to see what files mise has loaded in order of precedence.

When commands like mise use, mise set, or mise unuse need to write to a config file, they use the lowest precedence file in the highest precedence directory. This means:

This behavior ensures that shared configuration (mise.toml) is updated by default, while local overrides (mise.local.toml) and environment-specific configs remain untouched unless explicitly targeted.

Here is what a mise.toml looks like:

mise.toml files are hierarchical. The configuration in a file in the current directory will override conflicting configuration in parent directories. For example, if ~/src/myproj/mise.toml defines the following:

And ~/src/myproj/backend/mise.toml defines:

Then when inside of ~/src/myproj/backend, node will be 18, python will be 3.10, and ruby will be 3.1. You can check the active versions with mise ls --current.

You can also have environment specific config files like .mise.production.toml, see Configuration Environments for more details.

See Tools. In addition to specifying versions, each tool entry can include options such as:

See Settings for the full list of settings.

Use [plugins] to add/modify plugin shortnames. Note that this will only modify new plugin installations. Existing plugins can use any URL.

The plugin type prefix (e.g., asdf:, vfox: or vfox-backend:) is optional. If omitted, mise will fall back to either using asdf or vfox if the URL contains vfox- in the repo name.

If you simply want to install a plugin from a specific URL once, it's better to use mise plugin install <NAME> <GIT_URL>. Add this section to mise.toml if you want to share the plugin location/revision with other developers in your project.

This is similar to MISE_SHORTHANDS but doesn't require a separate file.

[alias] has been renamed to [tool_alias] to distinguish it from [shell_alias]. The old [alias] key still works but is deprecated.

The following makes mise install node@my_custom_node install node-20.x this can also be specified in a plugin. note adding an alias will also add a symlink, in this case:

Define shell aliases that are set when entering a directory and unset when leaving:

These work similar to environment variables—they're set dynamically based on your current directory. See Shell Aliases for more details.

Specify the minimum supported version of mise required for the configuration file.

You can set a hard minimum (errors if unmet) or a soft minimum (warns and continues):

When a soft minimum is not met, mise will print a warning and (if available) show self-update instructions. When a hard minimum is not met, mise errors and shows self-update instructions.

Mark a configuration file as a monorepo root to enable target path syntax for tasks. Requires MISE_EXPERIMENTAL=1.

See Monorepo Tasks for detailed usage and examples.

mise can be configured in ~/.config/mise/config.toml. It's like local mise.toml files except that it is used for all directories.

Similar to ~/.config/mise/config.toml but for all users on the system. This is useful for setting defaults for all users.

The .tool-versions file is asdf's config file and it can be used in mise just like mise.toml. It isn't as flexible so it's recommended to use mise.toml instead. It can be useful if you already have a lot of .tool-versions files or work on a team that uses asdf.

Here is an example with all the supported syntax:

See the asdf docs for more info on this file format.

Both mise.toml and .tool-versions support "scopes" which modify the behavior of the version:

mise supports "idiomatic version files" just like asdf. They're language-specific files like .node-version and .python-version. These are ideal for setting the runtime version of a project without forcing other developers to use a specific tool like mise or asdf.

They support aliases, which means you can have an .nvmrc file with lts/hydrogen and it will work in mise and nvm. Here are some of the supported idiomatic version files:

In mise, these are disabled by default, see https://github.com/jdx/mise/discussions/4345 for rationale.

There is a performance cost to having these when they're parsed as it's performed by the plugin in bin/parse-version-file. However, these are cached so it's not a huge deal. You may not even notice.

asdf called these "legacy version files". I think this was a bad name since it implies that they shouldn't be used—which is definitely not the case IMO. I prefer the term "idiomatic" version files since they are version files not specific to asdf/mise and can be used by other tools. (.nvmrc being a notable exception, which is tied to a specific tool.)

See Settings for the full list of settings.

See Tasks for the full list of configuration options.

Normally environment variables in mise are used to set settings so most environment variables are in that doc. The following are environment variables that are not settings.

A setting in mise is generally something that can be configured either as an environment variable or set in a config file.

mise can also be configured via environment variables. The following options are available:

Default: ~/.local/share/mise or $XDG_DATA_HOME/mise

This is the directory where mise stores plugins and tool installs. These are not supposed to be shared across machines.

Default (Linux): ~/.cache/mise or $XDG_CACHE_HOME/mise Default (macOS): ~/Library/Caches/mise or $XDG_CACHE_HOME/mise

This is the directory where mise stores internal cache. This is not supposed to be shared across machines. It may be deleted at any time mise is not running.

Default: std::env::temp_dir() implementation in rust

This is used for temporary storage such as when installing tools.

This is the directory where mise stores system-wide configuration.

Default: $MISE_CONFIG_DIR/config.toml (Usually ~/.config/mise/config.toml)

This is the path to the config file.

This is the path which is used as {{config_root}} for the global config file.

Set to a filename to read from env from a dotenv file. e.g.: MISE_ENV_FILE=.env. Uses dotenvy under the hood.

Set the version for a runtime. For example, MISE_NODE_VERSION=20 will use node@20.x regardless of what is set in mise.toml/.tool-versions.

This is a list of paths that mise will automatically mark as trusted. They can be separated with :.

This is a list of paths where mise will stop searching for configuration files and file tasks. This is useful to stop mise searching for files in slow loading directories. They are separated according to platform conventions for the PATH environment variable. On most Unix platforms, the separator is : and on Windows it is ;.

These change the verbosity of mise.

You can also use MISE_DEBUG=1, MISE_TRACE=1, and MISE_QUIET=1 as well as --log-level=trace|debug|info|warn|error.

Output logs to a file.

Same as MISE_LOG_LEVEL but for the log file output level. This is useful if you want to store the logs but not have them litter your display.

Display HTTP requests/responses in the logs.

Equivalent to MISE_LOG_LEVEL=warn.

Set the timeout for http requests in seconds. The default is 30.

Set to "1" to directly pipe plugin scripts to stdin/stdout/stderr. By default stdin is disabled because when installing a bunch of plugins in parallel you won't see the prompt. Use this if a plugin accepts input or otherwise does not seem to be installing correctly.

Sets MISE_JOBS=1 because only 1 plugin script can be executed at a time.

Configures the vendor_conf.d script for fish shell to automatically activate. This file is automatically used in homebrew and potentially other installs to automatically activate mise without configuring.

Defaults to enabled, set to "0" to disable.

**Examples:**

Example 1 (typescript):
```typescript
/
├── etc/mise/                         # System-wide config (highest precedence)
│   ├── conf.d/*.toml                 # System fragments, loaded alphabetically
│   ├── config.toml                   # System defaults
│   └── config.<env>.toml             # Env-specific system config (MISE_ENV or -E)
└── home/user/
    ├── .config/mise/
    │   ├── conf.d/*.toml             # User fragments, loaded alphabetically
    │   ├── config.toml               # Global user config
    │   ├── config.<env>.toml         # Env-specific user config
    │   ├── config.local.toml         # User-local overrides
    │   └── config.<env>.local.toml   # Env-specific user-local overrides
    └── work/
        ├── mise.toml                 # Work-wide settings
        └── myproject/
            ├── mise.local.toml       # Local overrides (git-ignored)
            ├── mise.toml             # Project config
            ├── mise.<env>.toml       # Env-specific project config
            ├── mise.<env>.local.toml # Env-specific project local overrides
            └── backend/
                └── mise.toml         # Service-specific config (lowest precedence)
```

Example 2 (markdown):
```markdown
# Global: node@18, python@3.11
# Project: node@20, go@1.21
# Result: node@20, python@3.11, go@1.21
```

Example 3 (typescript):
```typescript
# Global: NODE_ENV=development
# Project: NODE_ENV=production, API_URL=localhost
# Result: NODE_ENV=production, API_URL=localhost
```

Example 4 (markdown):
```markdown
# Global: [tasks.test] = "npm test"
# Project: [tasks.test] = "yarn test"
# Result: "yarn test" (completely replaces global)
```

---
