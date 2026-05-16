#!/usr/bin/env python3
"""
generate_wiki_index.py

Create `docs/wiki/INDEX.md` and per-tool stub pages from AVAILABLE_TOOLS
and `mcp_tool_defs/index.json`.

Usage:
  python scripts/generate_wiki_index.py [--write]

By default the script runs in dry-run mode and prints actions. Use `--write`
to actually create files under `docs/wiki/`.
"""

import ast
import json
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "ALiveMCP_Remote" / "tools" / "core" / "registry.py"
TOOL_DEFS = ROOT / "mcp_tool_defs" / "index.json"
OUT_DIR = ROOT / "docs" / "wiki"


def extract_available_tools(registry_path: Path):
    src = registry_path.read_text(encoding="utf-8")
    tree = ast.parse(src)
    for node in tree.body:
        if isinstance(node, ast.Assign):
            for target in node.targets:
                if getattr(target, "id", None) == "AVAILABLE_TOOLS":
                    val = node.value
                    # Prefer literal_eval for robustness across Python versions
                    if isinstance(val, (ast.List, ast.Tuple)):
                        try:
                            evaluated = ast.literal_eval(val)
                            if isinstance(evaluated, (list, tuple)):
                                return [str(x) for x in evaluated]
                        except Exception:
                            # Fallback: inspect AST nodes without referencing ast.Str directly
                            items = []
                            StrNode = getattr(ast, "Str", None)
                            ConstNode = getattr(ast, "Constant", None)
                            for elt in val.elts:
                                if StrNode is not None and isinstance(elt, StrNode):
                                    items.append(getattr(elt, "s", ""))
                                elif (
                                    ConstNode is not None
                                    and isinstance(elt, ConstNode)
                                    and isinstance(getattr(elt, "value", None), str)
                                ):
                                    items.append(elt.value)
                                else:
                                    # last-ditch: try common attributes
                                    v = getattr(elt, "s", None)
                                    if isinstance(v, str):
                                        items.append(v)
                                    else:
                                        v2 = getattr(elt, "value", None)
                                        if isinstance(v2, str):
                                            items.append(v2)
                            return items
    raise RuntimeError(f"AVAILABLE_TOOLS variable not found in {registry_path}")


def load_tool_defs(path: Path):
    if not path.exists():
        return {}
    with path.open("r", encoding="utf-8") as f:
        data = json.load(f)
    # index.json may be a dict or a list; normalize to mapping by name
    mapping = {}
    if isinstance(data, dict):
        # common formats: {'tools': [...]} or {toolname: {...}}
        if "tools" in data and isinstance(data["tools"], list):
            for item in data["tools"]:
                if isinstance(item, dict) and "name" in item:
                    mapping[item["name"]] = item
        else:
            mapping = data
    elif isinstance(data, list):
        for item in data:
            if isinstance(item, dict) and "name" in item:
                mapping[item["name"]] = item
    return mapping


def slugify(name: str) -> str:
    return name.replace(" ", "_").replace("/", "_")


def make_stub(tool_name: str, defs_map: dict, out_dir: Path, write: bool):
    slug = slugify(tool_name)
    # If an existing page exists anywhere in the wiki, prefer it and don't overwrite
    for p in out_dir.glob(f"tools/**/{slug}.md"):
        return str(p)

    meta = defs_map.get(tool_name, {})
    domain = meta.get("domain") or meta.get("module") or "general"
    target_dir = out_dir / "tools" / domain
    target_file = target_dir / (slug + ".md")
    if write:
        target_dir.mkdir(parents=True, exist_ok=True)
    if target_file.exists() and write:
        return str(target_file)

    front = [
        "---",
        "status: draft",
        "live_versions: [11]",
        "owners: []",
        "tags: []",
        f"last_updated: {date.today().isoformat()}",
        "---",
        "",
    ]
    body = [
        f"# {tool_name}",
        "",
        f"**Domain**: {domain}",
        "",
        "**Summary**: TODO",
        "",
        "**Parameters**: TODO",
        "",
        "**Live mapping**: TODO",
        "",
        "**Example request**:",
        "```json",
        f'{{"action": "{tool_name}"}}',
        "```",
        "",
        "**Example response**: TODO",
        "",
        "**Ableton docs**: TODO",
        "",
        "**See also**: TODO",
        "",
    ]
    content = "\n".join(front + body)
    if write:
        target_file.write_text(content, encoding="utf-8")
        return str(target_file)
    else:
        return content


def write_index(grouped: dict, out_file: Path, write: bool):
    lines = ["# Tools Index", ""]
    for domain in sorted(grouped.keys()):
        lines.append(f"## {domain}")
        lines.append("")
        for tool in sorted(grouped[domain]):
            relpath = f"tools/{domain}/{slugify(tool)}.md"
            lines.append(f"- [{tool}]({relpath})")
        lines.append("")
    content = "\n".join(lines)
    if write:
        out_file.parent.mkdir(parents=True, exist_ok=True)
        out_file.write_text(content, encoding="utf-8")
        return str(out_file)
    else:
        return content


def main(args):
    write = "--write" in args or "--generate" in args
    try:
        tools = extract_available_tools(REGISTRY)
    except Exception as e:
        print("Error reading AVAILABLE_TOOLS:", e)
        return 2
    defs = load_tool_defs(TOOL_DEFS)
    grouped = {}
    for t in tools:
        # Prefer existing file location when present
        slug = slugify(t)
        existing = None
        for p in OUT_DIR.glob(f"tools/**/{slug}.md"):
            existing = p
            break
        if existing:
            domain = existing.parent.name
        else:
            meta = defs.get(t, {}) if defs else {}
            domain = meta.get("domain") or meta.get("module") or "general"
        grouped.setdefault(domain, []).append(t)
        if write:
            make_stub(t, defs, OUT_DIR, write=True)

    index_path = OUT_DIR / "INDEX.md"
    written = write_index(grouped, index_path, write=write)
    print(f"Tools found: {len(tools)}")
    print(f"Index: {written}")
    if not write:
        print("\nDry-run complete. Use `--write` to create files under docs/wiki/")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
