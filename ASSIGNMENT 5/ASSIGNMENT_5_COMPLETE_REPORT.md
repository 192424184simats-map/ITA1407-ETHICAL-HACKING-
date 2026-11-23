# ITA14 Ethical Hacking — Assignment 5
# Hacking Operating Systems and Applications

**Student:** N. Arun Kumar  
**Register Number:** 192424184

---

# Part A — Analytical Modeling & Algorithm Development (25 Marks)

## Task A1 — OS Vulnerability Assessment Workflow (7 Marks)

### A1.1 Assessment requirements

The assessment covers one Windows server (W1) and one Linux server (L1) at fixed IP addresses inside an isolated test VLAN.

| Requirement | Definition |
|---|---|
| Scope | Only W1 and L1. Other hosts, production networks, denial-of-service tests, social engineering, and copying real data are out of scope. |
| Authorization | Written permission from the asset owner identifying tester, Kali source IP, test window, emergency contact, and confirmation of snapshots/backups. |
| Rules of engagement | Nmap timing capped at T3; no brute force or account-lockout tests; no exploitation without separate written approval; encrypt evidence; stop if a service crashes. |
| Windows information | IP/hostname, OS and patch level, open ports, service versions, RPC, users/groups, SMB shares and permissions. |
| Linux information | IP/hostname, OS and patch level, open services, RPC, NFS exports, R-services, trust files, SUID and world-writable permissions. |
| Expected outputs | Nmap XML/text output, enumeration logs, GVM report, verification evidence, CVSS-rated findings register, remediation plan, executive summary. |

**Windows objective:** determine whether anonymous or low-privilege users can learn about or access the system through RPC, SMB null sessions, shares, or unpatched services.

**Linux objective:** determine whether unnecessary services, R-services, NFS exports, risky permissions, or vulnerable binaries create access or privilege-escalation risks.

**Client decision:** determine whether W1 and L1 are suitable for production as configured, which fixes come first, and whether deeper testing is authorized.

### A1.2 Tool selection and justification

| Tool | Target | Reason |
|---|---|---|
| Nmap and safe NSE scripts | Both | Host discovery, port/service/OS detection, and structured output using `-oA`. |
| enum4linux | Windows/Samba | Collects users, groups, shares, and policy information over RPC/SMB. |
| rpcclient | Windows | Manually confirms what RPC queries reveal, including anonymous access. |
| smbclient and smbmap | Windows/Samba | Lists shares and checks access permissions. |
| rpcinfo and showmount | Linux | Lists RPC programs and NFS exports. |
| OpenVAS/GVM safe checks | Both | Matches versions/configurations to known vulnerabilities and provides candidate CVSS ratings. |
| Metasploit check modules | Lab only | Used at verification stage after approval; exploitation is not a discovery method. |

**Rejected or limited choices:** avoid unrestricted Nmap `-A` and all-script scans because intrusive scripts can disrupt services; do not use Metasploit for routine discovery; do not rely on OpenVAS alone because it may miss configuration and logic issues; use OS-specific tools only where relevant.

### A1.3 Assessment workflow

1. **Information gathering:** review scope and asset list; use `nmap -sn` and light banner checks.
2. **Enumeration:** use `nmap -sV -O -sC` with safe scripts, then OS-specific tools such as enum4linux, rpcclient, smbclient, rpcinfo, and showmount.
3. **Vulnerability identification:** run GVM safe checks and only safe NSE scripts; obtain permission before scanning fragile services.
4. **Verification:** check versions and patches first; use a Metasploit check where suitable; exploit only with explicit written approval and a snapshot.
5. **Evidence:** save Nmap output, screenshots, command logs, timestamps, and file hashes.
6. **Hardening:** apply approved fixes and repeat the checks.

### A1.4 Windows weaknesses and possible attack path

| Weakness | Exposure | Kali check | Fix |
|---|---|---|---|
| Exposed RPC | Ports 135, 139, 445 can reveal service and domain information. | `nmap -p135,139,445 -sV TARGET`; approved RPC queries. | Firewall RPC/SMB to trusted networks and disable unused services. |
| Null sessions | Anonymous access may reveal users, groups, policy, and shares. | `rpcclient -U "" -N TARGET`; `enum4linux -a TARGET`; `smbclient -L //TARGET -N`. | Restrict anonymous access and SMB exposure. |
| Weak share permissions | Excessive permissions may expose configuration files or allow unauthorized writes. | `smbmap -H TARGET`; `smbclient`; safe share enumeration. | Apply least privilege and remove unnecessary broad access. |
| Unpatched services | A vulnerable service may permit compromise. | Version/patch check and GVM; approved vulnerability check only. | Apply vendor patches, disable obsolete protocols, retest. |

