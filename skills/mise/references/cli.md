# Mise - Cli

**Pages:** 77

---

## mise ls ​

**URL:** https://mise.jdx.dev/cli/ls.html

**Contents:**
- mise ls ​
- Arguments ​
  - [INSTALLED_TOOL]… ​
- Flags ​
  - -c --current ​
  - -g --global ​
  - -i --installed ​
  - -J --json ​
  - -l --local ​
  - -m --missing ​

List installed and active tool versions

This command lists tools that mise "knows about". These may be tools that are currently installed, or those that are in a config file (active) but may or may not be installed.

It's a useful command to get the current state of your tools.

Only show tool versions from [TOOL]

Only show tool versions currently specified in a mise.toml

Only show tool versions currently specified in the global mise.toml

Only show tool versions that are installed (Hides tools defined in mise.toml but not installed)

Output in JSON format

Only show tool versions currently specified in the local mise.toml

Display missing tool versions

Don't display headers

Display whether a version is outdated

Display versions matching this prefix

List only tools that can be pruned with mise prune

**Examples:**

Example 1 (json):
```json
$ mise ls
node    20.0.0 ~/src/myapp/.tool-versions latest
python  3.11.0 ~/.tool-versions           3.10
python  3.10.0

$ mise ls --current
node    20.0.0 ~/src/myapp/.tool-versions 20
python  3.11.0 ~/.tool-versions           3.11.0

$ mise ls --json
{
  "node": [
    {
      "version": "20.0.0",
      "install_path": "/Users/jdx/.mise/installs/node/20.0.0",
      "source": {
        "type": "mise.toml",
        "path": "/Users/jdx/mise.toml"
      }
    }
  ],
  "python": [...]
}
```

---

## mise run ​

**URL:** https://mise.jdx.dev/cli/run.html

**Contents:**
- mise run ​
- Flags ​
  - -c --continue-on-error ​
  - -C --cd <CD> ​
  - -f --force ​
  - -j --jobs <JOBS> ​
  - -n --dry-run ​
  - -o --output <OUTPUT> ​
  - -q --quiet ​
  - -r --raw ​

This command will run a task, or multiple tasks in parallel. Tasks may have dependencies on other tasks or on source files. If source is configured on a task, it will only run if the source files have changed.

Tasks can be defined in mise.toml or as standalone scripts. In mise.toml, tasks take this form:

Alternatively, tasks can be defined as standalone scripts. These must be located in mise-tasks, .mise-tasks, .mise/tasks, mise/tasks or .config/mise/tasks. The name of the script will be the name of the tasks.

Continue running tasks even if one fails

Change to this directory before executing the command

Force the tasks to run even if outputs are up to date

Number of tasks to run in parallel [default: 4] Configure with jobs config or MISE_JOBS env var

Don't actually run the task(s), just print them in order of execution

Change how tasks information is output when running tasks

Don't show extra output

Read/write directly to stdin/stdout/stderr instead of by line Redactions are not applied with this option Configure with raw config or MISE_RAW env var

Shell to use to run toml tasks

Defaults to sh -c -o errexit -o pipefail on unix, and cmd /c on Windows Can also be set with the setting MISE_UNIX_DEFAULT_INLINE_SHELL_ARGS or MISE_WINDOWS_DEFAULT_INLINE_SHELL_ARGS Or it can be overridden with the shell property on a task.

Don't show any output except for errors

Tool(s) to run in addition to what is in mise.toml files e.g.: node@20 python@3.10

Bypass the environment cache and recompute the environment

Do not use cache on remote tasks

Skip automatic dependency preparation

Hides elapsed time after each task completes

Default to always hide with MISE_TASK_TIMINGS=0

Run only the specified tasks skipping all dependencies

Timeout for the task to complete e.g.: 30s, 5m

**Examples:**

Example 1 (json):
```json
[tasks.build]
run = "npm run build"
sources = ["src/**/*.ts"]
outputs = ["dist/**/*.js"]
```

Example 2 (unknown):
```unknown
$ cat .mise/tasks/build&lt;&lt;EOF
#!/usr/bin/env bash
npm run build
EOF
$ mise run build
```

Example 3 (markdown):
```markdown
# Runs the "lint" tasks. This needs to either be defined in mise.toml
# or as a standalone script. See the project README for more information.
$ mise run lint

# Forces the "build" tasks to run even if its sources are up-to-date.
$ mise run build --force

# Run "test" with stdin/stdout/stderr all connected to the current terminal.
# This forces `--jobs=1` to prevent interleaving of output.
$ mise run test --raw

# Runs the "lint", "test", and "check" tasks in parallel.
$ mise run lint ::: test ::: check

# Execute multiple tasks each with their own arguments.
$ mise run cmd1 arg1 arg2 ::: cmd2 arg1 arg2
```

---

## mise generate task-docs ​

**URL:** https://mise.jdx.dev/cli/generate/task-docs.html

**Contents:**
- mise generate task-docs ​
- Flags ​
  - -i --inject ​
  - -I --index ​
  - -m --multi ​
  - -o --output <OUTPUT> ​
  - -r --root <ROOT> ​
  - -s --style <STYLE> ​

Generate documentation for tasks in a project

inserts the documentation into an existing file

This will look for a special comment, <!-- mise-tasks -->, and replace it with the generated documentation. It will replace everything between the comment and the next comment, <!-- /mise-tasks --> so it can be run multiple times on the same file to update the documentation.

write only an index of tasks, intended for use with --multi

render each task as a separate document, requires --output to be a directory

writes the generated docs to a file/directory

root directory to search for tasks

**Examples:**

Example 1 (unknown):
```unknown
mise generate task-docs
```

---

## mise watch ​

**URL:** https://mise.jdx.dev/cli/watch.html

**Contents:**
- mise watch ​
- Arguments ​
  - [TASK] ​
  - [ARGS]… ​
- Flags ​
  - --skip-deps ​
  - -w --watch… <PATH> ​
  - -W --watch-non-recursive… <PATH> ​
  - -F --watch-file <PATH> ​
  - -c --clear <MODE> ​

Run task(s) and watch for changes to rerun it

This command uses the watchexec tool to watch for changes to files and rerun the specified task(s). It must be installed for this command to work, but you can install it with mise use -g watchexec@latest.

For more advanced process management (daemon management, auto-restart, readiness checks, cron scheduling), see mise's sister project: https://pitchfork.jdx.dev

Tasks to run Can specify multiple tasks by separating with ::: e.g.: mise run task1 arg1 arg2 ::: task2 arg1 arg2

Task and arguments to run

Run only the specified tasks skipping all dependencies

Watch a specific file or directory

By default, Watchexec watches the current directory.

When watching a single file, it's often better to watch the containing directory instead, and filter on the filename. Some editors may replace the file with a new one when saving, and some platforms may not detect that or further changes.

Upon starting, Watchexec resolves a "project origin" from the watched paths. See the help for '--project-origin' for more information.

This option can be specified multiple times to watch multiple files or directories.

The special value '/dev/null', provided as the only path watched, will cause Watchexec to not watch any paths. Other event sources (like signals or key events) may still be used.

Watch a specific directory, non-recursively

Unlike '-w', folders watched with this option are not recursed into.

This option can be specified multiple times to watch multiple directories non-recursively.

Watch files and directories from a file

Each line in the file will be interpreted as if given to '-w'.

For more complex uses (like watching non-recursively), use the argfile capability: build a file containing command-line options and pass it to watchexec with @path/to/argfile.

The special value '-' will read from STDIN; this in incompatible with '--stdin-quit'.

Clear screen before running command

If this doesn't completely clear the screen, try '--clear=reset'.

What to do when receiving events while the command is running

Default is to 'do-nothing', which ignores events while the command is running, so that changes that occur due to the command are ignored, like compilation outputs. You can also use 'queue' which will run the command once again when the current run has finished if any events occur while it's running, or 'restart', which terminates the running command and starts a new one. Finally, there's 'signal', which only sends a signal; this can be useful with programs that can reload their configuration without a full restart.

The signal can be specified with the '--signal' option.

Restart the process if it's still running

This is a shorthand for '--on-busy-update=restart'.

Send a signal to the process when it's still running

Specify a signal to send to the process when it's still running. This implies '--on-busy-update=signal'; otherwise the signal used when that mode is 'restart' is controlled by '--stop-signal'.

See the long documentation for '--stop-signal' for syntax.

Signals are not supported on Windows at the moment, and will always be overridden to 'kill'. See '--stop-signal' for more on Windows "signals".

Signal to send to stop the command

This is used by 'restart' and 'signal' modes of '--on-busy-update' (unless '--signal' is provided). The restart behaviour is to send the signal, wait for the command to exit, and if it hasn't exited after some time (see '--timeout-stop'), forcefully terminate it.

The default on unix is "SIGTERM".

Input is parsed as a full signal name (like "SIGTERM"), a short signal name (like "TERM"), or a signal number (like "15"). All input is case-insensitive.

On Windows this option is technically supported but only supports the "KILL" event, as Watchexec cannot yet deliver other events. Windows doesn't have signals as such; instead it has termination (here called "KILL" or "STOP") and "CTRL+C", "CTRL+BREAK", and "CTRL+CLOSE" events. For portability the unix signals "SIGKILL", "SIGINT", "SIGTERM", and "SIGHUP" are respectively mapped to these.

Time to wait for the command to exit gracefully

This is used by the 'restart' mode of '--on-busy-update'. After the graceful stop signal is sent, Watchexec will wait for the command to exit. If it hasn't exited after this time, it is forcefully terminated.

Takes a unit-less value in seconds, or a time span value such as "5min 20s". Providing a unit-less value is deprecated and will warn; it will be an error in the future.

The default is 10 seconds. Set to 0 to immediately force-kill the command.

This has no practical effect on Windows as the command is always forcefully terminated; see '--stop-signal' for why.

Translate signals from the OS to signals to send to the command

Takes a pair of signal names, separated by a colon, such as "TERM:INT" to map SIGTERM to SIGINT. The first signal is the one received by watchexec, and the second is the one sent to the command. The second can be omitted to discard the first signal, such as "TERM:" to not do anything on SIGTERM.

If SIGINT or SIGTERM are mapped, then they no longer quit Watchexec. Besides making it hard to quit Watchexec itself, this is useful to send pass a Ctrl-C to the command without also terminating Watchexec and the underlying program with it, e.g. with "INT:INT".

This option can be specified multiple times to map multiple signals.

Signal syntax is case-insensitive for short names (like "TERM", "USR2") and long names (like "SIGKILL", "SIGHUP"). Signal numbers are also supported (like "15", "31"). On Windows, the forms "STOP", "CTRL+C", and "CTRL+BREAK" are also supported to receive, but Watchexec cannot yet deliver other "signals" than a STOP.

Time to wait for new events before taking action

When an event is received, Watchexec will wait for up to this amount of time before handling it (such as running the command). This is essential as what you might perceive as a single change may actually emit many events, and without this behaviour, Watchexec would run much too often. Additionally, it's not infrequent that file writes are not atomic, and each write may emit an event, so this is a good way to avoid running a command while a file is partially written.

