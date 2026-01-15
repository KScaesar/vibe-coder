# Test-Driven Development (TDD)
[TOC]
## Overview

Write the test first. Watch it fail. Write minimal code to pass.

**Core principle:** If you didn't watch the test fail, you don't know if it tests the right thing.

**Violating the letter of the rules is violating the spirit of the rules.**

## When to Use

**Always:**
- New features
- Bug fixes
- Refactoring
- Behavior changes

**Exceptions (ask your human partner):**
- Throwaway prototypes
- Generated code
- Configuration files

## Constitution

```
You must have a failing test first;
otherwise, no production code should be written.
```

- Code before test
- Test after implementation
- Test passes immediately
- Can't explain why test failed
- Tests added "later"
- Rationalizing "just this once"
- "I already manually tested it"
- "Tests after achieve the same purpose"
- "It's about spirit not ritual"
- "Keep as reference" or "adapt existing code"
- "Already spent X hours, deleting is wasteful"
- "TDD is dogmatic, I'm being pragmatic"
- "This is different because..."

All of these mean: Delete code. Start over with TDD.

Write code before the test? Delete it. Start over.

## Workflow: Red-Green-Refactor

```mermaid
flowchart TB
    red["RED: Write failing test"]
    verify_red{"Verify fails correctly"}
    green["GREEN: Minimal code"]
    verify_green{"Verify passes, All green"}
    refactor["REFACTOR: Clean up"]
    next(["Next"])

    red --> verify_red
    verify_red -->|yes| green
    verify_red -->|wrong failure| red
    green --> verify_green
    verify_green -->|yes| refactor
    verify_green -->|no| green
    refactor -->|stay green| verify_green
    verify_green --> next
    next --> red
```

### 1.RED - Write Failing Test

Write one minimal test showing what should happen.

<Good>

```typescript
test('retries failed operations 3 times', async () => {
  let attempts = 0;
  const operation = () => {
    attempts++;
    if (attempts < 3) throw new Error('fail');
    return 'success';
  };

  const result = await retryOperation(operation);

  expect(result).toBe('success');
  expect(attempts).toBe(3);
});
```
Clear name, tests real behavior, one thing
</Good>

<Bad>

```typescript
test('retry works', async () => {
  const mock = jest.fn()
    .mockRejectedValueOnce(new Error())
    .mockRejectedValueOnce(new Error())
    .mockResolvedValueOnce('success');
  await retryOperation(mock);
  expect(mock).toHaveBeenCalledTimes(3);
});
```
Vague name, tests mock not code
</Bad>

**Requirements:**
- One behavior
- Clear name
- Real code (no mocks unless unavoidable)

### 2.Verify RED - Watch It Fail

**MANDATORY. Never skip.**

```bash
<test-runner> path/to/test_file
```

**Terminology:**
- **Fail** = Test runs, assertion doesn't match (expected ≠ actual)
- **Error** = Test can't run (exception, syntax error, missing import)

Confirm:
- Test fails (not errors)
- Failure message is expected
- Fails because feature missing (not typos)

**Test passes?** You're testing existing behavior. Fix test.

**Test errors?** Fix error, re-run until it fails correctly.

### 3.GREEN - Minimal Code

Write simplest code to pass the test.

<Good>

```typescript
async function retryOperation<T>(fn: () => Promise<T>): Promise<T> {
  for (let i = 0; i < 3; i++) {
    try {
      return await fn();
    } catch (e) {
      if (i === 2) throw e;
    }
  }
  throw new Error('unreachable');
}
```
Just enough to pass
</Good>

<Bad>

```typescript
async function retryOperation<T>(
  fn: () => Promise<T>,
  options?: {
    maxRetries?: number;
    backoff?: 'linear' | 'exponential';
    onRetry?: (attempt: number) => void;
  }
): Promise<T> {
  // YAGNI
}
```
Over-engineered
</Bad>

Don't add features, refactor other code, or "improve" beyond the test.

### 4.Verify GREEN - Watch It Pass

**MANDATORY.**

```bash
<test-runner> path/to/test_file
```

Confirm:
- Test passes
- Other tests still pass
- Output pristine (no errors, warnings)

**Test fails?** Fix code, not test.

**Other tests fail?** Fix now.

### 5.REFACTOR - Clean Up

After green only:
- Remove duplication
- Improve names
- Extract helpers

Keep tests green. Don't add behavior.

### 6.Repeat

Next failing test for next feature.

## Example TDD Workflow: Bug Fix

**Bug:** Empty email accepted

**RED**
```
test "rejects empty email":
    result = submitForm({ email: "" })
    assert result.error == "Email required"
```

**Verify RED**
```
$ <test-runner>
FAIL: expected "Email required", got undefined
```

**GREEN**
```
function submitForm(data):
    if isEmpty(data.email):
        return { error: "Email required" }
    // ...
```

**Verify GREEN**
```
$ <test-runner>
PASS
```

**REFACTOR**
Extract validation for multiple fields if needed.

## Verification Checklist

Before marking work complete:

- [ ] Every new function/method has a test
- [ ] Watched each test fail before implementing
- [ ] Each test failed for expected reason (feature missing, not typo)
- [ ] Wrote minimal code to pass each test
- [ ] All tests pass
- [ ] Output pristine (no errors, warnings)
- [ ] Tests use real code (mocks only if unavoidable)
- [ ] Edge cases and errors covered

Can't check all boxes? You skipped TDD. Start over.

## When Stuck

| Problem | Solution |
|---------|----------|
| Don't know how to test | Write wished-for API. Write assertion first. Ask your human partner. |
| Test too complicated | Design too complicated. Simplify interface. |
| Must mock everything | Code too coupled. Use dependency injection. |
| Test setup huge | Extract helpers. Still complex? Simplify design. |

## Debugging Integration

Bug found? Write failing test reproducing it. Follow TDD cycle. Test proves fix and prevents regression.

Never fix bugs without a test.
