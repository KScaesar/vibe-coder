"""Tagging precision tests for harvest_comments.

The harvester's value is entirely in its precision. SKILL.md tells the reader
to open the `conflict` bucket before anything else and to feed it straight
into vocabulary[].conflict_notes, so a false positive there is not noise the
reader filters out later -- it lands in the ontology. These tests exist to
keep that bucket honest, and to pin the length heuristic that decides what
counts as a rationale.
"""

import pytest
from tree_sitter_language_pack import get_parser

from harvest_comments import classify, clean, collect_nodes, merge_adjacent


def tag(source: str, lang: str = "go",
        min_doc_lines: int = 5, min_doc_chars: int = 100) -> list[list[str]]:
    """Run one source string through the same path main() uses per file.

    The keyword names mirror the CLI flags rather than classify()'s shorter
    parameter names, so a failing test reads like the command that reproduces it.
    """
    tree = get_parser(lang).parse(source.encode())
    comments, decls, hot_lines = collect_nodes(tree.root_node)
    return [
        classify(block, clean(block.text), decls, hot_lines,
                 min_doc_lines, min_doc_chars)
        for block in merge_adjacent(comments)
    ]


def tags_of(source: str, lang: str = "go", **kw) -> set[str]:
    """Union of every tag in a snippet, for single-comment cases."""
    return {t for kinds in tag(source, lang, **kw) for t in kinds}


# ---------------------------------------------------------------------------
# conflict -- the bucket SKILL.md says to read first
# ---------------------------------------------------------------------------

# Two names put in opposition. This is what the bucket is for.
CONFLICT_TRUE = [
    "// click_id is not the same as transaction_id.\nvar x = 1\n",
    "// Don't confuse orderNo with orderId; the vendor sends orderNo.\nvar x = 1\n",
    "// 這裡的 order_no 不要跟 order_id 混用，對帳以 order_no 為準。\nvar x = 1\n",
    "// 舊名 tx_id，現在統一用 transaction_id。\nvar x = 1\n",
    "// formerly called adSlotId, renamed to placementId in v2.\nvar x = 1\n",
]

# Ordinary prose that happens to contain a contrastive connective. None of
# these say anything about two names being different, and every one of them
# was tagged `conflict` before the two-tier rule landed.
CONFLICT_FALSE = [
    "// Signals that a comment is explaining a decision rather than restating code.\nvar x = 1\n",
    "// Heuristic for commented-out code rather than prose.\nvar x = 1\n",
    "// Error dropped rather than propagated.\nvar x = 1\n",
    "// 改名會讓所有引用斷掉，設定後盡量不動。\nvar x = 1\n",
    "// Prefer a channel here instead of a mutex.\nvar x = 1\n",
    "// Unlike the previous implementation, this one is lock free.\nvar x = 1\n",
]


@pytest.mark.parametrize("src", CONFLICT_TRUE)
def test_conflict_is_tagged_when_two_names_are_put_in_opposition(src):
    assert "conflict" in tags_of(src)


@pytest.mark.parametrize("src", CONFLICT_FALSE)
def test_contrastive_prose_alone_is_not_a_naming_conflict(src):
    assert "conflict" not in tags_of(src), (
        "a contrastive connective with no pair of names behind it is ordinary "
        "prose; tagging it pollutes vocabulary[].conflict_notes"
    )


def test_weak_marker_plus_a_pair_of_names_still_counts():
    # `等同於` is weak on its own, but here it is asked about two real names,
    # which is exactly the conflict Pass B is looking for.
    src = "// click_id 是否等同於 transaction_id?\nvar x = 1\n"
    assert "conflict" in tags_of(src)


def test_a_single_name_is_not_enough_for_a_weak_marker():
    src = "// 改名會讓所有引用斷掉，預期值 snake_case。\nvar x = 1\n"
    assert "conflict" not in tags_of(src)


def test_names_elsewhere_in_the_block_do_not_corroborate_a_weak_marker():
    # Verbatim from references/ontology-schema.yml, which survived the
    # two-tier rule because `axioms` and `snake_case` sit in
    # neighbouring sentences. Neither is being contrasted with anything.
    src = (
        "// 穩定識別碼，供 relations / axioms 引用。\n"
        "// 改名會讓所有引用斷掉，設定後盡量不動。預期值: snake_case\n"
        "var x = 1\n"
    )
    assert "conflict" not in tags_of(src)