An alternative use is to set a high value (like "30min" or longer), to save power or bandwidth on intensive tasks, like an ad-hoc backup script. In those use cases, note that every accumulated event will build up in memory.

Takes a unit-less value in milliseconds, or a time span value such as "5sec 20ms". Providing a unit-less value is deprecated and will warn; it will be an error in the future.

The default is 50 milliseconds. Setting to 0 is highly discouraged.

Exit when stdin closes

This watches the stdin file descriptor for EOF, and exits Watchexec gracefully when it is closed. This is used by some process managers to avoid leaving zombie processes around.

Don't load gitignores

Among other VCS exclude files, like for Mercurial, Subversion, Bazaar, DARCS, Fossil. Note that Watchexec will detect which of these is in use, if any, and only load the relevant files. Both global (like '~/.gitignore') and local (like '.gitignore') files are considered.

This option is useful if you want to watch files that are ignored by Git.

Don't load project-local ignores

This disables loading of project-local ignore files, like '.gitignore' or '.ignore' in the watched project. This is contrasted with '--no-vcs-ignore', which disables loading of Git and other VCS ignore files, and with '--no-global-ignore', which disables loading of global or user ignore files, like '~/.gitignore' or '~/.config/watchexec/ignore'.

Supported project ignore files:

VCS ignore files (Git, Mercurial, Bazaar, Darcs, Fossil) are only used if the corresponding VCS is discovered to be in use for the project/origin. For example, a .bzrignore in a Git repository will be discarded.

Don't load global ignores

This disables loading of global or user ignore files, like '~/.gitignore', '~/.config/watchexec/ignore', or '%APPDATA%\Bazzar\2.0\ignore'. Contrast with '--no-vcs-ignore' and '--no-project-ignore'.

Supported global ignore files

Like for project files, Git and Bazaar global files will only be used for the corresponding VCS as used in the project.

Don't use internal default ignores

Watchexec has a set of default ignore patterns, such as editor swap files, *.pyc, *.pyo, .DS_Store, .bzr, _darcs, .fossil-settings, .git, .hg, .pijul, .svn, and Watchexec log files.

Don't discover ignore files at all

This is a shorthand for '--no-global-ignore', '--no-vcs-ignore', '--no-project-ignore', but even more efficient as it will skip all the ignore discovery mechanisms from the get go.

Note that default ignores are still loaded, see '--no-default-ignore'.

Don't ignore anything at all

This is a shorthand for '--no-discover-ignore', '--no-default-ignore'.

Note that ignores explicitly loaded via other command line options, such as '--ignore' or '--ignore-file', will still be used.

Wait until first change before running command

By default, Watchexec will run the command once immediately. With this option, it will instead wait until an event is detected before running the command as normal.

Sleep before running the command

This option will cause Watchexec to sleep for the specified amount of time before running the command, after an event is detected. This is like using "sleep 5 && command" in a shell, but portable and slightly more efficient.

Takes a unit-less value in seconds, or a time span value such as "2min 5s". Providing a unit-less value is deprecated and will warn; it will be an error in the future.

Poll for filesystem changes

By default, and where available, Watchexec uses the operating system's native file system watching capabilities. This option disables that and instead uses a polling mechanism, which is less efficient but can work around issues with some file systems (like network shares) or edge cases.

Optionally takes a unit-less value in milliseconds, or a time span value such as "2s 500ms", to use as the polling interval. If not specified, the default is 30 seconds. Providing a unit-less value is deprecated and will warn; it will be an error in the future.

Aliased as '--force-poll'.

Use a different shell

By default, Watchexec will use '$SHELL' if it's defined or a default of 'sh' on Unix-likes, and either 'pwsh', 'powershell', or 'cmd' (CMD.EXE) on Windows, depending on what Watchexec detects is the running shell.

With this option, you can override that and use a different shell, for example one with more features or one which has your custom aliases and functions.

If the value has spaces, it is parsed as a command line, and the first word used as the shell program, with the rest as arguments to the shell.

The command is run with the '-c' flag (except for 'cmd' on Windows, where it's '/C').

The special value 'none' can be used to disable shell use entirely. In that case, the command provided to Watchexec will be parsed, with the first word being the executable and the rest being the arguments, and executed directly. Note that this parsing is rudimentary, and may not work as expected in all cases.

Using 'none' is a little more efficient and can enable a stricter interpretation of the input, but it also means that you can't use shell features like globbing, redirection, control flow, logic, or pipes.

$ watchexec -n -- zsh -x -o shwordsplit scr

Use with powershell core:

$ watchexec --shell=pwsh -- Test-Connection localhost

$ watchexec --shell=cmd -- dir

Use with a different unix shell:

$ watchexec --shell=bash -- 'echo $BASH_VERSION'

Use with a unix shell and options:

$ watchexec --shell='zsh -x -o shwordsplit' -- scr

Shorthand for '--shell=none'

Configure event emission

Watchexec can emit event information when running a command, which can be used by the child process to target specific changed files.

One thing to take care with is assuming inherent behaviour where there is only chance. Notably, it could appear as if the RENAMED variable contains both the original and the new path being renamed. In previous versions, it would even appear on some platforms as if the original always came before the new. However, none of this was true. It's impossible to reliably and portably know which changed path is the old or new, "half" renames may appear (only the original, only the new), "unknown" renames may appear (change was a rename, but whether it was the old or new isn't known), rename events might split across two debouncing boundaries, and so on.

This option controls where that information is emitted. It defaults to 'none', which doesn't emit event information at all. The other options are 'environment' (deprecated), 'stdio', 'file', 'json-stdio', and 'json-file'.

The 'stdio' and 'file' modes are text-based: 'stdio' writes absolute paths to the stdin of the command, one per line, each prefixed with create:, remove:, rename:, modify:, or other:, then closes the handle; 'file' writes the same thing to a temporary file, and its path is given with the $WATCHEXEC_EVENTS_FILE environment variable.

There are also two JSON modes, which are based on JSON objects and can represent the full set of events Watchexec handles. Here's an example of a folder being created on Linux:

"tags": [ { "kind": "path", "absolute": "/home/user/your/new-folder", "filetype": "dir" }, { "kind": "fs", "simple": "create", "full": "Create(Folder)" }, { "kind": "source", "source": "filesystem", } ], "metadata": { "notify-backend": "inotify" }

The fields are as follows:

The 'json-stdio' mode will emit JSON events to the standard input of the command, one per line, then close stdin. The 'json-file' mode will create a temporary file, write the events to it, and provide the path to the file with the $WATCHEXEC_EVENTS_FILE environment variable.

Finally, the 'environment' mode was the default until 2.0. It sets environment variables with the paths of the affected files, for filesystem events:

$WATCHEXEC_COMMON_PATH is set to the longest common path of all of the below variables, and so should be prepended to each path to obtain the full/real path. Then:

Multiple paths are separated by the system path separator, ';' on Windows and ':' on unix. Within each variable, paths are deduplicated and sorted in binary order (i.e. neither Unicode nor locale aware).

This is the legacy mode, is deprecated, and will be removed in the future. The environment is a very restricted space, while also limited in what it can usefully represent. Large numbers of files will either cause the environment to be truncated, or may error or crash the process entirely. The $WATCHEXEC_COMMON_PATH is also unintuitive, as demonstrated by the multiple confused queries that have landed in my inbox over the years.

Only emit events to stdout, run no commands.

This is a convenience option for using Watchexec as a file watcher, without running any commands. It is almost equivalent to using cat as the command, except that it will not spawn a new process for each event.

This option requires --emit-events-to to be set, and restricts the available modes to stdio and json-stdio, modifying their behaviour to write to stdout instead of the stdin of the command.

Add env vars to the command

This is a convenience option for setting environment variables for the command, without setting them for the Watchexec process itself.

Use key=value syntax. Multiple variables can be set by repeating the option.

Configure how the process is wrapped

By default, Watchexec will run the command in a process group in Unix, and in a Job Object in Windows.

Some Unix programs prefer running in a session, while others do not work in a process group.

Use 'group' to use a process group, 'session' to use a process session, and 'none' to run the command directly. On Windows, either of 'group' or 'session' will use a Job Object.

Alert when commands start and end

With this, Watchexec will emit a desktop notification when a command starts and ends, on supported platforms. On unsupported platforms, it may silently do nothing, or log a warning.

When to use terminal colours

Setting the environment variable NO_COLOR to any value is equivalent to --color=never.

Print how long the command took to run

This may not be exactly accurate, as it includes some overhead from Watchexec itself. Use the time utility, high-precision timers, or benchmarking tools for more accurate results.

Don't print starting and stopping messages

By default Watchexec will print a message when the command starts and stops. This option disables this behaviour, so only the command's output, warnings, and errors will be printed.

Ring the terminal bell on command completion

Set the project origin

Watchexec will attempt to discover the project's "origin" (or "root") by searching for a variety of markers, like files or directory patterns. It does its best but sometimes gets it it wrong, and you can override that with this option.

The project origin is used to determine the path of certain ignore files, which VCS is being used, the meaning of a leading '/' in filtering patterns, and maybe more in the future.

When set, Watchexec will also not bother searching, which can be significantly faster.

Set the working directory

By default, the working directory of the command is the working directory of Watchexec. You can change that with this option. Note that paths may be less intuitive to use with this.

Filename extensions to filter to

This is a quick filter to only emit events for files with the given extensions. Extensions can be given with or without the leading dot (e.g. 'js' or '.js'). Multiple extensions can be given by repeating the option or by separating them with commas.

Filename patterns to filter to

Provide a glob-like filter pattern, and only events for files matching the pattern will be emitted. Multiple patterns can be given by repeating the option. Events that are not from files (e.g. signals, keyboard events) will pass through untouched.

Files to load filters from

Provide a path to a file containing filters, one per line. Empty lines and lines starting with '#' are ignored. Uses the same pattern format as the '--filter' option.

This can also be used via the $WATCHEXEC_FILTER_FILES environment variable.

[experimental] Filter programs.

/!\ This option is EXPERIMENTAL and may change and/or vanish without notice.

Provide your own custom filter programs in jaq (similar to jq) syntax. Programs are given an event in the same format as described in '--emit-events-to' and must return a boolean. Invalid programs will make watchexec fail to start; use '-v' to see program runtime errors.

In addition to the jaq stdlib, watchexec adds some custom filter definitions:

'path | file_meta' returns file metadata or null if the file does not exist.

'path | file_size' returns the size of the file at path, or null if it does not exist.

'path | file_read(bytes)' returns a string with the first n bytes of the file at path. If the file is smaller than n bytes, the whole file is returned. There is no filter to read the whole file at once to encourage limiting the amount of data read and processed.

'string | hash', and 'path | file_hash' return the hash of the string or file at path. No guarantee is made about the algorithm used: treat it as an opaque value.

'any | kv_store(key)', 'kv_fetch(key)', and 'kv_clear' provide a simple key-value store. Data is kept in memory only, there is no persistence. Consistency is not guaranteed.

