# Mise - Plugins

**Pages:** 6

---

## mise plugins uninstall ​

**URL:** https://mise.jdx.dev/cli/plugins/uninstall.html

**Contents:**
- mise plugins uninstall ​
- Arguments ​
  - [PLUGIN]… ​
- Flags ​
  - -a --all ​
  - -p --purge ​

Also remove the plugin's installs, downloads, and cache

**Examples:**

Example 1 (unknown):
```unknown
mise uninstall node
```

---

## mise plugins ls-remote ​

**URL:** https://mise.jdx.dev/cli/plugins/ls-remote.html

**Contents:**
- mise plugins ls-remote ​
- Flags ​
  - -u --urls ​
  - --only-names ​

List all available remote plugins

The full list is here: https://github.com/jdx/mise/blob/main/registry.toml

Show the git url for each plugin e.g.: https://github.com/mise-plugins/mise-poetry.git

Only show the name of each plugin by default it will show a "*" next to installed plugins

**Examples:**

Example 1 (unknown):
```unknown
mise plugins ls-remote
```

---

## mise plugins ls ​

**URL:** https://mise.jdx.dev/cli/plugins/ls.html

**Contents:**
- mise plugins ls ​
- Flags ​
  - -u --urls ​

List installed plugins

Can also show remotely available plugins to install.

Show the git url for each plugin e.g.: https://github.com/asdf-vm/asdf-nodejs.git

**Examples:**

Example 1 (unknown):
```unknown
$ mise plugins ls
node
ruby

$ mise plugins ls --urls
node    https://github.com/asdf-vm/asdf-nodejs.git
ruby    https://github.com/asdf-vm/asdf-ruby.git
```

---

## mise plugins update ​

**URL:** https://mise.jdx.dev/cli/plugins/update.html

**Contents:**
- mise plugins update ​
- Arguments ​
  - [PLUGIN]… ​
- Flags ​
  - -j --jobs <JOBS> ​

Updates a plugin to the latest version

note: this updates the plugin itself, not the runtime versions

Number of jobs to run in parallel Default: 4

**Examples:**

Example 1 (sql):
```sql
mise plugins update            # update all plugins
mise plugins update node       # update only node
mise plugins update node#beta  # specify a ref
```

---

## mise plugins link ​

**URL:** https://mise.jdx.dev/cli/plugins/link.html

**Contents:**
- mise plugins link ​
- Arguments ​
  - <NAME> ​
  - [DIR] ​
- Flags ​
  - -f --force ​

Symlinks a plugin into mise

This is used for developing a plugin.

The name of the plugin e.g.: node, ruby

The local path to the plugin e.g.: ./mise-node

Overwrite existing plugin

**Examples:**

Example 1 (markdown):
```markdown
# essentially just `ln -s ./mise-node ~/.local/share/mise/plugins/node`
$ mise plugins link node ./mise-node

# infer plugin name as "node"
$ mise plugins link ./mise-node
```

---

## mise plugins install ​

**URL:** https://mise.jdx.dev/cli/plugins/install.html

**Contents:**
- mise plugins install ​
- Arguments ​
  - [NEW_PLUGIN] ​
  - [GIT_URL] ​
- Flags ​
  - -a --all ​
  - -f --force ​
  - -j --jobs <JOBS> ​
  - -v --verbose… ​

note that mise automatically can install plugins when you install a tool e.g.: mise install node@20 will autoinstall the node plugin

This behavior can be modified in ~/.config/mise/config.toml

The name of the plugin to install e.g.: node, ruby Can specify multiple plugins: mise plugins install node ruby python

The git url of the plugin

Install all missing plugins This will only install plugins that have matching shorthands. i.e.: they don't need the full git repo url

Reinstall even if plugin exists

Number of jobs to run in parallel

Show installation output

**Examples:**

Example 1 (julia):
```julia
# install the poetry via shorthand
$ mise plugins install poetry

# install the poetry plugin using a specific git url
$ mise plugins install poetry https://github.com/mise-plugins/mise-poetry.git

# install the poetry plugin using the git url only
# (poetry is inferred from the url)
$ mise plugins install https://github.com/mise-plugins/mise-poetry.git

# install the poetry plugin using a specific ref
$ mise plugins install poetry https://github.com/mise-plugins/mise-poetry.git#11d0c1e
```

---
