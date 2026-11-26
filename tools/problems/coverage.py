#!/usr/bin/env python3
"""Report authored problem coverage against a per-topic minimum."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
PROBLEMS = REPO / "problems"


def count_authored(topic_id: str) -> tuple[int, list[str]]:
    topic_dir = PROBLEMS / topic_id
    if not topic_dir.is_dir():
        return 0, []

    complete = 0
    incomplete: list[str] = []
    required = ("problem.json", "tests.py", "solution.py", "Solution.java")
    for folder in sorted(topic_dir.iterdir()):
        if not folder.is_dir() or folder.name.startswith((".", "_")):
            continue
        missing = [name for name in required if not (folder / name).is_file()]
        if missing:
            incomplete.append(f"{folder.name} (missing {', '.join(missing)})")
        else:
            complete += 1
    return complete, incomplete


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--minimum", type=int, default=100, help="required complete questions per topic (default: 100)")
    parser.add_argument("--fail-below-minimum", action="store_true", help="exit nonzero while any topic is below its minimum")
    args = parser.parse_args()
    if args.minimum < 1:
        parser.error("--minimum must be at least 1")

    topics = json.loads((PROBLEMS / "topics.json").read_text(encoding="utf-8"))
    total = 0
    deficient = 0
    incomplete_total = 0
    print(f"{'TOPIC':<24} {'QUESTIONS':>9} {'NEEDED':>8}  STATUS")
    print("-" * 62)
    for topic in topics:
        count, incomplete = count_authored(topic["id"])
        gap = max(0, args.minimum - count)
        total += count
        incomplete_total += len(incomplete)
        deficient += gap > 0
        status = f"add {gap}" if gap else "ready"
        if incomplete:
            status += f"; {len(incomplete)} incomplete source folder(s)"
        print(f"{topic['id']:<24} {count:>9} {gap:>8}  {status}")
    print("-" * 62)
    print(f"TOTAL: {total} complete problems across {len(topics)} topics; {deficient} topics below {args.minimum}; {incomplete_total} incomplete source folders.")
    return int(args.fail_below_minimum and (deficient > 0 or incomplete_total > 0))


if __name__ == "__main__":
    sys.exit(main())