'any | printout', 'any | printerr', and 'any | log(level)' will print or log any given value to stdout, stderr, or the log (levels = error, warn, info, debug, trace), and pass the value through (so '[1] | log("debug") | .[]' will produce a '1' and log '[1]').

All filtering done with such programs, and especially those using kv or filesystem access, is much slower than the other filtering methods. If filtering is too slow, events will back up and stall watchexec. Take care when designing your filters.

If the argument to this option starts with an '@', the rest of the argument is taken to be the path to a file containing a jaq program.

Jaq programs are run in order, after all other filters, and short-circuit: if a filter (jaq or not) rejects an event, execution stops there, and no other filters are run. Additionally, they stop after outputting the first value, so you'll want to use 'any' or 'all' when iterating, otherwise only the first item will be processed, which can be quite confusing!

Find user-contributed programs or submit your own useful ones at <https://github.com/watchexec/watchexec/discussions/592>.

Regexp ignore filter on paths:

'all(.tags[] | select(.kind == "path"); .absolute | test("[.]test[.]js$")) | not'

Pass any event that creates a file:

'any(.tags[] | select(.kind == "fs"); .simple == "create")'

Pass events that touch executable files:

'any(.tags[] | select(.kind == "path" && .filetype == "file"); .absolute | metadata | .executable)'

Ignore files that start with shebangs:

'any(.tags[] | select(.kind == "path" && .filetype == "file"); .absolute | read(2) == "#!") | not'

Filename patterns to filter out

Provide a glob-like filter pattern, and events for files matching the pattern will be excluded. Multiple patterns can be given by repeating the option. Events that are not from files (e.g. signals, keyboard events) will pass through untouched.

Files to load ignores from

Provide a path to a file containing ignores, one per line. Empty lines and lines starting with '#' are ignored. Uses the same pattern format as the '--ignore' option.

This can also be used via the $WATCHEXEC_IGNORE_FILES environment variable.

Filesystem events to filter to

This is a quick filter to only emit events for the given types of filesystem changes. Choose from 'access', 'create', 'remove', 'rename', 'modify', 'metadata'. Multiple types can be given by repeating the option or by separating them with commas. By default, this is all types except for 'access'.

This may apply filtering at the kernel level when possible, which can be more efficient, but may be more confusing when reading the logs.

Default: create,remove,rename,modify,metadata

Don't emit fs events for metadata changes

This is a shorthand for '--fs-events create,remove,rename,modify'. Using it alongside the '--fs-events' option is non-sensical and not allowed.

Print events that trigger actions

This prints the events that triggered the action when handling it (after debouncing), in a human readable form. This is useful for debugging filters.

Use '-vvv' instead when you need more diagnostic information.

This shows the manual page for Watchexec, if the output is a terminal and the 'man' program is available. If not, the manual page is printed to stdout in ROFF format (suitable for writing to a watchexec.1 file).

**Examples:**

Example 1 (markdown):
```markdown
* 'path', along with:
  + `absolute`, an absolute path.
  + `filetype`, a file type if known ('dir', 'file', 'symlink', 'other').
* 'fs':
  + `simple`, the "simple" event type ('access', 'create', 'modify', 'remove', or 'other').
  + `full`, the "full" event type, which is too complex to fully describe here, but looks like 'General(Precise(Specific))'.
* 'source', along with:
  + `source`, the source of the event ('filesystem', 'keyboard', 'mouse', 'os', 'time', 'internal').
* 'keyboard', along with:
  + `keycode`. Currently only the value 'eof' is supported.
* 'process', for events caused by processes:
  + `pid`, the process ID.
* 'signal', for signals sent to Watchexec:
  + `signal`, the normalised signal name ('hangup', 'interrupt', 'quit', 'terminate', 'user1', 'user2').
* 'completion', for when a command ends:
  + `disposition`, the exit disposition ('success', 'error', 'signal', 'stop', 'exception', 'continued').
  + `code`, the exit, signal, stop, or exception code.
```

Example 2 (sql):
```sql
$ mise watch build
Runs the "build" tasks. Will re-run the tasks when any of its sources change.
Uses "sources" from the tasks definition to determine which files to watch.

$ mise watch build --glob src/**/*.rs
Runs the "build" tasks but specify the files to watch with a glob pattern.
This overrides the "sources" from the tasks definition.

$ mise watch build --clear
Extra arguments are passed to watchexec. See `watchexec --help` for details.

$ mise watch serve --watch src --exts rs --restart
Starts an api server, watching for changes to "*.rs" files in "./src" and kills/restarts the server when they change.
```

---

## mise lock ​

**URL:** https://mise.jdx.dev/cli/lock.html

**Contents:**
- mise lock ​
- Arguments ​
  - [TOOL]… ​
- Flags ​
  - -j --jobs <JOBS> ​
  - -n --dry-run ​
  - -p --platform… <PLATFORM> ​
  - --local ​

Update lockfile checksums and URLs for all specified platforms

Updates checksums and download URLs for all platforms already specified in the lockfile. If no lockfile exists, shows what would be created based on the current configuration. This allows you to refresh lockfile data for platforms other than the one you're currently on. Operates on the lockfile in the current config root. Use TOOL arguments to target specific tools.

Tool(s) to update in lockfile e.g.: node python If not specified, all tools in lockfile will be updated

Number of jobs to run in parallel

Show what would be updated without making changes

Comma-separated list of platforms to target e.g.: linux-x64,macos-arm64,windows-x64 If not specified, all platforms already in lockfile will be updated

Update mise.local.lock instead of mise.lock Use for tools defined in .local.toml configs

**Examples:**

Example 1 (sql):
```sql
mise lock                       # update lockfile for all common platforms
mise lock node python           # update only node and python
mise lock --platform linux-x64  # update only linux-x64 platform
mise lock --dry-run             # show what would be updated
mise lock --local               # update mise.local.lock for local configs
```

---

## mise config ls ​

**URL:** https://mise.jdx.dev/cli/config/ls.html

**Contents:**
- mise config ls ​
- Flags ​
  - -J --json ​
  - --no-header ​
  - --tracked-configs ​

List config files currently in use

Output in JSON format

Do not print table header

List all tracked config files

**Examples:**

Example 1 (unknown):
```unknown
$ mise config ls
Path                        Tools
~/.config/mise/config.toml  pitchfork
~/src/mise/mise.toml        actionlint, bun, cargo-binstall, cargo:cargo-edit, cargo:cargo-insta
```

---

## mise generate github-action ​

**URL:** https://mise.jdx.dev/cli/generate/github-action.html

**Contents:**
- mise generate github-action ​
- Flags ​
  - -t --task <TASK> ​
  - -w --write ​
  - --name <NAME> ​

Generate a GitHub Action workflow file

This command generates a GitHub Action workflow file that runs a mise task like mise run ci when you push changes to your repository.

The task to run when the workflow is triggered

write to .github/workflows/$name.yml

the name of the workflow to generate

**Examples:**

Example 1 (unknown):
```unknown
mise generate github-action --write --task=ci
git commit -m "feat: add new feature"
git push # runs `mise run ci` on GitHub
```

---

## mise config get ​

**URL:** https://mise.jdx.dev/cli/config/get.html

**Contents:**
- mise config get ​
- Arguments ​
  - [KEY] ​
- Flags ​
  - -f --file <FILE> ​

Display the value of a setting in a mise.toml file

The path of the config to display

The path to the mise.toml file to edit

If not provided, the nearest mise.toml file will be used

**Examples:**

Example 1 (unknown):
```unknown
$ mise toml get tools.python
3.12
```

---

## mise self-update ​

**URL:** https://mise.jdx.dev/cli/self-update.html

**Contents:**
- mise self-update ​
- Arguments ​
  - [VERSION] ​
- Flags ​
  - -f --force ​
  - -y --yes ​
  - --no-plugins ​

Uses the GitHub Releases API to find the latest release and binary. By default, this will also update any installed plugins. Uses the GITHUB_API_TOKEN environment variable if set for higher rate limits.

This command is not available if mise is installed via a package manager.

Update to a specific version

Update even if already up to date

Skip confirmation prompt

Disable auto-updating plugins

---

## mise where ​

**URL:** https://mise.jdx.dev/cli/where.html

**Contents:**
- mise where ​
- Arguments ​
  - <TOOL@VERSION> ​

Display the installation path for a tool

The tool must be installed for this to work.

Tool(s) to look up e.g.: ruby@3 if "@<PREFIX>" is specified, it will show the latest installed version that matches the prefix otherwise, it will show the current, active installed version

**Examples:**

Example 1 (markdown):
```markdown
# Show the latest installed version of node
# If it is is not installed, errors
$ mise where node@20
/home/jdx/.local/share/mise/installs/node/20.0.0

# Show the current, active install directory of node
# Errors if node is not referenced in any .tool-version file
$ mise where node
/home/jdx/.local/share/mise/installs/node/20.0.0
```

---

## mise sync node ​

**URL:** https://mise.jdx.dev/cli/sync/node.html

**Contents:**
- mise sync node ​
- Flags ​
  - --brew ​
  - --nodenv ​
  - --nvm ​

Symlinks all tool versions from an external tool into mise

For example, use this to import all Homebrew node installs into mise

This won't overwrite any existing installs but will overwrite any existing symlinks

Get tool versions from Homebrew

Get tool versions from nodenv

Get tool versions from nvm

**Examples:**

Example 1 (python):
```python
brew install node@18 node@20
mise sync node --brew
mise use -g node@18 - uses Homebrew-provided node
```

---

## mise tasks ​

**URL:** https://mise.jdx.dev/cli/tasks.html

**Contents:**
- mise tasks ​
- Arguments ​
  - [TASK] ​
- Global Flags ​
  - -g --global ​
  - -J --json ​
  - -l --local ​
  - -x --extended ​
  - --all ​
  - --hidden ​

Task name to get info of

Only show global tasks

Output in JSON format

Only show non-global tasks

Load all tasks from the entire monorepo, including sibling directories. By default, only tasks from the current directory hierarchy are loaded.

Do not print table header

Sort by column. Default is name.

Sort order. Default is asc.

**Examples:**

Example 1 (unknown):
```unknown
mise tasks ls
```

---

## mise tool-alias get ​

**URL:** https://mise.jdx.dev/cli/tool-alias/get.html

**Contents:**
- mise tool-alias get ​
- Arguments ​
  - <PLUGIN> ​
  - <ALIAS> ​

Show an alias for a plugin

This is the contents of a tool_alias.<PLUGIN> entry in ~/.config/mise/config.toml

The plugin to show the alias for

**Examples:**

Example 1 (unknown):
```unknown
$ mise tool-alias get node lts-hydrogen
20.0.0
```

---

## mise cache clear ​

**URL:** https://mise.jdx.dev/cli/cache/clear.html

**Contents:**
- mise cache clear ​
- Arguments ​
  - [PLUGIN]… ​

Deletes all cache files in mise

Plugin(s) to clear cache for e.g.: node, python

---

## mise reshim ​

**URL:** https://mise.jdx.dev/cli/reshim.html

