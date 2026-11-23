"""Reconnaissance item validation using synthetic records only."""
from collections import Counter

ALLOWED_ASSETS = {"LAB-PORTAL", "LAB-DNS", "LAB-LMS"}

ITEMS = [
    {"id":"I1","asset":"LAB-PORTAL","fingerprint":"portal-home","age_days":2,"reliable":True},
    {"id":"I2","asset":"PROD-DB","fingerprint":"db-host","age_days":1,"reliable":True},
    {"id":"I3","asset":"LAB-DNS","fingerprint":"mx-record","age_days":120,"reliable":True},
    {"id":"I4","asset":"LAB-LMS","fingerprint":"lms-login","age_days":3,"reliable":True},
    {"id":"I5","asset":"LAB-LMS","fingerprint":"lms-login","age_days":3,"reliable":True},
    {"id":"I6","asset":"LAB-DNS","fingerprint":"unknown-txt","age_days":1,"reliable":False},
]

def validate(items):
    seen = set()
    results = []
    for item in items:
        # Cheap, decisive scope check first.
        if item["asset"] not in ALLOWED_ASSETS:
            status, reason = "REJECT", "out of scope"
        elif item["fingerprint"] in seen:
            status, reason = "DROP_DUPLICATE", "duplicate fingerprint"
        else:
            seen.add(item["fingerprint"])
            if item["age_days"] > 30:
                status, reason = "RECHECK", "stale; re-query or confirm"
            elif not item["reliable"]:
                status, reason = "RECHECK", "source reliability not established"
            else:
                status, reason = "PASS", "in scope, fresh, unique and reliable"
        results.append((item["id"], status, reason))
    return results

def main():
    results = validate(ITEMS)
    for row in results:
        print(*row, sep=" | ")
    print("SUMMARY:", dict(Counter(row[1] for row in results)))

if __name__ == "__main__":
    main()
