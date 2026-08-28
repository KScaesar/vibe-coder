---
name: code-ontology-extractor
description: Extract business logic from a codebase and express it as a domain ontology in YAML — entities, workflows, business rules, relationships, and explicitly tracked open questions. Use this whenever the user wants to understand what a system does in business terms rather than technical terms, asks to reverse-engineer or document legacy code, wants a domain model or glossary derived from source, needs to onboard onto an unfamiliar codebase, asks what business rules are buried in some code, or mentions ontology, domain knowledge extraction, or building a knowledge graph from code — even if they don't name a specific output format.
disable-model-invocation: true
---

# Code → Domain Ontology Extractor

## What this is not

Not a code summarizer. A summary says what a function does. An ontology says what concepts the system believes exist.

| Code summary | Ontology extraction |
|---|---|
| what a function does | what concepts exist |
| module structure | domain entities |
| API input/output | business workflows |
| if statement | business rule |

The task is translating **implementation language** into **business concept language**. The dominant failure mode is mistaking implementation detail for business meaning, and most of this skill exists to prevent that.

The second failure mode is filling gaps with plausible invention. A sparse ontology with honest gaps is more useful than a complete-looking one with invented edges.

## Output

Write `<system-name>.ontology.yml` following `references/ontology-schema.yml`. **Read that schema before producing output** — it defines every field's purpose and expected values.

Never generate the whole ontology in one pass. Work through the four passes below, stopping at the two mandatory breakpoints.

## Bundled resources

| Path | When to use it |
|---|---|
| `references/ontology-schema.yml` | The output format. See *Output* above. |
| `scripts/inventory.py` | Run in Pass A. Executed, never read into context. |
| `scripts/harvest_comments.py` | Run in Pass A, read in Pass B and C. Extracts and tags comments. |
| `scripts/rules/*.yml` + `sgconfig.yml` | Passed to `ast-grep` in Pass C. Executed, never read into context. |

`tests/`, `scripts/rule-tests/` and `evals/` are for maintaining this skill, not for running it — see *Keeping the scanners honest*. Add a rule file when a new detection pattern proves useful; the rule set is meant to accumulate across projects rather than live inside the scanner.

## Comments are primary evidence

Code states what happens. Comments state why. An ontology needs the why, so comments are not decoration here — they are frequently the only written record of a domain decision, and the single richest input this skill has.

```bash
uv run scripts/harvest_comments.py <repo> --json comments.json
uv run scripts/harvest_comments.py <repo> --kind conflict   # read these first
```

The harvester merges consecutive line comments into one block before tagging, because a multi-line explanation is one artifact — tagging each `//` line separately shreds the most valuable thing in the file. Tags are multi-label, since one comment is often a doc comment, a naming warning, and a billing rule at once.

| Tag | Why it matters |
|---|---|
| `conflict` | States that two names are not interchangeable. Goes straight to `glossary[].conflict_notes`. Read these before anything else. Deliberately narrow: a contrastive phrase like "rather than" only counts when two identifier-shaped names sit in the same sentence, because this bucket is trusted on sight. |
| `doc` | Attached to a declaration, so it names and defines a concept. Primary source for `entities[].description`. |
| `rationale` | Sits beside a constant or branch, reads as explanation, or is a substantial doc block (see below). Primary source for `business_rules[].description`. |
| `flag` | TODO / FIXME / 注意 / 待確認. Often records a known business constraint or a deliberate deviation someone had to justify. |
| `boilerplate`, `commented_code` | Filtered out by default. |

**Length above a declaration is itself a signal.** A doc comment longer than 5 lines is tagged `rationale` automatically, no keyword required. Nobody writes five lines above a declaration to restate what the declaration already says; the effort means someone judged the concept worth explaining. This catches teams whose convention is a prose block above every type — exactly the case keyword matching misses, because a good explanation often contains no marker words at all.

**Line count decides; character count adjusts the edges.** Lines are the primary test because they are language-neutral. Characters serve two auxiliary roles:

- **floor** — six lines of `// a`, `// b` is padding, not an explanation. A comment clearing the line threshold but falling under `min-doc-lines × 8` characters is rejected.
- **rescue** — three lines of solid prose is an explanation. A comment under the line threshold but over `--min-doc-chars` is accepted.

Because the primary test is language-neutral, cross-language tuning matters less than it would if characters drove the decision. Only the rescue path is language-sensitive.

