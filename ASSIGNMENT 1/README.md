# Assignment 1 — Ethical Hacking Engagement Framework

**Course:** ITA14 — Ethical Hacking  
**Student:** N. Arun Kumar  
**Register Number:** 192424184  
**Title:** Design and Develop a Complete Ethical-Hacking Engagement Framework for a University's Authorized Security-Assessment Programme

## Repository contents
- `docs/ASSIGNMENT_1_REPORT.md` — all 11 assignment tasks and the integrated framework.
- `docs/authorization-form.md`, `scope-roe.md`, `finding-report.md`, `disclosure-record.md` — reusable engagement documents.
- `code/framework_demo.py` — safe, local governance-rule simulator (no network access or exploitation).
- `code/generate_chart.py` — recreates the Task 10 scalability chart.
- `data/scalability_metrics.csv` — assignment's small/large programme comparison values.
- `diagrams/*.mmd` — editable Mermaid diagrams for framework flow, authorization/disclosure, and isolated lab.
- `images/task10-scalability.png` — generated chart.

## Run locally
Requires Python 3.9+ and Matplotlib for the chart.

```bash
python code/framework_demo.py
pip install matplotlib
python code/generate_chart.py
```

The demo uses fictional records and only validates governance decisions. It does not scan, exploit, or connect to any system.

## Safety boundary
This is a design/documentation assignment. Practical security testing is permitted only in a separately authorized isolated lab. Do not point tools at university production systems, third-party systems, public IP addresses, or assets that are not explicitly listed in a signed authorization and Rules of Engagement.

## Notes on interpretation
The assignment's model answer provides example legal mappings, disclosure windows, and scalability measurements. These are reproduced as academic scenario assumptions, not legal advice or measured real-world performance. Confirm current law and institutional policy with the university's legal/DPO team before an actual engagement.