**Contents:**
- mise reshim ​
- Flags ​
  - -f --force ​

Creates new shims based on bin paths from currently installed tools.

This creates new shims in ~/.local/share/mise/shims for CLIs that have been added. mise will try to do this automatically for commands like npm i -g but there are other ways to install things (like using yarn or pnpm for node) that mise does not know about and so it will be necessary to call this explicitly.

If you think mise should automatically call this for a particular command, please open an issue on the mise repo. You can also setup a shell function to reshim automatically (it's really fast so you don't need to worry about overhead):

Note that this creates shims for all installed tools, not just the ones that are currently active in mise.toml.

Removes all shims before reshimming

**Examples:**

Example 1 (unknown):
```unknown
npm() {
  command npm "$@"
  mise reshim
}
```

Example 2 (unknown):
```unknown
$ mise reshim
$ ~/.local/share/mise/shims/node -v
v20.0.0
```

---

## mise uninstall ​

**URL:** https://mise.jdx.dev/cli/uninstall.html

**Contents:**
- mise uninstall ​
- Arguments ​
  - [INSTALLED_TOOL@VERSION]… ​
- Flags ​
  - -a --all ​
  - -n --dry-run ​

Removes installed tool versions

This only removes the installed version, it does not modify mise.toml.

Delete all installed versions

Do not actually delete anything

**Examples:**

Example 1 (markdown):
```markdown
# will uninstall specific version
$ mise uninstall node@18.0.0

# will uninstall the current node version (if only one version is installed)
$ mise uninstall node

# will uninstall all installed versions of node
$ mise uninstall --all node@18.0.0 # will uninstall all node versions
```

---

## mise completion ​

**URL:** https://mise.jdx.dev/cli/completion.html

**Contents:**
- mise completion ​
- Arguments ​
  - [SHELL] ​
- Flags ​
  - --include-bash-completion-lib ​

Generate shell completions

Shell type to generate completions for

Include the bash completion library in the bash completion script

This is required for completions to work in bash, but it is not included by default you may source it separately or enable this flag to enable it in the script.

**Examples:**

Example 1 (bash):
```bash
mise completion bash --include-bash-completion-lib > ~/.local/share/bash-completion/completions/mise
mise completion zsh  > /usr/local/share/zsh/site-functions/_mise
mise completion fish > ~/.config/fish/completions/mise.fish
mise completion powershell >> $PROFILE
```

---

## mise version ​

**URL:** https://mise.jdx.dev/cli/version.html

**Contents:**
- mise version ​
- Flags ​
  - -J --json ​

Display the version of mise

Displays the version, os, architecture, and the date of the build.

If the version is out of date, it will display a warning.

Print the version information in JSON format

**Examples:**

Example 1 (unknown):
```unknown
mise version
mise --version
mise -v
mise -V
```

---

## mise ​

**URL:** https://mise.jdx.dev/cli/

**Contents:**
- mise ​
- Arguments ​
  - [TASK] ​
- Global Flags ​
  - -C --cd <DIR> ​
  - -E --env… <ENV> ​
  - -j --jobs <JOBS> ​
  - -q --quiet ​
  - -v --verbose… ​
  - -y --yes ​

Usage: mise [FLAGS] [TASK] <SUBCOMMAND>

Shorthand for mise tasks run <TASK>.

Change directory before running command

Set the environment for loading mise.<ENV>.toml

How many jobs to run in parallel [default: 8]

Suppress non-error messages

Show extra output (use -vv for even more)

Answer yes to all confirmation prompts

Read/write directly to stdin/stdout/stderr instead of by line

Require lockfile URLs to be present during installation

Fails if tools don't have pre-resolved URLs in the lockfile for the current platform. This prevents API calls to GitHub, aqua registry, etc. Can also be enabled via MISE_LOCKED=1 or settings.locked=true

Suppress all task output and mise non-error messages

Do not load any config files

Can also use MISE_NO_CONFIG=1

Do not load environment variables from config files

Can also use MISE_NO_ENV=1

Do not execute hooks from config files

Can also use MISE_NO_HOOKS=1

---

## mise shell-alias ls ​

**URL:** https://mise.jdx.dev/cli/shell-alias/ls.html

**Contents:**
- mise shell-alias ls ​
- Flags ​
  - --no-header ​

Shows the shell aliases that are set in the current directory. These are defined in mise.toml under the [shell_alias] section.

Don't show table header

**Examples:**

Example 1 (unknown):
```unknown
$ mise shell-alias ls
alias    command
ll       ls -la
gs       git status
```

---

## mise prepare ​

**URL:** https://mise.jdx.dev/cli/prepare.html

**Contents:**
- mise prepare ​
- Flags ​
  - -f --force ​
  - --list ​
  - -n --dry-run ​
  - --only… <ONLY> ​
  - --skip… <SKIP> ​

[experimental] Ensure project dependencies are ready

Runs all applicable prepare steps for the current project. This checks if dependency lockfiles are newer than installed outputs (e.g., package-lock.json vs node_modules/) and runs install commands if needed.

Providers with auto = true are automatically invoked before mise x and mise run unless skipped with the --no-prepare flag.

Force run all prepare steps even if outputs are fresh

Show what prepare steps are available

Only check if prepare is needed, don't run commands

Run specific prepare rule(s) only

Skip specific prepare rule(s)

**Examples:**

Example 1 (unknown):
```unknown
mise prepare              # Run all applicable prepare steps
mise prepare --dry-run    # Show what would run without executing
mise prepare --force      # Force run even if outputs are fresh
mise prepare --list       # List available prepare providers
mise prepare --only npm   # Run only npm prepare
mise prepare --skip npm   # Skip npm prepare
```

Example 2 (json):
```json
Configure prepare providers in mise.toml:

```toml
# Built-in npm provider (auto-detects lockfile)
[prepare.npm]
auto = true              # Auto-run before mise x/run

# Custom provider
[prepare.codegen]
auto = true
sources = ["schema/*.graphql"]
outputs = ["src/generated/"]
run = "npm run codegen"

[prepare]
disable = ["npm"]        # Disable specific providers at runtime
```

---

## mise use ​

**URL:** https://mise.jdx.dev/cli/use.html

**Contents:**
- mise use ​
- Arguments ​
  - [TOOL@VERSION]… ​
- Flags ​
  - -e --env <ENV> ​
  - -f --force ​
  - -g --global ​
  - -j --jobs <JOBS> ​
  - -n --dry-run ​
  - -p --path <PATH> ​

Installs a tool and adds the version to mise.toml.

This will install the tool version if it is not already installed. By default, this will use a mise.toml file in the current directory. If multiple config files exist (e.g., both mise.toml and mise.local.toml), the lowest precedence file (mise.toml) will be used. See https://mise.jdx.dev/configuration.html#target-file-for-write-operations

In the following order:

Use the --global flag to use the global config file instead.

Tool(s) to add to config file

e.g.: node@20, cargo:ripgrep@latest npm:prettier@3 If no version is specified, it will default to @latest

Tool options can be set with this syntax:

Create/modify an environment-specific config file like .mise.<env>.toml

Force reinstall even if already installed

Use the global config file (~/.config/mise/config.toml) instead of the local one

Number of jobs to run in parallel [default: 4]

Perform a dry run, showing what would be installed and modified without making changes

Specify a path to a config file or directory

If a directory is specified, it will look for a config file in that directory following the rules above.

Only install versions released before this date

Supports absolute dates like "2024-06-01" and relative durations like "90d" or "1y".

Save fuzzy version to config file

e.g.: mise use --fuzzy node@20 will save 20 as the version this is the default behavior unless MISE_PIN=1

Save exact version to config file e.g.: mise use --pin node@20 will save 20.0.0 as the version Set MISE_PIN=1 to make this the default behavior

Consider using mise.lock as a better alternative to pinning in mise.toml: https://mise.jdx.dev/configuration/settings.html#lockfile

Directly pipe stdin/stdout/stderr from plugin to user Sets --jobs=1

Remove the plugin(s) from config file

**Examples:**

Example 1 (unknown):
```unknown
mise use ubi:BurntSushi/ripgrep[exe=rg]
```

Example 2 (markdown):
```markdown
# run with no arguments to use the interactive selector
$ mise use

# set the current version of node to 20.x in mise.toml of current directory
# will write the fuzzy version (e.g.: 20)
$ mise use node@20

# set the current version of node to 20.x in ~/.config/mise/config.toml
# will write the precise version (e.g.: 20.0.0)
$ mise use -g --pin node@20

# sets .mise.local.toml (which is intended not to be committed to a project)
$ mise use --env local node@20