**A comment is strong evidence of intent and weak evidence of current behaviour.** Comments drift from the code they describe. Where a comment contradicts the code, that contradiction is a finding: raise it as an open question rather than choosing a side. A stale comment still tells you what the system was once meant to do, which is often exactly the business rule you are looking for.

Set `provenance.evidence_type: comment` for anything sourced this way, so a later reviewer can tell a claim about intent from an observation about behaviour. Where a finding could be labelled either by its tool or by its kind, the kind wins — the schema records the precedence.

## Script parameters

### `inventory.py <path>` — Pass A symbol and layer statistics

| Flag | Default | Purpose |
|---|---|---|
| `--json FILE` | — | Write the full result as JSON. Use this; the console output is truncated. |
| `--top N` | 60 | Rows printed to console. |
| `--min-layers N` | 1 | Drop identifiers appearing in fewer than N layers. On a large repo raise it to cut the tail; 3 is the threshold Pass A treats as a likely domain concept. |

### `harvest_comments.py <path>` — comment extraction and tagging

| Flag | Default | Purpose |
|---|---|---|
| `--json FILE` | — | Write the full result as JSON, UTF-8 unescaped. |
| `--kind TAG` | — | Filter to one tag: `conflict`, `doc`, `rationale`, `flag`, `other`. |
| `--top N` | 40 | Rows printed to console. |
| `--include-noise` | off | Also emit boilerplate and commented-out code. Normally leave off. |
| `--min-doc-lines N` | 5 | **Primary test.** A doc comment with more lines than this is tagged `rationale` regardless of wording. Language-neutral. |
| `--min-doc-chars N` | 100 | **Auxiliary.** Rescues a dense block that falls under the line threshold. Also derives a floor (`min-doc-lines × 8`) that rejects line counts padded with near-empty lines. Language-sensitive — see below. |

### Calling it: CJK vs Latin codebases

The line threshold works unchanged across languages. Only `--min-doc-chars`, which governs the rescue path, needs adjusting: 100 characters is a full paragraph in Chinese and a single sentence in English, so the default rescues too eagerly on English source.

**Chinese / Japanese / Korean comments** — defaults are calibrated for this, no tuning needed:

```bash
uv run scripts/inventory.py <repo> --json inventory.json
uv run scripts/harvest_comments.py <repo> --json comments.json
uv run scripts/harvest_comments.py <repo> --kind conflict          # read first
uv run scripts/harvest_comments.py <repo> --kind rationale --top 30
```

**English comments** — raise the character threshold so ordinary one-line docs don't all become rationale:

```bash
uv run scripts/harvest_comments.py <repo> --min-doc-chars 250 --json comments.json
```

**Mixed-language codebase** — disable the rescue path and let the line count decide alone:

```bash
uv run scripts/harvest_comments.py <repo> --min-doc-chars 99999 --min-doc-lines 4 --json comments.json
```

Note this also lowers the floor to 32 characters, since the floor tracks the line threshold.

**Calibrating.** Run the `rationale` filter first and look at the count. Hundreds of hits means the threshold is too low for this codebase — raise it. Single digits means comments are scarce, so Pass C will lean on the magic-number sweep instead and Breakpoint 1 will need more of the human's time. Either way, learn this number before starting Pass B.

Tag patterns cover English, Chinese and a few Japanese markers. For another language, extend the marker patterns at the top of the script — `FLAG_RE`, `RATIONALE_RE`, and the `STRONG_`/`WEAK_CONFLICT_RE` pair. The length rule works regardless of language and needs no change.

---

## Setup

Both tools install through `uv`. No Node, no compiler, no buildable project required.

```bash
uv tool install ast-grep-cli          # structural pattern scanning
uv run scripts/inventory.py <path>    # deps declared inline via PEP 723
```

`inventory.py` carries its own dependencies in a PEP 723 header, so `uv run` resolves them automatically — no virtualenv, no requirements.txt to drift out of sync.

If the team already standardises on mise, add ast-grep with an explicit npm backend (`"npm:@ast-grep/cli" = "latest"`). Avoid backends that resolve through the GitHub API — they hit rate limits without a token. Do not introduce mise solely for this skill.

**Tooling tiers.** Use the best available, and record it in `provenance.evidence_type` when no more specific kind applies:

