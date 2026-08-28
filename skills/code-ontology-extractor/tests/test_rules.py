"""Runs the ast-grep rule tests through the same entry point as everything else.

The rules have their own native test format (valid/invalid samples next to
each rule), which is better than anything reimplemented here. This wrapper
exists only so that one command covers all three scanners -- a rule that
silently matches nothing is the easiest defect in this skill to ship, and it
only stays caught if running the tests is a single habit.
"""

import shutil
import subprocess
from pathlib import Path

import pytest

SCRIPTS = Path(__file__).resolve().parent.parent / "scripts"


@pytest.mark.skipif(shutil.which("ast-grep") is None,
                    reason="ast-grep not installed; see Setup in SKILL.md")
def test_ast_grep_rules_match_what_they_claim_to():
    proc = subprocess.run(
        ["ast-grep", "test", "--skip-snapshot-tests"],
        cwd=SCRIPTS, capture_output=True, text=True,
    )
    assert proc.returncode == 0, proc.stdout + proc.stderr
