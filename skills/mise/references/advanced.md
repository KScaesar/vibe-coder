# Mise - Advanced

**Pages:** 11

---

## Mise + Node.js Cookbook ​

**URL:** https://mise.jdx.dev/mise-cookbook/nodejs.html

**Contents:**
- Mise + Node.js Cookbook ​
- Getting started with Node.js ​
- Add node modules binaries to the PATH ​
- Example Node.js Project ​
- Example with pnpm ​

Here are some tips on managing Node.js projects with mise.

To install Node.JS, in a directory, you can use the following command:

This will install the latest version of Node.js and create a mise.toml file with the following content:

If you want to install Node.JS globally instead (for example, node v24), you can use the following command:

When installing Node.js packages specified in package.json, you typically need to use npx or the full path to the binary. For example:

Thanks to mise, you can add the node modules binaries to the PATH. This will make CLIs installed with npm available without npx.

This example uses pnpm as the package manager. This will skip installing dependencies if the lock file hasn't changed.

With this setup, getting started in a NodeJS project is as simple as running mise dev:

**Examples:**

Example 1 (unknown):
```unknown
mise use node
```

Example 2 (unknown):
```unknown
node = "latest"
```

Example 3 (python):
```python
mise use -g node@24
```

Example 4 (unknown):
```unknown
npm install --save eslint
eslint --version # doesn't work
npx eslint --version # works
```

---

## Mise + C++ Cookbook ​

**URL:** https://mise.jdx.dev/mise-cookbook/cpp.html

**Contents:**
- Mise + C++ Cookbook ​
- A C++ Project with CMake ​

Here are some tips on managing C++ projects with mise.

**Examples:**

Example 1 (bash):
```bash
min_version = "2024.9.5"

[env]
# Project information
PROJECT_NAME = "{{ config_root | basename }}"

# Build directory
BUILD_DIR = "{{ config_root }}/build"

[tools]
# Install CMake and make
cmake = "latest"
make = "latest"

[tasks.configure]
description = "Configure the project"
run = "mkdir -p $BUILD_DIR && cd $BUILD_DIR && cmake .."

[tasks.build]
description = "Build the project"
alias = "b"
run = "cd $BUILD_DIR && make"

[tasks.clean]
description = "Clean the build directory"
alias = "c"
run = "rm -rf $BUILD_DIR"

[tasks.run]
alias = "r"
description = "Run the application"
run = "$BUILD_DIR/bin/$PROJECT_NAME"

[tasks.info]
description = "Print project information"
run = '''
echo "Project: $PROJECT_NAME"
echo "Build Directory: $BUILD_DIR"
'''
```

---

## Mise + Ruby Cookbook ​

**URL:** https://mise.jdx.dev/mise-cookbook/ruby.html

**Contents:**
- Mise + Ruby Cookbook ​
- A Ruby on Rails Project ​

Here are some tips on managing Ruby projects with mise.

**Examples:**

Example 1 (julia):
```julia
min_version = "2024.9.5"

[env]
# Project information
PROJECT_NAME = "{{ config_root | basename }}"

[tools]
# Install Ruby with the specified version
ruby = "{{ get_env(name='RUBY_VERSION', default='3.3.3') }}"

[tasks."bundle:install"]
description = "Install gem dependencies"
run = "bundle install"

[tasks.server]
description = "Start the Rails server"
alias = "s"
run = "rails server"

[tasks.test]
description = "Run tests"
alias = "t"
run = "rails test"

[tasks.lint]
description = "Run lint using Rubocop"
alias = "l"
run = "rubocop"
```

---

## Shell tricks ​

**URL:** https://mise.jdx.dev/mise-cookbook/shell-tricks.html

**Contents:**
- Shell tricks ​
- Prompt colouring ​
- Current configuration environment in powerline-go prompt ​
- Inspect what changed after mise hook ​

A collection of shell utities leveraging mise.

In ZSH to set the prompt colour whenever mise updates the environment (e.g. on cd into a project, or due to modification of the .mise*.toml):

Now, when mise makes any updates to the environment the prompt will go blue.

powerline-go's shell-var segment can be used to display the value of an environment variable in the prompt. The current mise configuration environment, MISE_ENV is a good candidate for this.

