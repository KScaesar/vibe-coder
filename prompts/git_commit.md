# Git Commit Message Generator

## Task
Generate a Git commit message based on community conventional commit standards, explicitly integrating both DDD (Domain-Driven Design) and Clean Architecture principles. For each message:
- Highlight the impacted domain or bounded context (e.g., user, order, payment).
- Identify the specific architecture layer affected (e.g., biz, use-case, db, api, cli).

### Workflow
1. Generate and list 3 distinct draft commit message options.
2. If the developer requests the detail flag, provide for each option a detailed body, presenting the rationale and changes in bulleted or list form.
3. Prompt the developer to indicate satisfaction with the generated commit message options.
    - If the developer is unsatisfied, repeat the process and present new options until satisfaction is confirmed.
4. Once the developer confirms their chosen commit message, stop and await further instructions. Do not execute any further actions.

After generating messages or detailed bodies, perform a short validation—ensure all required DDD and Clean Architecture elements are present and that formatting matches the specified template.

## Message Thinking Approach

- DDD: Clearly identify the affected domain or bounded context (e.g., user, order, payment).

- Clean Architecture: Specify the impacted architecture layer(s) (e.g., biz, use-case, db, api, cli).

## Commit Message Format
```
<type>(<scope>?): <description>

<body>

<footer>?
```
- **Type:** feat, fix, docs, style, refactor, perf, test, build, ci, chore, etc.
- **Description:** Concise summary of changes (≤60 characters, imperative mood)
- **Body (optional):** Detailed, bulleted or list-style explanation (include only with detail flag)
- **Scope (optional):** Affected module and contextual details
- **Footer (optional):** Notes such as BREAKING CHANGE or issue references (e.g., Fixes #issue)

## Examples
- feat(user/biz): add user validation service
- fix(order/use-case): resolve order payment processing issue
- refactor(payment/db): improve payment processing logic

## Constraints
- After developer confirmation, do not execute further commands. Await developer action.
- Do not use markdown bold, italics, or similar highlight formatting.
