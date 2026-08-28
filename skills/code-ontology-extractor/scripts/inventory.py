# /// script
# requires-python = ">=3.11"
# dependencies = [
#   "tree-sitter>=0.25",
#   "tree-sitter-language-pack>=0.9",
# ]
# ///
"""
Pass A inventory scanner.

Extracts declared symbols from a source tree and computes cross-layer survival
for each identifier. Output is a ranking signal for Pass B, not a verdict.

Usage:
    uv run inventory.py <path> [--json out.json]

Dependencies are declared inline (PEP 723); uv resolves them automatically.
No virtualenv setup, no requirements.txt.
"""

import argparse
import json
import math
import re
import sys
from collections import defaultdict
from pathlib import Path

from tree_sitter import Query, QueryCursor
from tree_sitter_language_pack import get_language, get_parser

# Extension -> tree-sitter language name.
LANGS = {
    ".go": "go", ".py": "python", ".ts": "typescript", ".tsx": "tsx",
    ".js": "javascript", ".java": "java", ".rb": "ruby", ".rs": "rust",
    ".kt": "kotlin", ".cs": "c_sharp", ".php": "php", ".scala": "scala",
}

# Files parsed as plain text: no grammar needed, still carries domain vocabulary.
TEXT_EXT = {".yaml", ".yml", ".toml", ".json", ".env", ".ini", ".sql", ".proto", ".md"}

# Declaration nodes worth capturing, per language. Unlisted languages fall back
# to a generic identifier sweep.
QUERIES = {
    "go": """
        (type_spec name: (type_identifier) @symbol)
        (function_declaration name: (identifier) @symbol)
        (method_declaration name: (field_identifier) @symbol)
        (field_declaration name: (field_identifier) @symbol)
        (const_spec name: (identifier) @symbol)
    """,
    "python": """
        (class_definition name: (identifier) @symbol)
        (function_definition name: (identifier) @symbol)
        (assignment left: (identifier) @symbol)
    """,
    "typescript": """
        (class_declaration name: (type_identifier) @symbol)
        (interface_declaration name: (type_identifier) @symbol)
        (type_alias_declaration name: (type_identifier) @symbol)
        (function_declaration name: (identifier) @symbol)
        (property_signature name: (property_identifier) @symbol)
        (enum_declaration name: (identifier) @symbol)
    """,
    "java": """
        (class_declaration name: (identifier) @symbol)
        (interface_declaration name: (identifier) @symbol)
        (method_declaration name: (identifier) @symbol)
        (field_declaration declarator: (variable_declarator name: (identifier) @symbol))
        (enum_declaration name: (identifier) @symbol)
    """,
    "rust": """
        (struct_item name: (type_identifier) @symbol)
        (enum_item name: (type_identifier) @symbol)
        (function_item name: (identifier) @symbol)
        (field_declaration name: (field_identifier) @symbol)
    """,
}
QUERIES["tsx"] = QUERIES["typescript"]
QUERIES["javascript"] = """
    (class_declaration name: (identifier) @symbol)
    (function_declaration name: (identifier) @symbol)
    (variable_declarator name: (identifier) @symbol)
"""

# Infrastructure vocabulary. These are DOWNWEIGHTED, never dropped: in some
# domains they are the core concept (an ad server's "request" is a domain
# entity, not plumbing). Pass B may override per system.
STOPWORDS = {
    "context", "ctx", "request", "req", "response", "resp", "payload", "data",
    "dto", "logger", "log", "util", "utils", "helper", "handler", "client",
    "server", "config", "cfg", "options", "opts", "params", "args", "err",
    "error", "result", "value", "item", "list", "map", "set", "key", "id",
    "name", "type", "kind", "status", "state", "info", "meta", "wrapper",
    "manager", "service", "factory", "builder", "base", "common", "core",
    "test", "mock", "stub", "fake", "temp", "tmp", "buf", "buffer",
    # SQL / config keywords leaking in from the text scan
    "create", "table", "select", "insert", "update", "delete", "from",
    "where", "primary", "foreign", "index", "unique", "null", "not",
    "text", "int", "bigint", "varchar", "float", "double", "boolean",
    "timestamp", "default", "constraint", "references", "true", "false",
}

# Documentation formats. Scanned for vocabulary, but see classify_layer:
# docs are deliberately not a layer.
DOC_EXT = {".md"}

STRUCTURED_EXT = {".yaml", ".yml", ".toml", ".json", ".env", ".ini"}

LAYER_PATTERNS = [
    ("test",    re.compile(r"(^|[/_.])(test|tests|spec|specs|__tests__)([/_.]|$)", re.I)),
    ("config",  re.compile(r"(^|[/_.])(config|configs|conf|deploy|helm|k8s|infra)([/_.]|$)", re.I)),
    ("storage", re.compile(r"(^|[/_.])(repo|repository|store|storage|dao|model|models|entity|entities|db|database|persistence|migration|migrations|schema)([/_.]|$)", re.I)),
    ("api",     re.compile(r"(^|[/_.])(api|apis|handler|handlers|route|routes|controller|controllers|endpoint|endpoints|rpc|grpc|http|web|transport|delivery)([/_.]|$)", re.I)),
    ("domain",  re.compile(r"(^|[/_.])(domain|core|business|service|services|svc|usecase|usecases|logic)([/_.]|$)", re.I)),
]