Mostly, it is as one would expect: include shell-var in -modules, and -shell-var MISE_ENV -shell-var-no-warn-empty in arguments, and make sure MISE_ENV is exported so powerline-go can "see" it.

A gotcha as of February 2025 is that the shell-var module does not tolerate unset (as opposed to empty) environment variables. To work around this, set MISE_ENV to an empty value early in the shell startup scripts, and avoid manually unseting it. For example for bash, typically in ~/.bashrc:

Using record-query you can inspect the __MISE_DIFF and __MISE_SESSION variables to see what's changing in your environment due to the mise hook.

**Examples:**

Example 1 (json):
```json
# activate mise like normal
source <(command mise activate zsh)

typeset -i _mise_updated

# replace default mise hook
function _mise_hook {
  local diff=${__MISE_DIFF}
  source <(command mise hook-env -s zsh)
  [[ ${diff} == ${__MISE_DIFF} ]]
  _mise_updated=$?
}

_PROMPT="❱ "  # or _PROMPT=${PROMPT} to keep the default

function _prompt {
  if (( ${_mise_updated} )); then
    PROMPT='%F{blue}${_PROMPT}%f'
  else
    PROMPT='%(?.%F{green}${_PROMPT}%f.%F{red}${_PROMPT}%f)'
  fi
}

add-zsh-hook precmd _prompt
```

Example 2 (unknown):
```unknown
export MISE_ENV=
```

Example 3 (json):
```json
[tools]
"cargo:record-query" = "latest"
```

Example 4 (swift):
```swift
function mise_parse_env {
  rq -m < <(
    zcat -q < <(
      printf $'\x1f\x8b\x08\x00\x00\x00\x00\x00'
      base64 -d <<< "$1"
    )
  )
}
```

---

## Cookbook ​

**URL:** https://mise.jdx.dev/mise-cookbook/

**Contents:**
- Cookbook ​
- Contributing ​

Here we are sharing a few mise setups that other people have found useful.

Finally, here is how to create presets and some shell tricks you might find useful.

If you would like to share your setup, please share it in this cookbook thread.

---

## Mise + Terraform/Opentofu Cookbook ​

**URL:** https://mise.jdx.dev/mise-cookbook/terraform.html

**Contents:**
- Mise + Terraform/Opentofu Cookbook ​
- Managing terraform/opentofu Projects ​

Here are some tips on managing Terraform projects with mise.

It is often necessary to have your terraform configuration in a terraform/ subdirectory. This necessitates the use of syntax like terraform -chdir=terraform plan to use appropriate terraform command. The following config allows you to invoke all of them from mise, leveraging mise tasks.

**Examples:**

Example 1 (json):
```json
[tools]
terraform = "1"

[tasks."terraform:init"]
description = "Initializes a Terraform working directory"
run = "terraform -chdir=terraform init"

[tasks."terraform:plan"]
description = "Generates an execution plan for Terraform"
run = "terraform -chdir=terraform plan"

[tasks."terraform:apply"]
description = "Applies the changes required to reach the desired state of the configuration"
run = "terraform -chdir=terraform apply"

[tasks."terraform:destroy"]
description = "Destroy Terraform-managed infrastructure"
run = "terraform -chdir=terraform destroy"

[tasks."terraform:validate"]
description = "Validates the Terraform files"
run = "terraform -chdir=terraform validate"

[tasks."terraform:format"]
description = "Formats the Terraform files"
run = "terraform -chdir=terraform fmt"

[tasks."terraform:check"]
description = "Checks the Terraform files"
depends = ["terraform:format", "terraform:validate"]

[env]
_.file = ".env"
```

---

## Mise + Neovim Cookbook ​

**URL:** https://mise.jdx.dev/mise-cookbook/neovim.html

**Contents:**
- Mise + Neovim Cookbook ​
- Syntax highlighting ​
  - Run commands ​
  - MISE and USAGE comments in file tasks ​
- Enable LSP for embedded lang in run commands ​

Here are some tips for an improved mise workflow with Neovim.

Use Treesitter to enable syntax highlighting for the code in the run commands of your mise files. See the example here on the left side of the image:

In your neovim config, create a after/queries/toml/injections.scm file with these queries:

To only apply the highlighting on mise files instead of all toml files, the is-mise? predicate is used. If you don't care for this distinction, the lines containing (#is-mise?) can be removed. Otherwise, make sure to also create the predicate somewhere in your neovim config.

