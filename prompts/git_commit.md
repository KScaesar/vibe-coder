# Git Commit Message Generator

## Task

Generate a Git commit message based on community conventional commit standards, explicitly integrating both DDD (Domain-Driven Design) and Clean Architecture principles.

## Flag Logic & Defaults

**Analyze the user's input for the following flags before generating messages:**

1. **Scope Flag (`scope`)**
    * **Default:** `false` (Do not include scope).
    * **Trigger:** If the user's input contains the word "scope" (or related terms like "add scope", "with scope"), set this flag to `true`.

2. **Body Flag (`body`)**
    * **Default:** `false` (Do not include body).
    * **Trigger:** If the user's input contains the word "body" (or related terms like "detailed", "explanation"), set this flag to `true`.

## Workflow

1. Codebase Diff: !{git --no-pager diff -U5 --staged}
2. Parse Flags: applying the logic defined in "Flag Logic & Defaults".
3. Generate Options: List 3 distinct draft commit message options.
  * If scope is false: Format must be `<type>: <description>`
  * If scope is true:
    * DDD: Highlight impacted Bounded Context or module (e.g., user, order, payment).
    * Clean Arch: Identify impacted layer (e.g., biz, db, api, workflow, gateway, mq).
  * If body is true: Append a bulleted list of changes and rationale.
4. Confirmation: Prompt the developer to indicate satisfaction.
  * If unsatisfied, repeat with new options.
5. Stop: Await further instructions after confirmation.

## Commit Message Format

```
<type>(<scope>?): <description>

<body>?

<footer>?
```

Detailed Rules:

* type: feat, fix, docs, style, refactor, perf, test, build, ci, chore.
* scope (Controlled by Flag):
    * **Case FALSE:** You **MUST NOT** output parentheses or scope text.
        * Correct: `feat: add user password validation`
        * Incorrect: `feat(user/biz): add user password validation`
    * **Case TRUE:**
        * Format must be `<type>(<context>/<layer>): <description>`
        * Vertical division (bounded context or module): Always required (e.g., user, order, payment)
        * Horizontal division (technical layer): Optional, **most cases don't need this**. Only add when the code architecture has clear technical layering (e.g., biz, db, api, workflow). **If unsure what layer to use, omit it.**
        * Format examples:
            * With layer: `feat(user/biz): add validation`
            * Without layer: `feat(user): add profile feature`
* body (Controlled by Flag):
    * **Case FALSE:** Omit entirely.
    * **Case TRUE:** Provide bullet points.
* footer (Optional): Include for breaking changes or issue tracking if context permits (e.g., BREAKING CHANGE: ... or Fixes #123).

## Constraints

* Do not use markdown bold (`**`), italics (`*`), or code blocks for the commit headers.
* Strictly follow the Flag Logic.