# Leading segments that say where code lives, not what it does. `internal` is
# a Go visibility rule and `src` is a build convention; neither describes a
# layer. Left in the path they swallow everything beneath them, and since
# `internal` used to sit in the domain group that meant every package in a Go
# repo arrived labelled domain -- including the plumbing the reader is trying
# to filter out.
CONVENTION_PREFIXES = {"internal", "pkg", "src", "lib", "app", "cmd"}

SPLIT_RE = re.compile(r"[_\-\s]+|(?<=[a-z0-9])(?=[A-Z])|(?<=[A-Z])(?=[A-Z][a-z])")
IDENT_RE = re.compile(r"[A-Za-z_][A-Za-z0-9_]{2,}")

# What a name looks like inside prose: something a programmer typed rather
# than wrote. Backticks, underscores and internal capitals all mark a token as
# belonging to the code rather than the sentence around it.
IDENT_SHAPE_RE = re.compile(
    r"`[^`\n]+`"                                  # `backticked`
    r"|\b[a-z][a-z0-9]*(?:_[a-z0-9]+)+\b"          # snake_case
    r"|\b[A-Z][A-Z0-9]*(?:_[A-Z0-9]+)+\b"          # UPPER_SNAKE
    r"|\b[a-z]+(?:[A-Z][a-z0-9]*)+\b"              # camelCase
    r"|\b[A-Z][a-z0-9]+(?:[A-Z][a-z0-9]*)+\b"      # PascalCase
)

# A key in yaml/toml/json/env/ini, allowing for a list dash and quoting.
KEY_RE = re.compile(r'^\s*-?\s*"?([A-Za-z_][\w.\-]*)"?\s*[:=]')

SKIP_DIRS = {".git", "node_modules", "vendor", "dist", "build", "target",
             ".venv", "venv", "__pycache__", ".idea", ".vscode", "third_party"}


def stem_word(w: str) -> str:
    """Lightweight English stemming/singularization to unify singular/plural forms
    (e.g., orders/order, conversions/conversion, categories/category)."""
    w = w.lower()
    if len(w) <= 3 or w.endswith(("ss", "us", "is", "os")):
        return w
    if w.endswith("ies") and len(w) > 4:
        return w[:-3] + "y"
    if w.endswith(("ches", "shes", "xes", "zes")) and len(w) > 4:
        return w[:-2]
    if w.endswith("sses") and len(w) > 5:
        return w[:-2]
    if w.endswith("s") and not w.endswith(("ss", "us", "is", "os")):
        return w[:-1]
    if w.endswith("ing") and len(w) > 5:
        base = w[:-3]
        if base.endswith(("tt", "pp", "nn", "mm", "gg", "rr")):
            return base[:-1]
        return base
    if w.endswith("ed") and len(w) > 4:
        base = w[:-2]
        if base.endswith(("tt", "pp", "nn", "mm", "gg", "rr")):
            return base[:-1]
        return base
    return w


def normalize(ident: str) -> str:
    """Collapse case variants and singularize tokens so adServingId / ad_serving_ids / AD_SERVING_ID unify."""
    return "".join(stem_word(t) for t in SPLIT_RE.split(ident) if t)


def tokens(ident: str) -> list[str]:
    return [stem_word(t) for t in SPLIT_RE.split(ident) if t]


def classify_layer(path: Path, root: Path) -> str:
    parts = path.relative_to(root).parts
    while len(parts) > 1 and parts[0].lower() in CONVENTION_PREFIXES:
        parts = parts[1:]
    rel = "/".join(parts)
    if path.suffix.lower() in DOC_EXT:
        return "docs"
    if path.suffix in {".sql"} or "migration" in rel.lower():
        return "storage"
    if path.suffix in {".yaml", ".yml", ".toml", ".env", ".ini"}:
        return "config"
    for layer, pat in LAYER_PATTERNS:
        if pat.search(rel):
            return layer
    return "logic"


def scan_code(path: Path, lang_name: str) -> list[tuple[str, int]]:
    """Return (symbol, line) for declarations. Comments and strings are excluded
    by construction: only declaration nodes are matched."""
    try:
        src = path.read_bytes()
        lang = get_language(lang_name)
        tree = get_parser(lang_name).parse(src)
    except Exception:
        return []

    q = QUERIES.get(lang_name)
    out = []
    if q:
        try:
            caps = QueryCursor(Query(lang, q)).captures(tree.root_node)
            for node in caps.get("symbol", []):
                out.append((node.text.decode("utf8", "replace"), node.start_point[0] + 1))
            return out
        except Exception:
            pass

    # Generic fallback: walk identifier nodes, skipping comments and strings.
    def walk(node):
        if node.type in ("comment", "string", "string_literal", "raw_string_literal"):
            return
        if node.type in ("identifier", "type_identifier", "field_identifier"):
            out.append((node.text.decode("utf8", "replace"), node.start_point[0] + 1))
        for c in node.children:
            walk(c)

    walk(tree.root_node)
    return out


