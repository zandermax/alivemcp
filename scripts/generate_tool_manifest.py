#!/usr/bin/env python3
"""Generate docs/tool_manifest.json from registry and MCP definitions.

Usage: python3 scripts/generate_tool_manifest.py

This script is idempotent and safe to run as part of CI or locally.
"""

import ast
import json
import os
import re
import sys
from datetime import datetime

BASE = os.path.dirname(os.path.dirname(__file__))
REGISTRY_PY = os.path.join(BASE, "ALiveMCP_Remote", "tools", "core", "registry.py")
MCP_DEFS_PY = os.path.join(BASE, "mcp_server_tool_defs.py")
OUT_PATH = os.path.join(BASE, "docs", "tool_manifest.json")


def parse_registry(path):
    src = open(path, encoding="utf-8").read()
    module = ast.parse(src, filename=path)
    for node in module.body:
        if isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name) and target.id == "AVAILABLE_TOOLS":
                    try:
                        tools = ast.literal_eval(node.value)
                        return list(tools)
                    except Exception:
                        # Fallback: try to evaluate the right-hand side safely
                        try:
                            # Extract slice from first [ to the matching ]
                            start = src.find("AVAILABLE_TOOLS")
                            eq = src.find("=", start)
                            list_src = src[eq + 1 :]
                            # Very small, controlled eval in empty namespace
                            ns = {}
                            exec("AVAILABLE_TOOLS = " + list_src, {}, ns)
                            return list(ns["AVAILABLE_TOOLS"])
                        except Exception as e:
                            raise RuntimeError("Failed to parse AVAILABLE_TOOLS: " + str(e))
    raise RuntimeError("AVAILABLE_TOOLS not found in " + path)


def parse_mcp_defs(path):
    src = open(path, encoding="utf-8").read()
    m = re.search(r'TOOL_DEFS_JSON\s*=\s*r?"""(.*?)"""', src, re.DOTALL)
    if m:
        json_text = m.group(1)
        raw_defs = json.loads(json_text)
        return raw_defs

    # Fallback: import the module and use runtime TOOL_DEFS export
    try:
        import importlib.util

        spec = importlib.util.spec_from_file_location("mcp_server_tool_defs", path)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)  # type: ignore
        defs = list(getattr(mod, "TOOL_DEFS"))
        return [[n, d, s] for n, d, s in defs]
    except Exception:
        raise RuntimeError("TOOL_DEFS_JSON not found in " + path)


def build_manifest(registry_tools, raw_defs):
    mcp_map = {entry[0]: {"description": entry[1], "schema": entry[2]} for entry in raw_defs}
    all_names = sorted(set(registry_tools) | set(mcp_map.keys()))
    tools = []
    warnings = []
    for name in all_names:
        in_registry = name in registry_tools
        in_mcp = name in mcp_map
        description = mcp_map[name]["description"] if in_mcp else ""
        schema = mcp_map[name]["schema"] if in_mcp else None
        if in_registry and not in_mcp:
            warnings.append(f"Present in registry but missing MCP def: {name}")
        if in_mcp and not in_registry:
            warnings.append(f"Present in MCP defs but missing registry entry: {name}")
        tools.append(
            {
                "name": name,
                "in_registry": in_registry,
                "in_mcp_defs": in_mcp,
                "description": description,
                "schema": schema,
            }
        )

    manifest = {
        "version": "0.1",
        "generated_from": [
            os.path.relpath(REGISTRY_PY, BASE),
            os.path.relpath(MCP_DEFS_PY, BASE),
        ],
        "generated_at": datetime.datetime.now(datetime.timezone.utc).isoformat() + "Z",
        "tool_count": len(tools),
        "tools": tools,
    }
    if warnings:
        manifest["warnings"] = warnings
    return manifest


def main():
    try:
        registry_tools = parse_registry(REGISTRY_PY)
    except Exception as e:
        print("Error parsing registry:", e, file=sys.stderr)
        sys.exit(2)

    try:
        raw_defs = parse_mcp_defs(MCP_DEFS_PY)
    except Exception as e:
        print("Error parsing MCP defs:", e, file=sys.stderr)
        sys.exit(2)

    manifest = build_manifest(registry_tools, raw_defs)

    os.makedirs(os.path.dirname(OUT_PATH), exist_ok=True)
    with open(OUT_PATH, "w", encoding="utf-8") as fh:
        json.dump(manifest, fh, indent=2, ensure_ascii=False)

    print(f"Wrote {OUT_PATH} ({manifest['tool_count']} tools)")
    if "warnings" in manifest:
        print("Warnings:")
        for w in manifest["warnings"]:
            print("  -", w)


if __name__ == "__main__":
    main()