For example, using lazy.nvim:

This will consider any toml file containing mise in its name as a mise file.

You can also use Treesitter to enable syntax highlighting for "#MISE and #USAGE comments in file based tasks. See the example here on the left side of the image:

In your neovim config, create a after/queries/bash/injections.scm file with these queries:

The same queries work as is for all languages that use # as a comment delimiter. Due to TS injections being per language, you need to put the same queries to the language specific query files. For example, put them to after/queries/python/injections.scm to enable them for Python in addition to bash.

For languages that use // as a comment delimiter, you need to modify the queries a bit:

Use otter.nvim to enable LSP features and code completion for code embedded in your mise files.

Again using lazy.nvim:

This will only work if the TS injection queries are also set up.

**Examples:**

Example 1 (julia):
```julia
; extends

(pair
  (bare_key) @key (#eq? @key "run")
  (string) @injection.content @injection.language

  (#is-mise?)
  (#match? @injection.language "^['\"]{3}\n*#!(/\\w+)+/env\\s+\\w+") ; multiline shebang using env
  (#gsub! @injection.language "^.*#!/.*/env%s+([^%s]+).*" "%1") ; extract lang
  (#offset! @injection.content 0 3 0 -3) ; rm quotes
)

(pair
  (bare_key) @key (#eq? @key "run")
  (string) @injection.content @injection.language

  (#is-mise?)
  (#match? @injection.language "^['\"]{3}\n*#!(/\\w+)+\s*\n") ; multiline shebang
  (#gsub! @injection.language "^.*#!/.*/([^/%s]+).*" "%1") ; extract lang
  (#offset! @injection.content 0 3 0 -3) ; rm quotes
)

(pair
  (bare_key) @key (#eq? @key "run")
  (string) @injection.content

  (#is-mise?)
  (#match? @injection.content "^['\"]{3}\n*.*") ; multiline
  (#not-match? @injection.content "^['\"]{3}\n*#!") ; no shebang
  (#offset! @injection.content 0 3 0 -3) ; rm quotes
  (#set! injection.language "bash") ; default to bash
)

(pair
  (bare_key) @key (#eq? @key "run")
  (string) @injection.content

  (#is-mise?)
  (#not-match? @injection.content "^['\"]{3}") ; not multiline
  (#offset! @injection.content 0 1 0 -1) ; rm quotes
  (#set! injection.language "bash") ; default to bash
)
```

Example 2 (json):
```json
{
  "nvim-treesitter/nvim-treesitter",
  init = function()
    require("vim.treesitter.query").add_predicate("is-mise?", function(_, _, bufnr, _)
      local filepath = vim.api.nvim_buf_get_name(tonumber(bufnr) or 0)
      local filename = vim.fn.fnamemodify(filepath, ":t")
      return string.match(filename, ".*mise.*%.toml$") ~= nil
    end, { force = true, all = false })
  end,
},
```

Example 3 (python):
```python
; extends

; ============================================================================
; #MISE comments - TOML injection
; ============================================================================
; This injection captures comment lines starting with "#MISE " or "#[MISE]" or
; "# [MISE]" and treats them as TOML code blocks for syntax highlighting.
;
; #MISE format
; The (#offset!) directive skips the "#MISE " prefix (6 characters) from the source
((comment) @injection.content
  (#lua-match? @injection.content "^#MISE ")
  (#offset! @injection.content 0 6 0 1)
  (#set! injection.language "toml"))

; #[MISE] format
((comment) @injection.content
  (#lua-match? @injection.content "^#%[MISE%] ")
  (#offset! @injection.content 0 8 0 1)
  (#set! injection.language "toml"))

; # [MISE] format
((comment) @injection.content
  (#lua-match? @injection.content "^# %[MISE%] ")
  (#offset! @injection.content 0 9 0 1)
  (#set! injection.language "toml"))

; ============================================================================
; #USAGE comments - KDL injection
; ============================================================================
; This injection captures consecutive comment lines starting with "#USAGE " or
; "#[USAGE]" or "# [USAGE]" and treats them as a single KDL code block for
; syntax highlighting.
;
; #USAGE format
((comment) @injection.content
  (#lua-match? @injection.content "^#USAGE ")
  ; Extend the range one byte to the right, to include the trailing newline.
  ; see https://github.com/neovim/neovim/discussions/36669#discussioncomment-15054154
  (#offset! @injection.content 0 7 0 1)
  (#set! injection.combined)
  (#set! injection.language "kdl"))

; #[USAGE] format
((comment) @injection.content
  (#lua-match? @injection.content "^#%[USAGE%] ")
  (#offset! @injection.content 0 9 0 1)
  (#set! injection.combined)
  (#set! injection.language "kdl"))

; # [USAGE] format
((comment) @injection.content
  (#lua-match? @injection.content "^# %[USAGE%] ")
  (#offset! @injection.content 0 10 0 1)
  (#set! injection.combined)
  (#set! injection.language "kdl"))

; NOTE: on neovim >= 0.12, you can use the multi node pattern instead of
; combining injections:
;
; ((comment)+ @injection.content
;   (#lua-match? @injection.content "^#USAGE ")
;   (#offset! @injection.content 0 7 0 1)
;   (#set! injection.language "kdl"))
;
; this is the preferred way as combined injections have multiple
; limitations:
; https://github.com/neovim/neovim/issues/32635
```