# sets .mise.staging.toml (which is used if MISE_ENV=staging)
$ mise use --env staging node@20
```

---

## mise implode ​

**URL:** https://mise.jdx.dev/cli/implode.html

**Contents:**
- mise implode ​
- Flags ​
  - -n --dry-run ​
  - --config ​

Removes mise CLI and all related data

Skips config directory by default.

List directories that would be removed without actually removing them

Also remove config directory

---

## mise deactivate ​

**URL:** https://mise.jdx.dev/cli/deactivate.html

**Contents:**
- mise deactivate ​

Disable mise for current shell session

This can be used to temporarily disable mise in a shell session.

**Examples:**

Example 1 (unknown):
```unknown
mise deactivate
```

---

## mise shell ​

**URL:** https://mise.jdx.dev/cli/shell.html

**Contents:**
- mise shell ​
- Arguments ​
  - <TOOL@VERSION>… ​
- Flags ​
  - -j --jobs <JOBS> ​
  - -u --unset ​
  - --raw ​

Sets a tool version for the current session.

Only works in a session where mise is already activated.

This works by setting environment variables for the current shell session such as MISE_NODE_VERSION=20 which is "eval"ed as a shell function created by mise activate.

Number of jobs to run in parallel [default: 4]

Removes a previously set version

Directly pipe stdin/stdout/stderr from plugin to user Sets --jobs=1

**Examples:**

Example 1 (python):
```python
$ mise shell node@20
$ node -v
v20.0.0
```

---

## mise activate ​

**URL:** https://mise.jdx.dev/cli/activate.html

**Contents:**
- mise activate ​
- Arguments ​
  - [SHELL_TYPE] ​
- Flags ​
  - -q --quiet ​
  - --no-hook-env ​
  - --shims ​

Initializes mise in the current shell session

This should go into your shell's rc file or login shell. Otherwise, it will only take effect in the current session. (e.g. ~/.zshrc, ~/.zprofile, ~/.zshenv, ~/.bashrc, ~/.bash_profile, ~/.profile, ~/.config/fish/config.fish, or $PROFILE for powershell)

Typically, this can be added with something like the following:

However, this requires that "mise" is in your PATH. If it is not, you need to specify the full path like this:

Customize status output with status settings.

Shell type to generate the script for

Suppress non-error messages

Do not automatically call hook-env

This can be helpful for debugging mise. If you run eval "$(mise activate --no-hook-env)", then you can call mise hook-env manually which will output the env vars to stdout without actually modifying the environment. That way you can do things like mise hook-env --trace to get more information or just see the values that hook-env is outputting.

Use shims instead of modifying PATH Effectively the same as:

mise activate --shims does not support all the features of mise activate. See https://mise.jdx.dev/dev-tools/shims.html#shims-vs-path for more information

**Examples:**

Example 1 (bash):
```bash
echo 'eval "$(mise activate zsh)"' >> ~/.zshrc
```

Example 2 (bash):
```bash
echo 'eval "$(/path/to/mise activate zsh)"' >> ~/.zshrc
```

Example 3 (bash):
```bash
PATH="$HOME/.local/share/mise/shims:$PATH"
```

Example 4 (unknown):
```unknown
eval "$(mise activate bash)"
eval "$(mise activate zsh)"
mise activate fish | source
execx($(mise activate xonsh))
(&mise activate pwsh) | Out-String | Invoke-Expression
```

---

## mise test-tool ​

**URL:** https://mise.jdx.dev/cli/test-tool.html

**Contents:**
- mise test-tool ​
- Arguments ​
  - [TOOLS]… ​
- Flags ​
  - -a --all ​
  - -j --jobs <JOBS> ​
  - --all-config ​
  - --include-non-defined ​
  - --raw ​

Test a tool installs and executes

Test every tool specified in registry.toml

Number of jobs to run in parallel [default: 4]

Test all tools specified in config files

Also test tools not defined in registry.toml, guessing how to test it

Directly pipe stdin/stdout/stderr from plugin to user Sets --jobs=1

**Examples:**

Example 1 (unknown):
```unknown
mise test-tool ripgrep
```

---

## mise shell-alias set ​

**URL:** https://mise.jdx.dev/cli/shell-alias/set.html

**Contents:**
- mise shell-alias set ​
- Arguments ​
  - <shell_alias> ​
  - <COMMAND> ​

Add/update a shell alias

This modifies the contents of ~/.config/mise/config.toml

**Examples:**

Example 1 (unknown):
```unknown
mise shell-alias set ll "ls -la"
mise shell-alias set gs "git status"
```

---

## mise config set ​

**URL:** https://mise.jdx.dev/cli/config/set.html

**Contents:**
- mise config set ​
- Arguments ​
  - <KEY> ​
  - <VALUE> ​
- Flags ​
  - -f --file <FILE> ​
  - -t --type <TYPE> ​

Set the value of a setting in a mise.toml file

The path of the config to display

The value to set the key to

The path to the mise.toml file to edit

If not provided, the nearest mise.toml file will be used

**Examples:**

Example 1 (markdown):
```markdown
$ mise config set tools.python 3.12
$ mise config set settings.always_keep_download true
$ mise config set env.TEST_ENV_VAR ABC
$ mise config set settings.disable_tools --type list node,rust

# Type for `settings` is inferred
$ mise config set settings.jobs 4
```

---

## mise tool-alias ls ​

**URL:** https://mise.jdx.dev/cli/tool-alias/ls.html

**Contents:**
- mise tool-alias ls ​
- Arguments ​
  - [TOOL] ​
- Flags ​
  - --no-header ​

List tool version aliases Shows the aliases that can be specified. These can come from user config or from plugins in bin/list-aliases.

For user config, aliases are defined like the following in ~/.config/mise/config.toml:

Show aliases for <TOOL>

Don't show table header

**Examples:**

Example 1 (json):
```json
[tool_alias.node.versions]
lts = "22.0.0"
```

Example 2 (unknown):
```unknown
$ mise tool-alias ls
node  lts-jod      22
```

---

## mise install ​

**URL:** https://mise.jdx.dev/cli/install.html

**Contents:**
- mise install ​
- Arguments ​
  - [TOOL@VERSION]… ​
- Flags ​
  - -f --force ​
  - -j --jobs <JOBS> ​
  - -n --dry-run ​
  - -v --verbose… ​
  - --before <BEFORE> ​
  - --raw ​

Install a tool version

Installs a tool version to ~/.local/share/mise/installs/<PLUGIN>/<VERSION> Installing alone will not activate the tools so they won't be in PATH. To install and/or activate in one command, use mise use which will create a mise.toml file in the current directory to activate this tool when inside the directory. Alternatively, run mise exec <TOOL>@<VERSION> -- <COMMAND> to execute a tool without creating config files.

Tools will be installed in parallel. To disable, set --jobs=1 or MISE_JOBS=1

Tool(s) to install e.g.: node@20

Force reinstall even if already installed

Number of jobs to run in parallel [default: 4]

Show what would be installed without actually installing

Show installation output

This argument will print plugin output such as download, configuration, and compilation output.

Only install versions released before this date

Supports absolute dates like "2024-06-01" and relative durations like "90d" or "1y".

Directly pipe stdin/stdout/stderr from plugin to user Sets --jobs=1

**Examples:**

Example 1 (python):
```python
mise install node@20.0.0  # install specific node version
mise install node@20      # install fuzzy node version
mise install node         # install version specified in mise.toml
mise install              # installs everything specified in mise.toml
```

---

## mise ls-remote ​

**URL:** https://mise.jdx.dev/cli/ls-remote.html

**Contents:**
- mise ls-remote ​
- Arguments ​
  - [TOOL@VERSION] ​
  - [PREFIX] ​
- Flags ​
  - --all ​
  - -J --json ​

List runtime versions available for install.

Note that the results may be cached, run mise cache clean to clear the cache and get fresh results.

Tool to get versions for

The version prefix to use when querying the latest version same as the first argument after the "@"

Show all installed plugins and versions

Output in JSON format (includes version metadata like created_at timestamps when available)

**Examples:**

Example 1 (json):
```json
$ mise ls-remote node
18.0.0
20.0.0

$ mise ls-remote node@20
20.0.0
20.1.0

$ mise ls-remote node 20
20.0.0
20.1.0

$ mise ls-remote github:cli/cli --json
[{"version":"2.62.0","created_at":"2024-11-14T15:40:35Z"},{"version":"2.61.0","created_at":"2024-10-23T19:22:15Z"}]
```

---

## mise set ​

**URL:** https://mise.jdx.dev/cli/set.html

**Contents:**
- mise set ​
- Arguments ​
  - [ENV_VAR]… ​
- Flags ​
  - -E --env <ENV> ​
  - -g --global ​
  - --age-encrypt ​
  - --age-key-file <PATH> ​
  - --age-recipient… <RECIPIENT> ​
  - --age-ssh-recipient… <PATH_OR_PUBKEY> ​

Set environment variables in mise.toml

By default, this command modifies mise.toml in the current directory. If multiple config files exist (e.g., both mise.toml and mise.local.toml), the lowest precedence file (mise.toml) will be used. See https://mise.jdx.dev/configuration.html#target-file-for-write-operations

Use -E <env> to create/modify environment-specific config files like mise.<env>.toml.

Environment variable(s) to set e.g.: NODE_ENV=production

Create/modify an environment-specific config file like .mise.<env>.toml

Set the environment variable in the global config file

[experimental] Encrypt the value with age before storing

[experimental] Age identity file for encryption

Defaults to ~/.config/mise/age.txt if it exists

[experimental] Age recipient (x25519 public key) for encryption

Can be used multiple times. Requires --age-encrypt.

[experimental] SSH recipient (public key or path) for age encryption

Can be used multiple times. Requires --age-encrypt.

The TOML file to update

Can be a file path or directory. If a directory is provided, will create/use mise.toml in that directory. Defaults to MISE_DEFAULT_CONFIG_FILENAME environment variable, or mise.toml.

Prompt for environment variable values

**Examples:**

Example 1 (json):
```json
$ mise set NODE_ENV=production

$ mise set NODE_ENV
production

$ mise set -E staging NODE_ENV=staging
# creates or modifies mise.staging.toml

$ mise set
key       value       source
NODE_ENV  production  ~/.config/mise/config.toml

$ mise set --prompt PASSWORD
Enter value for PASSWORD: [hidden input]

[experimental] Age Encryption:

$ mise set --age-encrypt API_KEY=secret

$ mise set --age-encrypt --prompt API_KEY
Enter value for API_KEY: [hidden input]
```

---

## mise exec ​

**URL:** https://mise.jdx.dev/cli/exec.html

**Contents:**
- mise exec ​
- Arguments ​
  - [TOOL@VERSION]… ​
  - [-- COMMAND]… ​
- Flags ​
  - -c --command <C> ​
  - -j --jobs <JOBS> ​
  - --fresh-env ​
  - --no-prepare ​
  - --raw ​

Execute a command with tool(s) set

use this to avoid modifying the shell session or running ad-hoc commands with mise tools set.

Tools will be loaded from mise.toml, though they can be overridden with <RUNTIME> args Note that only the plugin specified will be overridden, so if a mise.toml file includes "node 20" but you run mise exec python@3.11; it will still load node@20.

The "--" separates runtimes from the commands to pass along to the subprocess.

Tool(s) to start e.g.: node@20 python@3.10

Command string to execute (same as --command)

Command string to execute

Number of jobs to run in parallel [default: 4]

Bypass the environment cache and recompute the environment

Skip automatic dependency preparation

Directly pipe stdin/stdout/stderr from plugin to user Sets --jobs=1

**Examples:**

Example 1 (python):
```python
$ mise exec node@20 -- node ./app.js  # launch app.js using node-20.x
$ mise x node@20 -- node ./app.js     # shorter alias

# Specify command as a string:
$ mise exec node@20 python@3.11 --command "node -v && python -V"

# Run a command in a different directory:
$ mise x -C /path/to/project node@20 -- node ./app.js
```

---

## mise which ​

**URL:** https://mise.jdx.dev/cli/which.html

**Contents:**
- mise which ​
- Arguments ​
  - [BIN_NAME] ​
- Flags ​
  - -t --tool <TOOL@VERSION> ​
  - --plugin ​
  - --version ​

Shows the path that a tool's bin points to.

Use this to figure out what version of a tool is currently active.

Use a specific tool@version e.g.: mise which npm --tool=node@20

Show the plugin name instead of the path

Show the version instead of the path

**Examples:**

Example 1 (unknown):
```unknown
$ mise which node
/home/username/.local/share/mise/installs/node/20.0.0/bin/node

$ mise which node --plugin
node