**Possible attack chain:** exposed SMB/RPC → anonymous user/share enumeration → discovery of an over-permissioned share → exposure of sensitive configuration or credentials → greater access. This is a possible scenario, not a claim that it occurred in the user's lab. Blocking anonymous access, restricting shares, and patching break links in the chain.

### A1.5 Linux weaknesses

| Weakness | Risk | Kali-based check |
|---|---|---|
| Unnecessary services | Each exposed service increases attack surface. | `nmap -sV -p- TARGET`; compare against approved service baseline. |
| R-services and trust files | rlogin/rsh/rexec and unsafe trust entries can allow passwordless access. | `nmap -p512-514 TARGET`; inspect `/etc/hosts.equiv` and user `.rhosts` only after authorized lab access. |
| NFS exports | Broad exports or unsafe root mapping may expose files. | `rpcinfo -p TARGET`; `showmount -e TARGET`. |
| Risky file permissions | SUID root or world-writable files may enable privilege escalation. | After authorized lab access: `find / -perm -4000 -type f`; `find / -perm -0002 -type f`. |
| Unsafe buffer-handling programs | Unsafe functions may cause memory corruption if protections are absent. | Review a self-built practice binary with checksec/GDB in the lab. |

### A1.6 Interpreting and communicating results

Treat a finding as confirmed only when a second independent source agrees, such as another tool, a manual check, or a vendor patch check. Linux vendors may backport fixes without changing the displayed version, so a banner match alone is weak evidence. Mark uncertain items as **unconfirmed**.

Start with CVSS technical severity, then consider asset value, reachability, existing controls, and attack-chain importance. Report finding ID, evidence, reproducible steps, severity, fix, and retest result. Give management a plain-language summary and prioritized actions.

## Task A2 — Optimizing a Weak Assessment Plan (5 Marks)

### A2.1 Limitations of the proposed plan

1. Blind, aggressive testing can crash fragile services, trigger lockouts, and create unnecessary traffic.
2. Uniform testing ignores differences between Windows, Linux, and individual services.
3. Recording only crashes or shells misses configuration weaknesses such as exposed shares, trust files, and unsafe NFS exports.
4. Screenshots without command output are difficult to reproduce.
5. Default-password lists and brute-force tests can lock accounts and are outside normal rules of engagement unless explicitly approved.

### A2.2 Redesigned enumeration strategy

| Objective | Kali tools and techniques |
|---|---|
| Discover hosts and services | `nmap -sn`, then a scoped `nmap -sS -sV -O -T3` scan saved with `-oA`. |
| Windows RPC, null sessions, shares | enum4linux, rpcclient, smbclient, smbmap, safe SMB NSE scripts. |
| Linux R-services and NFS | Nmap ports 512–514, rpcinfo, showmount, safe NFS NSE scripts. |
| File permissions | Read-only `find` checks after authorized lab access. |

Sequence: discover → identify OS → run OS-specific enumeration → identify candidate vulnerabilities → verify selected findings. Log every step.

### A2.3 Technique for each client objective

| Client question | Best technique | Reason |
|---|---|---|
| Can anonymous users list Windows users or shares? | enum4linux and rpcclient, cross-checked with smbclient. | Directly tests anonymous requests and is read-only. |
| Does Linux trust other hosts without a password? | Check ports 512–514, then inspect trust files in the lab. | Trust is a configuration fact; exploitation is unnecessary. |
| Is a reported vulnerable service really vulnerable? | Version/patch check, then module check; controlled exploit only on an approved snapshot. | Increases certainty and risk gradually and stops when enough evidence exists. |

### A2.4 Challenging a critical result that did not exploit

First verify the service version and vendor patch status. Consider Linux backported fixes and Windows build/hotfix levels. Next check whether the verification tool used the correct target, port, architecture, and service settings. A failed exploit alone does not prove a false positive. Downgrade a finding only when independent evidence supports that decision.

