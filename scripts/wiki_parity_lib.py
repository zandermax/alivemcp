"""
Helpers for validate_wiki_parity script.
"""

import ast
import json
import os
import re
from pathlib import Path


def load_available_tools(registry_path):
    if not os.path.exists(registry_path):
        return []
    src = open(registry_path, encoding="utf-8").read()
    tree = ast.parse(src, registry_path)
    for node in tree.body:
        if isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name) and target.id == "AVAILABLE_TOOLS":
                    try:
                        return ast.literal_eval(node.value)
                    except Exception:
                        pass
    m = re.search(r"AVAILABLE_TOOLS\s*=\s*(\[[\s\S]*?\])", src)
    if m:
        try:
            return ast.literal_eval(m.group(1))
        except Exception:
            pass
    return []


def find_defined_symbols(tools_root):
    symbols = set()
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
                    symbols.add(node.name)
    return symbols


def find_wiki_pages(wiki_root):
    pages = set()
    if not os.path.isdir(wiki_root):
        return pages
    for root, _, files in os.walk(wiki_root):
        for fn in files:
            if not fn.endswith(".md"):
                continue
            stem = os.path.splitext(fn)[0]
            pages.add(stem)
    return pages


def find_docstrings(tools_root):
    docs = {}
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
                    docs[node.name] = ast.get_docstring(node)
    return docs


def slugify(name: str):
    return name.replace(" ", "_").replace("/", "_")


def gather_md_files(docs_root: str):
    md_map = {}
    for root, _, files in os.walk(docs_root):
        for f in files:
            if f.endswith(".md"):
                name = os.path.splitext(f)[0]
                rel = os.path.relpath(os.path.join(root, f), docs_root)
                md_map.setdefault(name, []).append(rel)
    return md_map


def load_mcp_tool_names(root: Path):
    parts_dir = root / "mcp_tool_defs"
    names = set()
    index_path = parts_dir / "index.json"
    if index_path.exists():
        try:
            data = json.loads(index_path.read_text(encoding="utf-8"))
        except Exception:
            return names

        if isinstance(data, dict) and "parts" in data and isinstance(data["parts"], list):
            for part in data["parts"]:
                p = parts_dir / part
                if p.exists():
                    try:
                        arr = json.loads(p.read_text(encoding="utf-8"))
                        for item in arr:
                            if isinstance(item, list) and item:
                                names.add(item[0])
                            elif isinstance(item, dict) and "name" in item:
                                names.add(item["name"])
                    except Exception:
                        pass
        elif isinstance(data, list):
            for item in data:
                if isinstance(item, list) and item:
                    names.add(item[0])
                elif isinstance(item, dict) and "name" in item:
                    names.add(item["name"])
        else:
            try:
                for k in getattr(data, "keys", lambda: [])():
                    names.add(k)
            except Exception:
                pass

        return names

    ms = root / "mcp_server_tool_defs.py"
    if ms.exists():
        try:
            text = ms.read_text(encoding="utf-8")
            m = re.search(r"TOOL_DEFS_JSON\s*=\s*r?([\'\"]{3})(.*?)\1", text, re.S)
            if m:
                blob = m.group(2)
                arr = json.loads(blob)
                for item in arr:
                    if isinstance(item, list) and item:
                        names.add(item[0])
                    elif isinstance(item, dict) and "name" in item:
                        names.add(item["name"])
                return names

            import importlib.util

            spec = importlib.util.spec_from_file_location("mcp_server_tool_defs", str(ms))
            mod = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(mod)  # type: ignore
            defs = list(getattr(mod, "TOOL_DEFS", []))
            for entry in defs:
                if isinstance(entry, (list, tuple)) and entry:
                    names.add(entry[0])
            return names
        except Exception:
            return names

    return names
