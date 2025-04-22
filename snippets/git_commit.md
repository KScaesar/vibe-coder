# Git Commit Message

description:  

指導 LLM 產出符合 Conventional Commits 格式，並結合 DDD (Domain-Driven Design) 與 Clean Architecture 概念的 Git commit message

## Prompt Reference

https://www.conventionalcommits.org/en/v1.0.0/

---

## Prompt

Must be combining DDD (Domain-Driven Design), Clean Architecture of a commit message, 
you would typically highlight the impacted domain, architecture layer. 

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
- body: detailed explanation

Optional:
- scope: specifies affected module and provides additional contextual information
- footer: includes BREAKING CHANGE or issue references (e.g. Fixes #issue or Refs)

## Example

- feat(user/biz): add user validation service
- fix(order/use-case): resolve order payment processing issue
- refactor(payment/db): improve payment processing logic