def scan_text(path: Path) -> list[tuple[str, int]]:
    """No grammar available, so extraction is format-aware instead.

    A flat identifier sweep works on SQL and proto, where every token is a
    name, and fails badly everywhere else: run it over a README and the top
    of the ranking fills with "The", "This" and "are", because English
    function words are frequent and appear in more than one file. The three
    branches below each ask what a name looks like in that format.

    Marked as text evidence so Pass B knows the precision is lower than a
    parsed declaration.
    """
    ext = path.suffix.lower()
    try:
        lines = path.read_text("utf8", "replace").splitlines()
    except Exception:
        return []

    out = []
    for i, line in enumerate(lines, 1):
        if line.lstrip().startswith(("#", "//", "--")):
            continue
        if ext in DOC_EXT:
            # Prose. Only identifier-shaped tokens are vocabulary; an ordinary
            # English word in a sentence is not, however often it recurs.
            for m in IDENT_SHAPE_RE.finditer(line):
                out.append((m.group().strip("`"), i))
        elif ext in STRUCTURED_EXT:
            # Keys name things; values are frequently a prose description.
            m = KEY_RE.match(line)
            if m:
                out.append((m.group(1), i))
        else:
            # SQL, proto: token-dense and name-dense, sweep everything.
            for m in IDENT_RE.finditer(line):
                out.append((m.group(), i))
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("path")
    ap.add_argument("--json", help="write full result here")
    ap.add_argument("--top", type=int, default=60, help="rows to print")
    ap.add_argument("--min-layers", type=int, default=1)
    args = ap.parse_args()

    root = Path(args.path).resolve()
    if not root.exists():
        sys.exit(f"path not found: {root}")

    # norm -> aggregated record
    agg: dict[str, dict] = defaultdict(
        lambda: {"surfaces": set(), "layers": set(), "count": 0,
                 "evidence": defaultdict(int), "sample": []}
    )
    files_by_lang = defaultdict(int)

    files = [p for p in root.rglob("*")
             if p.is_file() and not any(d in SKIP_DIRS for d in p.parts)]

    for path in files:
        ext = path.suffix.lower()
        lang = LANGS.get(ext)
        if lang:
            hits, evidence = scan_code(path, lang), "tree-sitter"
            files_by_lang[lang] += 1
        elif ext in TEXT_EXT:
            hits, evidence = scan_text(path), "text-scan"
            files_by_lang[ext] += 1
        else:
            continue

        layer = classify_layer(path, root)
        rel = str(path.relative_to(root))
        for ident, line in hits:
            if len(ident) < 3:
                continue
            rec = agg[normalize(ident)]
            rec["surfaces"].add(ident)
            rec["layers"].add(layer)
            rec["count"] += 1
            rec["evidence"][evidence] += 1
            if len(rec["sample"]) < 3:
                rec["sample"].append(f"{rel}:{line}")

    rows = []
    for norm, rec in agg.items():
        layers = rec["layers"] - {"test", "docs"}
        if not layers:
            continue
        toks = tokens(sorted(rec["surfaces"])[0])
        stop = bool(toks) and all(t in STOPWORDS for t in toks)
        # Cross-layer spread dominates raw frequency: a name appearing in api,
        # storage and config is far more likely a domain concept than one
        # appearing 400 times inside a single file.
        score = len(layers) * math.log1p(rec["count"])
        if stop:
            score *= 0.35  # downweighted, never excluded
        rows.append({
            "normalized": norm,
            "surfaces": sorted(rec["surfaces"]),
            "layers": sorted(layers),
            "layer_count": len(layers),
            "occurrences": rec["count"],
            "evidence": dict(rec["evidence"]),
            "stopword_downweighted": stop,
            "rank_score": round(score, 3),
            "sample_locations": rec["sample"],
        })

    rows.sort(key=lambda r: -r["rank_score"])
    rows = [r for r in rows if r["layer_count"] >= args.min_layers]

    result = {
        "root": str(root),
        "files_scanned": sum(files_by_lang.values()),
        "by_language": dict(files_by_lang),
        "candidates": rows,
        "note": ("rank_score orders what to inspect first. It is not evidence "
                 "of domain meaning. Stopword-flagged rows are downweighted, "
                 "not excluded — confirm against the system's own vocabulary."),
    }

    if args.json:
        Path(args.json).write_text(json.dumps(result, indent=2))
        print(f"wrote {args.json}")

    print(f"\nscanned {result['files_scanned']} files  {dict(files_by_lang)}\n")
    print(f"{'identifier':<28}{'layers':<8}{'occ':<6}{'score':<8}{'flag'}")
    print("-" * 62)
    for r in rows[: args.top]:
        flag = "downweighted" if r["stopword_downweighted"] else ""
        print(f"{r['surfaces'][0][:27]:<28}{r['layer_count']:<8}"
              f"{r['occurrences']:<6}{r['rank_score']:<8}{flag}")


if __name__ == "__main__":
    main()
