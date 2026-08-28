"""End-to-end detection tests against the planted fixture.

The unit tests elsewhere in this directory prove the classifiers draw their
boundaries where they are supposed to. They do not prove that a real tree,
laid out the way a Go service actually is, gives up the evidence an ontology
needs -- a rule can be individually correct and still never fire, because the
layout hides the file or the pattern assumes a shape nobody writes.

So: evals/fixtures/adserving is a small service with known evidence planted in
it, and evals/adserving.ground-truth.yml is the answer key, kept outside the
scanned tree so an eval agent cannot read it.

What these tests can and cannot settle is the point of the split. Whether the
30s timeout in middleware.go gets surfaced is a scanner question and is
answered here. Whether it then stays out of the ontology is a judgment
question, and no assertion here can reach it -- that plant's `judgment` field
is for an eval to grade.
"""

import json
import subprocess
import sys
from pathlib import Path

import pytest
import yaml

ROOT = Path(__file__).resolve().parent.parent
SCRIPTS = ROOT / "scripts"
EVALS = ROOT / "evals"
FIXTURE = EVALS / "fixtures" / "adserving"


def load_plants() -> list[dict]:
    return yaml.safe_load((EVALS / "adserving.ground-truth.yml").read_text())["plants"]


PLANTS = {p["id"]: p for p in load_plants()}


def scanner_plants(tool: str) -> list[str]:
    """Plant ids whose scanner-owned expectation names this tool."""
    return [
        pid for pid, p in PLANTS.items()
        if p.get("scanner", {}).get("tool") == tool
        or p.get("also_scanner", {}).get("tool") == tool
    ]


# ---------------------------------------------------------------------------
# scans, run once each
# ---------------------------------------------------------------------------

@pytest.fixture(scope="module")
def comments(tmp_path_factory) -> list[dict]:
    out = tmp_path_factory.mktemp("scan") / "comments.json"
    subprocess.run(
        [sys.executable, str(SCRIPTS / "harvest_comments.py"), str(FIXTURE), "--json", str(out)],
        check=True, capture_output=True,
    )
    return json.loads(out.read_text())["comments"]


@pytest.fixture(scope="module")
def candidates(tmp_path_factory) -> dict[str, dict]:
    out = tmp_path_factory.mktemp("scan") / "inventory.json"
    subprocess.run(
        [sys.executable, str(SCRIPTS / "inventory.py"), str(FIXTURE), "--json", str(out)],
        check=True, capture_output=True,
    )
    rows = json.loads(out.read_text())["candidates"]
    return {r["normalized"]: r for r in rows}


@pytest.fixture(scope="module")
def findings() -> list[dict]:
    proc = subprocess.run(
        ["ast-grep", "scan", "-c", str(SCRIPTS / "sgconfig.yml"), "--json", str(FIXTURE)],
        capture_output=True, text=True,
    )
    return json.loads(proc.stdout or "[]")


def in_file(items, plant_id, key="file"):
    """Findings or comments belonging to the plant's file."""
    want = PLANTS[plant_id]["file"]
    return [i for i in items if i[key].replace("\\", "/").endswith(want)]


# ---------------------------------------------------------------------------
# comment evidence
# ---------------------------------------------------------------------------

def test_p1_naming_conflict_is_surfaced(comments):
    hits = [c for c in in_file(comments, "P1") if "conflict" in c["kinds"]]
    assert hits, "the click_id / conversion_id note is the highest-value comment in the fixture"
    assert "conversion_id" in hits[0]["text"]


def test_p2_contract_rationale_is_surfaced(comments):
    hits = [c for c in in_file(comments, "P2") if "rationale" in c["kinds"]]
    assert any("合約" in c["text"] for c in hits)


def test_p7_stale_comment_is_surfaced(comments):
    # The value of this comment is that it disagrees with the constant below
    # it. It only becomes an open question if the reader sees it at all.
    text = PLANTS["P7"]["scanner"]["expect_text"]
    assert any(text in c["text"] for c in in_file(comments, "P7"))


def test_boilerplate_does_not_reach_the_reader(comments):
    assert not [c for c in comments if "boilerplate" in c["kinds"]]


# ---------------------------------------------------------------------------
# structural evidence
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("plant_id", ["P2", "P3", "P4", "P5"])
def test_planted_constants_are_surfaced(findings, plant_id):
    plant = PLANTS[plant_id]
    spec = plant.get("also_scanner") or plant["scanner"]
    hits = [f for f in in_file(findings, plant_id) if f["ruleId"] == spec["rule"]]
    assert spec["expect_literal"] in {f["text"] for f in hits}


@pytest.mark.parametrize("plant_id", ["P6", "P10"])
def test_silent_fallbacks_are_surfaced(findings, plant_id):
    hits = [f for f in in_file(findings, plant_id) if f["ruleId"] == "silent-fallback-go"]
    assert hits


def test_p11_settlement_lifecycle_is_surfaced(findings):
    hits = [f for f in in_file(findings, "P11") if f["ruleId"] == "state-transition-go"]
    # Both halves: the iota block declaring the state space, and the
    # assignment that moves an order through it.
    assert len(hits) >= 2


# ---------------------------------------------------------------------------
# vocabulary evidence
# ---------------------------------------------------------------------------

def test_p8_ad_request_survives_the_stopword_downweight(candidates):
    row = candidates.get("adrequest")
    assert row is not None, "AdRequest was dropped entirely"
    assert row["layer_count"] >= PLANTS["P8"]["scanner"]["expect_min_layers"], row["layers"]


@pytest.mark.parametrize("decoy", ["rediskeybuilder", "httpmiddleware"])
def test_p9_decoys_do_not_look_like_domain_concepts(candidates, decoy):
    row = candidates.get(decoy)
    if row is None:
        return  # dropped outright, which is a stronger version of the same result
    spec = PLANTS["P9"]["scanner"]
    assert row["layer_count"] <= spec["expect_max_layers"], row["layers"]
    # Surviving in one layer is not enough if that layer is the one the reader
    # is told to trust. Both decoys used to land in domain, because their path
    # begins with internal/.
    assert spec["expect_not_layer"] not in row["layers"], row["layers"]


def test_readme_prose_never_becomes_a_candidate(candidates):
    for word in ("the", "and", "which", "return"):
        assert word not in candidates
