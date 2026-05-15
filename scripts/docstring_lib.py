"""
Shared helpers for docstring checking scripts.
"""

import ast
import os
import sys
from pathlib import Path


def load_available_tools(registry_path):
    try:
        src = open(registry_path, encoding="utf-8").read()
    except Exception:
        return []
    tree = ast.parse(src, registry_path)
    for node in tree.body:
        if isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name) and target.id == "AVAILABLE_TOOLS":
                    try:
                        return ast.literal_eval(node.value)
                    except Exception:
                        pass
    return []


def collect_docstrings(tools_root):
    ds = {}
    files_by_symbol = {}
    for root, _, files in os.walk(tools_root):
        for fn in files:
            if not fn.endswith(".py"):
                continue
            path = os.path.join(root, fn)
            try:
                src = open(path, encoding="utf-8").read()
                tree = ast.parse(src, path)
            except Exception:
                continue
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    ds[node.name] = ast.get_docstring(node)
                    files_by_symbol[node.name] = path
    return ds, files_by_symbol


def check_docstring_structure(name, doc):
    if not doc:
        return ["missing"]
    errors = []
    for sec in ("Args:", "Returns:", "Raises:", "See Also:"):
        if sec not in doc:
            errors.append(f"missing {sec}")
    if "docs/wiki/tools" not in (doc or ""):
        errors.append("See Also missing wiki path")
    return errors


def fix_missing_see_also(missing_see_also, files_by_symbol):
    """Attempt to insert minimal See Also lines into docstrings for listed symbols."""
    for name in missing_see_also:
        path = files_by_symbol.get(name)
        if not path:
            continue
        try:
            src = open(path, encoding="utf-8").read()
            tree = ast.parse(src, path)
        except Exception:
            continue
        modified = False
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef) and node.name == name:
                if not node.body:
                    continue
                first = node.body[0]
                if not (
                    isinstance(first, ast.Expr)
                    and isinstance(first.value, ast.Constant)
                    and isinstance(first.value.value, str)
                ):
                    continue
                old_doc = ast.get_docstring(node)
                see_also = f"\n\nSee Also:\n    Wiki: docs/wiki/tools/{name}.md"
                new_doc = (old_doc or "") + see_also
                seg = ast.get_source_segment(src, first)
                if not seg:
                    continue
                new_literal = '"""' + new_doc + '"""'
                new_src = src.replace(seg, new_literal, 1)
                bak = path + ".bak"
                open(bak, "w", encoding="utf-8").write(src)
                open(path, "w", encoding="utf-8").write(new_src)
                modified = True
        if modified:
            print("Updated docstring for", name, "in", path)


# Additional helpers used by alternative docstring-checker variants
def extract_available_tools(registry_path: Path):
    src = registry_path.read_text(encoding="utf-8")
    tree = ast.parse(src)
    for node in tree.body:
        if isinstance(node, ast.Assign):
            for target in node.targets:
                if getattr(target, "id", None) == "AVAILABLE_TOOLS":
                    val = node.value
                    if isinstance(val, (ast.List, ast.Tuple)):
                        items = []
                        StrType = getattr(ast, "Str", None)
                        ConstType = getattr(ast, "Constant", None)
                        for elt in val.elts:
                            if (
                                ConstType is not None
                                and isinstance(elt, ConstType)
                                and isinstance(elt.value, str)
                            ):
                                items.append(elt.value)
                            elif StrType is not None and isinstance(elt, StrType):
                                items.append(elt.s)
                        return items
    raise RuntimeError(f"AVAILABLE_TOOLS not found in {registry_path}")


def slugify(name: str) -> str:
    return name.replace(" ", "_").replace("/", "_")


def gather_python_files(root: Path):
    base = root / "ALiveMCP_Remote" / "tools"
    files = []
    if not base.exists():
        return files
    for p in base.rglob("*.py"):
        files.append(p)
    return files


def find_tool_defs_in_files(files, expected_names):
    found = {}
    for f in files:
        try:
            src = f.read_text(encoding="utf-8")
            tree = ast.parse(src, filename=str(f))
        except Exception as e:
            print("Failed to parse", f, e, file=sys.stderr)
            continue

        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                name = node.name
                if name in expected_names:
                    doc = ast.get_docstring(node) or ""
                    found.setdefault(name, []).append(
                        {"file": str(f), "lineno": node.lineno, "doc": doc}
                    )

    return found


def check_docstring(doc: str, name: str):
    errors = []
    if not doc:
        errors.append("missing_docstring")
        return errors
    if "Args:" not in doc:
        errors.append("missing_Args")
    if "Returns:" not in doc:
        errors.append("missing_Returns")
    if "Raises:" not in doc:
        errors.append("missing_Raises")
    if "See Also:" not in doc or "docs/wiki/tools" not in doc:
        errors.append("missing_See_Also_or_wikilink")
    else:
        if slugify(name) not in doc:
            errors.append("see_also_missing_slug")
    return errors