## Task A3 — Evaluating OS Hacking Tools and Techniques (5 Marks)

### A3.1 Tool suitability

| Requirement | Recommended tool | Why suitable | Alternative and risk |
|---|---|---|---|
| RPC enumeration | rpcclient / enum4linux on Windows; rpcinfo on Linux | Direct service-specific queries. | Nmap NSE or Impacket; read-only queries are low risk. |
| Null session and shares | smbclient -L -N and smbmap | Lists shares and anonymous permissions. | enum4linux/NSE; avoid write tests except with a disposable test file. |
| NFS exports | showmount and rpcinfo | Purpose-built export and RPC listing. | Nmap NFS scripts; mounting/writing has higher risk. |
| R-services trust | Nmap ports 512–514 and authorized trust-file inspection | Port scan shows exposure; file inspection confirms trust. | Avoid brute-force tools due to noise and lockout risk. |
| File permissions | find for SUID/world-writable files | Direct read-only inspection. | LinPEAS/Lynis provide context but may produce large output. |

### A3.2 Comparison of approaches

| Criterion | Dedicated tools | Nmap NSE | Metasploit auxiliary |
|---|---|---|---|
| Ease/customization | Flexible manual commands. | Repeatable scripts with arguments. | Consistent module interface, heavier setup. |
| Depth | High for a selected service. | Broad coverage, less depth per service. | Useful module-specific detail. |
| Evidence | Raw text needs tidying. | XML, grepable, and normal output via `-oA`. | Workspace data and exportable reports. |
| Suitability | Strong OS/service-specific checks. | Good first pass on both OSs. | Keep for approved verification. |

**Recommendation:** use Nmap NSE for the first pass, dedicated tools for confirmation, and Metasploit only for approved verification.

### A3.3 Is exploitation always needed?

No. A shell is not the only proof. Configuration evidence can prove an exposed NFS export, anonymous share, or unsafe permission. Exploitation can crash services, change data, and exceed authorization. Non-exploitative verification is preferable on production or business-critical systems.

## Task A4 — Evaluating Application Hacking Approaches (4 Marks)

| Application | Typical weakness | Suitable tools | Defensive controls |
|---|---|---|---|
| Messaging/SMTP | User enumeration, open relay, cleartext authentication, header leakage. | Nmap SMTP scripts, smtp-user-enum, swaks, Wireshark. | Disable VRFY/EXPN where appropriate, restrict relaying, require STARTTLS/authentication, remove internal header details. |
| Web | SQL injection, XSS, weak authentication, IDOR. | Nikto, OWASP ZAP, Burp Suite, sqlmap in lab only. | Parameterized queries, output encoding, strong session/access controls, input validation. |
| Android | Hard-coded secrets, insecure local storage, weak transport security, exported components. | apktool, jadx, MobSF, adb, Frida in lab. | No embedded secrets, encrypted storage, secure TLS, minimal exported components and permissions. |
| Database | Weak/default credentials, network exposure, excessive privileges. | Nmap service scripts, database client, configuration review. | Private binding, remove defaults, strong credentials, least privilege. |

### A4.1 Suitability of approaches

- Automated scanning is fast and broad for known issues but cannot judge business logic.
- Manual proxy testing is needed for authorization, session, and workflow logic flaws.
- Static Android analysis identifies code, permissions, and embedded secrets; runtime analysis checks actual behavior.
- Credential and configuration review is more reliable for database and mail account settings than exploit scanning alone.

### A4.2 Automated scanner versus manual proxy testing

Automated scans cover many pages quickly and repeatably but depend on signatures and may produce false positives. Manual testing is slower but can inspect authenticated workflows, authorization boundaries, and business logic.

### A4.3 Why 80 findings became 12 confirmed

Possible reasons include banner-based false positives, duplicate URLs, informational items, WAF/filter behavior, unauthenticated scans, and aggressive scanner settings. Group duplicates and manually replay high/medium findings in ZAP or Burp before reporting them as confirmed.

A scanner score measures generic technical severity, not business impact. A successful exploit proves a particular attack path worked, but not its likelihood, repeatability, or business cost. Security decisions need technical evidence and context.

