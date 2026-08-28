"""Make the standalone scripts importable without packaging them."""

import sys
from pathlib import Path

for d in ("scripts", "evals"):
    path = Path(__file__).resolve().parent.parent / d
    if str(path) not in sys.path:
        sys.path.insert(0, str(path))
