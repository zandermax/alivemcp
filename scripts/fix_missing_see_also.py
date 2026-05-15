#!/usr/bin/env python3
"""Fix missing "See Also" entries in function docstrings by appending
links to the corresponding docs/wiki/tools pages.

Use with the repository root as CWD. It will modify Python files under
`ALiveMCP_Remote/tools/` in-place.
"""

import ast
import os
import re
import sys
from pathlib import Path

repo_root = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(repo_root))

try:
    import scripts.wiki_parity_lib as wpl
except Exception as e:
    print("Failed to import scripts.wiki_parity_lib:", e)
    raise

TOOLS_ROOT = repo_root / "ALiveMCP_Remote" / "tools"
DOCS_ROOT = repo_root / "docs" / "wiki" / "tools"
REGISTRY_PATH = repo_root / "ALiveMCP_Remote" / "tools" / "core" / "registry.py"

if not REGISTRY_PATH.exists():
    print("Registry not found at", REGISTRY_PATH)
    raise SystemExit(1)

available = wpl.load_available_tools(str(REGISTRY_PATH))
md_map = wpl.gather_md_files(str(DOCS_ROOT))
docstrings = wpl.find_docstrings(str(TOOLS_ROOT))

updated_files = set()


# Helper to find and update docstring in a given file for a function name.
def update_docstring_in_file(py_path: Path, func_name: str, md_list):
    src = py_path.read_text(encoding="utf-8")
    try:
        tree = ast.parse(src, str(py_path))
    except Exception as e:
        print("Skipping (parse error):", py_path, e)
        return False

    lines = src.splitlines(True)

    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef) and node.name == func_name:
            # Ensure function has a docstring node
            if not node.body:
                continue
            first = node.body[0]
            if not isinstance(first, ast.Expr):
                continue
            # Value can be ast.Constant (py3.8+) with str, or ast.Str
            val = first.value
            if not (
                isinstance(val, ast.Str)
                or (
                    hasattr(ast, "Constant")
                    and isinstance(val, ast.Constant)
                    and isinstance(val.value, str)
                )
            ):
                continue
            # Extract original docstring text
            orig_doc = ast.get_docstring(node, clean=False) or ""
            if "See Also" in orig_doc and "docs/wiki/tools" in orig_doc:
                # already ok
                return False

            # Build See Also block
            if not md_list:
                # Nothing to point to
                return False
            see_lines = ["\nSee Also:\n"]
            for rel in md_list:
                see_lines.append(f"- docs/wiki/tools/{rel}\n")
            see_block = "".join(see_lines)

            new_doc = orig_doc.rstrip() + "\n\n" + see_block.strip() + "\n"

            # Compute replacement block using line numbers on the AST node
            # AST Expr node has lineno and end_lineno attributes
            start = first.lineno - 1
            end = getattr(first, "end_lineno", None)
            if end is None:
                # fallback: find end by searching for closing triple quotes
                # join from start to start+10 lines
                end = start
                max_probe = min(start + 50, len(lines) - 1)
                joined = "".join(lines[start : max_probe + 1])
                m = re.search(r"([\"']{3})", joined)
                if not m:
                    # can't safely replace
                    print("Could not find docstring delimiters in", py_path)
                    return False
                # naive: assume closing delimiter exists later; find last occurrence
                quote = m.group(1)
                last = joined.rfind(quote)
                if last == -1:
                    return False
                # compute approximate end line
                pre = joined[: last + 3]
                end = start + pre.count("\n")
            else:
                end = end - 1

            # Get the original block to inspect delimiter/prefix
            orig_block = "".join(lines[start : end + 1])
            # Find opening triple quote (and optional prefix like r,u,f)
            m2 = re.match(
                r"(?P<indent>\s*)(?P<prefix>[rubfRUBF]*)?(?P<delim>[\"']{3})", lines[start]
            )
            if not m2:
                # fallback: inspect orig_block
                m3 = re.search(r"(?P<prefix>[rubfRUBF]*)?(?P<delim>[\"']{3})", orig_block)
                if not m3:
                    print(
                        "Could not detect docstring delimiter in",
                        py_path,
                        "for function",
                        func_name,
                    )
                    return False
                indent = ""
                prefix = m3.group("prefix") or ""
                delim = m3.group("delim")
            else:
                indent = m2.group("indent") or ""
                prefix = m2.group("prefix") or ""
                delim = m2.group("delim")

            # Recompose block with same delimiter and prefix
            # Escape delim inside content if necessary (rare)
            content = new_doc
            # Build new block lines
            new_block = indent + prefix + delim + content + delim + "\n"

            # Replace lines[start:end+1] with new_block
            new_lines = lines[:start] + [new_block] + lines[end + 1 :]
            py_path.write_text("".join(new_lines), encoding="utf-8")
            print(f"Updated docstring for {func_name} in {py_path}")
            return True
    return False


if __name__ == "__main__":
    tools_root = TOOLS_ROOT
    changed = []
    for t in sorted(available):
        d = docstrings.get(t)
        if d:
            if "See Also" in d and "docs/wiki/tools" in d:
                continue
            # find md pages for this tool
            md_list = md_map.get(t)
            if not md_list:
                # nothing to point to — skip
                continue
            # Find the file defining the function
            updated = False
            for root, _, files in os.walk(tools_root):
                for fn in files:
                    if not fn.endswith(".py"):
                        continue
                    path = Path(root) / fn
                    try:
                        res = update_docstring_in_file(path, t, md_list)
                        if res:
                            updated = True
                            changed.append(str(path))
                            break
                    except Exception as e:
                        print("Error updating", path, e)
                if updated:
                    break

    if changed:
        print("\nFiles updated:")
        for p in sorted(set(changed)):
            print("-", p)
    else:
        print("No docstring updates performed")