## Task A5 — When an Automated Scan Is Insufficient (4 Marks)

### A5.1 Limitations of one GVM scan

| Issue | Why one scan may be insufficient |
|---|---|
| Null-session exposure | It may not show which users, shares, or permissions are exposed. |
| NFS trust | Risk depends on allowed clients, root mapping, and exported data. |
| Web logic flaws | Broken access control and workflow bypass need manual testing. |
| Insecure mobile storage | Requires static and runtime inspection of the app/device. |

A single scan can also produce false positives, miss business impact, and disturb fragile systems if configured aggressively.

### A5.2 Choosing assessment depth

Consider target criticality, disruption risk, false-positive likelihood, evidence required, written authorization/rules of engagement, and the selected depth.

1. Automated safe scan with Nmap and GVM.
2. Manual verification of high and medium findings using OS-specific tools, proxy replay, mobile analysis, or configuration review.
3. Controlled exploitation only in an approved lab snapshot when impact remains uncertain and exploitation adds useful information.
4. Escalate if personal data, production systems, scope violations, or unapproved steps are encountered.

### A5.3 What has been sacrificed?

A finding's business importance depends on reachability, asset value, operational impact, and likelihood. Scanner-only work misses logic/configuration issues and may misdirect remediation. Exploitation-only work is risky and unethical without need and authorization. A sound decision combines scanner coverage, manual confirmation, limited controlled exploitation, and business context.

---

# Part B — Implementation & Computational Investigation (25 Marks)

**Part B requirement:** implement → enumerate → verify → evaluate → compare → report. All active work must be completed in the student's own isolated lab. The items below are the required implementation and evidence structure; fill them with actual lab results.

## Task B1 — Enumerate and Assess Windows and Linux Targets (7 Marks)

### B1.1 Prepare the lab and gather information (2 marks)

Record:
- Written scope and authorization, including target IPs, tester/Kali IP, time window, emergency contact, and snapshot status.
- Lab topology diagram and VM snapshots.
- Host discovery and scoped Nmap port/service/OS detection.
- Live hosts, open ports, service versions, OS/likely patch level, unnecessary services, and targets needing deeper enumeration.
- Explain scan type, timing, scripts, and why each is appropriate for the lab.

**Evidence to attach:** Nmap XML and text output, screenshots, topology, and command log.

### B1.2 Implement enumeration (2 marks)

Record at least five distinct findings across Windows and Linux. Candidate checks include Windows RPC, null-session/user/share listing, share permissions, Linux NFS exports, R-services/trust files, and risky file permissions after authorized access.

For each finding, record:
1. Finding ID and target.
2. Exact command and tool version.
3. Output or screenshot filename.
4. Interpretation and impact.
5. Confirmation status: confirmed / unconfirmed / false positive.

### B1.3 Compare tool approaches (1 mark)

Run one authorized enumeration task with two tools and compare readability, depth, speed, risk, and suitability. Example: enum4linux versus smbclient/rpcclient, or Nmap NSE versus an auxiliary module.

### B1.4 Evaluate findings (2 marks)

Explain the most serious weaknesses and possible chains, false positives/unconfirmed items, unexpected observations, and what needs verification next. Tie each conclusion to collected evidence and the hardening plan.

## Task B2 — Controlled Exploitation and Hardening (5 Marks)

Use only findings from B1 and isolated lab targets. Verify one Windows and one Linux vulnerability, then fix and retest each. A deliberately vulnerable self-built buffer-overflow practice program is optional.

Before verification, record the predicted reliability, possible service crash/lockout/data change, required proof, and snapshot status.

### B2.1 Compare verification approaches (2 marks)

| Measure | Approach A — non-exploitative check | Approach B — controlled lab module |
|---|---|---|
| Reliability | Fill from actual verification. | Fill from actual verification. |
| Risk to target | Usually lower; document observed risk. | Higher; document observed risk. |
| Evidence produced | Version/configuration evidence. | Module check/output; do not invent results. |
| Time and skill | Record actual effort. | Record actual effort. |
| Production suitability | Prefer where sufficient. | Generally unsuitable without exceptional authorization. |

### B2.2 Investigate technique parameters (1 mark)

Change at least two parameters (for example target setting, payload choice, scan timing, or privilege level). Record original value, changed value, observed result, and risk difference. Do not use destructive payloads.

