# Assignment 4 – Web Application and Wireless Network Security Assessment

**Course:** ITA14 – Ethical Hacking  
**Course Outcome:** CO4  
**Student:** N. Arun Kumar (192424184)

## Contents
- `docs/ASSIGNMENT_4_REPORT.md` – organized report summary for Tasks 1–10
- `scripts/web_header_audit.sh` – checks HTTP security headers on a local lab target
- `scripts/parse_findings.py` – validates and summarizes a findings CSV
- `data/findings_register.csv` – assessment findings register template
- `data/wireless_lab_checklist.csv` – passive, own-AP-only wireless audit checklist
- `diagrams/assessment-workflow.mmd` – assessment workflow
- `diagrams/defence-architecture.mmd` – layered protective architecture
- `charts/findings-severity.svg` – illustrative severity distribution from the supplied report

## Safety and scope
Use only systems and wireless equipment you own or have explicit written permission to assess. The supplied scripts do not exploit vulnerabilities, dump databases, capture handshakes, transmit deauthentication frames, crack passwords, or scan third-party networks. The web header script defaults to `http://127.0.0.1/`.

## Run the safe helper scripts
```bash
chmod +x scripts/web_header_audit.sh
./scripts/web_header_audit.sh http://127.0.0.1/
python3 scripts/parse_findings.py data/findings_register.csv
```

## Before submission
The source assignment explicitly marks multiple screenshots, scan outputs, counts, dates, versions and measured results as placeholders. Replace those with evidence from your own authorized lab run. Do not submit illustrative values as measured results. Hash or redact wireless identifiers for networks that are not yours.