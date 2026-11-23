# ITA14 – Ethical Hacking
## Assignment 4: Web Application and Wireless Network Security Assessment
**Course Outcome:** CO4  
**Student:** N. Arun Kumar (192424184)

> **Evidence note:** This repository organizes the submitted assignment content. The source document contains explicit placeholders for screenshots, scan outputs, versions, dates and measured counts. Those fields must be completed from the student's own authorized lab evidence; this report does not claim those scans were run.

## Authorization and scope
Testing is limited to self-owned or explicitly authorized lab systems. The source assignment uses a local DVWA-style web application and an assessor-deployed wireless access point. Do not scan, associate with, deauthenticate, capture, or test networks belonging to others. Remove or hash identifiers for unrelated wireless networks before retaining survey data.

## Task 1 – Reconnaissance and information gathering
Use WHOIS, theHarvester and dnsenum for authorized domain information; Nmap for port/service/OS inventory; WhatWeb and wafw00f for application and WAF fingerprinting. Record the domain, DNS results, target IP, open ports, service versions, server/framework and WAF status. The sample asset table identifies HTTP/80, MySQL/3306 and SSH/22 as possible services; confirm which are actually exposed in the lab.

## Task 2 – Web server vulnerability scanning
Run Nikto only against the authorized lab application. Independently verify HTTP security headers using a request-header check. Triage each alert as confirmed, false positive or requiring manual confirmation. Prioritize outdated server components, plaintext HTTP and missing CSP, X-Frame-Options, X-Content-Type-Options and HSTS. If HTTPS is not enabled, document it as a transport-security gap rather than inventing TLS scan results.

## Task 3 – OWASP web application assessment
Use OWASP ZAP or Burp against the isolated DVWA lab. Manually verify SQL injection, reflected/stored XSS, broken access control, default credentials, verbose errors and directory listing. Map findings to OWASP Top 10 categories: A01 Broken Access Control, A03 Injection and A05 Security Misconfiguration. Record alert counts from the actual exported report; the source template leaves these counts blank.

## Task 4 – SQL injection verification
Use sqlmap only for detection/verification against the authorized lab parameter, with low test level/risk and without database dumping. Capture the request and output, confirm the DBMS and technique from actual tool output, and do not copy the source document's placeholder values as confirmed results. Remediation: parameterized queries/prepared statements, input validation as defence in depth, least-privilege database credentials and a suitably tuned WAF.

## Task 5 – Directory and sensitive-file enumeration
Use directory enumeration tools only on the lab application. Confirm whether candidate paths really expose sensitive data before classifying them. Remove backups and configuration files from the web root, deny access to dotfiles and backup extensions, and keep secrets outside the document root. Record actual response codes and compare tool coverage using measured results.

## Task 6 – Wireless reconnaissance
Perform a passive survey of the assessor's own access point. Use monitor mode and a survey tool only where lawful and permitted. Keep the capture window and lab AP details in the report; hash the lab BSSID in any shared copy and redact all unrelated SSIDs/BSSIDs. Compare survey tools on the same controlled capture and record observed channel, signal and encryption details.

## Task 7 – Wireless standards and authentication
Record the lab AP's 802.11 standard, frequency band, channel width, authentication and cipher from its beacon/capability information. Explain the security differences: WEP is obsolete and cryptographically weak; WPA2-PSK depends strongly on passphrase entropy; WPA3-SAE improves resistance to offline dictionary guessing. Check WPS status on the owned AP and disable it if not required. Do not infer the AP's mode or capabilities without evidence.

## Task 8 – WPA/WPA2 password audit
The source assignment describes a weak passphrase configured specifically on the student's own lab AP. Any handshake capture or password audit must be restricted to that AP and its consenting client devices. This repository intentionally does not include deauthentication, handshake-capture or password-cracking automation. Record the actual result and timing from a permitted lab demonstration, or mark the task not performed. Recommended controls: use a unique high-entropy passphrase of at least 14 characters, disable WPS and prefer WPA3-SAE or enterprise 802.1X where supported.

## Task 9 – Network protection
Apply a default-deny inbound firewall policy carefully on a test VM, preserving required management access to avoid locking yourself out. Compare before/after exposure using authorized local test results. Deploy Snort or Suricata on a lab interface, generate benign test traffic and inspect alerts. Tune noisy rules with documented thresholds/suppressions and verify that relevant detections still fire.

## Task 10 – Consolidated findings and recommendations
The source document lists these illustrative findings: outdated Apache/PHP, missing security headers, no WAF, SQL injection, XSS, broken access control, exposed configuration/backup paths, WPS enabled, weak WPA2 passphrase and noisy IDS rules. Treat them as candidate findings until verified in the lab.

### Prioritized remediation
1. Patch the web server and runtime to supported releases.
2. Enforce HTTPS and add CSP, X-Frame-Options, X-Content-Type-Options and HSTS.
3. Fix SQL injection with parameterized queries and XSS with context-aware output encoding.
4. Enforce server-side authorization on every object reference.
5. Remove exposed configuration/backup files and use least-privilege database accounts.
6. Disable WPS; use WPA3-SAE or enterprise authentication and a strong unique passphrase.
7. Maintain a default-deny firewall and review IDS rules and suppressions regularly.

### Residual risk
Patching and configuration hardening do not eliminate zero-day vulnerabilities, social engineering, rogue access points or novel attack patterns. Controls reduce exposure but do not guarantee security.

## Evidence checklist before final submission
- [ ] Insert WHOIS, theHarvester, dnsenum, Nmap, WhatWeb and wafw00f outputs.
- [ ] Insert Nikto, HTTP header and (if applicable) TLS evidence.
- [ ] Insert ZAP/Burp report and manual verification screenshots.
- [ ] Replace sqlmap placeholders with observed output; do not include dumped data.
- [ ] Insert directory-enumeration output and confirmed path details.
- [ ] Insert own-AP passive survey and Kismet comparison; redact unrelated networks.
- [ ] Fill wireless standard, band, channel width, WPS and encryption observations.
- [ ] Insert authorized lab password-audit evidence or state not performed.
- [ ] Insert firewall before/after and IDS alert/tuning evidence.
- [ ] Fill actual dates, Kali version, counts, timings and contribution record.
