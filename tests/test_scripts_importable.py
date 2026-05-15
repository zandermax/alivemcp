def test_scripts_importable():
    # Ensure the CLI scripts are importable and expose a main() entry
    import importlib

    modules = [
        "scripts.generate_from_wiki",
        "scripts.validate_wiki_parity",
        "scripts.docstring_checker",
        "scripts.migrate_wiki_frontmatter",
    ]
    for m in modules:
        mod = importlib.import_module(m)
        assert hasattr(mod, "main")
        assert callable(getattr(mod, "main"))
