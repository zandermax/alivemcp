import ast
import json
from pathlib import Path


def _extract_literal(file_path: Path, var_name: str):
    src = file_path.read_text()
    module = ast.parse(src)
    for node in module.body:
        if isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name) and target.id == var_name:
                    return ast.literal_eval(node.value)
    raise RuntimeError(f"{var_name} not found in {file_path}")


def _normalize_registry_items(items):
    names = set()
    for i in items:
        if isinstance(i, str):
            names.add(i)
        elif isinstance(i, (list, tuple)) and i and isinstance(i[0], str):
            names.add(i[0])
        elif isinstance(i, dict) and "name" in i:
            names.add(i["name"])
        else:
            raise AssertionError(f"Unexpected registry item: {i!r}")
    return names


def _normalize_defs_items(items):
    names = set()
    if isinstance(items, dict):
        return set(items.keys())
    for item in items:
        if isinstance(item, (list, tuple)) and item and isinstance(item[0], str):
            names.add(item[0])
        elif isinstance(item, dict) and "name" in item:
            names.add(item["name"])
        else:
            raise AssertionError(f"Unexpected def item: {item!r}")
    return names


def test_tool_manifest_parity():
    root = Path(__file__).resolve().parents[1]
    registry_file = root / "ALiveMCP_Remote" / "tools" / "core" / "registry.py"
    defs_file = root / "mcp_server_tool_defs.py"
    manifest_file = root / "docs" / "tool_manifest.json"

    available_tools = _extract_literal(registry_file, "AVAILABLE_TOOLS")
    registry_names = _normalize_registry_items(available_tools)

    tool_defs = _extract_literal(defs_file, "TOOL_DEFS_JSON")
    defs_names = _normalize_defs_items(tool_defs)

    manifest = json.loads(manifest_file.read_text())
    manifest_tools = manifest.get("tools", [])
    manifest_names = set()
    for t in manifest_tools:
        if isinstance(t, dict) and "name" in t:
            manifest_names.add(t["name"])
        elif isinstance(t, str):
            manifest_names.add(t)
        else:
            raise AssertionError(f"Unexpected manifest tool entry: {t!r}")

    missing_in_manifest = (registry_names | defs_names) - manifest_names
    extra_in_manifest = manifest_names - (registry_names | defs_names)

    assert not missing_in_manifest, f"Tools missing from manifest: {sorted(missing_in_manifest)}"
    assert not extra_in_manifest, f"Extra tools in manifest: {sorted(extra_in_manifest)}"

    missing_in_registry = defs_names - registry_names
    missing_in_defs = registry_names - defs_names
    assert not missing_in_registry, f"Tools in defs but not registry: {sorted(missing_in_registry)}"
    assert not missing_in_defs, f"Tools in registry but not defs: {sorted(missing_in_defs)}"
