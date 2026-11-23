# Assignment 2 — Footprinting, Reconnaissance & Social-Engineering Awareness

**Student:** N. Arun Kumar · **Register No.:** 192424184 · **Course:** ITA14 Ethical Hacking · **CO2**

## Contents
- `docs/ASSIGNMENT_2_REPORT.md` — answers and evidence for Q1–Q7.
- `code/footprint_workflow.py` — local, synthetic footprinting workflow and source classification.
- `code/dns_workflow.py` — DNS record workflow using a reserved `.example` lab domain; optional AXFR is disabled unless explicitly enabled for a lab-owned DNS server.
- `code/validation_engine.py` — scope, freshness, duplicate and reliability validation.
- `code/hierarchy_traversal.py` — breadth-first traversal with scope/terminal boundaries.
- `data/*.csv` — synthetic prediction/observation and evaluation datasets.
- `diagrams/*.mmd` — editable Mermaid workflow diagrams.
- `images/q6-approach-comparison.svg`, `images/q7-redesign-comparison.svg` — charts embedded as SVG.

## Run
Python 3.9+; no third-party packages required.

```bash
python code/footprint_workflow.py
python code/dns_workflow.py
python code/validation_engine.py
python code/hierarchy_traversal.py
```

## Safety
All examples use synthetic records, reserved `.example` names and local data. No live target is queried. Do not run reconnaissance against real domains, people, networks or third-party services without explicit written authorization and a precise approved scope. Social-engineering activity is awareness analysis only; no real person is contacted or deceived.