$ mise which node --version
20.0.0
```

---

## mise tool-alias unset ​

**URL:** https://mise.jdx.dev/cli/tool-alias/unset.html

**Contents:**
- mise tool-alias unset ​
- Arguments ​
  - <PLUGIN> ​
  - [ALIAS] ​

Clears an alias for a backend/plugin

This modifies the contents of ~/.config/mise/config.toml

The backend/plugin to remove the alias from

**Examples:**

Example 1 (unknown):
```unknown
mise tool-alias unset maven
mise tool-alias unset node lts-jod
```

---

## mise tool-alias set ​

**URL:** https://mise.jdx.dev/cli/tool-alias/set.html

**Contents:**
- mise tool-alias set ​
- Arguments ​
  - <PLUGIN> ​
  - <ALIAS> ​
  - [VALUE] ​

Add/update an alias for a backend/plugin

This modifies the contents of ~/.config/mise/config.toml

The backend/plugin to set the alias for

The value to set the alias to

**Examples:**

Example 1 (unknown):
```unknown
mise tool-alias set maven asdf:mise-plugins/mise-maven
mise tool-alias set node lts-jod 22.0.0
```

---

## mise settings ls ​

**URL:** https://mise.jdx.dev/cli/settings/ls.html

**Contents:**
- mise settings ls ​
- Arguments ​
  - [SETTING] ​
- Flags ​
  - -a --all ​
  - -J --json ​
  - -l --local ​
  - -T --toml ​
  - --json-extended ​

Show current settings

This is the contents of ~/.config/mise/config.toml

Note that aliases are also stored in this file but managed separately with mise tool-alias

Output in JSON format

Use the local config file instead of the global one

Output in TOML format

Output in JSON format with sources

**Examples:**

Example 1 (unknown):
```unknown
$ mise settings ls
idiomatic_version_file = false
...

$ mise settings ls python
default_packages_file = "~/.default-python-packages"
...
```

---

## mise bin-paths ​

**URL:** https://mise.jdx.dev/cli/bin-paths.html

**Contents:**
- mise bin-paths ​
- Arguments ​
  - [TOOL@VERSION]… ​

List all the active runtime bin paths

Tool(s) to look up e.g.: ruby@3

---

## mise cache ​

**URL:** https://mise.jdx.dev/cli/cache.html

**Contents:**
- mise cache ​
- Subcommands ​

Manage the mise cache

Run mise cache with no args to view the current cache directory.

---

## mise settings unset ​

**URL:** https://mise.jdx.dev/cli/settings/unset.html

**Contents:**
- mise settings unset ​
- Arguments ​
  - <KEY> ​
- Flags ​
  - -l --local ​

This modifies the contents of ~/.config/mise/config.toml

The setting to remove

Use the local config file instead of the global one

**Examples:**

Example 1 (unknown):
```unknown
mise settings unset idiomatic_version_file
```

---

## mise settings get ​

**URL:** https://mise.jdx.dev/cli/settings/get.html

**Contents:**
- mise settings get ​
- Arguments ​
  - <SETTING> ​
- Flags ​
  - -l --local ​

Show a current setting

This is the contents of a single entry in ~/.config/mise/config.toml

Note that aliases are also stored in this file but managed separately with mise tool-alias get

Use the local config file instead of the global one

**Examples:**

Example 1 (unknown):
```unknown
$ mise settings get idiomatic_version_file
true
```

---

## mise upgrade ​

**URL:** https://mise.jdx.dev/cli/upgrade.html

**Contents:**
- mise upgrade ​
- Arguments ​
  - [INSTALLED_TOOL@VERSION]… ​
- Flags ​
  - -i --interactive ​
  - -j --jobs <JOBS> ​
  - -l --bump ​
  - -n --dry-run ​
  - -x --exclude… <INSTALLED_TOOL> ​
  - --before <BEFORE> ​

Upgrades outdated tools

By default, this keeps the range specified in mise.toml. So if you have node@20 set, it will upgrade to the latest 20.x.x version available. See the --bump flag to use the latest version and bump the version in mise.toml.

This will update mise.lock if it is enabled, see https://mise.jdx.dev/configuration/settings.html#lockfile

Tool(s) to upgrade e.g.: node@20 python@3.10 If not specified, all current tools will be upgraded

Display multiselect menu to choose which tools to upgrade

Number of jobs to run in parallel [default: 4]

Upgrades to the latest version available, bumping the version in mise.toml

For example, if you have node = "20.0.0" in your mise.toml but 22.1.0 is the latest available, this will install 22.1.0 and set node = "22.1.0" in your config.

It keeps the same precision as what was there before, so if you instead had node = "20", it would change your config to node = "22".

Just print what would be done, don't actually do it

Tool(s) to exclude from upgrading e.g.: go python

Only upgrade to versions released before this date

Supports absolute dates like "2024-06-01" and relative durations like "90d" or "1y". This can be useful for reproducibility or security purposes.

This only affects fuzzy version matches like "20" or "latest". Explicitly pinned versions like "22.5.0" are not filtered.

Directly pipe stdin/stdout/stderr from plugin to user Sets --jobs=1

**Examples:**

Example 1 (markdown):
```markdown
# Upgrades node to the latest version matching the range in mise.toml
$ mise upgrade node

# Upgrades node to the latest version and bumps the version in mise.toml
$ mise upgrade node --bump

# Upgrades all tools to the latest versions
$ mise upgrade

# Upgrades all tools to the latest versions and bumps the version in mise.toml
$ mise upgrade --bump

# Just print what would be done, don't actually do it
$ mise upgrade --dry-run

# Upgrades node and python to the latest versions
$ mise upgrade node python

# Upgrade all tools except go
$ mise upgrade --exclude go

# Show a multiselect menu to choose which tools to upgrade
$ mise upgrade --interactive
```

---

## mise unuse ​

**URL:** https://mise.jdx.dev/cli/unuse.html

**Contents:**
- mise unuse ​
- Arguments ​
  - <INSTALLED_TOOL@VERSION>… ​
- Flags ​
  - -e --env <ENV> ​
  - -g --global ​
  - -p --path <PATH> ​
  - --no-prune ​

Removes installed tool versions from mise.toml

By default, this will use the mise.toml file that has the tool defined. If multiple config files exist (e.g., both mise.toml and mise.local.toml), the lowest precedence file (mise.toml) will be used. See https://mise.jdx.dev/configuration.html#target-file-for-write-operations

In the following order:

Will also prune the installed version if no other configurations are using it.

Create/modify an environment-specific config file like .mise.<env>.toml

Use the global config file (~/.config/mise/config.toml) instead of the local one

Specify a path to a config file or directory

If a directory is specified, it will look for a config file in that directory following the rules above.

Do not also prune the installed version

**Examples:**

Example 1 (sql):
```sql
# will uninstall specific version
$ mise unuse node@18.0.0

# will uninstall specific version from global config
$ mise unuse -g node@18.0.0

# will uninstall specific version from .mise.local.toml
$ mise unuse --env local node@20

# will uninstall specific version from .mise.staging.toml
$ mise unuse --env staging node@20
```

---

## mise fmt ​

**URL:** https://mise.jdx.dev/cli/fmt.html

**Contents:**
- mise fmt ​
- Flags ​
  - -a --all ​
  - -c --check ​
  - -s --stdin ​

Sorts keys and cleans up whitespace in mise.toml

Format all files from the current directory

Check if the configs are formatted, no formatting is done

Read config from stdin and write its formatted version into stdout

---

## mise generate config ​

**URL:** https://mise.jdx.dev/cli/generate/config.html

**Contents:**
- mise generate config ​
- Flags ​
  - -o --output <OUTPUT> ​
  - -t --tool-versions <TOOL_VERSIONS> ​

[experimental] Generate a mise.toml file

Output to file instead of stdout

Path to a .tool-versions file to import tools from

**Examples:**

Example 1 (unknown):
```unknown
mise cf generate > mise.toml
mise cf generate --output=mise.toml
```

---

## mise mcp ​

**URL:** https://mise.jdx.dev/cli/mcp.html

**Contents:**
- mise mcp ​

[experimental] Run Model Context Protocol (MCP) server

This command starts an MCP server that exposes mise functionality to AI assistants over stdin/stdout using JSON-RPC protocol.

The MCP server provides access to:

Note: This is primarily intended for integration with AI assistants like Claude, Cursor, or other tools that support the Model Context Protocol.

**Examples:**

Example 1 (json):
```json
# Start the MCP server (typically used by AI assistant tools)
$ mise mcp

# Example integration with Claude Desktop (add to claude_desktop_config.json):
{
  "mcpServers": {
    "mise": {
      "command": "mise",
      "args": ["mcp"]
    }
  }
}

# Interactive testing with JSON-RPC commands:
$ echo '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2024-11-05","capabilities":{},"clientInfo":{"name":"test","version":"1.0"}}}' | mise mcp

# Resources you can query:
- mise://tools - List active tools
- mise://tools?include_inactive=true - List all installed tools
- mise://tasks - List all tasks
- mise://env - List environment variables
- mise://config - Show configuration info
```

---

## mise env ​

**URL:** https://mise.jdx.dev/cli/env.html

**Contents:**
- mise env ​
- Arguments ​
  - [TOOL@VERSION]… ​
- Flags ​
  - -D --dotenv ​
  - -J --json ​
  - -s --shell <SHELL> ​
  - --json-extended ​
  - --redacted ​
  - --values ​

Exports env vars to activate mise a single time

Use this if you don't want to permanently install mise. It's not necessary to use this if you have mise activate in your shell rc file.

Output in dotenv format

Output in JSON format

Shell type to generate environment variables for

Output in JSON format with additional information (source, tool)

Only show redacted environment variables

Only show values of environment variables

**Examples:**

Example 1 (unknown):
```unknown
eval "$(mise env -s bash)"
eval "$(mise env -s zsh)"
mise env -s fish | source
execx($(mise env -s xonsh))
```

---

## mise outdated ​

**URL:** https://mise.jdx.dev/cli/outdated.html

**Contents:**
- mise outdated ​
- Arguments ​
  - [TOOL@VERSION]… ​
- Flags ​
  - -J --json ​
  - -l --bump ​
  - --no-header ​

Shows outdated tool versions

See mise upgrade to upgrade these versions.

Tool(s) to show outdated versions for e.g.: node@20 python@3.10 If not specified, all tools in global and local configs will be shown

Output in JSON format

Compares against the latest versions available, not what matches the current config

For example, if you have node = "20" in your config by default mise outdated will only show other 20.x versions, not 21.x or 22.x versions.

Using this flag, if there are 21.x or newer versions it will display those instead of 20.x.

Don't show table header

**Examples:**

Example 1 (json):
```json
$ mise outdated
Plugin  Requested  Current  Latest
python  3.11       3.11.0   3.11.1
node    20         20.0.0   20.1.0

$ mise outdated node
Plugin  Requested  Current  Latest
node    20         20.0.0   20.1.0

$ mise outdated --json
{"python": {"requested": "3.11", "current": "3.11.0", "latest": "3.11.1"}, ...}
```

---

## mise config generate ​

**URL:** https://mise.jdx.dev/cli/config/generate.html

**Contents:**
- mise config generate ​
- Flags ​
  - -o --output <OUTPUT> ​
  - -t --tool-versions <TOOL_VERSIONS> ​

Generate a mise.toml file

Output to file instead of stdout

Path to a .tool-versions file to import tools from

**Examples:**

Example 1 (unknown):
```unknown
mise cf generate > mise.toml
mise cf generate --output=mise.toml
```

---

## mise install-into ​

**URL:** https://mise.jdx.dev/cli/install-into.html

**Contents:**
- mise install-into ​
- Arguments ​
  - <TOOL@VERSION> ​
  - <PATH> ​

Install a tool version to a specific path

Used for building a tool to a directory for use outside of mise

Tool to install e.g.: node@20

Path to install the tool into

**Examples:**

Example 1 (markdown):
```markdown
# install node@20.0.0 into ./mynode
$ mise install-into node@20.0.0 ./mynode && ./mynode/bin/node -v
20.0.0
```

---

## mise unset ​

**URL:** https://mise.jdx.dev/cli/unset.html

**Contents:**
- mise unset ​
- Arguments ​
  - [ENV_KEY]… ​
- Flags ​
  - -f --file <FILE> ​
  - -g --global ​

Remove environment variable(s) from the config file.

By default, this command modifies mise.toml in the current directory.

Environment variable(s) to remove e.g.: NODE_ENV

Specify a file to use instead of mise.toml

Use the global config file

**Examples:**

Example 1 (sql):
```sql
# Remove NODE_ENV from the current directory's config
$ mise unset NODE_ENV

