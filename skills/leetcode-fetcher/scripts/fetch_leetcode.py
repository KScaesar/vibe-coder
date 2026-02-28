#!/usr/bin/env python3
"""
fetch_problem.py — 從 LeetCode URL 或 slug 抓取題目詳細資訊（不需要登入）

Usage:
    uv run fetch_problem.py <leetcode-url-or-slug>
"""

import html as html_module
import json
import re
import sys
import urllib.error
import urllib.request

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
    codeSnippets {
      lang
      langSlug
      code
    }
    exampleTestcaseList
  }
}
"""


def extract_slug(url_or_slug: str) -> str:
    match = re.search(r"leetcode\.com/problems/([^/?#]+)", url_or_slug)
    if match:
        return match.group(1)

    contest_match = re.search(
        r"leetcode\.com/contest/[^/]+/problems/([^/?#]+)", url_or_slug
    )
    if contest_match:
        return contest_match.group(1)

    return url_or_slug.strip("/")


def html_to_text(html_content: str) -> str:
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
    return re.sub(r"\n{3,}", "\n\n", text).strip()


def fetch_problem(slug: str) -> dict:
    payload = json.dumps(
        {
            "query": QUERY,
            "variables": {"titleSlug": slug},
            "operationName": "questionData",
        }
    ).encode("utf-8")

    req = urllib.request.Request(GRAPHQL_URL, data=payload, method="POST")
    req.add_header("Content-Type", "application/json")
    req.add_header("User-Agent", "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36")
    req.add_header("Referer", f"https://leetcode.com/problems/{slug}/")
    req.add_header("Origin", "https://leetcode.com")
    req.add_header("x-csrftoken", "dummy")

    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            data = json.loads(resp.read().decode("utf-8"))
    except Exception as e:
        print(f"❌ Error: {e}", file=sys.stderr)
        sys.exit(1)

    question = data.get("data", {}).get("question")
    if not question:
        print(f"❌ 找不到題目：{slug}", file=sys.stderr)
        sys.exit(1)

    return question


def parse_contest_info(url: str):
    weekly_match = re.search(
        r"leetcode\.com/contest/weekly-contest-(\d+)/problems/([^/?#]+)", url
    )
    if weekly_match:
        return {
            "type": "weekly",
            "num": weekly_match.group(1),
            "slug": weekly_match.group(2),
        }

    biweekly_match = re.search(
        r"leetcode\.com/contest/biweekly-contest-(\d+)/problems/([^/?#]+)", url
    )
    if biweekly_match:
        return {
            "type": "biweekly",
            "num": biweekly_match.group(1),
            "slug": biweekly_match.group(2),
        }

    return None


def format_output(q: dict) -> str:
    """將題目資料格式化為 Markdown 註解字串。"""
    lines = []
    qid = q.get("questionId", "?")
    title = q.get("title", "Unknown")
    difficulty = q.get("difficulty", "Unknown")
    slug = q.get("titleSlug", "")
    url = f"https://leetcode.com/problems/{slug}/"
    difficulty_emoji = {"Easy": "🟢", "Medium": "🟡", "Hard": "🔴"}.get(
        difficulty, "⚪"
    )

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


def extract_method_name(code_snippet: str) -> str:
    if not code_snippet:
        return "method_name"
    match = re.search(r"def\s+([a-zA-Z0-9_]+)\s*\(self,", code_snippet)
    if match:
        return match.group(1)
    return "method_name"



def generate_python_content(q: dict, contest_info: dict = None) -> str:
    """
    僅產生基礎結構。
    將 `main()` 的 Test Cases 實作交由 LLM 去閱讀問題描述後補完，
    而不是寫死的 `EXPECTED_RESULT`。
    """
    markdown_desc = format_output(q)

    code_snippets = q.get("codeSnippets") or []
    python_snippet = next(
        (s["code"] for s in code_snippets if s["langSlug"] == "python3"), None
    )

    lines = []
    lines.append('"""')
    lines.append(markdown_desc.strip())
    lines.append('"""\n')
    lines.append("from typing import List, Optional, Dict, Tuple\n")

    if python_snippet:
        lines.append(python_snippet.rstrip() + "\n        pass\n")
    else:
        lines.append("# TODO: Provide function signature here\n")

    lines.append(
        "\n"
        + r"""
# --- LLM INSTRUCTION: ---
# 1. 建立對應的類別資料夾（若不存在）。
# 2. 建立此 Python 檔案。
# 3. 讀取上方 `Problem Description` 中提供的 Example，
#    在檔案最底下加入完整的 `def main():` 區塊，並把測試範例轉成 `assert`。
#    因為本來就還沒實作，測試執行失敗是正常的，重點是幫使用者寫好測試案例。
#    測試區塊參考格式：
#
#    def main():
#        solution = Solution()
#
#        # Test cases
#        # Case 1
#        # assert solution.searchRange([5,7,7,8,8,10], 8) == [3,4]
#
#        # Case 2
#        # ...
#
#        print("All tests passed!")
#
#    if __name__ == "__main__":
#        main()
""".strip()
    )

    return "\n".join(lines)


def main():
    if len(sys.argv) < 2:
        print("Usage: uv run fetch_problem.py <leetcode-url-or-slug>", file=sys.stderr)
        sys.exit(1)

    input_arg = sys.argv[1]
    slug = extract_slug(input_arg)
    print(f"🔍 Fetching: {slug} ...", file=sys.stderr)

    question = fetch_problem(slug)
    contest_info = parse_contest_info(input_arg)

    file_content = generate_python_content(question, contest_info)

    print("=== LEETCODE_FILE_CONTENT_START ===")
    print(file_content)
    print("=== LEETCODE_FILE_CONTENT_END ===")


if __name__ == "__main__":
    main()
