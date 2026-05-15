#!/usr/bin/env python3
"""Generate candidate YAML frontmatter for wiki pages (dry-run by default).

Writes `scripts/migration_candidates.json` with suggested frontmatter for
each page under `docs/wiki/tools/`.
"""

import argparse
import json
import os
import sys


def extract_title_and_summary(path):
    try:
        s = open(path, encoding="utf-8").read()
    except Exception:
        return None, None
    lines = s.splitlines()
    title = None
    summary_lines = []
    in_summary = False
    for i, line in enumerate(lines[:50]):
        if line.startswith("#") and not title:
            title = line.lstrip("#").strip()
            in_summary = True
            continue
        if in_summary:
            if line.strip() == "":
                break
            summary_lines.append(line.strip())
    summary = " ".join(summary_lines).strip() if summary_lines else ""
    return title, summary


def main(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument("--apply", action="store_true")
    args = parser.parse_args(argv)

    repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    wiki_root = os.path.join(repo_root, "docs", "wiki", "tools")
    out_path = os.path.join(os.path.dirname(__file__), "migration_candidates.json")

    candidates = []
    if not os.path.isdir(wiki_root):
        print("No wiki tools folder found at", wiki_root)
        return 1
    for root, _, files in os.walk(wiki_root):
        for fn in files:
            if not fn.endswith(".md"):
                continue
            path = os.path.join(root, fn)
            rel = os.path.relpath(path, repo_root)
            title, summary = extract_title_and_summary(path)
            candidates.append(
                {"path": rel, "title": title or os.path.splitext(fn)[0], "summary": summary}
            )
            if args.apply:
                # insert a minimal frontmatter if missing
                s = open(path, encoding="utf-8").read()
                if not s.lstrip().startswith("---"):
                    fm = '---\nname: "{}"\nsummary: "{}"\n---\n\n'.format(
                        (title or fn).replace('"', '"'), summary.replace('"', '"')
                    )
                    open(path, "w", encoding="utf-8").write(fm + s)
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump({"candidates": candidates}, f, indent=2)
    print("Wrote", out_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
