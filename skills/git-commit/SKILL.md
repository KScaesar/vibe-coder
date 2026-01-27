---
name: git-commit
description: Analyzes staged changes and drafts standardized commit messages (Conventional Commits v1.0.0 + DDD). STRICTLY DRAFTING ONLY - NEVER COMMITS AUTOMATICALLY.
---

# Git Commit Message Generator

This skill analyzes staged changes and generates high-quality commit message drafts following the **[Conventional Commits v1.0.0](https://www.conventionalcommits.org/en/v1.0.0/)** specification.

**CRITICAL**: This skill is a **TEXT GENERATOR**. It must **NEVER** execute `git add`, `git commit`, `git push`, or modify git history.

## Workflow

1.  **Analyze Staged Changes**
    - Command: !{git --no-pager diff -U5 --staged}
    - If no output/changes: Inform user that no files are staged and **STOP**. DO NOT run `git add`.

2.  **Analyze Intent & Flags**
    - Determine `scope` and `body` flags based on user input.
    - **Scope Flag** (Default: `scope=false`): When Flag `scope=false`, scope MUST be completely omitted from commit message. When Flag `scope=true` (ONLY if user explicitly requests it with phrases like "add scope", "with scope").
    - **Body Flag** (Default: `body=false`): When Flag `body=false`, body section MUST be completely omitted from commit message. When Flag `body=true` (ONLY if user explicitly requests it with phrases like "detailed", "add body").
    - **Breaking**: Detect if changes introduce breaking changes (SemVer MAJOR).

3.  **Generate 3 Draft Options**
    - You MUST provide exactly 3 distinct commit message options following [Commit Rules](#commit-rules).
    - **Option 1**: Concise & direct.
    - **Option 2**: Alternative focus/phrasing.
    - **Option 3**: Different angle.

4.  **Present & HALT**
    - Output the options in code blocks.
    - **STOP**. Do not ask "Shall I commit?".
    - Wait for the user to manually run the commit command.

## Commit Rules (Conventional Commits v1.0.0)

### Format Structure

```text
type(scope?): description

[optional body]

[optional footer(s)]
```

### 1.Header (First Line)

The header line MUST follow this pattern: `type(scope): description` or `type(scope)!: description`.

- **Type** (Required)
  - `feat`: New feature (SemVer MINOR)
  - `fix`: Bug fix (SemVer PATCH)
  - `docs`, `style`, `refactor`, `perf`, `test`, `build`, `ci`, `chore`
- **Scope** (Optional)
  - **Condition**: When Flag `scope=false`, scope MUST be completely omitted (no parentheses at all). When Flag `scope=true`, scope MUST be enclosed in parentheses immediately after the type: `feat(parser):` or `fix(auth/api):`.
  - **How to Determine Scope Content**: When Flag `scope=true`, use the following DDD/Clean Architecture principles to infer scope content:
    - **Autonomy**: You MUST autonomously infer these from file paths/content.
    - **Context (Business/DDD)**: REQUIRED. The business domain (e.g., `user`, `order`).
    - **Layer (Technical/Clean Arch)**: OPTIONAL. The technical layer (e.g., `api`, `domain`, `infra`).
    - **Format**: `(<context>)` or `(<context>/<layer>)`
    - **Examples**:
      - Context only: `feat(user): add profile`
      - Context + Layer: `feat(user/infra): add repo`
- **Breaking Indicator** (Optional)
  - Append `!` after type/scope for SemVer MAJOR changes
  - Example: `feat!: remove legacy api` or `fix(core)!: drop support for node 12`
- **Description** (Required)
  - Concise summary
  - Use imperative mood ("add" NOT "added")
  - Lowercase first letter
  - No trailing period

### 2.Body (Optional)

- **Condition**: When Flag `body=false`, body section MUST be completely omitted (no blank line after header). When Flag `body=true`, body MUST be included with explanation of why the change was made.
- Separate from header with a blank line.

### 3.Footer (Optional)

- Separate from body with a blank line.
- **Breaking Changes**: Start with `BREAKING CHANGE: <description>`.
- **Issues**: `Fixes #123`, `Closes #456`.

## Constraints (NON-NEGOTIABLE)

1.  **NO AUTO-EXECUTION**: You are forbidden from running `git add` or `git commit`. Draft text ONLY.
2.  **Strict Adherence**: Follow v1.0.0 spec strictly.
3.  **STOP AFTER DRAFTING**: Show options, then stop.
