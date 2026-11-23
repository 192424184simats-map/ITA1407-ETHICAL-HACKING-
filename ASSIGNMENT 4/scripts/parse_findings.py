#!/usr/bin/env python3
"""Validate and summarize an assessment findings CSV; performs no scanning."""
import csv
import sys
from collections import Counter
from pathlib import Path

REQUIRED = {"id", "finding", "tool", "domain", "severity", "status"}
ALLOWED = {"critical", "high", "medium", "low", "informational"}

def main(path: str) -> int:
    with Path(path).open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        missing = REQUIRED - set(reader.fieldnames or [])
        if missing:
            print("Missing columns:", ", ".join(sorted(missing)), file=sys.stderr)
            return 2
        rows = list(reader)
    ids = [row["id"].strip() for row in rows]
    if len(ids) != len(set(ids)):
        print("Duplicate finding IDs detected.", file=sys.stderr)
        return 3
    invalid = [row for row in rows if row["severity"].strip().lower() not in ALLOWED]
    if invalid:
        print("Invalid severity values:", ", ".join(r["id"] for r in invalid), file=sys.stderr)
        return 4
    print(f"Total findings: {len(rows)}")
    print("By severity:")
    counts = Counter(r["severity"].strip().title() for r in rows)
    for level in ("Critical", "High", "Medium", "Low", "Informational"):
        if counts[level]:
            print(f"  {level}: {counts[level]}")
    print("By status:")
    for status, count in sorted(Counter(r["status"].strip() for r in rows).items()):
        print(f"  {status or '(blank)'}: {count}")
    return 0

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} findings.csv", file=sys.stderr)
        raise SystemExit(1)
    raise SystemExit(main(sys.argv[1]))
