#!/usr/bin/env python3
"""Generate a docstring_report.json using `scripts.docstring_lib` helpers."""

import json
import sys
from pathlib import Path

from scripts.docstring_lib import (
    check_docstring_structure,
    collect_docstrings,
    load_available_tools,
)

repo_root = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(repo_root))

registry = repo_root / "ALiveMCP_Remote" / "tools" / "core" / "registry.py"
if not registry.exists():
    print("registry not found", registry)
    raise SystemExit(1)

available = load_available_tools(str(registry))
ds, files_by_symbol = collect_docstrings(str(repo_root / "ALiveMCP_Remote" / "tools"))

problems = {}
for t in available:
    doc = ds.get(t)
    errs = check_docstring_structure(t, doc)
    if errs:
        problems[t] = errs

out = repo_root / "scripts" / "docstring_report.json"
out.write_text(
    json.dumps({"problems": problems, "count": len(problems)}, indent=2), encoding="utf-8"
)
print("Wrote", out)
