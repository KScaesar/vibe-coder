---
name: code-ontology-extractor
description: Extract business logic from a codebase and express it as a domain ontology in YAML and Markdown — concepts, events, declared relations, axioms & constraints, workflows, governed vocabulary, cross-context alignment, and explicitly tracked open questions. Use this whenever the user wants to understand what a system does in business terms rather than technical terms, asks to reverse-engineer or document legacy code, wants a domain model or vocabulary derived from source, needs to onboard onto an unfamiliar codebase, asks what business rules are buried in some code, or mentions ontology, domain knowledge extraction, or building a knowledge graph from code — even if they don't name a specific output format.
disable-model-invocation: true
---

# Code → Domain Ontology Extractor

## 1. Core Mission: Semantic Disambiguation & Cross-Context Alignment

In complex software systems (especially legacy or microservice architectures), different packages, services, or **Bounded Contexts (限界上下文)** naturally diverge in terminology:
- **Different Names, Same Meaning (同義異名)**: Billing calls it `PayerAccount`, CRM calls it `Client`, Ad Delivery calls it `Advertiser`.
- **Same Name, Different Meaning (異義同名)**: The word `Order` in the Sales Context represents a customer purchasing intent; in the Warehouse Context it represents a shipping fulfillment ticket.

### The Purpose of Ontology in this System
According to formal Knowledge Engineering standards (Studer et al., 1998; Gruber, 1993; W3C OWL 2), an **Ontology** (本體論) is:
> **"A formal, explicit specification of a shared conceptualization."**
> （對共享概念化模型的形式化、明確規範）

An Enterprise Ontology does not force every microservice to abandon its local ubiquitous language; rather, it provides a **machine-interpretable shared semantic anchor** and **logical reasoning framework** under the **Open World Assumption (OWA)**:
1. **Deduce Equivalence across Contexts (同義異名推論)**: Map divergent local identifiers across contexts (`concepts[].context_mappings` & `vocabulary[].aliases`) to a single canonical concept, allowing AI and downstream tools to reason that `Billing.Account` and `CRM.Client` represent the same core concept.
2. **Disambiguate Homonyms (異義同名消歧)**: Model distinct concepts with `disjoint_with` and document contextual boundaries in `vocabulary[].conflict_notes`.
3. **Taxonomic & Relational Reasoning (階層與關係推理)**:
   - *Subsumption* (`sub_class_of`): Automatic inheritance of axioms and constraints (e.g. `SpecialAdRequest sub_class_of AdRequest`).
   - *Inverse & Transitive Relations* (`inverse_of`, `characteristics: [transitive, functional]`): Automatic bidirectional relationship inference (`places` $\iff$ `placed_by`).
4. **Open World Assumption (OWA) & Epistemic Tracking**: Unobserved code branches are treated as *unknown* rather than *false*, surfaced cleanly via `open_questions`.

---

## 2. The Core Knowledge Components

Every extracted domain ontology captures these essential knowledge components:
1. **Concepts / Classes (概念與類別, TBox)**: First-class business subjects, operational assets, agreements, and governed resources (e.g. `Customer`, `Order`, `AdCreative`, `Settlement`). (Represented as `concepts` in schema; *never call them `entities`*).
   - `sub_class_of`: Parent concept for taxonomic reasoning.
   - `disjoint_with`: Mutually exclusive concepts for consistency checking.
   - `context_mappings`: Local name & symbol projections across Bounded Contexts.
2. **Data Properties (數據屬性)**: Characteristics and value constraints associated with a concept (e.g. `placement`, `creationTimestamp`). Excludes physical database storage types. (Represented as `concepts[].properties`).
3. **Declared Object Properties / Relations (聲明對象關係)**: Intentional, directed semantic connections between concepts (`Subject - Predicate - Object`), supporting `inverse_of` and `characteristics`. (Represented as `relations`).
4. **World Events & Occurrences (世界事實與事件型態)**: Structured records of occurrences in the world (e.g. `AdImpression`, `ConversionRecorded`, `DeliveryDelayed`), capturing participants, targets, temporal aspect, and causality for knowledge querying. (Represented as `events`).
5. **Axioms & Domain Constraints (公理與約束)**: Formal logical assertions and invariant rules that necessarily hold in the domain:
   - *Cardinality*: Quantity bounds on relationships (e.g. `Order` contains $\ge 1$ `OrderItem`).
   - *Optionality*: Mandatory vs. conditional existence (e.g. `createdAt` mandatory; `cancelledAt` conditional).
   - *Validity Conditions*: Semantic validity boundaries (e.g. `amount >= 0`, `discount <= 0.85`).
   - *Classification Axioms*: Logical rules classifying instances into defined categories (e.g. `VIPCustomer` if spend $> 1M$).
   - *Access Restrictions*: Domain operational boundaries on read/write actions.
   (Represented as `axioms`).
