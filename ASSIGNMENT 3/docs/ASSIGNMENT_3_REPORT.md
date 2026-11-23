# ITA14 Ethical Hacking – Assignment 3
## CO3: Scan-Data Preparation and Pipeline

**Pair work:** N. Arun Kumar (192424184) and Abdul Samed K. (192426050)  
**Lab scope:** Isolated host-only network 192.168.56.0/24  
**Tools covered:** Nmap, fping, Bash, awk, sed, sort, join, comm, grep, grepcidr, datamash, sha256sum, diff, cmp and time.

> Authorization: scan only owned lab virtual machines in the authorized host-only subnet. Addresses outside 192.168.56.0/24 are out of scope and must be rejected.

## Q1 – Requirements and Scan-Data Architecture (6 Marks)

### 1.1 Requirements
The pipeline must discover live hosts, identify open TCP/UDP ports, detect service names and versions, estimate operating systems, and store enumeration findings for Windows SMB/NetBIOS, Android ADB, Java RMI, NetWare NCP and Symbian Bluetooth. Results must be correct, consistent, traceable to a scan session and reproducible.

### 1.2 Five datasets and schemas
| Dataset | Source | One row represents |
|---|---|---|
| hosts.csv | Nmap host discovery / fping | One host |
| ports.csv | Nmap TCP/UDP scan | One host, port and protocol |
| services.csv | Nmap service detection | One service on one port |
| os_versions.csv | Nmap OS detection | One OS guess per host |
| enum_findings.csv | Platform-specific enumeration | One finding per host |

Schemas:
- `hosts.csv`: ip, hostname, os_guess, status; primary key: ip.
- `ports.csv`: ip, port, protocol, state, service, version; primary key: ip+port+protocol.
- `services.csv`: ip, port, service_std, product, version; key: ip+port.
- `os_versions.csv`: ip, os_name, os_accuracy, device_type; key: ip.
- `enum_findings.csv`: ip, source_tool, finding_type, finding_value; key: ip+source_tool+finding_type.

The hosts table is the parent. Ports, OS versions and enumeration findings link to hosts by IP. Services link to ports by IP and port. The composite port key includes protocol because TCP/53 and UDP/53 are different records.

### 1.3 Enquiry questions
| ID | Question | Example pipeline |
|---|---|---|
| E1 | Which hosts have SMB (445) open? | Filter port 445 and state open |
| E2 | How many open ports does each host have? | Group open port rows by IP |
| E3 | Which services occur most often? | Count standardized service names |
| E4 | Are there duplicate host-port records? | Sort composite keys and use uniq -d |
| E5 | Which addresses are outside the authorized range? | Validate IPs against 192.168.56.0/24 |

Acceptance criteria: valid IPs within scope; ports 1–65535; state is open, closed or filtered; consistent service names and column order; every rejected row has a reason; outputs are timestamped/versioned; identical input produces identical content checksums.

## Q2 – Create and Validate Source Scan Datasets (7 Marks)

### 2.1 Collection commands
For an authorized lab only:
```bash
fping -a -g 192.168.56.0/24 2>/dev/null > live_hosts.txt
nmap -sn 192.168.56.0/24 -oG sweep.gnmap
nmap -sS -sV -O 192.168.56.101-106 -oX scan_full.xml -oG scan_full.gnmap
nmap -sU --top-ports 20 192.168.56.101-106 -oG udp.gnmap
```

The assignment's sample host inventory contains six devices:
| IP | Hostname | OS guess |
|---|---|---|
| 192.168.56.101 | kali-lab | Linux 5.x |
| 192.168.56.102 | win-srv01 | Windows Server 2016 |
| 192.168.56.103 | android-vm | Android 9 |
| 192.168.56.104 | java-rmi01 | Linux 4.x |
| 192.168.56.105 | netware01 | Novell NetWare 6.5 |
| 192.168.56.106 | symbian-bt | Symbian S60 |

### 2.2 Controlled defects
The exercise injects duplicate host/port rows, inconsistent service names, malformed/out-of-scope IP, port 65536 and a missing port. These test duplicate detection, normalization, scope enforcement and required-field validation.

### 2.3 Validation order
1. Check authorized subnet first because scope is an ethical/legal boundary.
2. Check required header and columns.
3. Validate IP octets and port range.
4. Detect duplicate composite keys (IP, port, protocol).
5. Normalize service names with a lookup map.

This order prevents malformed or unauthorized data from entering later merge/report stages.

## Q3 – Scan-Data Editing and Cleaning Module (7 Marks)

Reusable Bash functions validate IPs, normalize service names and clean port rows. A valid row must have a valid IPv4 address in 192.168.56.0/24, port 1–65535, tcp/udp protocol, valid state and a unique composite key. Invalid rows are written to a rejected CSV with a reason.

