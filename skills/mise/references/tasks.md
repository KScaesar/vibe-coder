# Mise - Tasks

**Pages:** 15

---

## Task System Architecture ​

**URL:** https://mise.jdx.dev/tasks/architecture.html

**Contents:**
- Task System Architecture ​
- Task Dependency System ​
  - Dependency Graph Resolution ​
  - Dependency Types ​
    - depends - Prerequisites ​
    - depends_post - Cleanup Tasks ​
    - wait_for - Soft Dependencies ​
- Parallel Execution Engine ​
  - Job Control ​
  - Example Execution Flow ​

Understanding how mise's task system works helps you write more efficient tasks and troubleshoot dependency issues.

mise uses a sophisticated dependency graph system to manage task execution order and parallelism. This ensures tasks run in the correct order while maximizing performance through parallel execution.

When you run mise run build, mise creates a directed acyclic graph (DAG) of all tasks and their dependencies:

This graph ensures that:

mise supports three types of task dependencies:

Tasks that must complete successfully before this task runs:

Tasks that run after this task completes (whether successful or failed):

Tasks that should run first if they're in the current execution, but don't fail if they're not available:

mise executes tasks in parallel up to the configured job limit:

The default is 4 parallel jobs, but you can configure this globally:

Execution with --jobs 2:

mise discovers tasks from multiple sources in this order:

When you run mise run build, mise:

Tasks are inherited from parent directories but can be overridden:

In frontend/, you have access to: lint (inherited), test (overridden), build (inherited), bundle (local).

Use task arguments for conditional behavior:

Tasks can specify dependencies at runtime:

Reference tasks from other directories:

Tasks can skip execution if sources haven't changed:

mise will only run the task if:

Use mise run --force to ignore source/output checking:

Use mise watch for continuous development:

This automatically reruns tasks when their source files change.

Circular Dependencies:

Solution: Remove the circular reference or use wait_for instead of depends.

Missing Dependencies:

Solution: Define the missing task or remove the dependency.

Slow Parallel Execution:

The task architecture is designed to scale from simple single-task projects to complex multi-service applications with intricate build dependencies.

**Examples:**

Example 1 (json):
```json
[tasks.test]
depends = ["lint", "build"]
run = "npm test"
```

Example 2 (json):
```json
[tasks.deploy]
depends = ["build", "test"]
depends_post = ["cleanup", "notify"]
run = "kubectl apply -f deployment.yaml"
```

Example 3 (json):
```json
[tasks.integration-test]
wait_for = ["start-services"]  # Only waits if start-services is also being run
run = "npm run test:integration"
```

Example 4 (unknown):
```unknown
mise run test --jobs 8        # Use 8 parallel jobs
mise run test -j 1            # Force sequential execution
```

---

## Running Tasks ​

**URL:** https://mise.jdx.dev/tasks/running-tasks.html

**Contents:**
- Running Tasks ​
- Task Grouping ​
- Wildcards ​
  - Examples ​
- Running on file changes ​
- Watching files ​
- mise run shorthand ​
- Execution order ​

See available tasks with mise tasks. To show tasks hidden with property hide=true, use the option --hidden.

List dependencies of tasks with mise tasks deps [tasks]....

Run a task with mise tasks run <task>, mise run <task>, mise r <task>, or just mise <task>—however that last one you should never put into scripts or documentation because if mise ever adds a command with that name in a future mise version, the task will be shadowed and must be run with one of the other forms.

Most mise users will have an alias for mise run like alias mr='mise run'.

By default, tasks will execute with a maximum of 4 parallel jobs. Customize this with the --jobs option, jobs setting or MISE_JOBS environment variable. The output normally will be by line, prefixed with the task label. By printing line-by-line we avoid interleaving output from parallel executions. However, if --jobs == 1, the output will be set to interleave.

To just print stdout/stderr directly, use --interleave, the task_output setting, or MISE_TASK_OUTPUT=interleave.

Stdin is not read by default. To enable this, set raw = true on the task that needs it. This will prevent it running in parallel with any other task—a RWMutex will get a write lock in this case. This also prevents redactions applied to the output.

Extra arguments will be passed to the task, for example, if we want to run in release mode:

If there are multiple commands, the args are only passed to the last command.

You can define arguments/flags for tasks which will provide validation, parsing, autocomplete, and documentation.

Autocomplete will work automatically for tasks if the usage CLI is installed and mise completions are working.

Markdown documentation can be generated with mise generate task-docs.

Multiple tasks/arguments can be separated with this ::: delimiter:

mise will run the task named "default" if no task is specified—and you've created one named "default". You can also alias a different task to "default".

Tasks can be grouped semantically by using name prefixes separated with :s. For example all testing related tasks may begin with test:. Nested grouping can also be used to further refine groups and simplify pattern matching. For example running mise run test:**:local will matchtest:units:local, test:integration:local and test:e2e:happy:local (See Wildcards for more information).

Glob style wildcards are supported when running tasks or specifying tasks dependencies.

Available Wildcard Patterns:

mise run generate:{completions,docs:*}

And with dependencies:

It's often handy to only execute a task if the files it uses changes. For example, we might only want to run cargo build if an ".rs" file changes. This can be done with the following config:

Now if target/debug/mycli is newer than Cargo.toml or any ".rs" file, the task will be skipped. This uses last modified timestamps. It wouldn't be hard to add checksum support.

Run a task when the source changes with mise watch

Currently, this just shells out to watchexec (which you can install however you want including with mise: mise use -g watchexec@latest. This may change in the future.)

Tasks can be run with mise run <TASK> or mise <TASK>—if the name doesn't conflict with a mise command. Because mise may later add a command with a conflicting name, it's recommended to use mise run <TASK> in scripts and documentation.

You can use depends, wait_for and depends_post to control the order of execution.

This will ensure that the build task is run before the test task.

You can also define a mise task to run other tasks in parallel or in series:

**Examples:**

Example 1 (unknown):
```unknown
mise run build --release
```

Example 2 (julia):
```julia
mise run build arg1 arg2 ::: test arg3 arg4
```

Example 3 (json):
```json
[tasks."lint:eslint"] # using a ":" means we need to add quotes
run = "eslint ."
[tasks."lint:prettier"]
run = "prettier --check ."
[tasks.lint]
depends = ["lint:*"]
wait_for = ["render"] # does not add as a dependency, but if it is already running, wait for it to finish
```

Example 4 (json):
```json
[tasks.build]
description = 'Build the CLI'
run = "cargo build"
sources = ['Cargo.toml', 'src/**/*.rs'] # skip running if these files haven't changed
outputs = ['target/debug/mycli']
```

---

## Task Arguments ​

**URL:** https://mise.jdx.dev/tasks/task-arguments.html

**Contents:**
- Task Arguments ​
- Recommended Methods ​
  - 1. Usage Field (Preferred) ​
    - Quick Example ​
- Complete Usage Specification Reference ​
  - Positional Arguments (arg) ​
    - Basic Syntax ​
    - With Defaults ​
    - Variadic Arguments ​
    - Environment Variable Backing ​

Task arguments allow you to pass parameters to tasks, making them more flexible and reusable. There are three ways to define task arguments in mise, but only two are recommended for current use.

The usage field is the recommended approach for defining task arguments. It provides a clean, declarative syntax that works with both TOML tasks and file tasks.

Arguments defined in the usage field are automatically available as environment variables prefixed with usage_:

In addition to environment variables, usage values are available inside Tera templates in task run scripts via a usage map:

The usage map uses snake_case argument/flag names as keys (just like the usage_ environment variables). Names with - are converted to _, so a flag like --dry-run becomes available as {{ usage.dry_run }} and $usage_dry_run. Variadic arguments/flags are exposed as arrays and can be used with Tera's for loops and filters like length. The usage map is separate from the deprecated Tera template functions (arg(), option(), flag()) described later on this page—you should not mix the two approaches in the same task.

Positional arguments are defined with arg and must be provided in order.

