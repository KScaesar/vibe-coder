"""Extraction tests for inventory.py.

Pass A's only job is to produce a reading order, and the signal it orders by
is cross-layer survival. Two things can wreck that signal quietly: sweeping
English prose into the identifier table, and counting a documentation file as
a layer. Both inflate exactly the rows a reader is told to inspect first, so
the tests below pin the boundary between an identifier and a word.
"""

import pytest

from inventory import classify_layer, normalize, scan_text, tokens


def extract(tmp_path, filename: str, content: str) -> set[str]:
    path = tmp_path / filename
    path.write_text(content, encoding="utf8")
    return {ident for ident, _line in scan_text(path)}


# ---------------------------------------------------------------------------
# markdown -- prose is not vocabulary
# ---------------------------------------------------------------------------

MARKDOWN = """\
# Ad Serving

The service decides which creative to return. That decision is made by the
ranker, and the result are cached for a short while.

Configure it with `frequency_cap` or by setting AdRequest.maxSlots, which
maps to the AD_TIMEOUT_MS environment variable.
"""


def test_english_prose_is_not_extracted_from_markdown(tmp_path):
    found = extract(tmp_path, "README.md", MARKDOWN)
    for word in ("The", "service", "decides", "That", "are", "while", "which"):
        assert word not in found, f"{word!r} is prose, not an identifier"


def test_identifier_shaped_tokens_survive_in_markdown(tmp_path):
    found = extract(tmp_path, "README.md", MARKDOWN)
    for name in ("frequency_cap", "AdRequest", "maxSlots", "AD_TIMEOUT_MS"):
        assert name in found


def test_documentation_is_not_a_layer(tmp_path):
    # Cross-layer survival is the ranking signal. A name mentioned in the
    # README and nowhere else has not survived anything; letting docs count
    # as a layer promotes it over names that genuinely span api and storage.
    assert classify_layer(tmp_path / "README.md", tmp_path) == "docs"
    assert classify_layer(tmp_path / "docs" / "architecture.md", tmp_path) == "docs"


# ---------------------------------------------------------------------------
# structured config -- keys are vocabulary, values are usually prose
# ---------------------------------------------------------------------------

YAML = """\
ad_serving:
  description: This is the primary service that handles every incoming call
  max_frequency_cap: 3
  timeout_ms: 2700
"""


def test_config_keys_are_extracted(tmp_path):
    found = extract(tmp_path, "config.yml", YAML)
    for key in ("ad_serving", "description", "max_frequency_cap", "timeout_ms"):
        assert key in found


def test_prose_inside_a_config_value_is_not_extracted(tmp_path):
    found = extract(tmp_path, "config.yml", YAML)
    for word in ("This", "the", "primary", "handles", "every", "incoming"):
        assert word not in found


def test_comment_lines_are_skipped(tmp_path):
    found = extract(tmp_path, "config.yml", "# retention_days is legacy\nkeep_days: 30\n")
    assert "keep_days" in found
    assert "retention_days" not in found


# ---------------------------------------------------------------------------
# sql / proto -- code-like, the plain sweep still applies
# ---------------------------------------------------------------------------

def test_sql_columns_are_extracted(tmp_path):
    found = extract(
        tmp_path,
        "schema.sql",
        "CREATE TABLE conversion_event (\n  click_id BIGINT,\n  settled_at TIMESTAMP\n);\n",
    )
    assert {"conversion_event", "click_id", "settled_at"} <= found


# ---------------------------------------------------------------------------
# normalisation -- case variants and plurals collapse
# ---------------------------------------------------------------------------

@pytest.mark.parametrize(
    "variants",
    [
        ("adServingId", "ad_serving_id", "AD_SERVING_ID", "AdServingId"),
        ("conversion", "conversions", "Conversions"),
        ("category", "categories"),
    ],
)
def test_case_and_plural_variants_collapse(variants):
    assert len({normalize(v) for v in variants}) == 1


def test_tokens_are_split_on_case_boundaries():
    assert tokens("adRequestId") == ["ad", "request", "id"]
    # -ing is stemmed away so adServing and adServe collapse together.
    assert tokens("adServingId") == ["ad", "serv", "id"]


# ---------------------------------------------------------------------------
# layers
# ---------------------------------------------------------------------------

@pytest.mark.parametrize(
    "rel,expected",
    [
        ("internal/api/handler.go", "api"),
        # `internal` is a Go visibility marker, not a layer. Treating it as one
        # files every package in the repo under domain, which is where the
        # reader is told to look for concepts -- so plumbing arrives wearing a
        # domain badge.
        ("internal/platform/redis_key.go", "logic"),
        ("internal/cache/lru.go", "logic"),
        ("pkg/transport/grpc.go", "api"),
        ("src/billing/invoice.go", "logic"),
        ("internal/domain/decision.go", "domain"),
        ("internal/repository/order.go", "storage"),
        ("migrations/001_init.sql", "storage"),
        ("deploy/values.yaml", "config"),
        ("internal/domain/decision_test.go", "test"),
    ],
)
def test_layer_classification(tmp_path, rel, expected):
    assert classify_layer(tmp_path / rel, tmp_path) == expected