Example 4 (python):
```python
((comment) @injection.content
  (#lua-match? @injection.content "^//MISE ")
  (#offset! @injection.content 0 7 0 1)
  (#set! injection.language "toml"))
((comment) @injection.content
  (#lua-match? @injection.content "^//%[MISE%] ")
  (#offset! @injection.content 0 9 0 1)
  (#set! injection.language "toml"))
((comment) @injection.content
  (#lua-match? @injection.content "^// %[MISE%] ")
  (#offset! @injection.content 0 10 0 1)
  (#set! injection.language "toml"))
((comment) @injection.content
  (#lua-match? @injection.content "^//USAGE ")
  (#offset! @injection.content 0 8 0 1)
  (#set! injection.combined)
  (#set! injection.language "kdl"))
((comment) @injection.content
  (#lua-match? @injection.content "^//%[USAGE%] ")
  (#offset! @injection.content 0 10 0 1)
  (#set! injection.combined)
  (#set! injection.language "kdl"))
((comment) @injection.content
  (#lua-match? @injection.content "^// %[USAGE%] ")
  (#offset! @injection.content 0 11 0 1)
  (#set! injection.combined)
  (#set! injection.language "kdl"))
```

---

## FAQs ​

**URL:** https://mise.jdx.dev/faq.html

**Contents:**
- FAQs ​
- I don't want to put a mise.toml/.tool-versions file into my project since git shows it as an untracked file ​
- What is the difference between "nodejs" and "node" (or "golang" and "go")? ​
- What does mise activate do? ​
- Windows support? ​
- How do I use mise with http proxies? ​
- How do the shorthand plugin names map to repositories? ​
- Does "node@20" mean the newest available version of node? ​
- How do I migrate from asdf? ​
- How compatible is mise with asdf? ​

Use mise.local.toml and put that into your global gitignore file. This file should never be committed.

If you really want to use a mise.toml or .tool-versions, here are 3 ways to make git ignore these files:

These are aliased. For example, mise use nodejs@14.0 is the same as mise install node@14.0. This means it is not possible to have these be different plugins.

This is for convenience so you don't need to remember which one is the "official" name. However if something with the aliasing is acting up, submit a ticket or just stick to using "node" and "go". Under the hood, when mise reads a config file or takes CLI input it will swap out "nodejs" and "golang".

It registers a shell hook to run mise hook-env every time the shell prompt is displayed. mise hook-env checks the current env vars (most importantly PATH but there are others like GOROOT or JAVA_HOME for some tools) and adds/removes/updates the ones that have changed.

For example, if you cd into a different directory that has java 18 instead of java 17 specified, just before the next prompt is displayed the shell runs: eval "$(mise hook-env)" which will execute something like this in the current shell session:

In reality updating PATH is a bit more complex than that because it also needs to remove java-17, but you get the idea.

You may think that is excessive to run mise hook-env every time the prompt is displayed and it should only run on cd, however there are plenty of situations where it needs to run without the directory changing, for example if .tool-versions or mise.toml was just edited in the current shell.

