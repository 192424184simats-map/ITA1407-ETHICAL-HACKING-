# Assignment 3 – Scan-Data Preparation and Pipeline

**Course:** ITA14 Ethical Hacking  
**CO:** CO3 – Scan-Data Preparation and Pipeline  
**Group:** N. Arun Kumar (192424184) and Abdul Samed K. (192426050)

## Contents
- `docs/ASSIGNMENT_3_REPORT.md` – answers for Q1–Q7
- `scripts/scanlib.sh` – reusable validation, cleaning, reshaping, merging and export functions
- `scripts/run_pipeline.sh` – end-to-end sample pipeline
- `data/` – sample host, port, service, OS, enumeration and wide-format scan datasets
- `diagrams/` – data relationship and processing workflow diagrams
- `charts/` – SVG charts for cleaning and benchmark results

## Lab safety and scope
The assignment describes an isolated, host-only lab network: **192.168.56.0/24**. The included scripts process sample CSV data only. Any real scanning must be performed only against systems owned by the group and explicitly authorized for testing. The pipeline rejects addresses outside the stated subnet.

## Run the sample pipeline
From this directory on Kali Linux or another Bash environment:

```bash
chmod +x scripts/run_pipeline.sh
./scripts/run_pipeline.sh
```

The script writes cleaned and rejected records to `out/`, produces a long-format scan file and a host summary, and creates checksums. It does not launch Nmap or scan a network.

## Data note
The CSVs are representative lab examples based on the assignment's stated six-host and scan-data design. Replace them with authorized lab exports when reproducing the exercise.