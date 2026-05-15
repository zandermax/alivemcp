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


def extract_live_mapping(path):
    try:
        s = open(path, encoding="utf-8").read()
    except Exception:
        return None
    lines = s.splitlines()
    for i, line in enumerate(lines):
        stripped = line.strip()
        # bolded inline section like "**Live mapping:** ..."
        if stripped.lower().startswith("**live mapping:**"):
            rest = stripped[len("**live mapping:**") :].strip()
            if rest:
                return rest
            # collect following paragraph lines
            mapping_lines = []
            for j in range(i + 1, len(lines)):
                lj = lines[j].strip()
                if not lj or lj.startswith("#") or lj.startswith("**") or lj.startswith("##"):
                    break
                mapping_lines.append(lj)
            return " ".join(mapping_lines).strip() or None
        # heading-style: "Live mapping:" or "## Live mapping:"
        if "live mapping:" in stripped.lower():
            pos = stripped.lower().find("live mapping:")
            rest = stripped[pos + len("live mapping:") :].strip()
            if rest:
                return rest
            mapping_lines = []
            for j in range(i + 1, len(lines)):
                lj = lines[j].strip()
                if not lj or lj.startswith("#") or lj.startswith("**") or lj.startswith("##"):
                    break
                mapping_lines.append(lj)
            return " ".join(mapping_lines).strip() or None
    return None


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
            live_map = extract_live_mapping(path)
            candidates.append(
                {
                    "path": rel,
                    "title": title or os.path.splitext(fn)[0],
                    "summary": summary,
                    "live_mapping": live_map,
                }
            )
            if args.apply:
                # insert a minimal frontmatter if missing
                s = open(path, encoding="utf-8").read()
                if not s.lstrip().startswith("---"):
                    # build frontmatter lines, include Live mapping when present
                    fm_lines = ["---"]
                    fm_lines.append('name: "{}"'.format((title or fn).replace('"', '\\"')))
                    fm_lines.append('summary: "{}"'.format(summary.replace('"', '\\"')))
                    if live_map:
                        fm_lines.append('Live mapping: "{}"'.format(live_map.replace('"', '\\"')))
                    fm_lines.append("---")
                    fm = "\n".join(fm_lines) + "\n\n"
                    open(path, "w", encoding="utf-8").write(fm + s)
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump({"candidates": candidates}, f, indent=2)
    print("Wrote", out_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