Because it runs on prompt display, if you attempt to use mise activate in a non-interactive session (like a bash script), it will never call mise hook-env and in effect will never modify PATH because it never displays a prompt. For this type of setup, you can either call mise hook-env manually every time you wish to update PATH, or use shims instead (preferred). Or if you only need to use mise for certain commands, just prefix the commands with mise x --. For example, mise x -- npm test or mise x -- ./my_script.sh.

mise hook-env will exit early in different situations if no changes have been made. This prevents adding latency to your shell prompt every time you run a command. You can run mise hook-env yourself to see what it outputs, however it is likely nothing if you're in a shell that has already been activated.

mise activate also creates a shell function (in most shells) called mise. This is a trick that makes it possible for mise shell and mise deactivate to work without wrapping them in eval "$(mise shell)".

While mise runs great in WSL, native Windows is also supported, though via the use of shims until someone adds powershell support.

As you'll need to use shims, this means you won't have environment variables from mise.toml unless you run mise via mise x or mise run—though that's actually how I use mise on my mac so for me that's my preferred workflow anyway.

Short answer: just set http_proxy and https_proxy environment variables. These should be lowercase.

This may not work with all plugins if they are not configured to use these env vars. If you're having a proxy-related issue installing something specific you should post an issue on the plugin's repository.

e.g.: how does mise plugin install elixir know to fetch https://github.com/asdf-vm/asdf-elixir?

We maintain an index of shorthands that mise uses as a base. This is regularly updated every time that mise has a release. This repository is stored directly into the codebase in registry.toml.

It depends on the command. Normally, for most commands and inside of config files, "node@20" will point to the latest installed version of node-20.x. You can find this version by running mise latest --installed node@20 or by seeing what the ~/.local/share/mise/installs/node/20 symlink points to:

There are some exceptions to this, such as the following:

These will use the latest available version of node-20.x. This generally makes sense because you wouldn't want to install a version that is already installed.

Note that mise does not consider ~/.tool-versions files to be a global config file like asdf does. mise uses a ~/.config/mise/config.toml file for global configuration.

Here is an example script you can use to migrate your global .tool-versions file to mise:

Once you are comfortable with mise, you can remove the .tool-versions.bak file and uninstall asdf

mise should be able to read/install any .tool-versions file used by asdf. Any asdf plugin should be usable in mise. The commands in mise are slightly different, such as mise install node@20.0.0 vs asdf install node 20.0.0—this is done so multiple tools can be specified at once. However, asdf-style syntax is still supported: (mise install node 20.0.0). This is the case for most commands, though the help for the command may say that asdf-style syntax is supported. When in doubt, just try asdf syntax and see if it works—it probably does.

UPDATE (2025-01-01): mise was designed to be compatible with the asdf written in bash (<=0.15). The new asdf written in go (>=0.16) has commands mise does not support like asdf set. mise set is an existing command that is completely different than asdf set—in mise that sets env vars.

This isn't important for usability reasons so much as making it so plugins continue to work that call asdf commands inside of the plugin code.

Using commands like mise use may output .tool-versions files that are not compatible with asdf, such as using fuzzy versions. You can set --pin or MISE_PIN=1 to make mise use output asdf-compatible versions in .tool-versions. Alternatively, you can have mise.toml and .tool-versions sitting side-by-side. mise.toml tools will override tools defined in a .tool-versions in the same directory.

That said, in general compatibility with asdf is no longer a design goal. It's long been the case that there is no reason to prefer asdf to mise so users should migrate. While plenty of users have teams which use both in tandem, issues with such a setup are unlikely to be prioritized.

mise uses console.rs which honors the clicolors spec:

Providing a secure supply chain is incredibly important. mise already provides a more secure experience when compared to asdf. Security-oriented evaluations and contributions are welcome. We also urge users to look after the plugins they use, and urge plugin authors to look after the users they serve.

For more details see SECURITY.md.

