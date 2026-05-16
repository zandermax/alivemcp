#!/usr/bin/env python3
"""Generate a validation_report.json using the current parity rules.
This duplicates the validation logic but ensures we use the current helpers
in `scripts.wiki_parity_lib`.
"""

import json
import sys
from pathlib import Path

repo_root = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(repo_root))

import scripts.wiki_parity_lib as wpl  # noqa: E402

registry_path = repo_root / "ALiveMCP_Remote" / "tools" / "core" / "registry.py"
tools_root = repo_root / "ALiveMCP_Remote" / "tools"
docs_root = repo_root / "docs" / "wiki" / "tools"

available = wpl.load_available_tools(str(registry_path))
defined = wpl.find_defined_symbols(str(tools_root))
pages = wpl.find_wiki_pages(str(docs_root))
docstrings = wpl.find_docstrings(str(tools_root))

missing_impl = sorted([t for t in available if t not in defined])
missing_wiki = sorted([t for t in available if t not in pages])
missing_docstrings = sorted([t for t in available if not docstrings.get(t)])
missing_see_also = []
for t in available:
    d = docstrings.get(t)
    if d:
        if "See Also" not in d or "docs/wiki/tools" not in d:
            if t in pages:
                continue
            missing_see_also.append(t)

report = {
    "available_tools_count": len(available),
    "defined_symbols_count": len(defined),
    "wiki_pages_count": len(pages),
    "missing_impl": missing_impl,
    "missing_wiki": missing_wiki,
    "missing_docstrings": missing_docstrings,
    "missing_see_also": missing_see_also,
}

out = repo_root / "scripts" / "validation_report.json"
out.write_text(json.dumps(report, indent=2), encoding="utf-8")
print("Wrote", out)
