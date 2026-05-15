#!/usr/bin/env python3
"""Normalize indentation of docstrings in ALiveMCP_Remote/tools/*.py files.

Creates a backup `*.docstr.bak` before writing changes.
"""

import ast
import os
import re


def normalize_file(path):
    with open(path, encoding="utf-8") as f:
        src = f.read()
    tree = ast.parse(src, path)
    lines = src.splitlines()
    changed = False
    for node in ast.walk(tree):
        if not hasattr(node, "body") or not node.body:
            continue
        first = node.body[0]
        if not (
            isinstance(first, ast.Expr)
            and isinstance(getattr(first, "value", None), ast.Constant)
            and isinstance(first.value.value, str)
        ):
            continue
        old_segment = ast.get_source_segment(src, first)
        if old_segment is None:
            continue
        doc = ast.get_docstring(node)
        if doc is None:
            continue
        # compute indentation of the opening quote line
        start_line_no = first.lineno - 1
        start_line = lines[start_line_no]
        m = re.match(r"(\s*)(['\"]{3})", start_line)
        indent = m.group(1) if m else re.match(r"(\s*)", start_line).group(1)

        doc_lines = doc.splitlines()
        # Build new literal: summary on first line, blank line, then remaining lines
        if len(doc_lines) == 1:
            new_segment = indent + '"""' + doc_lines[0].strip() + '"""'
        else:
            head = indent + '"""' + (doc_lines[0].strip() or "")
            body = [indent + ""]
            for dl in doc_lines[1:]:
                if dl.strip() == "":
                    body.append(indent + "")
                else:
                    body.append(indent + dl)
            tail = indent + '"""'
            new_segment = "\n".join([head] + body + [tail])

        if old_segment != new_segment:
            src = src.replace(old_segment, new_segment, 1)
            lines = src.splitlines()
            changed = True

    if changed:
        bak = path + ".docstr.bak"
        with open(bak, "w", encoding="utf-8") as f:
            f.write(open(path, encoding="utf-8").read())
        with open(path, "w", encoding="utf-8") as f:
            f.write(src)
        return True
    return False


def main():
    repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    tools_root = os.path.join(repo_root, "ALiveMCP_Remote", "tools")
    modified = []
    for root, _, files in os.walk(tools_root):
        for fn in files:
            if not fn.endswith(".py"):
                continue
            path = os.path.join(root, fn)
            if path.endswith(".bak") or path.endswith(".docstr.bak"):
                continue
            if normalize_file(path):
                modified.append(path)
    if modified:
        print("Modified", len(modified), "files")
        for p in modified:
            print("-", p)
    else:
        print("No changes needed")


if __name__ == "__main__":
    main()