6. **Governed Vocabulary / Lexicon (受治理詞彙)**: Single source of semantic truth, unifying canonical terms, recording aliases, and documenting cross-module semantic divergences (`conflict_notes`). (Represented as `vocabulary`).
7. **Workflows & Operational Processes (業務流程與運作過程)**: Structured causal sequences of operations and world events describing how the domain operates. (Represented as `workflows`).
8. **Epistemic Gap Tracking (認知缺口追蹤)**: Explicit tracking of unconfirmed inferences, low-confidence assumptions, and code/comment contradictions. (Represented as `open_questions`).

---

## 3. Boundary: Semantic Model (Ontology) vs. Behavioral Model (Code / DDD)

| Ontology (Semantic Layer) | Code / DDD (Behavioral Layer) | Boundary & Distinction |
|---|---|---|
| **Concept / Class** | **Entity / Value Object** | Concept is a semantic category. Software Entity has identity, lifecycle, and **active behavior** (`order.cancel()`). |
| **Declared Relation** | **Association / Reference** | Declared Relation is a semantic triple (`places`, `settles`); code references are bound to aggregate root transactions. |
| **Axiom / Constraint** | **Invariant** | Axiom declares domain logic/meaning; Invariant is enforced by application code inside transaction boundaries. |
| **World Event (世界事實)** | **Domain Event (領域事件)** | **Ontology Event** records what happened in the world (participants, temporal, causality) for knowledge querying; **DDD Domain Event** is a signal the software system **must actively react to** (workflow triggers). |
| **Vocabulary / Namespace** | **Bounded Context** | **Ontology** establishes mapped, cross-context shared semantics; **DDD** maintains isolated local models per Bounded Context. |

---

## 4. Output Deliverables & Format

Extraction produces **two paired deliverables**:
1. **Machine-Readable Knowledge Base**: `<system-name>.ontology.yml`  
   Strictly adheres to `references/ontology-schema.yml`. Defines the formal conceptualization and logic.
2. **Human-Readable Ontology Report**: `<system-name>.ontology.md`  
   Rendered from the finalized YAML according to `references/ontology-report-template.md`. Contains Mermaid semantic graphs, scalable bullet-list cross-context alignment, concepts, relations, events, axioms, workflows, and epistemic gaps.

Never generate the whole ontology in one pass. Work through the four passes below, stopping at the two mandatory breakpoints.

## Bundled Resources & CLI Reference

| Resource | Purpose | Invocation & Flags |
|---|---|---|
| `references/ontology-schema.yml` | Output schema specification for `<system>.ontology.yml`. | Read before producing YAML knowledge bases. |
| `references/ontology-report-template.md` | Template guide for `<system>.ontology.md` report. | Read before rendering Markdown reports. |
| `scripts/inventory.py` | Pass A AST & text cross-layer symbol inventory. | `uv run scripts/inventory.py <repo> [--json out.json] [--top 60] [--min-layers 1]` |
| `scripts/harvest_comments.py` | Pass A/B/C comment extractor & classifier. | `uv run scripts/harvest_comments.py <repo> [--json out.json] [--kind conflict] [--top 40]` |
| `scripts/rules/*.yml` + `sgconfig.yml` | Pass C structural AST rules for magic numbers & fallbacks. | `ast-grep scan -c scripts/sgconfig.yml <repo> [--json]` |
| `evals/validate_ontology.py` | Two-tier structural & semantic ontology validator. | `uv run evals/validate_ontology.py <file.ontology.yml> [--json out.json]` |

