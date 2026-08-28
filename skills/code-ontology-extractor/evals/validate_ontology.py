# /// script
# requires-python = ">=3.11"
# dependencies = ["pyyaml>=6"]
# ///
"""Structural checks on a produced ontology.

Two tiers, because most of what makes an ontology good is a judgment call and
there is no one right way to write code or to describe it.

  error   — wrong whatever the house style: a relation pointing at nothing,
            a claim the skill's own rules say must carry an open question.
  review  — looks off, might be perfectly fine. Reported as a question for a
            person to answer, never as a verdict.

Only errors set the exit code. A review item is the same kind of thing as an
open_questions entry: the tool noticed something and is handing the decision
to someone who knows the domain.

    uv run evals/validate_ontology.py <file.ontology.yml> [--json out.json]
"""

import argparse
import json
import re
import sys
from pathlib import Path

import yaml

# Standard Knowledge Engineering sections with backwards-compatible aliases
SECTION_ALIASES = {
    "system": ["system"],
    "vocabulary": ["vocabulary", "glossary"],
    "concepts": ["concepts", "entities", "classes"],
    "workflows": ["workflows", "processes"],
    "axioms": ["axioms", "business_rules", "constraints"],
    "relations": ["relations", "relationships", "object_properties"],
    "open_questions": ["open_questions", "epistemic_gaps"],
}

# Storage vocabulary has its own layer. A property typed `varchar`
# describes the column, not the domain concept.
STORAGE_TYPE_RE = re.compile(
    r"\b(bigint|smallint|integer|int[248]?|varchar|nvarchar|char|text|numeric|"
    r"decimal|float[48]?|double|real|boolean|bool|timestamp(?:tz)?|datetime|date|"
    r"time|uuid|jsonb?|bytea|blob|serial|bigserial)\b", re.I)

# Ranking output is an input to judgment, not a finding.
SCANNER_LEAK_RE = re.compile(r"\b(rank_score|layer_count|layers?_survived|"
                             r"stopword_downweighted|occurrences|sample_locations)\b")

CONFIDENCE_FLOOR = 0.5


def walk_strings(node, path="$"):
    if isinstance(node, dict):
        for k, v in node.items():
            yield from walk_strings(v, f"{path}.{k}")
    elif isinstance(node, list):
        for i, v in enumerate(node):
            yield from walk_strings(v, f"{path}[{i}]")
    elif isinstance(node, str):
        yield path, node


def get_section(doc: dict, canonical_name: str) -> list | dict:
    for alias in SECTION_ALIASES.get(canonical_name, [canonical_name]):
        if alias in doc:
            return doc[alias]
    return []


def check(doc: dict) -> list[dict]:
    out = []

    def record(cid, text, passed, evidence="", tier="error"):
        out.append({"id": cid, "text": text, "passed": passed,
                    "evidence": evidence, "tier": tier})

    missing = [
        canonical for canonical, aliases in SECTION_ALIASES.items()
        if not any(alias in doc for alias in aliases)
    ]
    record("schema.sections", "Every schema section is present",
           not missing, f"missing: {missing}" if missing else "all present")

    concepts = get_section(doc, "concepts") or []
    events = doc.get("events") or []
    axioms = get_section(doc, "axioms") or []
    workflows = get_section(doc, "workflows") or []
    relations = get_section(doc, "relations") or []
    vocabulary = get_section(doc, "vocabulary") or []
    questions = get_section(doc, "open_questions") or []

    # A confidence score nobody acts on is decoration. The rule that makes it
    # mean something is that a low one has to surface as a question.
    referenced = {r for q in questions for r in (q.get("related_to") or [])}
    scored = concepts + events + axioms + workflows + vocabulary
    unbacked = [
        i.get("id") or i.get("term") for i in scored
        if isinstance(i, dict)
        and isinstance(i.get("confidence"), (int, float))
        and i["confidence"] < CONFIDENCE_FLOOR
        and (i.get("id") or i.get("term")) not in referenced
    ]
    record("confidence.open_question",
           f"Every claim below {CONFIDENCE_FLOOR} confidence has a matching open question",
           not unbacked, f"unbacked: {unbacked}" if unbacked else "none below floor, or all backed")

    typed = []
    for c in (concepts + events):
        if not isinstance(c, dict):
            continue
        props = c.get("properties") or c.get("attributes") or []
        for p in props:
            if isinstance(p, dict) and STORAGE_TYPE_RE.search(f"{p.get('name', '')} {p.get('description', '')}"):
                typed.append(f"{c.get('id')}.{p.get('name')}: {p.get('description', '')[:40]}")

    # A word like "timestamp" or "text" reads as a column type, but it is also
    # ordinary English. Worth a look, not worth a verdict.
    record("concepts.storage_flavoured_properties",
           "Do these properties describe the concept, or the column it is stored in?",
           not typed, "; ".join(typed) if typed else "none", tier="review")

    leaks = [f"{p}: {v[:60]}" for p, v in walk_strings(doc) if SCANNER_LEAK_RE.search(v)]
    record("no_scanner_leak", "No scanner output appears in the ontology",
           not leaks, "; ".join(leaks[:3]) if leaks else "clean")

    known = {i.get("id") for i in (concepts + events + axioms + workflows) if isinstance(i, dict)}
    dangling = []
    for r in relations:
        if not isinstance(r, dict):
            continue
        for end in ("subject", "object"):
            ref = r.get(end)
            if ref and ref not in known and not (r.get("description") or "").strip():
                dangling.append(f"{r.get('subject')} -{r.get('predicate')}-> {r.get('object')} ({end})")
    record("relations.resolvable",
           "Every relation end resolves to a declared id or is described as external",
           not dangling, "; ".join(dangling[:3]) if dangling else "all resolve")

    # A question with no suggested answer makes the human compose one from
    # scratch, which is the cost the protocol exists to avoid.
    no_default = [q.get("question", "")[:50] for q in questions
                  if isinstance(q, dict) and not (q.get("proposed_default") or "").strip()]
    record("questions.proposed_default",
           "These questions make the reviewer compose an answer from scratch. Worth a suggested default?",
           not no_default, "; ".join(no_default[:3]) if no_default else "all have one",
           tier="review")

    bad_sev = [q.get("severity") for q in questions
               if isinstance(q, dict) and q.get("severity") not in {"P0", "P1", "P2"}]
    record("questions.severity", "Every open question is graded P0/P1/P2",
           not bad_sev, f"bad: {bad_sev}" if bad_sev else "all graded")

    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("path")
    ap.add_argument("--json")
    args = ap.parse_args()

    try:
        doc = yaml.safe_load(Path(args.path).read_text("utf8"))
    except Exception as exc:
        print(f"could not parse: {exc}")
        sys.exit(1)
    if not isinstance(doc, dict):
        print("top level is not a mapping")
        sys.exit(1)

    results = check(doc)
    errors = [r for r in results if r["tier"] == "error"]
    review = [r for r in results if r["tier"] == "review" and not r["passed"]]

    for r in errors:
        print(f"{'PASS' if r['passed'] else 'FAIL'}  {r['id']:<38} {r['evidence'][:66]}")
    if review:
        print("\nfor a human to judge:")
        for r in review:
            print(f"  ? {r['text']}\n    {r['evidence'][:80]}")

    if args.json:
        Path(args.json).write_text(json.dumps(results, indent=2, ensure_ascii=False))
    sys.exit(0 if all(r["passed"] for r in errors) else 1)


if __name__ == "__main__":
    main()
