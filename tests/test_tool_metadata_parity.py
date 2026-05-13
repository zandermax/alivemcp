import json
import os

import mcp_server_tool_defs
from ALiveMCP_Remote.tools.core import registry as registry_mod


def test_manifest_registry_mcp_parity():
    # Paths
    repo_root = os.path.dirname(os.path.dirname(__file__))
    manifest_path = os.path.join(repo_root, "docs", "tool_manifest.json")

    # Load manifest
    with open(manifest_path, encoding="utf-8") as fh:
        manifest = json.load(fh)
    manifest_names = [t["name"] for t in manifest.get("tools", [])]

    # Load registry
    registry_names = list(registry_mod.AVAILABLE_TOOLS)

    # Load MCP defs from runtime export
    raw_defs = list(mcp_server_tool_defs.TOOL_DEFS)
    mcp_names = [entry[0] for entry in raw_defs]

    set_manifest = set(manifest_names)
    set_registry = set(registry_names)
    set_mcp = set(mcp_names)

    assert set_manifest == set_registry == set_mcp, (
        "Tool metadata mismatch across sources:\n"
        f" - manifest only: {sorted(set_manifest - set_registry)}\n"
        f" - registry only: {sorted(set_registry - set_manifest)}\n"
        f" - mcp only: {sorted(set_mcp - set_manifest)}"
    )