def test_a_generic_cross_reference_tag_is_not_a_conflict_on_its_own():
    # @see appears on most documented symbols; @deprecated names a
    # replacement and does assert a naming relationship.
    assert "conflict" not in tags_of("// @see the settlement package.\ntype T struct{}\n")
    assert "conflict" in tags_of("// @deprecated use placementId.\ntype T struct{}\n")


# ---------------------------------------------------------------------------
# rationale -- the length heuristic
# ---------------------------------------------------------------------------

# Two dense lines carrying no RATIONALE_RE keyword and sitting beside no
# numeric literal, so the only thing that can tag it is the length rule. Keeping
# it keyword-free is the whole point: an earlier draft used "vendor" and
# "invoice" here and passed through the keyword path without ever exercising
# the rescue it claimed to test.
NEUTRAL_DENSE_DOC = (
    "// The identifier is assembled from the site code and a running counter,\n"
    "// so it looks numeric while behaving as an opaque string everywhere.\n"
    "type Cycle struct{}\n"
)


def test_long_doc_block_is_rationale_without_any_keyword():
    # The premise of the length rule: nobody writes six lines above a
    # declaration to restate the declaration.
    src = (
        "// A placement is one slot on one page where a creative may appear.\n"
        "// It is negotiated per publisher and does not change once signed.\n"
        "// Sales owns the mapping; engineering only reads it.\n"
        "// Historically placements were per-site, which is why the id is\n"
        "// prefixed with the site code even for network-wide placements.\n"
        "// The prefix carries no meaning beyond that.\n"
        "type Placement struct{}\n"
    )
    assert "rationale" in tags_of(src)


def test_padded_lines_do_not_clear_the_floor():
    # Six lines that say nothing. The character floor exists for this.
    src = "// a\n// b\n// c\n// d\n// e\n// f\n// g\ntype T struct{}\n"
    assert "rationale" not in tags_of(src)


def test_dense_short_block_is_rescued_by_the_character_threshold():
    src = NEUTRAL_DENSE_DOC
    assert "rationale" in tags_of(src, min_doc_chars=100)


def test_rescue_can_be_disabled_for_mixed_language_repos():
    # SKILL.md documents --min-doc-chars 99999 as the way to let the
    # language-neutral line count decide alone.
    src = NEUTRAL_DENSE_DOC
    assert "rationale" not in tags_of(src, min_doc_lines=5, min_doc_chars=99999)


def test_comment_beside_a_numeric_literal_is_rationale():
    src = "func f() {\n\t// Vendor contract caps us at seven days.\n\tcoolOff := 7\n}\n"
    assert "rationale" in tags_of(src)


# ---------------------------------------------------------------------------
# noise buckets
# ---------------------------------------------------------------------------

def test_licence_header_is_boilerplate():
    assert tags_of("// Copyright 2024 Acme Inc. All rights reserved.\nvar x = 1\n") == {"boilerplate"}


def test_generated_file_marker_is_boilerplate():
    assert tags_of("// Code generated by protoc-gen-go. DO NOT EDIT.\nvar x = 1\n") == {"boilerplate"}


def test_commented_out_code_is_not_prose():
    src = "// if err != nil {\n// \treturn nil, err\n// }\nvar x = 1\n"
    assert tags_of(src) == {"commented_code"}


def test_attention_markers_are_flagged():
    assert "flag" in tags_of("// TODO: confirm the cap with finance.\nvar x = 1\n")
    assert "flag" in tags_of("// 待確認：這個上限是誰定的。\nvar x = 1\n")


# ---------------------------------------------------------------------------
# block merging -- a multi-line explanation is one artifact
# ---------------------------------------------------------------------------

def test_consecutive_line_comments_merge_into_one_block():
    src = "// first line\n// second line\n// third line\nvar x = 1\n"
    assert len(tag(src)) == 1


def test_a_blank_line_separates_two_blocks():
    src = "// first block\n\n\n// second block\nvar x = 1\n"
    assert len(tag(src)) == 2