Priority order: CLI argument > Environment variable > Default value

Flags can be defined as booleans or as accepting values.

Custom completion can be defined for any argument or flag by name:

Output format (split on : for value and description):

For detailed help text, use multi-line format:

Hide arguments from help output (useful for deprecated or internal options):

For file tasks, you can define arguments directly in the file using special #MISE or #USAGE comment syntax:

Use #MISE (uppercase, recommended) or #USAGE for defining arguments in file tasks. # [MISE] or # [USAGE] are also accepted as workarounds for formatters.

When accessing usage-defined variables in bash scripts, use parameter expansion syntax to help shellcheck understand these variables and provide default values for boolean flags.

Use ${usage_var?} since usage guarantees they'll be set:

Use ${usage_var:-false} to provide a default value:

Use ${usage_var:?} to ensure non-empty values:

Use ${usage_var:+value} to pass flags only when set:

These expansions help shellcheck understand your script and prevent warnings about potentially unset variables while maintaining proper error handling.

Deprecated - Removal in 2026.11.0

The Tera template method for defining task arguments is deprecated and will be removed in mise 2026.11.0.

Why it's being removed:

Migration required: Please migrate to the usage field method before 2026.11.0.

Opt-out setting: If you want to disable the two-pass parsing behavior immediately (before removal), you can set:

Or via environment variable: MISE_TASK_DISABLE_SPEC_FROM_RUN_SCRIPTS=1

When enabled, mise will only use the usage field for spec generation, ignoring any arg(), option(), or flag() functions in run scripts. See Settings for more details.

Previously, you could define arguments inline in run scripts using Tera template functions:

Problems with this approach:

Empty strings during parsing: During spec collection (first pass), template functions return empty strings, so you can't use them in templates like:

Escaping complexity: Different shell types require different escaping:

No help generation: Doesn't generate proper --help output

Here's how to migrate from Tera templates to the usage field:

**Examples:**

Example 1 (bash):
```bash
[tasks.deploy]
description = "Deploy application"
usage = '''
arg "<environment>" help="Target environment" {
  choices "dev" "staging" "prod"
}
flag "-v --verbose" help="Enable verbose output"
flag "--region <region>" help="AWS region" default="us-east-1" env="AWS_REGION"
'''

run = '''
echo "Deploying to ${usage_environment?} in ${usage_region?}"
[[ "${usage_verbose?}" == "true" ]] && set -x
./deploy.sh "${usage_environment?}" "${usage_region?}"
'''
```

Example 2 (markdown):
```markdown
# Execute with arguments
$ mise run deploy staging --verbose --region us-west-2

# Inside the task, these are available as:
# $usage_environment = "staging"
# $usage_verbose = "true"
# $usage_region = "us-west-2"
```

Example 3 (json):
```json
[tasks.deploy]
description = "Deploy application"
usage = '''
arg "<environment>" help="Target environment"
flag "-v --verbose" help="Enable verbose output"
flag "--region <region>" help="AWS region" default="us-east-1"
'''
run = '''
echo "Deploying to {{ usage.environment }} in {{ usage.region }}"
{% if usage.verbose %}
  echo "Verbose mode enabled"
{% endif %}
'''
```

Example 4 (yaml):
```yaml
$ mise run deploy --help
Deploy application

Usage: deploy <environment> [OPTIONS]

Arguments:
  <environment>  Target environment [possible values: dev, staging, prod]

Options:
  -v, --verbose          Enable verbose output
      --region <region>  AWS region [env: AWS_REGION] [default: us-east-1]
  -h, --help            Print help
```

---

## mise tasks validate ​

**URL:** https://mise.jdx.dev/cli/tasks/validate.html

**Contents:**
- mise tasks validate ​
- Arguments ​
  - [TASKS]… ​
- Flags ​
  - --errors-only ​
  - --json ​

Validate tasks for common errors and issues

Tasks to validate If not specified, validates all tasks

Only show errors (skip warnings)

Output validation results in JSON format

The validate command performs the following checks:

• Circular Dependencies: Detects dependency cycles • Missing References: Finds references to non-existent tasks • Usage Spec Parsing: Validates #USAGE directives and specs • Timeout Format: Checks timeout values are valid durations • Alias Conflicts: Detects duplicate aliases across tasks • File Existence: Verifies file-based tasks exist • Directory Templates: Validates directory paths and templates • Shell Commands: Checks shell executables exist • Glob Patterns: Validates source and output patterns • Run Entries: Ensures tasks reference valid dependencies

**Examples:**

Example 1 (markdown):
```markdown
# Validate all tasks
$ mise tasks validate

# Validate specific tasks
$ mise tasks validate build test

# Output results as JSON
$ mise tasks validate --json

# Only show errors (skip warnings)
$ mise tasks validate --errors-only
```

---

## mise tasks add ​

**URL:** https://mise.jdx.dev/cli/tasks/add.html

**Contents:**
- mise tasks add ​
- Arguments ​
  - <TASK> ​
  - [-- RUN]… ​
- Flags ​
  - -a --alias… <ALIAS> ​
  - -d --depends… <DEPENDS> ​
  - -D --dir <DIR> ​
  - -f --file ​
  - -H --hide ​

Adds a task to the local mise.toml file. See https://mise.jdx.dev/configuration.html#target-file-for-write-operations

Other names for the task

Add dependencies to the task

Run the task in a specific directory

Create a file task instead of a toml task

Hide the task from mise tasks and completions

Do not print the command before running

Directly connect stdin/stdout/stderr

Glob patterns of files this task uses as input

Wait for these tasks to complete if they are to run

Dependencies to run after the task runs

Description of the task

Glob patterns of files this task creates, to skip if they are not modified

Command to run on windows

Run the task in a specific shell

Do not print the command or its output

**Examples:**

Example 1 (bash):
```bash
mise tasks add pre-commit --depends "test" --depends "render" -- echo pre-commit
```

---

## mise tasks edit ​

**URL:** https://mise.jdx.dev/cli/tasks/edit.html

**Contents:**
- mise tasks edit ​
- Arguments ​
  - <TASK> ​
- Flags ​
  - -p --path ​

Edit a task with $EDITOR

The task will be created as a standalone script if it does not already exist.

Display the path to the task instead of editing it

**Examples:**

Example 1 (unknown):
```unknown
mise tasks edit build
mise tasks edit test
```

---

## mise tasks ls ​

**URL:** https://mise.jdx.dev/cli/tasks/ls.html

**Contents:**
- mise tasks ls ​
- Flags ​
  - -g --global ​
  - -J --json ​
  - -l --local ​
  - -x --extended ​
  - --all ​
  - --hidden ​
  - --no-header ​
  - --sort <COLUMN> ​

List available tasks to execute These may be included from the config file or from the project's .mise/tasks directory mise will merge all tasks from all parent directories into this list.

