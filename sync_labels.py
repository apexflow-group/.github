#!/usr/bin/env python3
"""Sync labels.yml to every apexflow-group repo.

    python3 ~/workspace/apexflow/.github/sync_labels.py [--dry-run] [repo ...]

Creates missing labels, corrects colour/description drift, and deletes the
retired GitHub defaults. Labels present on a repo but absent from labels.yml
are REPORTED, never auto-deleted -- an unknown label may be carrying real state
on an open issue, and losing that silently is worse than a noisy report.

Source of truth: labels.yml.
Rules: ~/workspace/apexflow/handbook/TASK_PROCESS.md §3.
"""

from __future__ import annotations

import json
import os
import re
import subprocess
import sys

ORG = "apexflow-group"
HERE = os.path.dirname(os.path.abspath(__file__))
LABELS_YML = os.path.join(HERE, "labels.yml")

# GitHub defaults we deliberately do not use. Deleted only when unused.
RETIRED = ["bug", "enhancement", "documentation",
           "good first issue", "help wanted", "question"]


def gh(*args: str) -> str:
    r = subprocess.run(["gh", *args], capture_output=True, text=True)
    if r.returncode != 0:
        raise RuntimeError(f"gh {' '.join(args)}\n{r.stderr.strip()}")
    return r.stdout


def unquote(v: str) -> str:
    v = v.strip()
    if len(v) >= 2 and v[0] == v[-1] and v[0] in "\"'":
        v = v[1:-1]
    return v


def parse_labels() -> list[dict]:
    """Minimal reader for our own flat list-of-mappings file.

    Deliberately not PyYAML: this must run on a bare interpreter with no
    virtualenv, and the file's shape is fixed by us.
    """
    out: list[dict] = []
    cur: dict | None = None
    for raw in open(LABELS_YML, encoding="utf-8"):
        if raw.lstrip().startswith("#"):
            continue
        m = re.match(r"^-\s+name:\s*(.+)$", raw)
        if m:
            cur = {"name": unquote(m.group(1)), "color": "cccccc", "description": ""}
            out.append(cur)
            continue
        if cur is None:
            continue
        m = re.match(r"^\s+color:\s*(.+)$", raw)
        if m:
            cur["color"] = unquote(m.group(1)).lstrip("#")
            continue
        m = re.match(r"^\s+description:\s*(.+)$", raw)
        if m:
            cur["description"] = unquote(m.group(1))
    return out


def main() -> int:
    dry = "--dry-run" in sys.argv
    repos = [a for a in sys.argv[1:] if not a.startswith("-")]
    if not repos:
        repos = json.loads(gh("repo", "list", ORG, "--limit", "100",
                              "--json", "name"))
        repos = [r["name"] for r in repos]

    wanted = parse_labels()
    by_name = {w["name"]: w for w in wanted}
    print(f"labels.yml defines {len(wanted)} labels; syncing {len(repos)} repos")
    if dry:
        print("(dry run -- no writes)")
    print()

    created = updated = deleted = unknown = 0

    for repo in repos:
        full = f"{ORG}/{repo}"
        print(f"-- {full}")
        have = {
            l["name"]: l
            for l in json.loads(gh("label", "list", "--repo", full, "--limit", "200",
                                   "--json", "name,color,description"))
        }

        for w in wanted:
            n, c, d = w["name"], w["color"], w["description"]
            cur = have.get(n)
            if cur is None:
                print(f"   + create  {n}")
                if not dry:
                    gh("label", "create", n, "--repo", full,
                       "--color", c, "--description", d)
                created += 1
            elif cur["color"].lower() != c.lower() or (cur.get("description") or "") != d:
                print(f"   ~ update  {n}")
                if not dry:
                    gh("label", "edit", n, "--repo", full,
                       "--color", c, "--description", d)
                updated += 1

        for r in RETIRED:
            if r not in have:
                continue
            used = json.loads(gh("issue", "list", "--repo", full, "--state", "all",
                                 "--label", r, "--limit", "1", "--json", "number"))
            if used:
                print(f"   ! retired label {r!r} still on issues -- relabel first")
                continue
            print(f"   - delete  {r} (retired GitHub default, unused)")
            if not dry:
                gh("label", "delete", r, "--repo", full, "--yes")
            deleted += 1

        for n in sorted(have):
            if n in by_name or n in RETIRED:
                continue
            print(f"   ? unknown label {n!r} -- add to labels.yml or remove by hand")
            unknown += 1

    print()
    print(f"created={created}  updated={updated}  deleted={deleted}  unknown={unknown}")
    if unknown:
        print("NOTE: unknown labels are never auto-deleted.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
