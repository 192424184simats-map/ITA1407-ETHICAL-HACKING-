#!/usr/bin/env python3
"""Validate the Assignment 5 evidence register and print a completion summary.

This script only reads the local CSV. It does not scan hosts or run security tests.
Usage: python3 scripts/validate_evidence.py evidence/evidence_register.csv
"""
import csv
import sys
from collections import Counter
from pathlib import Path

REQUIRED = {
    "ID", "Section", "Target", "Check_or_finding", "Tool",
    "Command_or_method", "Evidence_file", "Severity", "Status",
    "Remediation", "Retest_evidence",
}

def main() -> int:
    path = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("evidence/evidence_register.csv")
    if not path.is_file():
        print(f"ERROR: file not found: {path}")
        return 1

    with path.open(newline="", encoding="utf-8-sig") as handle:
        reader = csv.DictReader(handle)
        missing = REQUIRED - set(reader.fieldnames or [])
        if missing:
            print("ERROR: missing columns:", ", ".join(sorted(missing)))
            return 1
        rows = list(reader)

    ids = [row["ID"].strip() for row in rows]
    duplicates = sorted(item for item, count in Counter(ids).items() if count > 1)
    if duplicates:
        print("ERROR: duplicate IDs:", ", ".join(duplicates))
        return 1

    statuses = Counter((row["Status"].strip() or "Not started") for row in rows)
    complete = sum(count for status, count in statuses.items()
                   if status.lower() in {"confirmed", "completed", "retested"})
    print(f"Evidence entries: {len(rows)}")
    print(f"Completed/confirmed/retested: {complete}")
    print("Status summary:")
    for status, count in sorted(statuses.items()):
        print(f"  {status}: {count}")

    incomplete = [row["ID"] for row in rows
                  if row["Status"].strip().lower() not in {"confirmed", "completed", "retested"}]
    if incomplete:
        print("Still requiring work:", ", ".join(incomplete))
    print("Reminder: only enter findings supported by actual authorized lab evidence.")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