1. **tree-sitter / ast-grep** (default). Parses without resolving dependencies, so it works on projects that don't build. Excludes comments and strings from symbol extraction, which is the main gain over grep.
2. **LSP** (opt-in). If a language server is already running and the project resolves, cross-file reference counts are more accurate than anything above. Treat as a bonus, not the main path — LSP answers syntax questions, and the hard part here is semantics.
3. **Plain grep** (fallback). For languages without a grammar. Works, but will match inside comments and strings.

Never convert tool precision into a confidence penalty. Precision and semantic certainty are independent axes; see the schema's note on `evidence_type`.

---

## Pass A — Map (no inference)

Scan only. Produce no entities, no rules, no relationships.

```bash
uv run scripts/inventory.py <repo> --json inventory.json
uv run scripts/harvest_comments.py <repo> --json comments.json
```

The script extracts declared symbols per file, classifies each file into a layer (api / domain / storage / config / logic), and computes **cross-layer survival**: how many distinct layers each identifier appears in, after normalising case variants so `orderItemId`, `order_item_id` and `ORDER_ITEM_ID` collapse together.

An identifier surviving across three or more layers is likely a domain concept. One living in a single file is likely a technical artifact.

Tests and documentation are scanned for vocabulary but do not count as layers. A name that appears in the README and nowhere else has crossed no boundary, and letting docs count would promote it over names that genuinely span api and storage.

**Treat `rank_score` as a reading order, not a verdict.** It says what to inspect first and nothing more. Do not carry the number into the ontology.

The scanner excludes comments from these counts on purpose — a comment mentioning `AccountLimit` should not inflate its layer count. That exclusion applies to the identifier statistics only. Comments are collected separately by the harvester and carry more domain signal than the symbol table does.

Also collect by hand what the script doesn't: external integrations, third-party specs the system must conform to, and any README or architecture doc. External contracts are the strongest evidence available in Pass C.

### Downstream Call-Graph Traversal (Entry Point Rule)

When the analysis target is an entry point (e.g. HTTP route, RPC handler, CLI command, or event listener):
- **Entry points are interaction boundaries and protocol dispatchers, not domain entities.** An endpoint represents a transport interface or an operation trigger.
- **Trace data and call flows downstream:** Follow function invocations and data dependencies into the service, domain, and state layers to discover the persistent data structures and business models being loaded, evaluated, or mutated.

## Pass B — Vocabulary, then stop

Classify each candidate as `domain_candidate`, `technical_artifact`, or `unknown`.

An entity normally has all three of: **identity** (something distinguishes one instance from another), **lifecycle** (created, updated, expired, converted), and **meaning to someone who has never read the code**. `Account`, `Order`, and `Subscription` qualify. `RedisKey`, `HTTPRequest`, `KafkaMessage` do not.

### Protocol Envelopes vs. Domain Entities

