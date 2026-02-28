#!/usr/bin/env python3
"""
fetch_problem.py — 從 LeetCode URL 或 slug 抓取題目詳細資訊（不需要登入）

Usage:
    uv run fetch_problem.py <leetcode-url-or-slug>

Examples:
    uv run fetch_problem.py https://leetcode.com/problems/number-of-islands/
    uv run fetch_problem.py two-sum
"""

import sys
import re
import json
import urllib.request
import urllib.error
import html as html_module


GRAPHQL_URL = "https://leetcode.com/graphql"

QUERY = """
query questionData($titleSlug: String!) {
  question(titleSlug: $titleSlug) {
    questionId
    title
    titleSlug
    difficulty
    content
    topicTags {
      name
    }
    hints
    similarQuestions
  }
}
"""


def extract_slug(url_or_slug: str) -> str:
    """從 URL 或 slug 字串中取出 title slug。"""
    match = re.search(r"leetcode\.com/problems/([^/?#]+)", url_or_slug)
    if match:
        return match.group(1)
    return url_or_slug.strip("/")


def html_to_text(html_content: str) -> str:
    """將 HTML 內容轉換為可讀的 Markdown 格式純文字。"""
    if not html_content:
        return ""
    text = re.sub(r"<br\s*/?>", "\n", html_content, flags=re.IGNORECASE)
    text = re.sub(r"</p>", "\n\n", text, flags=re.IGNORECASE)
    text = re.sub(r"<li>", "- ", text, flags=re.IGNORECASE)
    text = re.sub(r"</li>", "\n", text, flags=re.IGNORECASE)
    text = re.sub(r"<pre>", "\n```\n", text, flags=re.IGNORECASE)
    text = re.sub(r"</pre>", "\n```\n", text, flags=re.IGNORECASE)
    text = re.sub(r"<strong>|</strong>|<b>|</b>", "**", text, flags=re.IGNORECASE)
    text = re.sub(r"<em>|</em>|<i>|</i>", "_", text, flags=re.IGNORECASE)
    text = re.sub(r"<code>", "`", text, flags=re.IGNORECASE)
    text = re.sub(r"</code>", "`", text, flags=re.IGNORECASE)
    text = re.sub(r"<sup>", "^", text, flags=re.IGNORECASE)
    text = re.sub(r"</sup>", "", text, flags=re.IGNORECASE)
    text = re.sub(r"<[^>]+>", "", text)
    text = html_module.unescape(text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def fetch_problem(slug: str) -> dict:
    """呼叫 LeetCode GraphQL API 取得題目資料。"""
    payload = json.dumps({
        "query": QUERY,
        "variables": {"titleSlug": slug},
        "operationName": "questionData",
    }).encode("utf-8")

    req = urllib.request.Request(GRAPHQL_URL, data=payload, method="POST")
    req.add_header("Content-Type", "application/json")
    req.add_header("User-Agent", "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36")
    req.add_header("Referer", f"https://leetcode.com/problems/{slug}/")
    req.add_header("Origin", "https://leetcode.com")
    req.add_header("x-csrftoken", "dummy")

    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            data = json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        print(f"❌ HTTP Error {e.code}: {e.reason}", file=sys.stderr)
        sys.exit(1)
    except urllib.error.URLError as e:
        print(f"❌ Network Error: {e.reason}", file=sys.stderr)
        sys.exit(1)

    question = data.get("data", {}).get("question")
    if not question:
        print(f"❌ 找不到題目：{slug}", file=sys.stderr)
        sys.exit(1)

    return question


def format_output(q: dict) -> str:
    """將題目資料格式化為 Markdown 字串。"""
    lines = []

    qid = q.get("questionId", "?")
    title = q.get("title", "Unknown")
    difficulty = q.get("difficulty", "Unknown")
    slug = q.get("titleSlug", "")
    url = f"https://leetcode.com/problems/{slug}/"

    difficulty_emoji = {"Easy": "🟢", "Medium": "🟡", "Hard": "🔴"}.get(difficulty, "⚪")

    lines.append(f"# [{qid}. {title}]({url})")
    lines.append(f"**Difficulty:** {difficulty_emoji} {difficulty}")

    tags = [t["name"] for t in q.get("topicTags", [])]
    if tags:
        lines.append(f"**Tags:** {', '.join(tags)}")

    lines.append("")

    content = html_to_text(q.get("content", ""))
    if content:
        lines.append("## Problem Description")
        lines.append("")
        lines.append(content)
        lines.append("")

    hints = q.get("hints", [])
    if hints:
        lines.append("## Hints")
        for i, hint in enumerate(hints, 1):
            lines.append(f"{i}. {html_to_text(hint)}")
        lines.append("")

    similar_raw = q.get("similarQuestions", "")
    if similar_raw:
        try:
            similar = json.loads(similar_raw)
            if similar:
                lines.append("## Similar Questions")
                for sq in similar:
                    lines.append(
                        f"- [{sq['title']}](https://leetcode.com/problems/{sq['titleSlug']}/) "
                        f"({sq['difficulty']})"
                    )
                lines.append("")
        except (json.JSONDecodeError, KeyError):
            pass

    return "\n".join(lines)


def main():
    if len(sys.argv) < 2:
        print("Usage: uv run fetch_problem.py <leetcode-url-or-slug>", file=sys.stderr)
        sys.exit(1)

    input_arg = sys.argv[1]
    slug = extract_slug(input_arg)
    print(f"🔍 Fetching: {slug} ...", file=sys.stderr)

    question = fetch_problem(slug)
    output = format_output(question)
    print(output)


if __name__ == "__main__":
    main()