usage (https://usage.jdx.dev/) is a spec and CLI for defining CLI tools.

Arguments, flags, environment variables, and config files can all be defined in a Usage spec. It can be thought of like OpenAPI (swagger) for CLIs.

usage can be installed with mise using mise use -g usage and is required to get the autocompletion working. See autocompletion.

You can leverage usage in file tasks to get auto-completion working, see file tasks arguments.

pitchfork (https://pitchfork.jdx.dev/) is a process manager for developers.

It handles daemon management with features like automatic restarts on failure, smart readiness checks, shell-based auto-start/stop when entering project directories, and cron-style scheduling for periodic tasks.

In VSCode, many extensions will throw an "error spawn EINVAL" due to a Node.js security fix.

You can change windows_shim_mode to hardlink or symlink

mise uses Calver versioning (2024.1.0). Breaking changes will be few but when they do happen, they will be communicated in the CLI with plenty of notice whenever possible.

Rather than have SemVer major releases to communicate change in large releases, new functionality and changes can be opted-into with settings like experimental = true. This way plugin authors and users can test out new functionality immediately without waiting for a major release.

The numbers in Calver (YYYY.MM.RELEASE) simply represent the date of the release—not compatibility or how many new features were added. Each release will be small and incremental.

**Examples:**

Example 1 (bash):
```bash
export JAVA_HOME=$HOME/.local/share/installs/java/18
export PATH=$HOME/.local/share/installs/java/18/bin:$PATH
```

Example 2 (json):
```json
$ ls -l ~/.local/share/mise/installs/node/20
[...] /home/jdx/.local/share/mise/installs/node/20 -> node-v20.0.0-linux-x64
```

Example 3 (unknown):
```unknown
mv ~/.tool-versions ~/.tool-versions.bak
cat ~/.tool-versions.bak | tr -s ' ' | tr ' ' '@' | xargs -n2 mise use -g
```

---

## Mise + Python Cookbook ​

**URL:** https://mise.jdx.dev/mise-cookbook/python.html

**Contents:**
- Mise + Python Cookbook ​
- A Python Project with virtualenv ​
- mise + uv ​
  - Syncing python versions installed by mise and uv ​
  - uv scripts ​

Here are some tips on managing Python projects with mise.

Here is an example python project with a requirements.txt file.

If you are using a uv project initialized with uv init ., here is how you can use it with mise.

Here is how the uv project will look like:

If you run uv run main.py in the uv project, uv will automatically create a virtual environment for you using the python version specified in the .python-version file. This will also create a uv.lock file.

mise will detect the python version in .python-version, however, it won't use the virtual env created by uv by default. So, using which python will show a global python installation from mise.

If you want mise to use the virtual environment created by uv, you can set the python.uv_venv_auto setting to true in your mise.toml file.

Using which python will now show the python version from the virtual environment created by uv.

Another option is to use _.python.venv in your mise.toml file to specify the path to the virtual environment created by uv.

You can use mise sync python --uv to sync the python version installed by mise with the python version specified in the .python-version file in the uv project.

You can take advantage of uv run in shebang in toml or file tasks. Note that using --script is required if the filename does not end in .py.

Here is an example toml task:

You can then run it with mise run print_peps:

**Examples:**

Example 1 (bash):
```bash
min_version = "2024.9.5"

[env]
# Use the project name derived from the current directory
PROJECT_NAME = "{{ config_root | basename }}"

# Automatic virtualenv activation
_.python.venv = { path = ".venv", create = true }

[tools]
python = "{{ get_env(name='PYTHON_VERSION', default='3.11') }}"
ruff = "latest"

[tasks.install]
description = "Install dependencies"
alias = "i"
run = "uv pip install -r requirements.txt"

[tasks.run]
description = "Run the application"
run = "python app.py"

[tasks.test]
description = "Run tests"
run = "pytest tests/"

[tasks.lint]
description = "Lint the code"
run = "ruff src/"

[tasks.info]
description = "Print project information"
run = '''
echo "Project: $PROJECT_NAME"
echo "Virtual Environment: $VIRTUAL_ENV"
'''
```

Example 2 (markdown):
```markdown
.
├── .gitignore
├── .python-version
├── main.py
├── pyproject.toml
└── README.md

cat .python-version
# 3.12
```

Example 3 (markdown):
```markdown
mise i
which python
# ~/.local/share/mise/installs/python/3.12.4/bin/python
```

Example 4 (json):
```json
[settings]
python.uv_venv_auto = true
```

---

## Presets ​

**URL:** https://mise.jdx.dev/mise-cookbook/presets.html

**Contents:**
- Presets ​
- Example python preset ​

You can create your own presets by leveraging mise tasks to reduce boilerplate and make it easier to set up new projects.

Here is an example of how to create your python preset that creates a mise.toml file to work with python and pdm

Then in any directory, you can run mise preset:pdm 3.10 to scaffold a new project with python and pdm:

Here is the generated mise.toml file:

**Examples:**

Example 1 (unknown):
```unknown
#!/usr/bin/env bash
#MISE dir="{{cwd}}"

mise use pre-commit
mise config set env._.python.venv.path .venv
mise config set env._.python.venv.create true -t bool
mise tasks add lint -- pre-commit run -a
```

Example 2 (typescript):
```typescript
#!/usr/bin/env bash
#MISE dir="{{cwd}}"
#MISE depends=["preset:python"]
#USAGE arg "<version>"

mise use python@${usage_version?}
mise use pdm@latest
mise config set hooks.postinstall "pdm sync"
```

Example 3 (julia):
```julia
cd my-project
mise preset:pdm 3.10
# [preset:python] $ ~/.config/mise/tasks/preset/python
# mise WARN  No untrusted config files found.
# mise ~/my-project/mise.toml tools: pre-commit@4.0.1
# [preset:pdm] $ ~/.config/mise/tasks/preset/pdm 3.10
# mise WARN  No untrusted config files found.
# mise ~/my-project/mise.toml tools: python@3.10.15
# mise ~/my-project/mise.toml tools: pdm@2.21.0
# mise creating venv with uv at: ~/my-project/.venv
# Using CPython 3.10.15 interpreter at: /Users/simon/.local/share/mise/installs/python/3.10.15/bin/python
# Creating virtual environment at: .venv
# Activate with: source .venv/bin/activate.fish

~/my-project via 🐍 v3.10.15 (.venv)
# we are in the virtual environment ^
```

Example 4 (json):
```json
[tools]
pdm = "latest"
pre-commit = "latest"
python = "3.10"

[hooks]
postinstall = "pdm sync"

[env]
[env._]
[env._.python]
[env._.python.venv]
path = ".venv"
create = true

[tasks.lint]
run = "pre-commit run -a"
```

---

## Mise + Docker Cookbook ​

**URL:** https://mise.jdx.dev/mise-cookbook/docker.html

**Contents:**
- Mise + Docker Cookbook ​
- Docker image with mise ​
- Task to run mise in a Docker container ​

Here are some tips on using Docker with mise.

Here is an example Dockerfile showing how to install mise in a Docker image.

Build and run the Docker image:

This can be useful use if you need to reproduce an issue you're having with mise in a clean environment.

**Examples:**

Example 1 (sql):
```sql
FROM debian:12-slim

RUN apt-get update  \
    && apt-get -y --no-install-recommends install  \
        # install any other dependencies you might need
        sudo curl git ca-certificates build-essential \
    && rm -rf /var/lib/apt/lists/*

SHELL ["/bin/bash", "-o", "pipefail", "-c"]
ENV MISE_DATA_DIR="/mise"
ENV MISE_CONFIG_DIR="/mise"
ENV MISE_CACHE_DIR="/mise/cache"
ENV MISE_INSTALL_PATH="/usr/local/bin/mise"
ENV PATH="/mise/shims:$PATH"
# ENV MISE_VERSION="..."

RUN curl https://mise.run | sh
```

Example 2 (unknown):
```unknown
docker build -t debian-mise .
docker run -it --rm debian-mise
```

Example 3 (json):
```json
[tasks.docker]
run = "docker run --pull=always -it --rm --entrypoint bash jdxcode/mise:latest"
```

Example 4 (sql):
```sql
❯ mise docker
[docker] $ docker run --pull=always -it --rm --entrypoint bash jdxcode/mise:latest
# latest: Pulling from jdxcode/mise
# Digest: sha256:eecc479b6259479ffca5a4f9c68dbfe8631ca62dc59aa60c9ab5e4f6e9982701
# Status: Image is up to date for jdxcode/mise:latest
root@75f179a190a1:/mise# eval "$(mise activate bash)"
# overwrite configuration and prune to give us a clean state
root@75f179a190a1:/mise# echo "" >/mise/config.toml
root@75f179a190a1:/mise# mise prune --yes
# mise pruned configuration links
# mise python@3.13.1 ✓ remove /mise/cache/python/3.13.1
# ...
```

---
