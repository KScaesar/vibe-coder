# Mise - Environments

**Pages:** 4

---

## Secrets ​

**URL:** https://mise.jdx.dev/environments/secrets/

**Contents:**
- Secrets ​

Use mise to manage sensitive environment variables securely. There are multiple supported approaches:

---

## Environments ​

**URL:** https://mise.jdx.dev/environments/

**Contents:**
- Environments ​
- Using environment variables ​
- Environment in tasks ​
- Lazy eval ​
- Redactions ​
  - Viewing Redacted Environment Variables ​
- Required Variables ​
  - Required Variable Behavior ​
  - Validation Behavior ​
  - Use Cases ​

Like direnv it manages environment variables for different project directories.

Use mise to specify environment variables used for different projects.

To get started, create a mise.toml file in the root of your project directory:

To clear an env var, set it to false:

You can also use the CLI to get/set env vars:

Additionally, the mise env [--json] [--dotenv] command can be used to export the environment variables in various formats (including PATH and environment variables set by tools or plugins).

Environment variables are available when using mise x|exec, or with mise r|run (i.e. with tasks):

You can of course combine them with tools:

If mise is activated, it will automatically set environment variables in the current shell session when you cd into a directory.

If you are using shims, the environment variables will be available when using the shim:

Finally, you can also use mise en to start a new shell session with the environment variables set.

It is also possible to define environment inside a task

Environment variables typically are resolved before tools—that way you can configure tool installation with environment variables. However, sometimes you want to access environment variables produced by tools. To do that, turn the value into a map with tools = true:

Variables can be redacted from the output by setting redact = true:

You can also use the redactions array to mark multiple environment variables as sensitive:

The mise env command provides flags to work with redacted variables:

Because mise may output sensitive values that could show up in CI logs you'll need to be configure your CI setup to know which values are sensitive.

For example, when using GitHub Actions, you should use ::add-mask:: to prevent secrets from appearing in logs:

Note: If you're using mise-action, it will automatically redact values marked with redact = true or matching patterns in the redactions array.

You can mark environment variables as required by setting required = true. This ensures that the variable is defined either before mise runs or in a later config file (like mise.local.toml):

You can also provide help text to guide users on how to set the variable:

When a required variable is missing, mise will show the help text in the error message to assist users.

When a variable is marked as required = true, mise validates that it is defined through one of these sources:

Required variables are useful for:

config_root is the canonical project root directory that mise uses when resolving relative paths inside configuration files. Generally, when you use relative paths in mise you're referring to this directory.

Here's some example config files and their config_root:

You can see the implementation in config_root.rs.

env._.* define special behavior for setting environment variables. (e.g.: reading env vars from a file). Since nested environment variables do not make sense, we make use of this fact by creating a key named "_" which is a TOML table for the configuration of these directives.

In mise.toml: env._.file can be used to specify a dotenv file to load.

This uses dotenvy under the hood. If you have problems with the way env._.file works, you will likely need to post an issue there, not to mise since there is not much mise can do about the way that crate works.

The env._.file directive supports:

You can set MISE_ENV_FILE=.env to automatically load dotenv files in any directory.

See secrets for ways to read encrypted files with env._.file.

PATH is treated specially. Use env._.path to add extra directories to the PATH, making any executables in those directories available in the shell without needing to type the full path:

The env._.path directive supports:

Relative paths like tools/bin or ./tools/bin are resolved against {{config_root}}. For example, with a config file at /path/to/project/.config/mise/config.toml, tools/bin resolves to /path/to/project/tools/bin.

Source an external bash script and pull exported environment variables out of it:

This must be a script that runs in bash as if it were executed like this:

The shebang will be ignored. See #1448 for a potential alternative that would work with binaries or other script languages.

The env._.source directive supports:

Plugins can provide their own env._ directives that dynamically set environment variables and modify your PATH. This is particularly useful for:

Simple plugin activation:

Plugin with configuration options:

When you use env._.<plugin-name>, mise:

The configuration options you provide (the TOML table after =) are passed to the plugin's hooks via ctx.options, allowing plugins to be configured per-project or per-environment.

The plugin could then fetch secrets from HashiCorp Vault and expose them as environment variables.

The plugin could detect the current git branch and set ENVIRONMENT=production when on main, or ENVIRONMENT=development otherwise.

See Environment Plugins in the Plugins documentation for a complete guide to creating your own environment plugins.

For a working example, see the mise-env-sample repository.

It may be necessary to use multiple env._ directives, however TOML fails with this syntax because it has 2 identical keys in a table:

For this use-case, you can optionally make [env] an array-of-tables instead by using [[env]] instead:

It works identically but you can have multiple tables.

Environment variable values can be templates, see Templates for details.

You can use the value of an environment variable in later env vars:

Of course the ordering matters when doing this.

**Examples:**

Example 1 (json):
```json
[env]
NODE_ENV = 'production'
```

