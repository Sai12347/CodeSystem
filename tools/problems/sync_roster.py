#!/usr/bin/env python3
"""Deterministically rebuild problems/roster.json from problems/<topic>/<NN>-<slug>/problem.json."""
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PROBLEMS_DIR = ROOT / "problems"
DIR_RE = re.compile(r"^(\d{2,3})-([a-z0-9]+(?:-[a-z0-9]+)*)$")


def main():
    topics = json.loads((PROBLEMS_DIR / "topics.json").read_text(encoding="utf-8"))
    roster_path = PROBLEMS_DIR / "roster.json"
    old_roster = json.loads(roster_path.read_text(encoding="utf-8")) if roster_path.exists() else {}

    old_lc = {}
    for tid, rows in old_roster.items():
        for row in rows:
            if len(row) >= 5 and row[4] is not None:
                old_lc[(tid, row[0])] = row[4]

    new_roster = {}
    total = 0
    for t in topics:
        tid = t["id"]
        tdir = PROBLEMS_DIR / tid
        rows = []
        if tdir.exists():
            dirs = []
            for d in tdir.iterdir():
                if not d.is_dir():
                    continue
                m = DIR_RE.match(d.name)
                if m and (d / "problem.json").exists():
                    dirs.append((int(m.group(1)), d.name, d))
            dirs.sort(key=lambda x: (x[0], x[1]))
            for _, dname, d in dirs:
                meta = json.loads((d / "problem.json").read_text(encoding="utf-8"))
                lc = meta.get("leetcode", old_lc.get((tid, dname)))
                rows.append([dname, meta["title"], meta["difficulty"], meta["subtopic"], lc])
        new_roster[tid] = rows
        total += len(rows)

    roster_path.write_text(json.dumps(new_roster, indent=2) + "\n", encoding="utf-8")
    print(f"Synced roster.json: {total} problems across {len(new_roster)} topics")


if __name__ == "__main__":
    main()