So if you have global tasks in ~/.config/mise/tasks/* and project-specific tasks in ~/myproject/.mise/tasks/*, then they'll both be available but the project-specific tasks will override the global ones if they have the same name.

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

## Tasks ​

**URL:** https://mise.jdx.dev/tasks/

**Contents:**
- Tasks ​
- Tasks in mise.toml files ​
- File Tasks ​
- Environment variables passed to tasks ​

Like make it manages tasks used to build and test projects.

You can define tasks in mise.toml files or as standalone shell scripts. These are useful for things like running linters, tests, builders, servers, and other tasks that are specific to a project. Of course, tasks launched with mise will include the mise environment—your tools and env vars defined in mise.toml.

Here's my favorite features about mise's task runner:

There are 2 ways to define tasks: inside of mise.toml files or as standalone shell scripts.

Tasks are defined in the [tasks] section of the mise.toml file.

You can then run the task with mise run build (or mise build if it doesn't conflict with an existing command).

You can also define tasks as standalone shell scripts. All you have to do is to create an executable file in a specific directory like mise-tasks.

You can then run the task with mise run build like for TOML tasks. See the file tasks reference for more information.

The following environment variables are passed to the task:

**Examples:**

Example 1 (json):
```json
[tasks.build]
description = "Build the CLI"
run = "cargo build"
```

Example 2 (unknown):
```unknown
#!/usr/bin/env bash
#MISE description="Build the CLI"
cargo build
```

---

## TOML-based Tasks ​

**URL:** https://mise.jdx.dev/tasks/toml-tasks.html

**Contents:**
- TOML-based Tasks ​
- Trivial task examples ​
- Detailed task examples ​
- Adding tasks ​
- Common options ​
  - Run command ​
  - Specifying which directory to use ​
  - Adding a description and alias ​
  - Dependencies ​
  - Environment variables ​

Tasks can be defined in mise.toml files in different ways. Trivial tasks can be written into a [tasks] section, while more detailed tasks each get their own section.

You can use environment variables or vars to define common arguments:

You can edit the mise.toml file directly or using mise tasks add

will add the following to mise.toml:

For an exhaustive list, see task configuration.

Provide the script to run. Can be a single command or an array of commands:

Commands are run in series. If a command fails, the task will stop and the remaining commands will not run.

You can specify an alternate command to run on Windows by using the run_windows key:

The dir property determines the cwd in which the task is executed. You can use the directory from where the task was run with dir = "{{cwd}}":

Also, MISE_ORIGINAL_CWD is set to the original working directory and will be passed to the task.

You can add a description to a task and alias for a task.

You can specify dependencies for a task. Dependencies are run before the task itself. If a dependency fails, the task will not run.

There are other ways to specify dependencies, see wait_for and depends_post

You can specify environment variables for a task:

If you want to skip executing a task if certain files haven't changed (up-to-date), you should specify sources and outputs:

You can use sources alone if with mise watch to run the task when the sources change. You can use the task_source_files() function to get the resolved paths of a task's sources from within its template.

A message to show before running the task. The user will be prompted to confirm before the task is run.

Tasks are executed with set -e (set -o erropt) if the shell is sh, bash, or zsh. This means that the script will exit if any command fails. You can disable this by running set +e in the script.

You can specify a shell command to run the script with (default is sh -c or cmd /c):

By using a shebang (or shell), you can run tasks in different languages (e.g., Python, Node.js, Ruby, etc.):

A shebang is the character sequence #! at the beginning of a script file that tells the system which program should be used to interpret/execute the script. The env command comes from GNU Coreutils. mise does not use env but will behave similarly.

For example, #!/usr/bin/env python will run the script with the Python interpreter found in the PATH.

The -S flag allows passing multiple arguments to the interpreter. It treats the rest of the line as a single argument string to be split.

This is useful when you need to specify interpreter flags or options. Example: #!/usr/bin/env -S python -u will run Python with unbuffered output.

You can specify a file to run as a task:

Task files can be fetched remotely with multiple protocols:

Please note that the file will be downloaded and executed. Make sure you trust the source.

Url format must follow these patterns git::<protocol>://<url>//<path>?<ref>

Each task file is cached in the MISE_CACHE_DIR directory. If the file is updated, it will not be re-downloaded unless the cache is cleared.

You can reset the cache by running mise cache clear.

You can use the MISE_TASK_REMOTE_NO_CACHE environment variable to disable caching of remote tasks.

For comprehensive information about task arguments, see the dedicated Task Arguments page.

By default, arguments are passed to the last script in the run array. So if a task was defined as:

Then running mise run test foo bar will pass foo bar to ./scripts/test-e2e.sh but not to cargo test.

The recommended way to define arguments is using the usage field:

Arguments defined in the usage field are available as environment variables prefixed with usage_.

See the Task Arguments page for complete documentation.

Deprecated - Removal in 2026.11.0

Using Tera template functions (arg(), option(), flag()) in run scripts is deprecated and will be removed in mise 2026.11.0. Versions >= 2026.5.0 will show a deprecation warning.

Why it's being removed:

Please migrate to using the usage field instead. See the migration guide.

You can define arguments using Tera template functions (deprecated):

Then running mise run test foo bar will pass foo bar to cargo test. mise run test --e2e-args baz will pass baz to ./scripts/test-e2e.sh.

These are defined in scripts with {{arg()}}. They are used for positional arguments where the order matters.

These are defined in scripts with {{option()}}. They are used for named arguments where the order doesn't matter.

Flags are like options except they don't take values. They are defined in scripts with {{flag()}}.

The value will be true if the flag is passed, and false otherwise.

**Examples:**

Example 1 (unknown):
```unknown
build = "cargo build"
test = "cargo test"
lint = "cargo clippy"
```

Example 2 (sql):
```sql
[tasks.cleancache]
run = "rm -rf .cache"
hide = true # hide this task from the list

[tasks.clean]
depends = ['cleancache']
run = "cargo clean" # runs as a shell command

[tasks.build]
description = 'Build the CLI'
run = "cargo build"
alias = 'b' # `mise run b`

[tasks.test]
description = 'Run automated tests'
# multiple commands are run in series
run = [
    'cargo test',
    './scripts/test-e2e.sh',
]
dir = "{{cwd}}" # run in user's cwd, default is the project's base directory

[tasks.lint]
description = 'Lint with clippy'
env = { RUST_BACKTRACE = '1' } # env vars for the script
# you can specify a multiline script instead of individual commands
run = '''
#!/usr/bin/env bash
cargo clippy
'''

[tasks.ci] # only dependencies to be run
description = 'Run CI tasks'
depends = ['build', 'lint', 'test']

[tasks.release]
confirm = 'Are you sure you want to cut a new release?'
description = 'Cut a new release'
file = 'scripts/release.sh' # execute an external script
```

Example 3 (json):
```json
[env]
VERBOSE_ARGS = '--verbose'

# Vars can be shared between tasks like environment variables,
# but they are not passed as environment variables to the scripts
[vars]
e2e_args = '--headless'

[tasks.test]
run = './scripts/test-e2e.sh {{vars.e2e_args}} $VERBOSE_ARGS'
```

Example 4 (bash):
```bash
mise tasks add pre-commit --depends "test" --depends "render" -- echo pre-commit
```

---

## Task Configuration ​

**URL:** https://mise.jdx.dev/tasks/task-configuration.html

**Contents:**
- Task Configuration ​
- Task properties ​
  - run ​
  - run_windows ​
  - description ​
  - alias ​
  - depends ​
    - Passing environment variables to dependencies ​
  - depends_post ​
  - wait_for ​

This is an exhaustive list of all the configuration options available for tasks in mise.toml or as file tasks.

All examples are in toml-task format instead of file, however they apply in both except where otherwise noted.

The command(s) to run. This is the only required property for a task.

You can now mix scripts with task references:

Simple forms still work and are equivalent:

Windows-specific variant of run supporting the same structured syntax:

A description of the task. This is used in (among other places) the help output, completions, mise run (without arguments), and mise tasks.

An alias for the task so you can run it with mise run <alias> instead of the full task name.

Tasks that must be run before this task. This is a list of task names or aliases. Arguments can be passed to the task, e.g.: depends = ["build --release"]. If multiple tasks have the same dependency, that dependency will only be run once. mise will run whatever it can in parallel (up to --jobs) through the use of depends and related properties.

You can pass environment variables to specific dependencies using two syntaxes:

Structured object format:

The structured format also supports combining env vars with arguments:

Note: These environment variables are passed only to the specified dependency, not to the current task or other dependencies.

Like depends but these tasks run after this task and its dependencies complete. For example, you may want a postlint task that you can run individually without also running lint:

Supports the same argument and environment variable syntax as depends.

Similar to depends, it will wait for these tasks to complete before running however they won't be added to the list of tasks to run. This is essentially optional dependencies.

Supports the same argument and environment variable syntax as depends.

Environment variables specific to this task. These will not be passed to depends tasks.

Tools to install and activate before running the task. This is useful for tasks that require a specific tool to be installed or a tool with a different version. It will only be used for that task, not dependencies.

The directory to run the task from. The most common way this is used is when you want the task to execute in the user's current directory:

Hide the task from help, completion, and other output like mise tasks. Useful for deprecated or internal tasks you don't want others to easily see.

A message to show before running the task. This is useful for tasks that are destructive or take a long time to run. The user will be prompted to confirm before the task is run.

Connects the task directly to the shell's stdin/stdout/stderr. This is useful for tasks that need to accept input or output in a way that mise's normal task handling doesn't support. This is not recommended to use because it really screws up the output whenever mise runs tasks in parallel. Ensure when using this that no other tasks are running at the same time.

In the future we could have a property like single = true or something that prevents multiple tasks from running at the same time. If that sounds useful, search/file a ticket.

Files or directories that this task uses as input, if this and outputs is defined, mise will skip executing tasks where the modification time of the oldest output file is newer than the modification time of the newest source file. This is useful for tasks that are expensive to run and only need to be run when their inputs change.

The task itself will be automatically added as a source, so if you edit the definition that will also cause the task to be run.

This is also used in mise watch to know which files/directories to watch.

This can be specified with relative paths to the config file and/or with glob patterns, e.g.: src/**/*.rs. Ensure you don't go crazy with adding a ton of files in a glob though—mise has to scan each and every one to check the timestamp.