Distinguish between **transport envelopes** and **domain entities**:
- **Protocol Envelopes (Transport & Serialization Containers)**: Wire formats, Data Transfer Objects (DTOs), and serialization wrappers (e.g. JSON payloads, XML envelopes, RPC request/response buffers). These represent transport mechanisms and technical plumbing, not domain entities (unless the system's explicit core domain is protocol conversion).
- **Domain Entities (Core Business Subjects & Assets)**: The persistent business subjects, agreements, operational assets, and resources governed by the system's business policies.

To ensure comprehensive entity discovery across diverse architectures without assuming specific design paradigms (e.g. DDD or Clean Architecture), verify candidates against the **Universal Structural Inquiries**:
1. **Commercial / Account Boundary**: What entity establishes the legal, billing, account, or contractual boundary?
2. **Operational Asset**: What entity represents the primary work, product, payload, or inventory being processed, scheduled, or delivered?
3. **Resource / Spatial Boundary**: What entity models the capacity, location, slot, channel, or environment where the operation occurs?
4. **Governing Policy & Quota**: What data structures model the limits, frequency caps, rate budgets, or state transition constraints?

Infrastructure vocabulary (`request`, `handler`, `payload`, `config`) is **downweighted by the scanner, never dropped** — in some systems, an inbound request (such as a claim or bid) is a core domain entity, not plumbing. Record any correction in `system.vocabulary_overrides` so the next run inherits it.

Then detect naming conflicts, the highest-value output of this pass. Start from the harvester's `conflict`-tagged comments — where someone has already written down that two names differ, that note is worth more than any amount of inference:
- different names used for what appears to be one concept
- one name used for different concepts in different modules
- names colliding with an external specification's term but carrying different semantics

Record these in `glossary[].conflict_notes`. **Never resolve a conflict by picking a winner.** The disagreement is the finding.

### 🛑 Breakpoint 1 — vocabulary review

**Save intermediate state first.** Write the current Pass B results and vocabulary findings to `<system-name>.pass-b-draft.yml` following the schema structure. This ensures state persistence and prevents context loss in multi-turn or automated agent execution.

**Self-check before presenting:** Confirm that the candidate list captures the underlying domain assets (the entities answering the Universal Structural Inquiries) and has not merely recorded top-level API endpoint names or protocol envelopes.

Stop. Present the candidate list, the proposed classifications, and every naming conflict — all of it in one message. This is the cheapest correction point in the pipeline: a wrong definition fixed here saves correcting entities, rules and relationships downstream.

If the host offers a structured question tool, it will cap how many questions fit at once. Spend that budget on the classifications that genuinely turn on a yes/no, and put the rest in the message body; splitting a batch across several prompts costs the reviewer more than one long message does.

Invite the human to **add concepts the scan could not find**, not just correct what it did. Tribal knowledge — "we don't serve that partner on weekends, but it's handled upstream" — exists in no repository.

Wait for the response. Do not proceed on assumption.

## Pass C — Behavior

Derive `workflows` and `business_rules` from the confirmed vocabulary.

```bash
ast-grep scan -c scripts/sgconfig.yml <repo>              # every rule at once
ast-grep scan -r scripts/rules/magic-numbers-<lang>.yml <repo>   # or one at a time
```

Rules exist for Go and Python. On a language with no rule file, the three
discriminators below still apply — you just have to find the constants and
fallbacks by reading, so say so in `provenance.evidence_type` rather than
implying a scanner confirmed them.

Three discriminators, in order of usefulness:

### The constant matrix

Every numeric literal that isn't obvious boilerplate came from a person making a decision that the code does not record. Classify each:

| | Technical artifact | Business rule |
|---|---|---|
| **What changes if you alter it** | server load, throughput, memory, retry latency | billed amount, state transition condition, risk limit, compliance window |
| **Where it lives** | client init, middleware, connection pool | inside an entity, a state machine, a precondition check |
| **Typical shape** | `timeout: 30s`, `max_conns: 100`, `backoff: 2.0` | `discount: 0.85`, `cool_off_days: 7`, `max_loan: 50000` |
| **Handling** | exclude from the ontology | record in `business_rules`; if undocumented, also raise an open question |

**Exception worth watching for:** an unusually specific technical constant. `timeout: 30s` is a template value; `timeout: 2.7s` means someone measured something. For instance, an upstream timeout may be dictated by an external contractual SLA or downstream partner window — a business constraint wearing a performance-tuning costume. Technical constants are excluded by default, but a suspiciously precise one earns an open question.

### Silent fallbacks are policy in disguise

Default returns, swallowed errors, and "return the first item if nothing qualifies" routinely encode a business decision such as *never return an empty response*. They look like defensive coding and get skipped. Check every one the rules surface, and ask what the caller is being protected from.

### Read the rationale comments before guessing

Before inferring intent behind a constant, check whether `harvest_comments.py` already tagged a `rationale` comment on or beside that line. A written explanation moves the rule up the confidence table; reaching for inference when one already exists is the most avoidable error in this pass.

### The rewrite test

If this system were rebuilt in another language on a different database, would this logic survive? `if err != nil` disappears. A frequency cap does not.

Do not promote error handling, retries, connection pooling, or serialization concerns into business rules by default.

**If this pass reveals a concept Pass B never registered, go back to Pass B and add it** rather than forcing it into an existing entity. The pipeline has a loop here on purpose.

## Pass D — Graph and contradictions

Build `relationships` last, once entities and workflows are stable. `subject`/`object` aren't limited to `entities[].id` — they can point at a `workflows[].id` or `business_rules[].id` too, when that's the true shape of the connection. `predicate` is an open string, not a closed enum: write the verb a domain person would actually use ("places", not a forced-fit "owns"). Use `implemented_by` to connect a business concept to the function or service that realises it — this is what lets the ontology answer "who actually owns this". Put the code coordinates in `provenance`, not in a second set of fields on the relationship.

Because `predicate` is open text, watch for the same concept getting written as two different verbs across the same ontology (`owns` in one place, `has` in another). Don't silently pick one — that's a naming conflict like any other, so record it in `glossary[].conflict_notes` rather than letting both spellings stand.

Finalise `open_questions`. Every contradiction found in earlier passes lands here, unresolved.

### 🛑 Breakpoint 2 — ontology review

**Save final ontology file.** Write the complete ontology to `<system-name>.ontology.yml`.

Present the complete YAML plus the open questions grouped P0 / P1 / P2, each with its proposed default. Lead with the P0s — those are the ones that stop the model from standing up at all. Then stop.

---

## Confidence

Anchor `confidence` to evidence type, not intuition:

| Score | Evidence |
|---|---|
| 0.9 | an external contract (spec, vendor doc, schema) agrees with the name and the usage |
| 0.7 | a comment explains the intent, or usage is consistent across several files |
| 0.5 | single-site inference, the name is suggestive, nobody wrote anything down |
| 0.3 | magic number or opaque flag, the meaning is guessed |

**Anything below 0.5 must emit a matching `open_questions` entry.** Without that rule the score is decoration nobody acts on.

## Interaction protocol

**Batch questions.** One interruption with ten questions costs the human far less than ten interruptions.

**Attach a `proposed_default` to every question**, so the common case is confirming rather than composing an answer from scratch.

**Record answers in `human_note` and set `human_verified: true`.** Every reviewable section carries those two fields — see the schema's shared review block. Do not overwrite the original inferred `description`. Keeping the wrong first guess beside the correction is useful later, when someone asks why a field is named the way it is.

**An unanswered question stays open.** Never quietly promote a `proposed_default` into the body.

## Keeping the scanners honest

```bash
uv run tests/run_tests.py     # both scanners and every ast-grep rule
```

These scanners fail in a way that is easy to miss: they keep running and
quietly return the wrong set. A detector that matches nothing looks exactly
like a clean codebase; a tagger that over-matches looks like a codebase full
of findings. Neither surfaces as an error, and both corrupt the ontology
downstream — a false `conflict` lands directly in `glossary[].conflict_notes`,
which is the one bucket this skill tells you to trust on sight.

So checks are placed by what their failure would tell you:

| Failure | Where the check belongs |
|---|---|
| A pattern matched the wrong thing | `tests/` — deterministic, no transcript needed |
| A rule matched nothing | `scripts/rule-tests/` — ast-grep's own valid/invalid samples |
| The model invented an entity, skipped a breakpoint, or promoted a timeout to a business rule | an eval — judgment failures, diagnosable only from a transcript |

Anything a regex decides belongs in the first two rows. Reaching for an eval to
find a regex bug costs a full run and still leaves you reading transcripts to
learn which pattern broke.

`evals/fixtures/adserving` is a small Go service with eleven pieces of
evidence planted in it, and `evals/adserving.ground-truth.yml` is the answer
key — kept outside the fixture so scanning cannot reach it. Each plant says
which row above owns it: the tests assert only that the evidence surfaces,
while its `judgment` field describes what an eval would have to grade.
`evals/validate_ontology.py` sits between the two, failing only on what is
wrong whatever the house style and raising the rest as questions for a person.

**Add a rule's samples in the same change as the rule.** Several defects found
while writing these tests were rules that had never matched anything — among
them `$OBJ.Transition($$$)`, which does not parse as a Go pattern at all.
Running the scanner would never have revealed that; it just reported nothing.
Write the invalid samples inside a function, too: at file scope Go reads
`order.SetStatus(x)` as a type conversion, so a bare statement tests a shape
that does not occur in real source.

## What not to do

A recall list, deliberately repeating rules argued for above. If one of these
ever disagrees with the section it came from, the section is right — this is
the summary, not the source.

- Do not invent entities to make the graph look complete.
- Do not resolve naming conflicts. Record them.
- Do not put storage types (`bigint`, `varchar`) in entity attributes. Storage belongs to a metadata layer.
- Do not describe a workflow step by paraphrasing code line by line. If the description would be meaningless to someone who cannot read the language, rewrite it.
- Do not let `rank_score`, layer counts, or any scanner output appear in the final ontology. Those are inputs to your judgment, not findings.