### B2.3 Challenge the technique (1 mark)

Controlled exploitation is inappropriate on a live business-critical server where a crash, lockout, or data change could interrupt service. Safer alternatives include version/patch checks, configuration review, authenticated non-exploitative checks, and testing a cloned snapshot.

### B2.4 Hardening decision (1 mark)

Apply one fix to each OS, repeat the exact check, and attach before/after evidence. Possible fixes include restricting anonymous SMB access/shares, patching a service, removing R-services, restricting NFS exports, or correcting file permissions. Recommend the fix that removes the greatest verified risk.

## Task B3 — Assess Applications in the Lab (8 Marks)

Use deliberately vulnerable or self-built lab applications: a mail server, DVWA/OWASP Juice Shop/bWAPP, a vulnerable Android app, and a MySQL/PostgreSQL lab database.

### B3.1 Web application assessment (2 marks)

Use Nikto, OWASP ZAP or Burp Suite and sqlmap in the lab only. Demonstrate at least three vulnerability classes, such as SQL injection, XSS, weak authentication, or IDOR. For each, attach request/response evidence and explain why it is vulnerable.

### B3.2 Messaging and database assessment (2 marks)

For SMTP, check user enumeration, open relay behavior, unencrypted authentication, and header leakage using suitable Nmap SMTP scripts, smtp-user-enum, swaks, and Wireshark in the lab. For the database, check service exposure, weak/default credentials, and excessive privileges. Record the defensive control for each verified issue.

### B3.3 Mobile application analysis (2 marks)

Use apktool, jadx, MobSF, and (in the lab) adb or Frida. Identify at least three issues, such as hard-coded secrets, insecure local storage, weak transport security, exported components, or excessive permissions. Explain user impact and attach the relevant static/runtime evidence.

### B3.4 Compare and validate findings (2 marks)

| Finding | Tool used | Evidence | CVSS/severity | Manually confirmed (Y/N) | Fix |
|---|---|---|---|---|---|
| Finding 1 | To complete | To attach | To assess | To complete | To recommend |
| Finding 2 | To complete | To attach | To assess | To complete | To recommend |
| Finding 3 | To complete | To attach | To assess | To complete | To recommend |

Compare automated results with manual confirmation. Identify at least one actual false positive or tool limitation and recommend an improvement.

## Task B4 — Reporting Results and Final Security Decision (5 Marks)

Use all verified B1–B3 findings to explain which systems are most at risk, what must be fixed first, and whether the environment is acceptable for deployment.

### B4.1 Assessment report (2 marks)

Include executive summary, scope/authorization, methodology/tools, findings with evidence and CVSS severity, risk rating, remediation steps, and prioritized action list.

### B4.2 Challenge one finding (1 mark)

Select a potentially misleading finding (for example, a scanner false positive, high CVSS with low business impact, or a finding not reachable from the internet). Re-check it in Kali and document whether the rating is confirmed or corrected.

### B4.3 Final security decision note (2 marks)

Answer using actual evidence:
- Which OS or application presents the highest risk?
- Which tool/technique gave the most useful evidence?
- What evidence supports the ranking?
- What are the assessment limitations?
- Would you recommend deployment after the fixes?

**Decision:** [Complete only after lab verification.]  
**Highest-risk asset:** [Evidence-backed asset/finding.]  
**Deployment recommendation:** [Accept / accept after remediation / do not accept], with justification.

---

# Consolidated submission checklist

- [ ] Part A analytical answers A1–A5 included.
- [ ] Part B scope, authorization, topology, and snapshots included.
- [ ] Windows and Linux Nmap outputs saved.
- [ ] At least five OS findings documented with commands and evidence.
- [ ] Two-tool enumeration comparison completed.
- [ ] One Windows and one Linux vulnerability verified, fixed, and retested in the lab.
- [ ] Two technique parameters compared.
- [ ] Web, SMTP, mobile, and database evidence attached.
- [ ] Application findings manually validated and severity assessed.
- [ ] False-positive/tool limitation discussed.
- [ ] Prioritized remediation and final security decision completed.

**Integrity note:** No live scan output, exploit result, screenshot, CVSS score, or successful remediation is asserted by this template. Enter only results that were actually observed in the authorized lab.
