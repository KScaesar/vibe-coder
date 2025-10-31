# Git Commit Message

## Task

Generates a Git commit message base on community conventional commits.

The commit message must be combining DDD (Domain-Driven Design), Clean Architecture of a commit message, you would typically highlight the impacted domain, architecture layer.

First, list 5 optional draft commit messages.
Then provide vary detailed body for every option only if the developer requests detail flag.

Keep asking the developer whether they are satisfied with the generated commit message.
If the developer disagrees, generate next process, and repeat this process until the developer agrees.

## Guideline

Design Thinking Approach:
- DDD: Focus on the domain or bounded context (e.g., user, order, payment).
- Clean Architecture: Specify the layer affected (e.g., biz, use-case, db, api, cli).

## Format

```
<type>(<scope>?): <description>

<body>

<footer>?
```

Rules:
- type: feat, fix, docs, style, refactor, perf, test, build, ci, chore ... etc
- description: brief change summary, ≤60 chars, imperative mood
- body: detailed explanation, present the information in a bulleted (or list) format.

Optional:
- scope: specifies affected module and provides additional contextual information
- footer: includes BREAKING CHANGE or issue references (e.g. Fixes #issue or Refs)

## Example

- feat(user/biz): add user validation service
- fix(order/use-case): resolve order payment processing issue
- refactor(payment/db): improve payment processing logic

## Constraints

- 開發者確定 commit message 之後, 不要再執行任何指令, 等待開發者行動
- 不要有任何 markdown 粗體或斜線等 highlight 格式