Running the above will only execute cargo build if mise.toml, Cargo.toml, or any ".rs" file in the src directory has changed since the last build.

The task_source_files function can be used to iterate over a task's sources within its template context.

The counterpart to sources, these are the files or directories that the task will create/modify after it executes.

auto = true is an alternative to specifying output files manually. In that case, mise will touch an internally tracked file based on the hash of the task definition (stored in ~/.local/state/mise/task-outputs/<hash> if you're curious). This is useful if you want mise run to execute when sources change but don't want to have to manually touch a file for sources to work.

The shell to use to run the task. This is useful if you want to run a task with a different shell than the default such as fish, zsh, or pwsh. Generally though, it's recommended to use a shebang instead because that will allow IDEs with mise support to show syntax highlighting and linting for the script.

Suppress mise's output for the task such as showing the command that is run, e.g.: [build] $ cargo build. When this is set, mise won't show any output other than what the script itself outputs. If you'd also like to hide even the output that the task emits, use silent.

Suppress all output from the task. If set to "stdout" or "stderr", only that stream will be suppressed.

For comprehensive information about task arguments and the usage field, see the dedicated Task Arguments page.

More advanced usage specs can be added to the task's usage field. This only applies to toml-tasks.

Both args and flags in usage specs can specify an environment variable as an alternative source for their value. This allows task arguments to be provided through environment variables when not specified on the command line.

The precedence order is:

For positional arguments:

File tasks (tasks defined as executable files in mise-tasks/ or .mise/tasks/) also support the env attribute:

Environment variables can satisfy required argument checks. If an argument is marked as required (using angle brackets <arg>), providing its value through the environment variable specified in the env attribute fulfills that requirement:

Vars are variables that can be shared between tasks like environment variables but they are not passed as environment variables to the scripts. They are defined in the vars section of the mise.toml file.

Like most configuration in mise, vars can be defined across several files. So for example, you could put some vars in your global mise config ~/.config/mise/config.toml, use them in a task at ~/src/work/myproject/mise.toml. You can also override those vars in "later" config files such as ~/src/work/myproject/mise.local.toml and they will be used inside tasks of any config file.

As of this writing vars are only supported in TOML tasks. I want to add support for file tasks, but I don't want to turn all file tasks into tera templates just for this feature.

Options available in the top-level mise.toml [task_config] section. These apply to all tasks which are included by that config file or use the same root directory, e.g.: ~/src/myprojec/mise.toml's [task_config] applies to file tasks like ~/src/myproject/mise-tasks/mytask but not to tasks in ~/src/myproject/subproj/mise.toml.

Change the default directory tasks are run from.

Add toml files containing toml tasks, or file tasks to include when looking for tasks.

If using included task toml files, note that they have a different format than the mise.toml file. They are just a list of tasks. The file should be the same format as the [tasks] section of mise.toml but without the [task] prefix:

If you want auto-completion/validation in included toml tasks files, you can use the following JSON schema: https://mise.jdx.dev/schema/mise-task.json

You can include directories of tasks from git repositories using the git:: URL syntax:

URL format: git::<protocol>://<url>//<path>?<ref>

The repository will be cloned and cached in MISE_CACHE_DIR/remote-git-tasks-cache. Tasks from the included directory will be loaded as if they were local file tasks. You can disable caching with MISE_TASK_REMOTE_NO_CACHE=true or the --no-cache flag.

mise supports monorepo-style task organization with target path syntax. Enable it by setting experimental_monorepo_root = true in your root mise.toml.

For complete documentation on monorepo tasks including:

See the dedicated Monorepo Tasks documentation.

Redactions are a way to hide sensitive information from the output of tasks. This is useful for things like API keys, passwords, or other sensitive information that you don't want to accidentally leak in logs or other output.

A list of environment variables to redact from the output.

Running the above task will output echo [redacted] instead.

You can also specify these as a glob pattern, e.g.: redactions.env = ["SECRETS_*"].

Vars are variables that can be shared between tasks like environment variables but they are not passed as environment variables to the scripts. They are defined in the vars section of the mise.toml file.

Like [env], vars can also be read in as a file:

Secrets are also supported as vars.

The following settings control task behavior. These can be set globally in ~/.config/mise/config.toml or per-project in mise.toml:

Pushes tools' bin-paths to the front of PATH instead of allowing modifications of PATH after activation to take precedence. For example, if you have the following in your mise.toml:

But you also have this in your ~/.zshrc:

What will happen is /some/other/python will be used instead of the python installed by mise. This means you typically want to put mise activate at the end of your shell config so nothing overrides it.

If you want to always use the mise versions of tools despite what is in your shell config, set this to true. In that case, using this example again, /some/other/python will be after mise's python in PATH.

Default: false unless running NixOS or Alpine (let me know if others should be added)

Do not use precompiled binaries for all languages. Useful if running on a Linux distribution like Alpine that does not use glibc and therefore likely won't be able to run precompiled binaries.

Note that this needs to be setup for each language. File a ticket if you notice a language that is not working with this config.

should mise keep downloaded files after installation

should mise keep install files after installation even if the installation fails

Architecture to use for precompiled binaries. This is used to determine which precompiled binaries to download. If unset, mise will use the system's architecture.

Automatically install missing tools when running mise x, mise run, or as part of the 'not found' handler.

List of tools to skip automatically installing when running mise x, mise run, or as part of the 'not found' handler.

The age of the cache before it is considered stale. mise will occasionally delete cache files which have not been accessed in this amount of time.

Set to 0s to keep cache files indefinitely.

Directories where mise stops searching for config files. By default, mise will search from the current directory up to the root of the filesystem.

Setting this to a list of directories will stop the search when one of those directories is reached. This is useful to prevent mise from searching outside of a project directory.

This is an early-init setting: it must be set in .miserc.toml, environment variables, or CLI flags. Setting it in mise.toml will have no effect because config file discovery has already occurred by the time mise.toml is read.

Use color in mise terminal output

Sets the color theme for interactive prompts like mise run task selection. Available themes:

If you're using a light terminal and the default theme is hard to read, try setting this to base16.

The default config filename read. mise use and other commands that create new config files will use this value. This must be an env var.

The default .tool-versions filename read. This will not ignore .tool-versions—use override_tool_versions_filename for that. This must be an env var.

Backends to disable such as asdf or pipx

Disable the default mapping of short tool names like php -> asdf:mise-plugins/asdf-php. This parameter disables only for the backends vfox and asdf.

Turns off helpful hints when using different mise features

Tools defined in mise.toml that should be ignored

Tools defined in mise.toml that should be used - all other tools are ignored

Enables profile-specific config files such as .mise.development.toml. Use this for different env vars or different tool versions in development/staging/production environments. See Configuration Environments for more on how to use this feature.

Multiple envs can be set by separating them with a comma, e.g. MISE_ENV=ci,test. They will be read in order, with the last one taking precedence.

This is an early-init setting: it must be set in .miserc.toml, environment variables, or CLI flags (-E/--env). Setting it in mise.toml will have no effect because MISE_ENV determines which config files to load.

When enabled, mise will cache the computed environment (env vars and PATH) to disk. This dramatically speeds up nested mise invocations (e.g., mise x -- mise env).

The cache is encrypted using a session-scoped key (__MISE_ENV_CACHE_KEY) that is generated when you run mise activate or mise exec. This means:

Cache invalidation happens when:

Modules (vfox plugins) can declare themselves cacheable by returning {cacheable = true, watch_files = [...], env = [...]} from their mise_env hook. Modules that don't declare cacheability are treated as dynamic and will be re-executed on each cache hit.

Directives can opt out of caching by setting cacheable = false:

How long cached environments remain valid before being regenerated. Accepts duration strings like "1h", "30m", "1d".

Even with a valid TTL, caches are still invalidated when config files, tool versions, settings, or watched files change.

Path to a file containing environment variables to automatically load.

Automatically install missing tools when running mise x.

Enables experimental features. I generally will publish new features under this config which needs to be enabled to use them. While a feature is marked as "experimental" its behavior may change or even disappear in any release.

The idea is experimental features can be iterated on this way so we can get the behavior right, but once that label goes away you shouldn't expect things to change without a proper deprecation—and even then it's unlikely.

Also, I very often will use experimental as a beta flag as well. New functionality that I want to test with a smaller subset of users I will often push out under experimental mode even if it's not related to an experimental feature.

If you'd like to help me out, consider enabling it even if you don't have a particular feature you'd like to try. Also, if something isn't working right, try disabling it if you can.

duration that remote version cache is kept for "fast" commands (represented by PREFER_STALE), these are always cached. For "slow" commands like mise ls-remote or mise install:

Timeout in seconds for HTTP requests to fetch new tool versions in mise.

Enable/disable GitHub Artifact Attestations verification globally. When enabled, mise will verify the authenticity and integrity of downloaded tools using GitHub's artifact attestation system for tools that support it (e.g., Ruby precompiled binaries).

Individual tools can override this setting with their own <tool>.github_attestations setting.

Path to the global mise config file. Default is ~/.config/mise/config.toml. This must be an env var.

Path which is used as {{config_root}} for the global config file. Default is $HOME. This must be an env var.

Path to a file containing default go packages to install when installing go

Mirror to download go sdk tarballs from.

URL to fetch go from.

Defaults to ~/.local/share/mise/installs/go/.../bin. Set to true to override GOBIN if previously set. Set to false to not set GOBIN (default is ${GOPATH:-$HOME/go}/bin).

[deprecated] Set to true to set GOPATH=~/.local/share/mise/installs/go/.../packages.

Sets GOROOT=~/.local/share/mise/installs/go/.../.

Set to true to skip checksum verification when downloading go sdk tarballs.

Use gpg to verify all tool signatures.

Uses an exponential backoff strategy. The duration is calculated by taking the base (10ms) to the n-th power.

Timeout in seconds for all HTTP requests in mise.

By default, idiomatic version files are disabled. You can enable them for specific tools with this setting.

For example, to enable idiomatic version files for node and python:

See Idiomatic Version Files for more information.

This is a list of config paths that mise will ignore.

This is an early-init setting: it must be set in .miserc.toml, environment variables, or CLI flags. Setting it in mise.toml will have no effect because config file discovery has already occurred by the time mise.toml is read.

Filter tool versions by release date. Supports:

This is useful for reproducible builds or security purposes where you want to ensure you're only installing versions that existed before a certain point in time.

Only affects backends that provide release timestamps (aqua, cargo, npm, pipx, and some core plugins). Versions without timestamps are included by default.

Behavior: This filter only applies when resolving fuzzy version requests like node@20 or latest. Explicitly pinned versions like node@22.5.0 are not filtered, allowing you to selectively use newer versions for specific tools while keeping others behind the cutoff date.

Can be overridden with the --before CLI flag.

How many jobs to run concurrently such as tool installs.

[!NOTE] This setting requires both lockfile and experimental to be enabled.

When enabled, mise install will fail if tools don't have pre-resolved URLs in the lockfile for the current platform. This prevents API calls to GitHub, aqua registry, etc. and ensures reproducible installations.

This is useful in CI/CD environments where you want to:

To generate lockfile URLs, run:

Equivalent to passing --locked to mise install.

[!NOTE] This feature is experimental and may change in the future.

Read/update lockfiles for tool versions. This is useful when you'd like to have loose versions in mise.toml like this:

But you'd like the versions installed to be consistent within a project. When this is enabled, mise will update mise.lock files next to mise.toml files containing pinned versions. When installing tools, mise will reference this lockfile if it exists and this setting is enabled to resolve versions.

The lockfiles are not created automatically. To generate them, run the following (assuming the config file is mise.toml):

The lockfile is named the same as the config file but with .lock instead of .toml as the extension, e.g.:

When enabled, mise will read credentials from the netrc file and apply HTTP Basic authentication for matching hosts. This is useful for accessing private artifact repositories like Artifactory or Nexus.

On Unix/macOS, the default path is ~/.netrc. On Windows, mise looks for %USERPROFILE%\_netrc first, then falls back to %USERPROFILE%\.netrc.

The netrc file format is:

You can also specify a custom netrc file path using the netrc_file setting.

Override the default netrc file path. This is useful if you want to use a different netrc file for mise or if your netrc file is in a non-standard location.

Do not load environment variables from config files.

Do not execute hooks from config files.

Set to false to disable the "command not found" handler to autoinstall missing tool versions. Disable this if experiencing strange behavior in your shell when a command is not found.

Important limitation: This handler only installs missing versions of tools that already have at least one version installed. mise cannot determine which tool provides a binary without having the tool installed first, so it cannot auto-install completely new tools.

This also runs in shims if the terminal is interactive.

OS to use for precompiled binaries.

If set, mise will ignore default config files like mise.toml and use these filenames instead.

This is an early-init setting: it must be set in .miserc.toml, environment variables, or CLI flags. Setting it in mise.toml will have no effect because config file discovery has already occurred by the time mise.toml is read.

If set, mise will ignore .tool-versions files and use these filenames instead. Can be set to none to disable .tool-versions entirely.

This is an early-init setting: it must be set in .miserc.toml, environment variables, or CLI flags. Setting it in mise.toml will have no effect because config file discovery has already occurred by the time mise.toml is read.

Enables extra-secure behavior. See Paranoid.

This sets --pin by default when running mise use in mise.toml files. This can be overridden by passing --fuzzy on the command line.

How long to wait before updating plugins automatically (note this isn't currently implemented).

Suppress all output except errors.

Connect stdin/stdout/stderr to child processes.

Use a custom file for the shorthand aliases. This is useful if you want to share plugins within an organization.

Shorthands make it so when a user runs something like mise install elixir mise will automatically install the asdf-elixir plugin. By default, it uses the shorthands in registry.toml.

The file should be in this toml format:

Suppress all mise run|watch output except errors—including what tasks output.

Enable/disable SLSA provenance verification globally for all backends that support it. When enabled, mise will verify the supply-chain integrity of downloaded tools using SLSA provenance attestations.

Path to the system mise config file. Default is /etc/mise/config.toml. This must be an env var.

Paths that mise will not look for tasks in.

Change output style when executing tasks. This controls the output of mise run.

Mise will always fetch the latest tasks from the remote, by default the cache is used.

Automatically install missing tools when executing tasks.

Disable truncation of command lines in task execution output. When true, the full command line will be shown.

Tasks to skip when running mise run.

Run only specified tasks skipping all dependencies.

Default timeout for tasks. Can be overridden by individual tasks.

Show completion message with elapsed time for each task on mise run. Default shows when output type is prefix.

Enable terminal progress indicators using OSC 9;4 escape sequences. This provides native progress bars in the terminal window chrome for terminals that support it, including Ghostty, iTerm2, VS Code's integrated terminal, Windows Terminal, and VTE-based terminals (GNOME Terminal, Ptyxis, etc.).

When enabled, mise will send progress updates to the terminal during operations like tool installations. The progress bar appears in the terminal's window UI, separate from the text output.

mise automatically detects whether your terminal supports OSC 9;4 and will only send these sequences if supported. Terminals like Alacritty, WezTerm, and kitty do not support OSC 9;4 and will not receive these sequences.

Set to false to disable this feature if you prefer not to see these indicators.

This is a list of config paths that mise will automatically mark as trusted.

Default shell arguments for Unix to be used for file commands. For example, sh for sh.

Default shell arguments for Unix to be used for inline commands. For example, sh -c for sh.

Map of URL patterns to replacement URLs. This feature supports both simple hostname replacements and advanced regex-based URL transformations for download mirroring and custom registries.

See URL Replacements for more information.

Determines whether to use a specified shell for executing tasks in the tasks directory. When set to true, the shell defined in the file will be used, or the default shell specified by windows_default_file_shell_args or unix_default_file_shell_args will be applied. If set to false, tasks will be executed directly as programs.

Set to "false" to disable using mise-versions as a quick way for mise to query for new versions. This host regularly grabs all the latest versions of core and community plugins. It's faster than running a plugin's list-all command and gets around GitHub rate limiting problems when using it.

mise-versions itself also struggles with rate limits but you can help it to fetch more frequently by authenticating with its GitHub app. It does not require any permissions since it simply fetches public repository information.

See Troubleshooting for more information.

When enabled, mise sends anonymous download statistics to mise-versions.jdx.dev after successfully installing a tool. This helps show tool popularity on mise-versions.jdx.dev.

This is automatically disabled if use_versions_host is set to false. Set to false to opt-out of anonymous statistics collection.

Shows more verbose output such as installation logs when installing tools.

Default shell arguments for Windows to be used for file commands. For example, cmd /c for cmd.exe.

Default shell arguments for Windows to be used for inline commands. For example, cmd /c for cmd.exe.

List of executable extensions for Windows. For example, exe for .exe files, bat for .bat files, and so on.

This will automatically answer yes or no to prompts. This is useful for scripting.

[experimental] List of age identity files to use for decryption.

[experimental] Path to the age private key file to use for encryption/decryption.

[experimental] List of SSH identity files to use for age decryption.

If true, fail when age decryption fails (including when age is not available, the key is missing, or the key is invalid). If false, skip decryption and continue in these cases.

Use baked-in aqua registry.

Use cosign to verify aqua tool signatures.

Extra arguments to pass to cosign when verifying aqua tool signatures.

Enable/disable GitHub Artifact Attestations verification for aqua tools. When enabled, mise will verify the authenticity and integrity of downloaded tools using GitHub's artifact attestation system.

Use minisign to verify aqua tool signatures.

URL to fetch aqua registry from. This is used to install tools from the aqua registry.

If this is set, the baked-in aqua registry is not used.

By default, the official aqua registry is used: https://github.com/aquaproj/aqua-registry

Use SLSA to verify aqua tool signatures.

If true, mise will use cargo binstall instead of cargo install if cargo-binstall is installed and on PATH. This makes installing CLIs with cargo much faster by downloading precompiled binaries.

You can install it with mise:

Packages are installed from the official cargo registry.

You can set this to a different registry name if you have a custom feed or want to use a different source.

Please follow the cargo alternative registries documentation to configure your registry.

Default conda channel when installing packages with the conda backend. Override per-package with conda:package[channel=bioconda].

The most common channels are:

This is a list of flags to extend the search and install abilities of dotnet tools.

Here are the available flags:

URL to fetch dotnet tools from. This is used when installing dotnet tools.

By default, mise will use the nuget API to fetch.

However, you can set this to a different URL if you have a custom feed or want to use a different source.

If true, compile erlang from source. If false, use precompiled binaries. If not set, use precompiled binaries if available.

Enable/disable GitHub Artifact Attestations verification for github backend tools. When enabled, mise will verify the authenticity and integrity of downloaded tools using GitHub's artifact attestation system.

Enable/disable SLSA provenance verification for github backend tools. When enabled, mise will verify the supply-chain integrity of downloaded tools using SLSA provenance attestations.

On slow filesystems (like NFS with cold cache), mise's hook-env can be slow due to multiple filesystem stat operations. Setting this to a positive value (e.g., "5s") will cache the results of directory traversal and only re-check after the TTL expires.

When set to "0s" (default), no caching is performed and every hook-env call will check the filesystem for changes. This is the safest option but slowest on NFS.

Note: When caching is enabled, newly created config files may not be detected until the TTL expires. Use mise hook-env --force to bypass the cache.

When enabled, mise will only perform full config file checks when the directory changes (chpwd), not on every shell prompt (precmd). This significantly reduces filesystem operations on slow filesystems like NFS.

With this enabled, changes to config files will not be detected until you change directories. Use mise hook-env --force to manually trigger a full update.

This setting is useful when:

Compile node from source.

Install a specific node flavor like glibc-217 or musl. Use with unofficial node build repo.

Use gpg to verify node tool signatures.

Mirror to download node tarballs from.

If true, mise will use bun instead of npm if bun is installed and on PATH. This makes installing CLIs faster by using bun as the package manager.

You can install it with mise:

Package manager to use for installing npm packages. Can be one of:

URL to use for pipx registry.

This is used to fetch the latest version of a package from the pypi registry.

The default is https://pypi.org/pypi/{}/json which is the JSON endpoint for the pypi registry.

You can also use the HTML endpoint by setting this to https://pypi.org/simple/{}/.

If true, mise will use uvx instead of pipx if uv is installed and on PATH. This makes installing CLIs much faster by using uv as the package manager.

You can install it with mise:

Path to a file containing default python packages to install when installing a python version.

URL to fetch python patches from to pass to python-build.

Directory to fetch python patches from.

Specify the architecture to use for precompiled binaries.

Specify the flavor to use for precompiled binaries.

Options are available here: https://gregoryszorc.com/docs/python-build-standalone/main/running.html

Specify the architecture to use for precompiled binaries. If on an old CPU, you may want to set this to "x86_64" for the most compatible binaries. See https://gregoryszorc.com/docs/python-build-standalone/main/running.html for more information.

URL to fetch pyenv from for compiling python with python-build.

Integrate with uv to automatically create/source venvs if uv.lock is present.

Arguments to pass to uv when creating a venv.

Automatically create virtualenvs for python tools.

Arguments to pass to python when creating a venv. (not used for uv venv creation)

Prefer to use venv from Python's standard library.

A list of patch files or URLs to apply to ruby source.

Controls whether Ruby is compiled from source or downloaded as precompiled binaries. Requires experimental = true to be enabled.

Example to force compilation:

Path to a file containing default ruby gems to install when installing ruby.

[experimental] Override architecture identifier for precompiled Ruby binaries.

[experimental] Override OS identifier for precompiled Ruby binaries.

Override the global github_attestations setting for Ruby precompiled binaries. When enabled, mise will verify the authenticity of precompiled Ruby binaries from jdx/ruby. Requires experimental = true.

Defaults to the global github_attestations setting if not specified.

Options to pass to ruby-build.

The URL used to fetch ruby-build. This accepts either a Git repository or a ZIP archive.

Use ruby-install instead of ruby-build.

Options to pass to ruby-install.

The URL used to fetch ruby-install. This accepts either a Git repository or a ZIP archive.

Set to true to enable verbose output during ruby installation.

Path to the cargo home directory. Defaults to ~/.cargo or %USERPROFILE%\.cargo

Path to the rustup home directory. Defaults to ~/.rustup or %USERPROFILE%\.rustup

The age private key to use for sops secret decryption. Takes precedence over standard SOPS_AGE_KEY environment variable.

Path to the age private key file for sops secret decryption. Takes precedence over standard SOPS_AGE_KEY_FILE environment variable.

The age public keys to use for sops secret encryption.

Use rops to decrypt sops files. Disable to shell out to sops which will slow down mise but sops may offer features not available in rops.

If true, fail when sops decryption fails (including when sops is not available, the key is missing, or the key is invalid). If false, skip decryption and continue in these cases.

Show a warning if tools are not installed when entering a directory with a mise.toml file.

Disable tools with disable_tools.

Show configured env vars when entering a directory with a mise.toml file.

Show configured tools when entering a directory with a mise.toml file.

Show warning when prepare providers have stale dependencies.

Truncate status messages.

Use gpg to verify swift tool signatures.

Override the platform to use for precompiled binaries.

When enabled, arg(), option(), and flag() Tera functions in run scripts will not contribute to the task's usage spec—only the explicit usage field is used.

When using monorepo mode (experimental_monorepo_root = true), this controls how deep mise will search for task files in subdirectories.

Performance tip: Reduce this value if you have a very large monorepo and notice slow task discovery. For example, if your projects are all at projects/*, set to 2.

Or via environment variable:

If empty (default), uses default exclusions: node_modules, target, dist, build. If you specify any patterns, ONLY those patterns will be excluded (defaults are NOT included). For example, setting to [".temp", "vendor"] will exclude only those two directories.

When enabled, mise will skip directories that are ignored by .gitignore files when discovering tasks in a monorepo.

This setting allows mise to fetch Zig from one of many community-maintained mirrors.

The ziglang.org website does not offer any uptime or speed guarantees, and it recommends to use the mirrors. The mirror list is cached and allows the installs to succeed even if the main server is unavailable.

The downloaded tarballs are always verified against Zig Software Foundation's public key, so there is no risk of third-party modifications. Read more on ziglang.org.

If you don't have the mirror list cached locally, you can place the newline-separated server list inside mise cache path, folder zig as community-mirrors.txt.

**Examples:**

Example 1 (json):
```json
[tasks.grouped]
run = [
  { task = "t1" },          # run t1 (with its dependencies)
  { tasks = ["t2", "t3"] }, # run t2 and t3 in parallel (with their dependencies)
  "echo end",               # then run a script
]
```

Example 2 (json):
```json
tasks.a = "echo hello"
tasks.b = ["echo hello"]
tasks.c.run = "echo hello"
[tasks.d]
run = "echo hello"
[tasks.e]
run = ["echo hello"]
```

Example 3 (json):
```json
[tasks.build]
run = "cargo build"
run_windows = "cargo build --features windows"
```

Example 4 (json):
```json
[tasks.build]
description = "Build the CLI"
run = "cargo build"
```

---

## mise tasks run ​

**URL:** https://mise.jdx.dev/cli/tasks/run.html

**Contents:**
- mise tasks run ​
- Arguments ​
  - [TASK] ​
  - [ARGS]… ​
- Flags ​
  - -c --continue-on-error ​
  - -C --cd <CD> ​
  - -f --force ​
  - -j --jobs <JOBS> ​
  - -n --dry-run ​

This command will run a task, or multiple tasks in parallel. Tasks may have dependencies on other tasks or on source files. If source is configured on a task, it will only run if the source files have changed.

Tasks can be defined in mise.toml or as standalone scripts. In mise.toml, tasks take this form:

Alternatively, tasks can be defined as standalone scripts. These must be located in mise-tasks, .mise-tasks, .mise/tasks, mise/tasks or .config/mise/tasks. The name of the script will be the name of the tasks.

Tasks to run Can specify multiple tasks by separating with ::: e.g.: mise run task1 arg1 arg2 ::: task2 arg1 arg2

Arguments to pass to the tasks. Use ":::" to separate tasks

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

## mise tasks info ​

**URL:** https://mise.jdx.dev/cli/tasks/info.html

**Contents:**
- mise tasks info ​
- Arguments ​
  - <TASK> ​
- Flags ​
  - -J --json ​

Get information about a task

Name of the task to get information about

Output in JSON format

**Examples:**

Example 1 (json):
```json
$ mise tasks info
Name: test
Aliases: t
Description: Test the application
Source: ~/src/myproj/mise.toml

$ mise tasks info test --json
{
  "name": "test",
  "aliases": "t",
  "description": "Test the application",
  "source": "~/src/myproj/mise.toml",
  "depends": [],
  "env": {},
  "dir": null,
  "hide": false,
  "raw": false,
  "sources": [],
  "outputs": [],
  "run": [
    "echo \"testing!\""
  ],
  "file": null,
  "usage_spec": {}
}
```

---

## Monorepo Tasks experimental ​

**URL:** https://mise.jdx.dev/tasks/monorepo.html

**Contents:**
- Monorepo Tasks experimental ​
- Overview ​
  - Benefits ​
- Configuration ​
  - Enabling Monorepo Mode ​
  - Example Structure ​
- Task Path Syntax ​
  - Absolute Paths ​
  - Current config_root Tasks ​
  - Wildcard Patterns ​

mise supports monorepo-style task organization with target path syntax. This feature allows you to manage tasks across multiple projects in a single repository, where each project can have its own mise.toml configuration with tools, environment variables, and tasks that may be different from where the task is called from.

When experimental_monorepo_root is enabled in your root mise.toml, mise will automatically discover tasks in subdirectories and prefix them with their relative path from the monorepo root. This creates a unified task namespace across your entire repository.

The directory containing a mise.toml file is called the config_root. In monorepo mode, each project can have its own config_root with its own configuration, separate from the monorepo root. Note that if you use one of the alternate paths in a subdirectory like ./projects/frontend/.mise/config.toml, the config_root will be ./projects/frontend–not ./projects/frontend/.mise.

Add experimental_monorepo_root = true to your root mise.toml:

This feature requires MISE_EXPERIMENTAL=1 environment variable.

With this structure, tasks will be automatically namespaced:

Monorepo tasks use special path syntax with // and : prefixes. You can run these tasks directly with mise or with mise run. With non-monorepo tasks, the guidance is to avoid using the direct syntax for scripts because it could conflict with future core mise commands. However, mise will never define commands with a // or : prefix, so this guidance does not apply to monorepo tasks.

Use // prefix to specify the absolute path from the monorepo root:

Use : prefix to run tasks in the current config_root:

Optional Colon Syntax

The leading : is optional when running tasks from subdirectories or defining task dependencies. While both syntaxes work, we encourage using the : prefix to be explicit about monorepo task references.

Running from subdirectory:

The bare name syntax (without :) is supported primarily to ease migration from non-monorepo to monorepo configurations. When migrating, you won't need to update all your task dependencies immediately - they'll continue to work. However, using the : prefix makes it clear you're referencing a task in the current config_root.

mise supports two types of wildcards for flexible task execution:

Use ellipsis (...) to match any directory depth:

Additional glob patterns may be added in a future version so mise //projects/*:build and mise '//projects/**:build' will likely be supported. We're using ... because it matches how bazel and buck2 do it.

Use asterisk (*) to match task names:

You can combine both types of wildcards for powerful patterns:

Subdirectory tasks automatically inherit tools and environment variables from parent config files in the hierarchy. However, each subdirectory can also define its own tools and environment variables in its config_root. This allows you to:

You must explicitly list your config roots using the [monorepo] section:

This tells mise exactly which directories contain project configurations. Benefits:

Single-level globs (*) are supported, but recursive globs (**) are not. This ensures predictable performance while still allowing flexible patterns.

Automatic Discovery Deprecated

Automatic filesystem walking to discover monorepo subdirectories is deprecated. If you don't define [monorepo].config_roots, mise will still walk the filesystem but will emit a deprecation warning. Please migrate to explicit config roots.

The difference between mise tasks and mise tasks --all:

Given this structure:

When in projects/frontend/:

Place commonly-used tools and environment in the root mise.toml to avoid repetition:

Only override tools in subdirectories when they genuinely need different versions:

Prefix related tasks with common names to enable pattern matching:

Then run all test tasks: mise '//...:test*'

Organize projects in subdirectories to enable targeted execution:

Then run tasks by group:

The monorepo ecosystem offers many excellent tools, each with different strengths. Here's how mise's Monorepo Tasks compares:

Taskfile and Just are fantastic for single-project task automation. They're lightweight and easy to set up, but they weren't designed with monorepos in mind. While you can have multiple Taskfiles/Justfiles in a repo, they don't provide unified task discovery, cross-project wildcards, or automatic tool/environment inheritance across projects.

mise's advantage: Automatic task discovery across the entire monorepo with a unified namespace and powerful wildcard patterns.

Nx, Turborepo, and Lerna are powerful tools specifically designed for JavaScript/TypeScript monorepos.

mise's advantage: Language-agnostic support. While these tools excel in JS/TS ecosystems, mise works equally well with Rust, Go, Python, Ruby, or any mix of languages. You also get unified tool version management (not just tasks) and environment variables across your entire stack.

Bazel (Google) and Buck2 (Meta) are industrial-strength build systems designed for massive, multi-language monorepos at companies with thousands of engineers.

Both are extremely powerful but come with significant complexity:

mise's advantage: Simplicity through non-hermetic builds. mise doesn't try to control your entire build environment in isolation - instead, it manages tools and tasks in a flexible, practical way. This "non-hermetic" approach means you can use mise without restructuring your entire codebase or learning a new language. You get powerful monorepo task management with simple TOML configuration - enough power for most teams without the enterprise-level complexity that hermetic builds require.

Rush (Microsoft) offers strict dependency management and build orchestration for JavaScript monorepos, with a focus on safety and convention adherence.

Moon is a newer Rust-based build system that aims to be developer-friendly while supporting multiple languages.

mise's Monorepo Tasks aims to hit the sweet spot between simplicity and power:

When to consider alternatives:

The best tool is the one that fits your team's needs. mise's Monorepo Tasks is designed for teams who want powerful monorepo management without the complexity overhead, especially when working across multiple languages.

**Examples:**

Example 1 (json):
```json
# /myproject/mise.toml
experimental_monorepo_root = true

[tools]
# Tools defined here are inherited by all subdirectories
node = "20"
```

Example 2 (unknown):
```unknown
myproject/
├── mise.toml (with experimental_monorepo_root = true)
├── projects/
│   ├── frontend/
│   │   └── mise.toml (with tasks: build, test)
│   └── backend/
│       └── mise.toml (with tasks: build, test)
```

Example 3 (markdown):
```markdown
# Direct syntax (preferred for monorepo tasks)
mise //projects/frontend:build

# Also works with 'run'
mise run //projects/frontend:build

# Need quotes for wildcards
mise '//projects/frontend:*'
```

Example 4 (markdown):
```markdown
# Run build task in frontend project
mise //projects/frontend:build

# Run test task in backend project
mise //projects/backend:test
```

---

## mise tasks deps ​

**URL:** https://mise.jdx.dev/cli/tasks/deps.html

**Contents:**
- mise tasks deps ​
- Arguments ​
  - [TASKS]… ​
- Flags ​
  - --dot ​
  - --hidden ​

Display a tree visualization of a dependency graph

Tasks to show dependencies for Can specify multiple tasks by separating with spaces e.g.: mise tasks deps lint test check

Display dependencies in DOT format

**Examples:**

Example 1 (markdown):
```markdown
# Show dependencies for all tasks
$ mise tasks deps

# Show dependencies for the "lint", "test" and "check" tasks
$ mise tasks deps lint test check

# Show dependencies in DOT format
$ mise tasks deps --dot
```

---

## File Tasks ​

**URL:** https://mise.jdx.dev/tasks/file-tasks.html

**Contents:**
- File Tasks ​
- Task Configuration ​
- Shebang ​
- Editing tasks ​
- Task Grouping ​
- Arguments ​
  - Example file task with arguments ​
  - Example of a NodeJS file task with arguments ​
- CWD ​
- Running tasks directly ​

In addition to defining tasks through the configuration, they can also be defined as standalone script files in one of the following directories:

Note that you can configure directories using the task_config section.

Here is an example of a file task that builds a Rust CLI:

Ensure that the file is executable, otherwise mise will not be able to detect it.

Having the code in a bash file and not TOML helps make it work better in editors since they can do syntax highlighting and linting more easily.

They also still work great for non-mise users—though of course they'll need to find a different way to install their dev tools the tasks might use.

All configuration options can be found here task configuration You can provide additional configuration for file tasks by adding #MISE comments at the top of the file.

Assuming that file was located in mise-tasks/build, it can then be run with mise run build (or with its alias: mise run b).

Beware of formatters changing #MISE to # MISE. It's intentionally ignored by mise to avoid unintentional configuration. To workaround this, use the alternative: # [MISE].

The shebang line is optional, but if it is present, it will be used to determine the shell to run the script with. You can also use it to run the script with various programming languages.

This script can be edited by running mise tasks edit build (using $EDITOR). If it doesn't exist it will be created. This is convenient for quickly editing or creating new scripts.

File tasks in mise-tasks, .mise/tasks, mise/tasks, or .config/mise/tasks can be grouped into sub-directories which will automatically apply prefixes to their names when loaded.

Example: With a folder structure like below:

Running mise tasks will give the below output:

For comprehensive information about task arguments, see the dedicated Task Arguments page.

usage spec can be used within these files to provide argument parsing, autocompletion, documentation when running mise and can be exported to markdown. Essentially this turns tasks into fully-fledged CLIs.

The usage CLI is not required to execute mise tasks with the usage spec. However, for completions to work, the usage CLI must be installed and available in the PATH.

Here is an example of a file task that builds a Rust CLI using some of the features of usage:

For details on bash parameter expansion patterns like ${var?}, ${var:-default}, and ${var:+value}, see Bash Variable Expansion for Usage Variables.

If you have installed usage, completions will be enabled for your task. In this example,

(Note that cli and markdown help for tasks is not yet implemented in mise as of this writing but that is planned.)

If you don't get any autocomplete suggestions, use the -v (verbose) flag to see what's going on. For example, if you use mise run build -v and have an invalid usage spec, you will see an error message such as DEBUG failed to parse task file with usage

Here is how you can use usage to parse arguments in a Node.js script:

If you pass an invalid argument, you will get an error message:

Autocomplete will show the available choices for the output_file argument if usage is installed.

mise sets the current working directory to the directory of mise.toml before running tasks. This can be overridden by setting dir="{{cwd}}" in the task header:

Also, the original working directory is available in the MISE_ORIGINAL_CWD environment variable:

Tasks don't need to be configured as part of a config, you can just run them directly by passing the path to the script:

Note that the path must start with / or ./ to be considered a file path. (On Windows it can be C:\ or .\)

**Examples:**

Example 1 (unknown):
```unknown
#!/usr/bin/env bash
#MISE description="Build the CLI"
cargo build
```

Example 2 (unknown):
```unknown
chmod +x mise-tasks/build
```

Example 3 (unknown):
```unknown
#MISE description="Build the CLI"
#MISE alias="b"
#MISE sources=["Cargo.toml", "src/**/*.rs"]
#MISE outputs=["target/debug/mycli"]
#MISE env={RUST_BACKTRACE = "1"}
#MISE depends=["lint", "test"]
#MISE tools={rust="1.50.0"}
```

Example 4 (javascript):
```javascript
#!/usr/bin/env node
//MISE description="Hello, World in Node.js"

console.log("Hello, World!");
```

---
