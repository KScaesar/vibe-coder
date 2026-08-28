# /// script
# requires-python = ">=3.11"
# dependencies = [
#   "pytest>=8",
#   "pyyaml>=6",
#   "tree-sitter>=0.25",
#   "tree-sitter-language-pack>=0.9",
# ]
# ///
"""Test runner for the skill's scanners.

The scripts are standalone PEP 723 files, so the tests are too: there is no
project to install and no virtualenv to keep in sync. Run with:

    uv run tests/run_tests.py [-- extra pytest args]
"""

import sys
from pathlib import Path

import pytest

HERE = Path(__file__).resolve().parent

if __name__ == "__main__":
    sys.exit(pytest.main([str(HERE), "-q", *sys.argv[1:]]))
