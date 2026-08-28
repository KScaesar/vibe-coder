"""Tests for the ontology validator.

A validator is only worth running if it fails on bad input and passes on good
input, and the second half is the one that quietly rots: a pattern that never
matches reports a clean bill of health forever. The `timestamptz?` in the
storage-type list did exactly that until a deliberately broken fixture was run
through it -- the `?` bound to the `z` alone, so the pattern demanded a
literal "timestampt" and no real column type ever matched.
"""

from pathlib import Path

import pytest
import yaml

from validate_ontology import check

DATA = Path(__file__).resolve().parent / "data"


def results_for(name: str) -> dict[str, dict]:
    doc = yaml.safe_load((DATA / name).read_text("utf8"))
    return {r["id"]: r for r in check(doc)}


def test_a_well_formed_ontology_raises_nothing():
    failed = [r["id"] for r in results_for("good.ontology.yml").values() if not r["passed"]]
    assert not failed, failed


@pytest.mark.parametrize("check_id", [
    "confidence.open_question",
    "relations.resolvable",
    "questions.severity",
])
def test_structural_defects_fail(check_id):
    result = results_for("bad.ontology.yml")[check_id]
    assert result["tier"] == "error"
    assert result["passed"] is False


@pytest.mark.parametrize("check_id", [
    "concepts.storage_flavoured_properties",
    "questions.proposed_default",
])
def test_judgment_calls_are_raised_for_review_not_failed(check_id):
    # There is no one right way to word an attribute/property, so a suspicious word is
    # a question for someone who knows the domain -- not a verdict the tool
    # gets to hand down.
    result = results_for("bad.ontology.yml")[check_id]
    assert result["tier"] == "review"


def test_a_low_confidence_claim_is_accepted_once_a_question_backs_it():
    # The rule is not "no low confidence"; it is "no low confidence that
    # nobody was asked about". conversion_event sits at 0.3 in the good
    # fixture and passes because an open question references it.
    assert results_for("good.ontology.yml")["confidence.open_question"]["passed"]