# Remove NODE_ENV from the global config
$ mise unset NODE_ENV -g
```

---

## mise tool ​

**URL:** https://mise.jdx.dev/cli/tool.html

**Contents:**
- mise tool ​
- Arguments ​
  - <TOOL> ​
- Flags ​
  - -J --json ​
  - --active ​
  - --backend ​
  - --config-source ​
  - --description ​
  - --installed ​

Gets information about a tool

Tool name to get information about

Output in JSON format

Only show active versions

Only show backend field

Only show config source

Only show description field

Only show installed versions

Only show requested versions

Only show tool options

**Examples:**

Example 1 (swift):
```swift
$ mise tool node
Backend:            core
Installed Versions: 20.0.0 22.0.0
Active Version:     20.0.0
Requested Version:  20
Config Source:      ~/.config/mise/mise.toml
Tool Options:       [none]
```

---

## mise en ​

**URL:** https://mise.jdx.dev/cli/en.html

**Contents:**
- mise en ​
- Arguments ​
  - [DIR] ​
- Flags ​
  - -s --shell <SHELL> ​

Starts a new shell with the mise environment built from the current configuration

This is an alternative to mise activate that allows you to explicitly start a mise session. It will have the tools and environment variables in the configs loaded. Note that changing directories will not update the mise environment.

Directory to start the shell in

**Examples:**

Example 1 (unknown):
```unknown
$ mise en .
$ node -v
v20.0.0

Skip loading bashrc:
$ mise en -s "bash --norc"

Skip loading zshrc:
$ mise en -s "zsh -f"
```

---

## mise prune ​

**URL:** https://mise.jdx.dev/cli/prune.html

**Contents:**
- mise prune ​
- Arguments ​
  - [INSTALLED_TOOL]… ​
- Flags ​
  - -n --dry-run ​
  - --configs ​
  - --tools ​

Delete unused versions of tools

mise tracks which config files have been used in ~/.local/state/mise/tracked-configs Versions which are no longer the latest specified in any of those configs are deleted. Versions installed only with environment variables MISE_<PLUGIN>_VERSION will be deleted, as will versions only referenced on the command line mise exec <PLUGIN>@<VERSION>.

You can list prunable tools with mise ls --prunable

Prune only these tools

Do not actually delete anything

Prune only tracked and trusted configuration links that point to non-existent configurations

Prune only unused versions of tools

**Examples:**

Example 1 (unknown):
```unknown
$ mise prune --dry-run
rm -rf ~/.local/share/mise/versions/node/20.0.0
rm -rf ~/.local/share/mise/versions/node/20.0.1
```

---

## mise plugins ​

**URL:** https://mise.jdx.dev/cli/plugins.html

**Contents:**
- mise plugins ​
- Flags ​
  - -c --core ​
  - -u --urls ​
  - --user ​
- Subcommands ​

The built-in plugins only Normally these are not shown

Show the git url for each plugin e.g.: https://github.com/asdf-vm/asdf-nodejs.git

List installed plugins

This is the default behavior but can be used with --core to show core and user plugins

---

## mise generate git-pre-commit ​

**URL:** https://mise.jdx.dev/cli/generate/git-pre-commit.html

**Contents:**
- mise generate git-pre-commit ​
- Flags ​
  - -t --task <TASK> ​
  - -w --write ​
  - --hook <HOOK> ​

Generate a git pre-commit hook

This command generates a git pre-commit hook that runs a mise task like mise run pre-commit when you commit changes to your repository.

Staged files are passed to the task as STAGED.

For more advanced pre-commit functionality, see mise's sister project: https://hk.jdx.dev/

The task to run when the pre-commit hook is triggered

write to .git/hooks/pre-commit and make it executable

Which hook to generate (saves to .git/hooks/$hook)

**Examples:**

Example 1 (unknown):
```unknown
mise generate git-pre-commit --write --task=pre-commit
git commit -m "feat: add new feature" # runs `mise run pre-commit`
```

---

## mise doctor path ​

**URL:** https://mise.jdx.dev/cli/doctor/path.html

**Contents:**
- mise doctor path ​
- Flags ​
  - -f --full ​

Print the current PATH entries mise is providing

Print all entries including those not provided by mise

**Examples:**

Example 1 (unknown):
```unknown
Get the current PATH entries mise is providing
$ mise path
/home/user/.local/share/mise/installs/node/24.0.0/bin
/home/user/.local/share/mise/installs/rust/1.90.0/bin
/home/user/.local/share/mise/installs/python/3.10.0/bin
```

---

## mise latest ​

**URL:** https://mise.jdx.dev/cli/latest.html

**Contents:**
- mise latest ​
- Arguments ​
  - <TOOL@VERSION> ​
- Flags ​
  - -i --installed ​

Gets the latest available version for a plugin

Supports prefixes such as node@20 to get the latest version of node 20.

Tool to get the latest version of

Show latest installed instead of available version

**Examples:**

Example 1 (python):
```python
$ mise latest node@20  # get the latest version of node 20
20.0.0

$ mise latest node     # get the latest stable version of node
20.0.0
```

---

## mise sync ​

**URL:** https://mise.jdx.dev/cli/sync.html

**Contents:**
- mise sync ​
- Subcommands ​

Synchronize tools from other version managers with mise

---

## mise trust ​

**URL:** https://mise.jdx.dev/cli/trust.html

**Contents:**
- mise trust ​
- Arguments ​
  - [CONFIG_FILE] ​
- Flags ​
  - -a --all ​
  - --ignore ​
  - --show ​
  - --untrust ​

Marks a config file as trusted

This means mise will parse the file with potentially dangerous features enabled.

The config file to trust

Trust all config files in the current directory and its parents

Do not trust this config and ignore it in the future

Show the trusted status of config files from the current directory and its parents. Does not trust or untrust any files.

No longer trust this config, will prompt in the future

**Examples:**

Example 1 (markdown):
```markdown
# trusts ~/some_dir/mise.toml
$ mise trust ~/some_dir/mise.toml

# trusts mise.toml in the current or parent directory
$ mise trust
```

---

## mise sync python ​

**URL:** https://mise.jdx.dev/cli/sync/python.html

**Contents:**
- mise sync python ​
- Flags ​
  - --pyenv ​
  - --uv ​

Symlinks all tool versions from an external tool into mise

For example, use this to import all pyenv installs into mise

This won't overwrite any existing installs but will overwrite any existing symlinks

Get tool versions from pyenv

Sync tool versions with uv (2-way sync)

**Examples:**

Example 1 (python):
```python
pyenv install 3.11.0
mise sync python --pyenv
mise use -g python@3.11.0 - uses pyenv-provided python

uv python install 3.11.0
mise install python@3.10.0
mise sync python --uv
mise x python@3.11.0 -- python -V - uses uv-provided python
uv run -p 3.10.0 -- python -V - uses mise-provided python
```

---

## mise cache prune ​

**URL:** https://mise.jdx.dev/cli/cache/prune.html

**Contents:**
- mise cache prune ​
- Arguments ​
  - [PLUGIN]… ​
- Flags ​
  - -v --verbose… ​
  - --dry-run ​

Removes stale mise cache files

By default, this command will remove files that have not been accessed in 30 days. Change this with the MISE_CACHE_PRUNE_AGE environment variable.

Plugin(s) to clear cache for e.g.: node, python

Just show what would be pruned

---

## mise generate devcontainer ​

**URL:** https://mise.jdx.dev/cli/generate/devcontainer.html

**Contents:**
- mise generate devcontainer ​
- Flags ​
  - -i --image <IMAGE> ​
  - -m --mount-mise-data ​
  - -n --name <NAME> ​
  - -w --write ​

Generate a devcontainer to execute mise

The image to use for the devcontainer

Bind the mise-data-volume to the devcontainer

The name of the devcontainer

write to .devcontainer/devcontainer.json

**Examples:**

Example 1 (unknown):
```unknown
mise generate devcontainer
```

---

## mise generate tool-stub ​

**URL:** https://mise.jdx.dev/cli/generate/tool-stub.html

**Contents:**
- mise generate tool-stub ​
- Arguments ​
  - <OUTPUT> ​
- Flags ​
  - -b --bin <BIN> ​
  - --bootstrap ​
  - --bootstrap-version <BOOTSTRAP_VERSION> ​
  - --fetch ​
  - --http <HTTP> ​
  - --platform-bin… <PLATFORM_BIN> ​

Generate a tool stub for HTTP-based tools

This command generates tool stubs that can automatically download and execute tools from HTTP URLs. It can detect checksums, file sizes, and binary paths automatically by downloading and analyzing the tool.

When generating stubs with platform-specific URLs, the command will append new platforms to existing stub files rather than overwriting them. This allows you to incrementally build cross-platform tool stubs.

Output file path for the tool stub

Binary path within the extracted archive

If not specified and the archive is downloaded, will auto-detect the most likely binary

Wrap stub in a bootstrap script that installs mise if not already present

When enabled, generates a bash script that:

Specify mise version for the bootstrap script

By default, uses the latest version from the install script. Use this to pin to a specific version (e.g., "2025.1.0").

Fetch checksums and sizes for an existing tool stub file

This reads an existing stub file and fills in any missing checksum/size fields by downloading the files. URLs must already be present in the stub.

HTTP backend type to use

Platform-specific binary paths in the format platform:path

Examples: --platform-bin windows-x64:tool.exe --platform-bin linux-x64:bin/tool

Platform-specific URLs in the format platform:url or just url (auto-detect platform)

When the output file already exists, new platforms will be appended to the existing platforms table. Existing platform URLs will be updated if specified again.

If only a URL is provided (without platform:), the platform will be automatically detected from the URL filename.

Examples: --platform-url linux-x64:https://... --platform-url https://nodejs.org/dist/v22.17.1/node-v22.17.1-darwin-arm64.tar.gz

Skip downloading for checksum and binary path detection (faster but less informative)

URL for downloading the tool

Example: https://github.com/owner/repo/releases/download/v2.0.0/tool-linux-x64.tar.gz

**Examples:**

Example 1 (sql):
```sql
Generate a tool stub for a single URL:
$ mise generate tool-stub ./bin/gh --url "https://github.com/cli/cli/releases/download/v2.336.0/gh_2.336.0_linux_amd64.tar.gz"

