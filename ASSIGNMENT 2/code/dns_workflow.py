"""Offline DNS-footprinting workflow design and synthetic case analysis.

This file deliberately makes no DNS queries. It prints safe command templates
for a lab-owned .example zone. AXFR is not executed by this program.
"""
RECORD_TYPES = ("A", "MX", "NS", "TXT")
CASES = [
    ("Secured", "A/MX/NS/TXT; transfer denied", "Published records only"),
    ("AXFR misconfiguration", "Whole lab zone may be exposed", "Mock dataset: transfer allowed"),
    ("Stale record", "Old host remains listed", "Expired A record in synthetic data"),
    ("Split-horizon", "External view omits internal names", "Public-only view"),
    ("Delegated child", "Child NS answers separately", "Delegated lab NS"),
    ("Wildcard DNS", "Random names may resolve", "Synthetic wildcard response"),
]

def main():
    zone = "lab.example"
    print("SAFE COMMAND TEMPLATES — use only with an explicitly authorized lab-owned zone")
    for record_type in RECORD_TYPES:
        print(f"dig {record_type} {zone}")
    print(f"nslookup -type=A {zone}")
    print("\nAXFR is intentionally disabled. Do not attempt transfers without explicit written authorization.")
    print("\nSynthetic DNS cases:")
    for name, predicted, observed in CASES:
        print(f"{name}: predicted={predicted}; observed={observed}")
    print("\nCountermeasure design: restrict transfers to approved secondary servers and use TSIG.")

if __name__ == "__main__":
    main()