### Detailed Script Parameters:

#### 1. `scripts/inventory.py`
- `<repo>` *(positional, required)*: Root path of the codebase to scan.
- `--json <path>`: Write complete candidate inventory (with metrics, layer counts, evidence) to a JSON file.
- `--top <N>` *(default: 60)*: Number of top-ranked candidates to print to stdout.
- `--min-layers <N>` *(default: 1)*: Filter candidates to only those spanning $\ge N$ architectural layers (`api`, `domain`, `storage`, `config`, `logic`). Use `--min-layers 2` or `3` to eliminate single-file local variables.

#### 2. `scripts/harvest_comments.py`
- `<repo>` *(positional, required)*: Root path of the codebase to scan.
- `--json <path>`: Write structured harvested comments to a JSON file.
- `--kind <tag>`: Filter comments by semantic tag:
  - `conflict`: Naming collisions and cross-context disagreements (feed to `vocabulary[].conflict_notes`).
  - `rationale`: Domain rules and business logic rationale (feed to `axioms`).
  - `doc`: Concept definitions attached to declarations (feed to `concepts[].description`).
  - `flag`: TODO, FIXME, warning notes, and known edge constraints.
- `--top <N>` *(default: 40)*: Number of comments to display in stdout.
- `--include-noise`: Include boilerplate headers, linter pragmas, and commented-out code.
- `--min-doc-lines <N>` *(default: 5)*: Doc comment line count threshold promoted to `rationale`.
- `--min-doc-chars <N>` *(default: 100)*: Character count threshold floor/rescue for dense comments (e.g. CJK prose).

#### 3. `evals/validate_ontology.py`
- `<file.ontology.yml>` *(positional, required)*: Path to the ontology YAML file.
- `--json <path>`: Write detailed check results (error tier and human review tier) to JSON.

`tests/`, `scripts/rule-tests/` and `evals/` are for maintaining this skill — see *Keeping the scanners honest*.

---

## 5. Comments Are Primary Evidence

Code states what happens. Comments state why. An ontology needs the why, so comments are frequently the only written record of a domain decision.

```bash
uv run scripts/harvest_comments.py <repo> --json comments.json
uv run scripts/harvest_comments.py <repo> --kind conflict   # read these first
```

| Tag | Why it matters |
|---|---|
| `conflict` | States that two names are not interchangeable or carry different meanings across contexts. Goes straight to `vocabulary[].conflict_notes`. Read these first. |
| `doc` | Attached to a declaration; primary source for `concepts[].description` and `events[].description`. |
| `rationale` | Sits beside a constant or branch, explaining domain rules or business rationale. Primary source for `axioms[].description`. |
| `flag` | TODO / FIXME / 注意 / 待確認. Often records a known business constraint or deliberate deviation. |
| `boilerplate`, `commented_code` | Filtered out by default. |

**Length rule**: A doc comment longer than 5 lines is tagged `rationale` automatically. Lines are language-neutral; characters provide auxiliary floor and rescue checks.

**Intent vs. Current Behavior**: Comments drift from code. Contradictions between comment and code are findings: raise them as `open_questions` rather than guessing a winner.

---

## 6. Execution Pipeline

### Pass A — Map (No Inference)

Scan only. Produce no concepts, no axioms, no relations.

```bash
uv run scripts/inventory.py <repo> --json inventory.json
uv run scripts/harvest_comments.py <repo> --json comments.json
```

- Calculates **cross-layer survival**: how many distinct architectural layers (`api`, `domain`, `storage`, `config`, `logic`) each normalized identifier spans.
- Identifiers spanning $\ge 3$ layers are strong domain candidates. Single-file identifiers are likely technical artifacts.
- `rank_score` is a reading priority order, not a verdict.

#### Downstream Call-Graph Traversal (Entry Point Rule)
When the analysis target is an entry point (e.g. HTTP route, RPC handler, CLI command, event listener):
- **Entry points are interaction boundaries and protocol dispatchers, not domain concepts.**
- **Trace data and call flows downstream:** Follow function invocations and data dependencies into the service, domain, and state layers to discover persistent domain concepts and world events.

---

### Pass B — Vocabulary, Concepts & Context Alignment, Then STOP