Example 2 (json):
```json
[env]
NODE_ENV = false # unset a previously set NODE_ENV
```

Example 3 (markdown):
```markdown
mise set NODE_ENV=development
# mise set NODE_ENV
# development

mise set
# key       value        source
# NODE_ENV  development  mise.toml

cat mise.toml
# [env]
# NODE_ENV = 'development'

mise unset NODE_ENV
```

Example 4 (bash):
```bash
mise set MY_VAR=123
mise exec -- echo $MY_VAR
# 123
```

---

## Direct age Encryption experimental ​

**URL:** https://mise.jdx.dev/environments/secrets/age.html

**Contents:**
- Direct age Encryption experimental ​
- Quick start ​
- CLI flags ​
- Storage format ​
- Decryption identities ​
- Defaults for recipients (encryption) ​
- Settings ​
- age.identity_files
- age.key_file
- age.ssh_identity_files

Encrypt individual environment variable values directly in mise.toml using age encryption. The age tool is not required—mise has support built-in.

This is a simple method of storing encrypted environment variables directly in mise.toml. You can use it simply by running mise set --age-encrypt <key>=<value>. By default, mise will use your ssh key (~/.ssh/id_ed25519 or ~/.ssh/id_rsa) if it exists.

It's recommended to use --prompt to avoid accidentally exposing the value to your shell history. You don't have to though, you can use mise set --age-encrypt DB_PASSWORD="password123".

If no recipients are provided explicitly, mise will try defaults (see below).

Encrypted values are stored as base64 along with a format field:

mise looks for identities in this order:

Decrypted values are always marked as redacted.

If no identities are found or decryption fails, mise returns the encrypted value as-is (non-strict behavior).

When --age-encrypt is used without explicit recipients, mise attempts to derive recipients from:

If none are found, the command fails with an error asking you to provide recipients or configure settings.age.key_file.

[experimental] List of age identity files to use for decryption.

[experimental] Path to the age private key file to use for encryption/decryption.

[experimental] List of SSH identity files to use for age decryption.

If true, fail when age decryption fails (including when age is not available, the key is missing, or the key is invalid). If false, skip decryption and continue in these cases.

**Examples:**

Example 1 (markdown):
```markdown
age-keygen -o ~/.config/mise/age.txt
# Note the public key output for encryption
```

Example 2 (markdown):
```markdown
mise set --age-encrypt --prompt DB_PASSWORD
# Enter value for DB_PASSWORD: [hidden input]
```

Example 3 (json):
```json
[env]
DB_PASSWORD = { age = { value = "<base64>" } }
```

Example 4 (unknown):
```unknown
mise env  # Variables are decrypted automatically
```

---

## sops experimental ​

**URL:** https://mise.jdx.dev/environments/secrets/sops.html

**Contents:**
- sops experimental ​
- Example ​
- Encrypt with sops ​
- Environment Variables ​
- Redaction ​
  - CI masking (GitHub Actions) ​
- Settings ​
- sops.age_key
- sops.age_key_file
- sops.age_recipients

mise reads encrypted secret files and makes values available as environment variables via env._.file.

mise will automatically decrypt the file if it is sops-encrypted.

Currently age is the only sops encryption method supported.

Install tools: mise use -g sops age

Generate an age key and note the public key:

The -i overwrites the file. The encrypted file is safe to commit. Set SOPS_AGE_KEY_FILE=~/.config/mise/age.txt or MISE_SOPS_AGE_KEY_FILE=~/.config/mise/age.txt to decrypt/edit with sops.

Now mise env exposes the values.

mise supports both mise-specific environment variables and standard SOPS ones:

Mise-specific variables (highest priority):

Standard SOPS variables (fallback):

This allows you to override SOPS settings specifically for mise while keeping your standard SOPS configuration intact for other tools.

Mark secrets from files as sensitive:

Work with redacted values:

If you use mise-action, values marked redact = true are masked automatically.

The age private key to use for sops secret decryption. Takes precedence over standard SOPS_AGE_KEY environment variable.

Path to the age private key file for sops secret decryption. Takes precedence over standard SOPS_AGE_KEY_FILE environment variable.

The age public keys to use for sops secret encryption.

Use rops to decrypt sops files. Disable to shell out to sops which will slow down mise but sops may offer features not available in rops.

If true, fail when sops decryption fails (including when sops is not available, the key is missing, or the key is invalid). If false, skip decryption and continue in these cases.

**Examples:**

Example 1 (json):
```json
{
  "AWS_ACCESS_KEY_ID": "AKIAIOSFODNN7EXAMPLE",
  "AWS_SECRET_ACCESS_KEY": "wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY"
}
```

Example 2 (json):
```json
[env]
_.file = ".env.json"
```

Example 3 (jsx):
```jsx
age-keygen -o ~/.config/mise/age.txt
# Public key: <public key>
```

Example 4 (jsx):
```jsx
sops encrypt -i --age "<public key>" .env.json
```

---
