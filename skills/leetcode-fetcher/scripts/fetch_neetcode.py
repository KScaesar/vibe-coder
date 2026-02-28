#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "httpx",
#     "beautifulsoup4",
#     "markdownify",
# ]
# ///
"""
fetch_neetcode.py — 通用網頁題目抓取腳本 (支援 NeetCode)

Usage:
    uv run fetch_neetcode.py <url>
"""

import sys
import re
import httpx
from bs4 import BeautifulSoup
from markdownify import markdownify as md


def fetch_and_parse(url: str) -> str:
    try:
        # 加上 User-Agent 避免基本的阻擋
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        }
        # 使用 httpx 抓取網頁內容 (有時單純抓 HTML 就有足夠資訊)
        with httpx.Client(follow_redirects=True, headers=headers) as client:
            response = client.get(url, timeout=15)
            response.raise_for_status()
            html_content = response.text

        soup = BeautifulSoup(html_content, "html.parser")

        # 移除非內容區塊 (nav, header, footer, script, style)
        for tag in soup(
            [
                "nav",
                "header",
                "footer",
                "script",
                "style",
                "noscript",
                "iframe",
                "svg",
                "button",
            ]
        ):
            tag.decompose()

        # 嘗試尋找主要內容區塊 (heuristic: main tag or body)
        main_content = soup.find("main") or soup.body or soup

        # 將 HTML 轉成 Markdown
        markdown_text = md(str(main_content), heading_style="ATX")
        # 清理多餘空行
        markdown_text = re.sub(r"\n{3,}", "\n\n", markdown_text)
        return markdown_text.strip()

    except Exception as e:
        print(f"❌ NeetCode 網頁抓取失敗: {e}", file=sys.stderr)
        print(
            "請 AI Agent 改用 `webfetch` (format: markdown) 或 `playwright` 技能處理此 SPA 網頁。",
            file=sys.stderr,
        )
        sys.exit(1)




def main():
    if len(sys.argv) < 2:
        print("Usage: uv run fetch_neetcode.py <url>", file=sys.stderr)
        sys.exit(1)

    url = sys.argv[1]
    print(f"🌐 Fetching NeetCode URL: {url} ...", file=sys.stderr)

    markdown_desc = fetch_and_parse(url)

    # 組裝成與 fetch_leetcode.py 一致的輸出格式
    lines = []
    lines.append("=== LEETCODE_FILE_CONTENT_START ===")
    lines.append('"""')
    lines.append(f"# [Generic Problem]({url})")
    lines.append(f"**Source:** {url.split('/')[2] if '//' in url else 'Unknown'}")
    lines.append("\n## Problem Description\n")
    if not markdown_desc or len(markdown_desc) < 50:
        lines.append("> ⚠️ **注意**: 網頁內容可能需要 JavaScript 動態渲染 (SPA)。")
        lines.append(
            "> 此腳本抓取到的內容過少，請 AI Agent 直接改用 `webfetch` 或 `playwright` 重新讀取。"
        )
        lines.append(markdown_desc)
    else:
        lines.append(markdown_desc)
    lines.append('"""\n')
    lines.append("from typing import List, Optional, Dict, Tuple\n")

    # Attempt to infer a camelCase method name from the URL slug
    # NeetCode URLs: /problems/<slug>/question?... -> we need <slug>, not "question"
    # e.g. "kth-largest-element-in-an-array" -> "kthLargestElementInAnArray"
    try:
        path = url.rstrip("/").split("?")[0]   # strip query string
        segments = [s for s in path.split("/") if s]  # non-empty path parts
        # Find "problems" and grab the segment right after it
        if "problems" in segments:
            slug = segments[segments.index("problems") + 1]
        else:
            slug = segments[-1]
        parts = slug.split("-")
        method_name = parts[0] + "".join(w.capitalize() for w in parts[1:])
    except Exception:
        method_name = "solve"

    lines.append("class Solution:")
    lines.append(f"    # TODO: Replace parameters with the actual signature for `{method_name}`")
    lines.append(f"    def {method_name}(self):")
    lines.append("        pass\n")

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
#        # assert solution.solve(...) == ...
#
#        print("All tests passed!")
#
#    if __name__ == "__main__":
#        main()
""".strip()
    )
    lines.append("=== LEETCODE_FILE_CONTENT_END ===")

    print("\n".join(lines))


if __name__ == "__main__":
    main()