Assignment sample accounting: **16 input rows = 11 cleaned + 5 rejected**. Example rejection reasons include duplicate, malformed_ip, out_of_scope, port_out_of_range and missing_port.

Boundary tests: port 0 invalid; ports 1 and 65535 valid; port 65536 invalid; 192.168.56.255 valid; 192.168.56.256 invalid.

Automatic correction is appropriate for deterministic service aliases and harmless case/whitespace changes. Missing port values and out-of-range ports require manual review. Out-of-scope or malformed IPs are rejected and flagged.

Automated cleaning alone cannot establish whether a finding is true. A duplicate may represent a changed service between scans, and a parsing error may need analyst review. Keep rejected records, reasons, reconciliation counts and human review.

## Q4 – Scan-Result Reshaping with Melting and Casting (7 Marks)

The wide dataset has one row per host and one column per scanned port. Melting converts it to long format with columns `host,port,state`, where one row is one host-port observation. With 3 hosts and 6 ports, the long dataset must contain 18 data rows.

Casting summarizes the long data by host. The sample open-port totals are:
| Host | Open ports |
|---|---:|
| 192.168.56.101 | 3 |
| 192.168.56.102 | 2 |
| 192.168.56.103 | 1 |

Identifier: host. Dimension: port. Measured variable: state. Round-trip validation uses sha256sum and cmp; identical hashes and a successful cmp indicate that the transformation preserved the source data.

## Q5 – Multi-Stage Scan-Data Merging Strategy (6 Marks)

Join keys: IP for hosts↔ports, hosts↔OS versions and hosts↔enumeration; IP+port for ports↔services. Inputs must be sorted on the join key before using `join`.

| Join | Meaning |
|---|---|
| Inner | Only matching keys |
| Left | Every row from the left dataset |
| Full outer | All keys from both datasets |
| `join -v1` / `join -v2` | Unmatched records from one side |

The assignment example reports 10 matching rows and one unmatched port (192.168.56.107:443), giving 11 port records in total. A host without a ping response may need an authorized `-Pn` rescan. Reconcile row counts, inspect unmatched rows and check duplicate keys to verify joins.

## Q6 – Automated Scan-File Reading and Writing Pipeline (7 Marks)

The pipeline imports Nmap XML or grepable output into CSV, validates its header and fields, and exports versioned files using the pattern:
`subnet_scantype_YYYYMMDD-HHMMSS_vN.csv`.

Use `set -o noclobber` or a unique version number to avoid accidental overwrite. Store SHA-256 checksums. Read-back checks use `sha256sum -c`, `cmp`, `diff` and row counts to verify exported content.

Import status convention: 0 success, 2 missing/unreadable file, 3 header mismatch, 4 invalid data.

## Q7 – Reusable Scanning and Enumeration Function Library (10 Marks)

### Stage 1 – Function design
Student A's functions: `valid_ip`, `import_check`, `clean_ports` and `norm_service`. Student B's functions: `melt`, `cast`, `merge_tables` and `export_result`.

### Stage 2 – Integrated pipeline
The sample counts are 16 input port rows, 5 rejected and 11 cleaned. Host/port integration produces 10 matched rows and one unmatched port. Two runs on identical input should produce identical checksums.

### Stage 3 – Reporting
Report open ports per host and frequency per standardized service. Reconcile the sum of per-host counts with the number of open rows in the master table. Vulnerability checks and management reporting should identify exposed legacy services and recommend patching, disabling unnecessary services or restricting access with firewall rules. Perform these checks only in the authorized lab.

### Stage 4 – Stress test and optimization
The assignment reports a 5,000-row benchmark: a per-line grep loop took 5.79 seconds; a single awk pass took 0.02 seconds (about 290× faster in that VM). Actual timing varies by system. The improvement comes from avoiding a new grep process for every row. For very large files, an external sort-based deduplication or database pipeline may use less memory than a large awk array.

### Stage 5 – Redesign for changed requirements
- UDP scans require the key IP+port+protocol.
- UDP state may be open|filtered; do not count it as confirmed open.
- Add/retain device_type for new platform types.
- Preserve historical sessions with versioned files and a scan_id.
- Compare sessions with sorted IP lists and Nmap ndiff to find retained, missing, new and changed hosts.

### Stage 6 – Joint evaluation
A structured sequence is important: import → validate → clean → reshape → merge → export. Each stage depends on the guarantees of the previous stage. Modular functions improve correctness, maintainability and efficiency. Challenges include extra tests, error handling, storage and manual exception review. For very large data, changing Nmap formats or new protocols, a database or Python/pandas pipeline may be more suitable.

## Conclusion
A reliable scan-data pipeline enforces authorized scope, validates schemas and values, records every rejected row, produces reproducible checksums, uses modular parameterized functions, stores versioned results, documents tests and evolves as scan sources and protocols change.

## Contribution record
The submitted source document leaves the contribution table for the students to complete. Update it to reflect the work actually performed by each member before final submission.