Classify candidates into `domain_candidate`, `technical_artifact`, or `unknown`.

#### Architectural Layers (技術分層) vs. Bounded Contexts (業務限界上下文)
> [!IMPORTANT]
> **絕對嚴禁將技術架構分層（`api`, `storage`, `dto`）混淆為 DDD 限界上下文（Bounded Contexts）**：
> - **架構技術分層（Layers）**：`api` (Handler/DTO), `domain` (業務邏輯), `storage` (DAO/DB Table)。這是單一服務內部的技術管線，DTO 與 DAO 是技術產物，直接過濾排除。
> - **業務限界上下文（Bounded Contexts）**：`billing` (帳務), `crm` (客戶關係), `settlement` (結算履約), `ad_decision` (廣告決策)。這是業務子領域與通用語言邊界。`concepts[].context_mappings` 專門記錄不同 Bounded Context 間的語意對齊。

#### Detecting "Different Names, Same Meaning" (Cross-Context Aliasing)
- Compare data models and comments across distinct business modules / subdomains (e.g. `billing` calls it `PayerAccount` vs. `crm` calls it `Client`).
- If they refer to the same underlying business subject, declare one canonical concept in `concepts` and record local names in `concepts[].context_mappings` and `vocabulary[].aliases`.

#### Detecting "Same Name, Different Meaning" (Homonym Disambiguation)
- Identify vocabulary collisions from `conflict`-tagged comments and cross-subdomain divergence.
- If the same term is used for different domain models across Bounded Contexts (e.g. `Order` in Sales vs. `Order` in Warehouse), split them into distinct `concepts`, mark them with `disjoint_with` if applicable, and document the divergence in `vocabulary[].conflict_notes`. **Never pick a winner.** The disagreement is the finding.

#### Universal Structural Inquiries
To discover domain concepts and world events across any codebase:
1. **Commercial / Account Boundary**: What concept establishes legal, billing, account, or contractual boundaries?
2. **Operational Asset**: What concept represents the primary product, payload, material, or inventory being processed or scheduled?
3. **Resource / Spatial Boundary**: What concept models capacity, location, slot, channel, or operating environment?
4. **Governing Policy & Quota**: What data structures model limits, frequency caps, rate budgets, or state constraints?
5. **Historical World Events**: What occurrences represent business facts that happened in the world (e.g. conversions, impressions, transactions)?

#### Protocol Envelopes vs. Domain Concepts & Events
- **Protocol Envelopes (Transport Plumbing)**: DTOs, wire formats, serialization wrappers (e.g., `JSONPayload`, `RPCRequestBuffer`, `HTTPMiddleware`, `RedisKeyBuilder`). Exclude from concepts unless the system's core business is protocol conversion.
- **Domain Concepts & Events (Core Business Subjects & Facts)**: Core business subjects, operational assets, and historical world events governed by domain policies.

#### 🛑 Breakpoint 1 — Vocabulary, Concepts & Context Review
1. Save intermediate state to `<system-name>.pass-b-draft.yml`.
2. Present the candidate list, classifications, cross-context aliases, and naming conflicts in **one batched message**.
3. Attach `proposed_default` to questions to minimize human review effort.
4. Wait for user confirmation before proceeding.

---

### Pass C — Axioms, Constraints & Workflows

Derive `workflows`, `events`, and `axioms` (business constraints & axioms) from confirmed vocabulary and concepts.

```bash
ast-grep scan -c scripts/sgconfig.yml <repo>
```

#### Discriminators:
1. **The Constant Matrix**:
   | | Technical Artifact | Business Constraint / Axiom |
   |---|---|---|
   | **What changes if altered** | Server load, memory, retry latency | Billed amount, discount, risk limit, qualification window |
   | **Where it lives** | Client init, connection pool, transport middleware | Domain concept, state transition check, pricing logic |
   | **Typical shape** | `timeout: 30s`, `max_conns: 100` | `discount: 0.85`, `cool_off_days: 7`, `max_loan: 50000` |
   | **Handling** | Exclude from ontology | Record in `axioms`; if undocumented, raise `open_question` |
   *Exception*: Unusually specific constants (e.g. `timeout: 2.7s`) often disguise contractual SLAs or downstream partner windows; raise an `open_question`.

