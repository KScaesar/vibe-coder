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
fetch_generic.py — 通用網頁內容抓取腳本 (單純抓取，不組裝 Python)

Usage:
    uv run fetch_generic.py <url>
"""

import sys
import httpx
from bs4 import BeautifulSoup
from markdownify import markdownify as md


def main():
    if len(sys.argv) < 2:
        print("Usage: uv run fetch_generic.py <url>", file=sys.stderr)
        sys.exit(1)

    url = sys.argv[1]
    print(f"🌐 Fetching generic URL for raw data: {url} ...", file=sys.stderr)

    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        }
        with httpx.Client(follow_redirects=True, headers=headers) as client:
            response = client.get(url, timeout=15)
            response.raise_for_status()
            html_content = response.text

        soup = BeautifulSoup(html_content, "html.parser")

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
                "aside",
            ]
        ):
            tag.decompose()

        main_content = soup.find("main") or soup.find("article") or soup.body or soup

        markdown_text = md(str(main_content), heading_style="ATX").strip()

        print("=== GENERIC_FILE_CONTENT_START ===")
        if not markdown_text or len(markdown_text) < 50:
            print("> ⚠️ **注意**: 網頁內容可能需要 JavaScript 動態渲染 (SPA)。")
            print("> 請 AI Agent 直接改用 `webfetch` 或 `playwright` 重新讀取。")
        else:
            print(markdown_text)
        print("=== GENERIC_FILE_CONTENT_END ===")

    except Exception as e:
        print(f"❌ 通用網頁抓取失敗: {e}", file=sys.stderr)
        print(
            "請 AI Agent 改用 `webfetch` (format: markdown) 或 `playwright` 技能處理此網頁。",
            file=sys.stderr,
        )
        sys.exit(1)


if __name__ == "__main__":
    main()