Generate a tool stub with platform-specific URLs:
$ mise generate tool-stub ./bin/rg \
    --platform-url linux-x64:https://github.com/BurntSushi/ripgrep/releases/download/14.0.3/ripgrep-14.0.3-x86_64-unknown-linux-musl.tar.gz \
    --platform-url darwin-arm64:https://github.com/BurntSushi/ripgrep/releases/download/14.0.3/ripgrep-14.0.3-aarch64-apple-darwin.tar.gz

Append additional platforms to an existing stub:
$ mise generate tool-stub ./bin/rg \
    --platform-url linux-x64:https://example.com/rg-linux.tar.gz
$ mise generate tool-stub ./bin/rg \
    --platform-url darwin-arm64:https://example.com/rg-darwin.tar.gz
# The stub now contains both platforms

Use auto-detection for platform from URL:
$ mise generate tool-stub ./bin/node \
    --platform-url https://nodejs.org/dist/v22.17.1/node-v22.17.1-darwin-arm64.tar.gz
# Platform 'macos-arm64' will be auto-detected from the URL

Generate with platform-specific binary paths:
$ mise generate tool-stub ./bin/tool \
    --platform-url linux-x64:https://example.com/tool-linux.tar.gz \
    --platform-url windows-x64:https://example.com/tool-windows.zip \
    --platform-bin windows-x64:tool.exe

Generate without downloading (faster):
$ mise generate tool-stub ./bin/tool --url "https://example.com/tool.tar.gz" --skip-download

Fetch checksums for an existing stub:
$ mise generate tool-stub ./bin/jq --fetch
# This will read the existing stub and download files to fill in any missing checksums/sizes

Generate a bootstrap stub that installs mise if needed:
$ mise generate tool-stub ./bin/tool --url "https://example.com/tool.tar.gz" --bootstrap
# The stub will check for mise and install it automatically before running the tool

Generate a bootstrap stub with a pinned mise version:
$ mise generate tool-stub ./bin/tool --url "https://example.com/tool.tar.gz" --bootstrap --bootstrap-version 2025.1.0
```

---

## mise search ​

**URL:** https://mise.jdx.dev/cli/search.html

**Contents:**
- mise search ​
- Arguments ​
  - [NAME] ​
- Flags ​
  - -i --interactive ​
  - -m --match-type <MATCH_TYPE> ​
  - --no-header ​

Search for tools in the registry

This command searches a tool in the registry.

By default, it will show all tools that fuzzy match the search term. For non-fuzzy matches, use the --match-type flag.

The tool to search for

Show interactive search

Match type: equal, contains, or fuzzy

Don't display headers

**Examples:**

Example 1 (julia):
```julia
$ mise search jq
Tool  Description
jq    Command-line JSON processor. https://github.com/jqlang/jq
jqp   A TUI playground to experiment with jq. https://github.com/noahgorstein/jqp
jiq   jid on jq - interactive JSON query tool using jq expressions. https://github.com/fiatjaf/jiq
gojq  Pure Go implementation of jq. https://github.com/itchyny/gojq

$ mise search --interactive
Tool
Search a tool
❯ jq    Command-line JSON processor. https://github.com/jqlang/jq
  jqp   A TUI playground to experiment with jq. https://github.com/noahgorstein/jqp
  jiq   jid on jq - interactive JSON query tool using jq expressions. https://github.com/fiatjaf/jiq
  gojq  Pure Go implementation of jq. https://github.com/itchyny/gojq
/jq 
esc clear filter • enter confirm
```

---

## mise settings ​

**URL:** https://mise.jdx.dev/cli/settings.html

**Contents:**
- mise settings ​
- Arguments ​
  - [SETTING] ​
  - [VALUE] ​
- Global Flags ​
  - -l --local ​
- Flags ​
  - -a --all ​
  - -J --json ​
  - -T --toml ​

Show current settings

This is the contents of ~/.config/mise/config.toml

Note that aliases are also stored in this file but managed separately with mise tool-alias

Use the local config file instead of the global one

Output in JSON format

Output in TOML format

Output in JSON format with sources

**Examples:**

Example 1 (markdown):
```markdown
# list all settings
$ mise settings

# get the value of the setting "always_keep_download"
$ mise settings always_keep_download

# set the value of the setting "always_keep_download" to "true"
$ mise settings always_keep_download=true

# set the value of the setting "node.mirror_url" to "https://npm.taobao.org/mirrors/node"
$ mise settings node.mirror_url https://npm.taobao.org/mirrors/node
```

---

## mise generate bootstrap ​

**URL:** https://mise.jdx.dev/cli/generate/bootstrap.html

**Contents:**
- mise generate bootstrap ​
- Flags ​
  - -l --localize ​
  - -V --version <VERSION> ​
  - -w --write <WRITE> ​
  - --localized-dir <LOCALIZED_DIR> ​

Generate a script to download+execute mise

This is designed to be used in a project where contributors may not have mise installed.

Sandboxes mise internal directories like MISE_DATA_DIR and MISE_CACHE_DIR into a .mise directory in the project

This is necessary if users may use a different version of mise outside the project.

Specify mise version to fetch

instead of outputting the script to stdout, write to a file and make it executable

Directory to put localized data into

**Examples:**

Example 1 (unknown):
```unknown
mise generate bootstrap >./bin/mise
chmod +x ./bin/mise
./bin/mise install – automatically downloads mise to .mise if not already installed
```

---

## mise sync ruby ​

**URL:** https://mise.jdx.dev/cli/sync/ruby.html

**Contents:**
- mise sync ruby ​
- Flags ​
  - --brew ​

Symlinks all ruby tool versions from an external tool into mise

Get tool versions from Homebrew

**Examples:**

Example 1 (unknown):
```unknown
brew install ruby
mise sync ruby --brew
mise use -g ruby - Use the latest version of Ruby installed by Homebrew
```

---

## mise shell-alias unset ​

**URL:** https://mise.jdx.dev/cli/shell-alias/unset.html

**Contents:**
- mise shell-alias unset ​
- Arguments ​
  - <shell_alias> ​

Removes a shell alias

This modifies the contents of ~/.config/mise/config.toml

**Examples:**

Example 1 (unknown):
```unknown
mise shell-alias unset ll
```

---

## mise generate task-stubs ​

**URL:** https://mise.jdx.dev/cli/generate/task-stubs.html

**Contents:**
- mise generate task-stubs ​
- Flags ​
  - -d --dir <DIR> ​
  - -m --mise-bin <MISE_BIN> ​

Generates shims to run mise tasks

By default, this will build shims like ./bin/<task>. These can be paired with mise generate bootstrap so contributors to a project can execute mise tasks without installing mise into their system.

Directory to create task stubs inside of

Path to a mise bin to use when running the task stub.

Use --mise-bin=./bin/mise to use a mise bin generated from mise generate bootstrap

**Examples:**

Example 1 (bash):
```bash
$ mise tasks add test -- echo 'running tests'
$ mise generate task-stubs
$ ./bin/test
running tests
```

---

## mise config ​

**URL:** https://mise.jdx.dev/cli/config.html

**Contents:**
- mise config ​
- Flags ​
  - -J --json ​
  - --no-header ​
  - --tracked-configs ​
- Subcommands ​

Output in JSON format

Do not print table header

List all tracked config files

**Examples:**

Example 1 (unknown):
```unknown
$ mise config ls
Path                        Tools
~/.config/mise/config.toml  pitchfork
~/src/mise/mise.toml        actionlint, bun, cargo-binstall, cargo:cargo-edit, cargo:cargo-insta
```

---

## mise tool-stub ​

**URL:** https://mise.jdx.dev/cli/tool-stub.html

**Contents:**
- mise tool-stub ​
- Arguments ​
  - <FILE> ​
  - [ARGS]… ​

Tool stubs are executable files containing TOML configuration that specify which tool to run and how to run it. They provide a convenient way to create portable, self-contained executables that automatically manage tool installation and execution.

A tool stub consists of: - A shebang line: #!/usr/bin/env -S mise tool-stub - TOML configuration specifying the tool, version, and options - Optional comments describing the tool's purpose

Example stub file: #!/usr/bin/env -S mise tool-stub # Node.js v20 development environment

tool = "node" version = "20.0.0" bin = "node"

The stub will automatically install the specified tool version if missing and execute it with any arguments passed to the stub.

For more information, see: https://mise.jdx.dev/dev-tools/tool-stubs.html

Path to the TOML tool stub file to execute

The stub file must contain TOML configuration specifying the tool and version to run. At minimum, it should specify a 'version' field. Other common fields include 'tool', 'bin', and backend-specific options.

Arguments to pass to the tool

All arguments after the stub file path will be forwarded to the underlying tool. Use '--' to separate mise arguments from tool arguments if needed.

---

## mise settings add ​

**URL:** https://mise.jdx.dev/cli/settings/add.html

**Contents:**
- mise settings add ​
- Arguments ​
  - <SETTING> ​
  - <VALUE> ​
- Flags ​
  - -l --local ​

Adds a setting to the configuration file

Used with an array setting, this will append the value to the array. This modifies the contents of ~/.config/mise/config.toml

Use the local config file instead of the global one

**Examples:**

Example 1 (unknown):
```unknown
mise settings add disable_hints python_multi
```

---

## mise settings set ​

**URL:** https://mise.jdx.dev/cli/settings/set.html

**Contents:**
- mise settings set ​
- Arguments ​
  - <SETTING> ​
  - <VALUE> ​
- Flags ​
  - -l --local ​

This modifies the contents of ~/.config/mise/config.toml by default. With --local, modifies the local config file instead. See https://mise.jdx.dev/configuration.html#target-file-for-write-operations

Use the local config file instead of the global one

**Examples:**

Example 1 (unknown):
```unknown
mise settings idiomatic_version_file=true
```

---

## mise tool-alias ​

**URL:** https://mise.jdx.dev/cli/tool-alias.html

**Contents:**
- mise tool-alias ​
- Flags ​
  - -p --plugin <PLUGIN> ​
  - --no-header ​
- Subcommands ​

Manage tool version aliases.

filter aliases by plugin

Don't show table header

---

## mise link ​

**URL:** https://mise.jdx.dev/cli/link.html

**Contents:**
- mise link ​
- Arguments ​
  - <TOOL@VERSION> ​
  - <PATH> ​
- Flags ​
  - -f --force ​

Symlinks a tool version into mise

Use this for adding installs either custom compiled outside mise or built with a different tool.

Tool name and version to create a symlink for

The local path to the tool version e.g.: ~/.nvm/versions/node/v20.0.0

Overwrite an existing tool version if it exists

**Examples:**

Example 1 (markdown):
```markdown
# build node-20.0.0 with node-build and link it into mise
$ node-build 20.0.0 ~/.nodes/20.0.0
$ mise link node@20.0.0 ~/.nodes/20.0.0

# have mise use the node version provided by Homebrew
$ brew install node
$ mise link node@brew $(brew --prefix node)
$ mise use node@brew
```

---
