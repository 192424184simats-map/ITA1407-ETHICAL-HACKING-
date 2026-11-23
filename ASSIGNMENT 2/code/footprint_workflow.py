"""Synthetic, offline footprinting strategy demonstration.

No DNS, WHOIS, search-engine, archive or network requests are made.
All targets and observations are fictional.
"""
from dataclasses import dataclass

@dataclass
class Source:
    name: str
    mode: str
    yields: str
    caveat: str

SOURCES = [
    Source("WHOIS/RDAP", "Passive", "Registrar, dates, name servers", "Privacy redaction and stale metadata"),
    Source("Search operators", "Passive", "Indexed pages and public documents", "Index is incomplete or outdated"),
    Source("Archived pages", "Passive", "Historical public content", "May no longer be current"),
    Source("DNS A/MX/NS/TXT", "Active", "Published host and mail records", "Caching, delegation, split-horizon"),
    Source("Service metadata", "Active", "Service/version hints", "Only in explicitly authorized lab scope"),
]

TARGETS = {
    "A-well-protected": {"prediction": "minimal metadata", "observed": "registrar only; transfer denied"},
    "B-information-leak": {"prediction": "public documents and verbose TXT", "observed": "synthetic PDF metadata and TXT clue"},
    "C-misconfigured-DNS": {"prediction": "stale record and lab AXFR exposure", "observed": "stale A record; mock AXFR allowed"},
    "D-minimal-footprint": {"prediction": "very little public data", "observed": "NS/A only; no archive entries"},
}

def main():
    print("OFFLINE FOOTPRINTING STRATEGY — SYNTHETIC DATA ONLY")
    for source in SOURCES:
        print(f"- {source.name}: {source.mode}; yields={source.yields}; caveat={source.caveat}")
    print("\nPrediction vs observation:")
    for name, result in TARGETS.items():
        print(f"{name}: predicted={result['prediction']} | observed={result['observed']}")
    print("\nScale design: batch ingest -> scope allow-list -> normalize -> deduplicate -> prioritize.")
    print("Third-party assets remain excluded without written provider authorization.")

if __name__ == "__main__":
    main()