2. **Silent Fallbacks are Policy in Disguise**:
   Default returns, swallowed errors, and "return first item if none qualify" often encode implicit business decisions (e.g., *never return empty creative*).

3. **The Rewrite Test**:
   If the system were rewritten in another language on a different database, would this logic survive? Infrastructure plumbing (`if err != nil`, connection retry) disappears; business quotas and domain constraints do not.

---

### Pass D — Declared Relations, Final Review & Report Generation

Build `relations`, finalize `open_questions`, save both YAML and Markdown deliverables.

1. **Declared Semantic Triples & Inverses**:
   - Model as open triples (`subject - predicate - object`).
   - Define `inverse_of` where meaningful (e.g. `places` <-> `placed_by`).
   - Specify `characteristics` (e.g. `transitive` for hierarchical containment, `functional` for 1-to-1 associations).
   - Use `implemented_by` to link a business concept to its realizing service/function (put code coordinates in `provenance`, not in custom fields).
2. **Finalize Open Questions (OWA Compliance)**:
   - Group by severity (`P0`: blocking model integrity, `P1`: plausible default needing confirmation, `P2`: minor edge case).
   - Every claim with `confidence < 0.5` **must** have a corresponding `open_questions` entry.
3. **Generate Paired Output Artifacts**:
   - Step 1: Save machine-readable specification to `<system-name>.ontology.yml`.
   - Step 2: Render human-readable report to `<system-name>.ontology.md` following `references/ontology-report-template.md`.

#### 🛑 Breakpoint 2 — Ontology Review
1. Validate output: `uv run evals/validate_ontology.py <system-name>.ontology.yml`.
2. Present the summary along with prioritized open questions (`P0` leading) and links to `<system-name>.ontology.yml` and `<system-name>.ontology.md`.
3. Record human adjustments in `human_note` and set `human_verified: true`. Do not overwrite initial inferred guesses.

---

## 7. Confidence & Evidence Tiers

Anchor `confidence` to objective evidence:
- `0.9`: External contract (spec, vendor doc, schema, API contract) agrees with name and usage.
- `0.7`: Doc comment or explicit written rationale explains intent, or usage is consistent across $\ge 3$ layers.
- `0.5`: Single-site inference, suggestive naming, no written documentation.
- `0.3`: Magic number, opaque fallback, or speculative intent.

---

## 8. Keeping the Scanners Honest

Run test suites before and after modifying detection rules:
```bash
uv run tests/run_tests.py
```

| Verification Layer | Where it belongs |
|---|---|
| Pattern matches wrong syntax / regex defect | `tests/` — deterministic |
| ast-grep rule syntax / pattern validity | `scripts/rule-tests/` |
| LLM judgment (hallucinated concept, skipped breakpoint, promoted technical constant) | `evals/` — transcript evaluation |

---

## 9. What NOT to Do (Summary Checklist)

- **Do NOT confuse Ontology with Code Summary**: Do not paraphrase functions line-by-line or list AST structures.
- **Do NOT confuse Ontology with Database Storage (ERD)**: Do not include storage data types (`bigint`, `varchar`, `jsonb`) in concept properties.
- **Do NOT confuse Ontology with Software Execution (DDD)**: Do not assign procedural execution responsibilities or aggregate locking rules to ontology concepts.
- **Do NOT confuse World Events with DDD Domain Events**: Do not treat world event definitions as Message Queue callback code; model who, what, when, and causality.
- **Do NOT invent concepts, events, or relations** just to make a knowledge graph appear complete. Honest gaps are better than hallucinations.
- **Do NOT silently resolve naming conflicts**. Record the ambiguity in `vocabulary[].conflict_notes` and use `context_mappings` / `disjoint_with` for disambiguation.
- **Do NOT confuse Architectural Layers with DDD Bounded Contexts**: Do NOT treat `api`, `storage`, `dto`, or `middleware` as Bounded Contexts. Context mappings strictly map business subdomains (`billing`, `settlement`, `ad_decision`, `crm`), not technical tiers.
- **Do NOT leak scanner metrics** (`rank_score`, `layer_count`, `occurrences`) into the final ontology YAML or Markdown report.
