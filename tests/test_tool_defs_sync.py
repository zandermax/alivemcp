import mcp_server_tool_defs
from ALiveMCP_Remote.tools.core import registry as registry_mod


def test_tool_defs_match_registry():
    # Use the runtime `TOOL_DEFS` export (list of (name, desc, schema)).
    raw_defs = list(mcp_server_tool_defs.TOOL_DEFS)
    names_from_defs = [entry[0] for entry in raw_defs]
    registry_names = list(registry_mod.AVAILABLE_TOOLS)

    missing = set(registry_names) - set(names_from_defs)
    extra = set(names_from_defs) - set(registry_names)

    assert not missing and not extra, (
        f"Tool defs mismatch — missing: {sorted(missing)}, extra: {sorted(extra)}"
    )
