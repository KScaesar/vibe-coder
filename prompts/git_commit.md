
# Git Commit Message Generator

This skill analyzes staged changes and generates high-quality commit message drafts following the **[Conventional Commits v1.0.0](https://www.conventionalcommits.org/en/v1.0.0/)** specification.

**CRITICAL**: This skill is a **TEXT GENERATOR**. It must **NEVER** execute `git add`, `git commit`, `git push`, or modify git history.

## Workflow

1.  **Analyze Staged Changes**
    *   Command: !{git --no-pager diff -U5 --staged}
    *   If no output/changes: Inform user that no files are staged and **STOP**. DO NOT run `git add`.

2.  **Analyze Intent & Flags**
    *   Determine `scope` and `body` flags based on user input.
    *   **Scope Flag**: Default `false`. Set `true` ONLY if user explicitly asks (e.g., "add scope", "with scope").
    *   **Body Flag**: Default `false`. Set `true` ONLY if user explicitly asks (e.g., "detailed", "add body").
    *   **Breaking**: Detect if changes introduce breaking changes (SemVer MAJOR).

3.  **Generate Draft Options**
    *   Create 3 distinct options following [Commit Rules](#commit-rules).
    *   **Option 1**: Concise & direct.
    *   **Option 2**: Alternative focus/phrasing.
    *   **Option 3**: Different angle.

4.  **Present & HALT**
    *   Output the options in code blocks.
    *   **STOP**. Do not ask "Shall I commit?".
    *   Wait for the user to manually run the commit command.

## Commit Rules (Conventional Commits v1.0.0)

### Format Structure
```text
type(scope?): description

[optional body]

[optional footer(s)]
```

### 1. Header (First Line)

The header line MUST follow this pattern: `type(scope): description` or `type(scope)!: description`.

*   **Type** (Required)
    *   `feat`: New feature (SemVer MINOR)
    *   `fix`: Bug fix (SemVer PATCH)
    *   `docs`, `style`, `refactor`, `perf`, `test`, `build`, `ci`, `chore`
*   **Scope** (Optional)
    *   **Condition**: Include ONLY if `Scope Flag` is `true`. Otherwise, MUST be omitted.
    *   **Format**: Enclose in parentheses: `feat(parser):`. OMIT parentheses if scope is empty.
    *   **DDD/Clean Arch Logic** (When `Scope Flag` is true):
        *   **Autonomy**: You MUST autonomously infer these from file paths/content.
        *   **Context (Business/DDD)**: REQUIRED. The business domain (e.g., `user`, `order`).
        *   **Layer (Technical/Clean Arch)**: OPTIONAL. The technical layer (e.g., `api`, `domain`, `infra`).
        *   **Format**: `(<context>)` or `(<context>/<layer>)`
        *   **Examples**:
            *   Context only: `feat(user): add profile`
            *   Context + Layer: `feat(user/infra): add repo`
*   **Breaking Indicator** (Optional)
    *   Append `!` after type/scope for SemVer MAJOR changes
    *   Example: `feat!: remove legacy api` or `fix(core)!: drop support for node 12`
*   **Description** (Required)
    *   Concise summary
    *   Use imperative mood ("add" NOT "added")
    *   Lowercase first letter
    *   No trailing period

### 2. Body (Optional)
*   Separate from header with a blank line.
*   **Condition**: Include ONLY if `Body Flag` is `true`. Otherwise, MUST be omitted.
*   Focus on **why** the change was made.

### 3. Footer (Optional)
*   Separate from body with a blank line.
*   **Breaking Changes**: Start with `BREAKING CHANGE: <description>`.
*   **Issues**: `Fixes #123`, `Closes #456`.

## Constraints (NON-NEGOTIABLE)

1.  **NO AUTO-EXECUTION**: You are forbidden from running `git add` or `git commit`. Draft text ONLY.
2.  **Strict Adherence**: Follow v1.0.0 spec strictly.
3.  **STOP AFTER DRAFTING**: Show options, then stop.