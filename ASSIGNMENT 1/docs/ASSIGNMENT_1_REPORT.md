# Assignment 1 — Complete Ethical-Hacking Engagement Framework

**Student:** N. Arun Kumar  
**Register Number:** 192424184  
**Course Code:** ITA14  
**Course:** Ethical Hacking  
**CO1:** Apply foundational concepts of ethical hacking, hacker types, ethical principles, legal frameworks, and responsible disclosure.

## Scenario and objective
The university plans to assess approximately 20 systems and 50 staff initially, including the student portal, learning-management system (LMS), email service, and an authorized campus-network segment. The framework must scale to the whole university and support internal and external assessors. Some systems contain personal data. The design therefore makes written authority, explicit scope, legal/data-protection review, safe testing, auditable evidence, and coordinated disclosure mandatory.

No live exploitation is performed as part of this assignment. Hands-on testing is confined to an isolated lab.

---

## TASK 1 — Enquiry and framework blueprint

### 1.1 Engagement-governance requirements

| Area | Requirement | Governance response |
|---|---|---|
| Assets | Student portal, LMS, email, approved campus-network segment; approximately 20 systems initially | Maintain asset inventory with unique IDs and in-scope/out-of-scope tags |
| People | Management/CISO, department requester, system owner, internal testers, external assessors, legal team, DPO, staff and students | Define accountable approvers, operators, data custodians and escalation contacts |
| Activities | Reconnaissance, scanning and enumeration only where expressly permitted; lab testing; evidence recording; reporting | RoE allow-list and lab-only boundary; record every action |
| Data | Systems may hold personal or sensitive data | Data minimisation, no unnecessary extraction, secure evidence storage, DPO review |
| Timing | Agreed maintenance/testing windows | Start/end dates and emergency-stop procedure |
| Growth | Whole-university coverage and third-party assessors | Standard templates, delegated approval thresholds, assessor vetting and audit trail |

### 1.2 Framework blueprint

`diagrams/framework-flow.mmd` contains the editable end-to-end diagram. The operating sequence is:

**Request → written authorization → scope/RoE → legal and privacy check → threat model → isolated-lab validation → finding record → coordinated disclosure → remediation verification → closure.**

A governance record links all stages using a unique Engagement ID. Each finding links back to the engagement, asset, authorization, RoE version, legal review and disclosure record.

### 1.3 Enquiry questions
1. Who can authorize an assessment, and how is the signed approval verified?
2. Which asset IDs and techniques are in scope, and how are out-of-scope requests blocked?
3. Which Indian legal and data-protection obligations apply when personal data may be encountered?
4. How are findings reported, assigned, remediated and disclosed without exposing users?
5. What controls are required for external assessors and continuous assessment?

### 1.4 Acceptance criteria
- **C1:** No engagement starts without verified written authorization.
- **C2:** Scope is explicit, versioned and checked against the asset inventory.
- **C3:** Each legal/privacy obligation maps to a named control and approver.
- **C4:** Production harm is prevented; hands-on testing remains inside the isolated lab.
- **C5:** Findings use a standard report and a defined coordinated-disclosure workflow.
- **C6:** Every approval, action, finding and status change is auditable.
- **C7:** The process supports external assessors and growth without weakening controls.

**Rationale:** These criteria directly address unauthorized access, unclear scope, personal-data exposure, disruption, poor disclosure coordination and future scale.

---

## TASK 2 — Hacker threat model and classification

### 2.1 Classification table

| Actor type | Typical motivation | Typical capability | Likely university target |
|---|---|---|---|
| White-hat | Improve security with permission | High; disciplined and scoped | Explicitly authorized systems |
| Black-hat | Financial gain, theft or damage | Medium to high; malicious | Student records, credentials, email |
| Grey-hat | Curiosity or recognition without permission | Variable; may identify weaknesses | Exposed portal or services |
| Script kiddie | Thrill, attention or experimentation | Low; relies on ready-made tools | Easy-to-find exposed services |
| Hacktivist | Political or social message | Variable; disruption or defacement | Public-facing website |
| Insider | Grievance, personal gain or misuse of access | Medium to high; legitimate access can be abused | Internal applications, HR/finance data |
| State-sponsored | Espionage or strategic advantage | High; persistent and stealthy | Research data and sensitive records |

### 2.2 Classification criteria
Classify an observed actor using four attributes:
1. **Authorization:** written permission present or absent.
2. **Intent:** benign, negligent, opportunistic or malicious.
3. **Capability:** low, medium or high.
4. **Affiliation:** internal, external, organized group or state-linked.

Do not infer identity from a single technical action. Record evidence and uncertainty.

### 2.3 Borderline actor
**Case:** A student discovers a portal weakness without permission and reports it without accessing further data.

- **Alternative A — Script kiddie:** possible if the student only ran an automated tool and demonstrated little understanding.
- **Alternative B — Grey-hat:** fits the unauthorized discovery combined with apparently non-malicious intent and subsequent reporting.
- **Chosen classification:** Grey-hat, provisionally. The absence of authorization is decisive; the responsible report does not retroactively authorize the activity. If the actor threatens the university or seeks payment through coercion, reassess intent and potential black-hat behaviour.

---

## TASK 3 — Ethics and code-of-conduct module

### 3.1 Ethical principles
- **Written authorization:** verify the signed approval and Engagement ID before any assessment activity.
- **Agreed scope:** interact only with asset IDs, methods and time windows listed in the approved RoE.
- **Confidentiality:** protect credentials, personal information, findings and system details.
- **Integrity:** preserve original evidence, timestamps and hashes where appropriate; do not alter logs or evidence.
- **Avoid harm:** use least-intrusive methods; avoid service disruption and unnecessary data access.
- **Honest reporting:** report successes, failures, limitations and uncertainty accurately.
- **Data minimisation:** do not copy or retain personal data unless a separately approved, strictly necessary procedure exists.
- **Accountability:** log actions and promptly report mistakes, unexpected access and scope issues.

### 3.2 Preventive checks and decision rules
1. **Pre-flight gate:** missing or invalid authorization → deny start.
2. **Scope gate:** target not on the current approved asset list → block, stop and escalate.
3. **Method gate:** prohibited technique or out-of-window activity → block.
4. **Data gate:** unexpected personal data → stop interaction, do not copy, notify the engagement lead and DPO.
5. **Evidence gate:** record only minimum necessary proof in the approved evidence store.
6. **Dual control:** require a second approver for sensitive or high-impact actions where the RoE permits them.
7. **Emergency stop:** any suspected service impact, accidental access or control failure → halt and notify the named contact.

### 3.3 Scenario test cases

| Scenario | Classification | Required response |
|---|---|---|
| Test an approved lab target during the agreed window using permitted checks | Acceptable | Proceed and log the activity |
| A permitted scan reveals an unlisted host | Borderline | Stop interaction; do not enumerate it; report it for a scope decision |
| Reuse discovered credentials on another service or copy student records | Unacceptable | Stop immediately, preserve minimal evidence, escalate to governance/DPO; no further access |
| A tester notices that a lab VM is bridged to the production network | Unacceptable condition | Stop the test, isolate the lab, report and revalidate configuration before restarting |
| Tester finds a critical weakness and wants to post screenshots publicly | Unacceptable | Use private coordinated disclosure; remove personal data and sensitive details from evidence |

### 3.4 Trust and professionalism
The module creates predictable boundaries and makes the tester accountable. It protects the university and data subjects by ensuring that technical capability is not treated as permission. It also gives testers a safe route to pause and report unexpected conditions without improvising.

---

## TASK 4 — Legal-compliance mapping

> **Academic mapping only:** Legal provisions and penalty descriptions below follow the supplied assignment's model-answer outline. They are not a complete or current legal opinion. The university legal team/DPO must validate applicability, amendments, rules and exact penalties before an actual engagement.

### 4.1 Mapping table

| Risk / obligation | India: IT Act, 2000 (assignment mapping) | International comparison | Framework control |
|---|---|---|---|
| Unauthorized access, copying or damage | Section 43 | CFAA, 18 U.S.C. §1030 (e.g., unauthorized access provisions) | Signed authorization, scope allow-list, no out-of-scope interaction |
| Dishonest or fraudulent computer-related acts | Section 66 | CFAA, 18 U.S.C. §1030 | Approval verification, activity logs, incident escalation |
| Identity theft / personation | Sections 66C and 66D | U.S. identity-theft provisions; CFAA may apply depending on facts | No credential reuse, controlled test accounts, identity/data handling rules |
| Breach of confidentiality / disclosure | Sections 72 and 72A | Privacy/confidentiality rules depend on jurisdiction | NDA, least-privilege access, encrypted evidence store, limited recipients |
| Sensitive personal data protection | Section 43A (as referenced by the supplied model answer) and applicable data-protection framework | Not a direct CFAA equivalent | DPO review, data minimisation, retention limit, breach escalation |

### 4.2 Offence and penalty notes
The supplied model-answer table gives indicative penalties such as compensation under Section 43, up to three years/fine for some Section 66/66C/66D offences, and up to two–three years/fine for confidentiality provisions. Exact penalties depend on the specific provision, facts, amendments and applicable rules; do not rely on these indicative figures for operational decisions.

### 4.3 Personal-data decision
When a system may contain personal data, the engagement must apply both the unauthorized-access controls and the relevant privacy/data-protection obligations. The DPO/legal team must review purpose, lawful basis, data categories, access limits, storage, retention, transfer and incident handling. The default is **no production personal-data extraction**. If personal data is unexpectedly encountered, stop, minimise evidence and escalate. The supplied assignment also references the DPDP Act 2023; confirm current commencement and applicable obligations with counsel before an engagement.

---

## TASK 5 — Scope and Rules of Engagement (RoE)

### 5.1 Scope definition

**In scope (only when asset IDs are listed in the signed engagement):**
- Student portal application endpoints designated by the owner.
- LMS test instance or explicitly authorised components.
- University email test tenant or approved components.
- Specifically identified campus-network segment and lab endpoints.

**Out of scope by default:**
- Live production databases and personal-data stores unless separately and explicitly approved.
- Third-party hosted services without written provider permission.
- Unlisted IP addresses, domains, accounts, devices and cloud resources.
- Denial-of-service, destructive testing, persistence, malware deployment, credential harvesting, social engineering of real staff, data exfiltration and lateral movement.
- Any activity outside the approved window.

### 5.2 Rules
- A signed authorization must identify requester, system owner, assessor, asset IDs, methods, dates, time zone, emergency contact and approvers.
- The governance team verifies signature/identity and records a unique Engagement ID.
- The asset inventory is the source of truth. Unknown asset → deny and escalate; never assume adjacency implies authorization.
- Testing occurs only in the named window. An extension requires renewed approval.
- Use dedicated test accounts and synthetic data whenever possible.
- Stop immediately on service degradation, unexpected access to personal data, or scope ambiguity.
- Escalation order: tester → engagement lead → system owner/CISO → legal/DPO/security incident team as relevant.

### 5.3 Pre-engagement checklist
- [ ] Authorization signed, identity verified and Engagement ID recorded.
- [ ] System owner approval and tester identity confirmed.
- [ ] Asset list and RoE version frozen and checked.
- [ ] Out-of-scope assets and prohibited methods communicated.
- [ ] Testing window and emergency-stop contact confirmed.
- [ ] Legal/privacy review and DPO decision recorded where needed.
- [ ] Lab isolation verified; no route to production or public internet.
- [ ] Evidence storage, retention and disclosure contacts agreed.

---

## TASK 6 — Authorization and responsible-disclosure layer

### 6.1 Authorization workflow
**Request → governance review → system-owner approval → legal/DPO review → signed authorization → Engagement ID issuance → RoE lock → execution → closure.**

No signature or missing approver means the request remains **PENDING** and testing cannot start.

### 6.2 Approval/status operations
The safe local simulator in `code/framework_demo.py` implements:
- `verify_authorization(record)`: checks required approval fields.
- `is_asset_in_scope(asset_id, approved_assets)`: enforces explicit asset membership.
- `can_start_engagement(record)`: requires authorization, RoE and privacy gates.
- `disclosure_decision(finding)`: chooses private coordinated disclosure or escalation.

All records in the demo are fictional. It performs no network activity.

### 6.3 Coordinated disclosure process
1. Tester creates a structured finding report with asset, impact, severity, evidence and recommended remediation.
2. Engagement lead validates that the finding is in-scope and evidence contains no unnecessary personal data.
3. Report privately to the authorized system owner/security contact.
4. Agree a remediation plan and target date; track status and communications.
5. Retest only under the original or updated authorization.
6. Close after remediation is verified or an accepted risk is documented.

**Scenario timing:** The supplied assignment model uses 90 days for normal findings and 30 days for critical findings. For the changed requirement in Task 11 it proposes 30 days and 7 days for critical findings. These are framework targets for the assignment, not universal legal deadlines; adopt dates through a risk-based policy and owner agreement.

### 6.4 Disclosure model comparison

| Model | Description | Benefits | Risks / limitations | University position |
|---|---|---|---|---|
| Coordinated disclosure | Private report, remediation coordination, controlled later communication | Reduces user exposure and supports remediation | Requires responsive owner and time tracking | Default |
| Full disclosure | Details published publicly, often immediately | Creates public pressure and awareness | Can enable exploitation before a fix; may expose personal or sensitive information | Exceptional, legal-approved only |
| Bug bounty | Pre-authorized testing under programme rules, usually with reward | Clear scope and researcher channel | Requires budget, triage and strict programme conditions | Possible future extension |

### 6.5 Decision rules
- Default to coordinated/private disclosure.
- Personal data, credentials, exploitable details or unresolved legal questions → keep private and escalate to the authorized owner, legal/DPO and relevant authority under applicable policy.
- Consider limited public communication only after risk/legal review, remediation opportunity and confirmation that personal data and operational secrets are excluded.
- Never publish raw evidence, credentials or personal data.
- The supplied model answer names CERT-In for relevant personal-data/security reporting; the responsible team must confirm the applicable reporting trigger, recipient and deadline.

---

## TASK 7 — Isolated ethical-hacking lab

### 7.1 Lab topology
See `diagrams/isolated-lab.mmd`.

| Component | Role | Example address |
|---|---|---|
| Kali Linux VM | Authorized tester workstation | 192.168.56.10/24 |
| DVWA or other intentionally vulnerable target VM | Training target only | 192.168.56.20/24 |
| Host-only virtual switch | Private VM-to-VM network | 192.168.56.0/24; no gateway |

Use synthetic accounts/data. Disable bridged mode and remove any second adapter that would provide a path to production or the public internet.

### 7.2 Safe verification operations
**Operation 1 — Configuration inspection:** On each VM, inspect network interfaces and routes using the operating system's local network-configuration display (for example, `ip address` and `ip route`). Confirm both VM addresses belong to 192.168.56.0/24 and that no default route points outside the host-only segment.

**Operation 2 — Lab connectivity:** From the Kali VM, verify that the specifically assigned target VM at 192.168.56.20 is reachable. Record the timestamp and result. Do not substitute a different host or scan an external network.

**Operation 3 — Evidence record:** Save VM names, adapter mode, MAC/IP addresses, virtual-switch name, snapshot IDs, date and operator into a configuration record. Capture screenshots of the hypervisor network settings.

### 7.3 Host-only vs NAT

| Aspect | Host-only (chosen) | NAT |
|---|---|---|
| Internet connectivity | None by design | Usually outbound connectivity via host |
| Exposure risk | Lower when configured correctly | Higher because traffic can leave |
| VM-to-VM training | Supported | Supported |
| Suitability | Preferred for contained practical tests | Less suitable when strict isolation is required |

**Choice:** Host-only, with no gateway and no bridged adapter. Validate the actual virtual-machine configuration; the label alone is not proof of isolation.

---

## TASK 8 — Reusable document library

The following templates are provided as standalone files in `docs/`:
1. **Authorization Form** — Engagement ID, requester, owner, assessor, assets, dates, approvals and signatures.
2. **Scope/RoE Form** — in-scope and out-of-scope assets, methods, windows, prohibitions and escalation.
3. **Finding Report** — finding ID, asset ID, severity, evidence reference, impact, remediation and status.
4. **Disclosure Record** — report date, recipient, target window, communication log, status and closure.
5. **Pre-engagement Checklist** — derived from the RoE.

### 8.1 Structured integration
A finding report exports a structured record containing `finding_id`, `engagement_id`, `asset_id`, `severity`, `personal_data_involved`, `status` and `disclosure_due_date`. The disclosure layer reads this record and enforces private handling when personal data is involved. The Task 10 metric process counts the number of findings and disclosure workflow steps.

### 8.2 Input tests

| Test input | Class | Expected result |
|---|---|---|
| Complete authorization with verified signatures and asset list | Valid | Accept; issue Engagement ID |
| Authorization missing one approver signature | Boundary | Hold as pending; do not start |
| No authorization record | Invalid | Reject before any activity |
| Finding references an asset not listed in the RoE | Invalid | Quarantine record and escalate; do not disclose as an authorized finding |
| Finding includes personal-data flag | Boundary/high-risk | Private handling; notify DPO and minimise evidence |

---

## TASK 9 — Integration, walkthrough and refinement

### 9.1 Integrated workflow
Authorization → RoE → legal/privacy review → threat model → isolated lab → finding report → disclosure → remediation verification → closure.

### 9.2 Walkthrough
A department requests an assessment of a student-portal test component. Governance checks the request and system-owner approval, legal/DPO reviews any personal-data implications, and a signed authorization creates an Engagement ID. The RoE identifies the exact test asset and time window. The lab uses a host-only network and a deliberately vulnerable training target. A simulated finding is recorded in the structured report, privately sent to the system owner, assigned a remediation target, retested under authorization and closed after verification.

This walkthrough is a governance simulation; it does not perform SQL injection or access a live university portal.

### 9.3 Systematic test cases

| Test | Expected behaviour |
|---|---|
| Missing authorization | Reject before any assessment activity |
| Target not in approved asset inventory | Block and escalate for a scope decision |
| Personal-data system has no DPO/legal approval | Hold engagement; no testing |
| Disclosure target date passes without remediation | Escalate to owner and governance lead; review risk and communication plan |
| Lab has bridged/network route to production | Stop immediately; isolate and revalidate before restart |

### 9.4 Refinements
- Manual scope checking was vulnerable to mistakes → use asset IDs and explicit allow-list checks.
- Disclosure timing was ambiguous → record severity-based target dates and escalation.
- Third-party assessors increase risk → require vetting, NDA, least privilege and full logging.
- Lab isolation could be misconfigured → add pre-flight route/adapter verification and a recorded configuration snapshot.

---

## TASK 10 — Scalability and governance evaluation

### 10.1 Scenarios and sample measures
The supplied assignment's model answer gives the following scenario values. Treat them as illustrative evaluation inputs, not measured production data.

| Process | Small programme | Large programme |
|---|---:|---:|
| Scope | 5 systems; 2 internal testers | About 200 systems; 20 internal + 10 external testers |
| Approval turnaround | About 4 hours | About 36 hours |
| Scope coverage | 100% | 82% |
| Disclosure workflow steps | 5 | 9 |

The chart `images/task10-scalability.png` visualizes the three process measures. Note that the chart uses the given units; approval turnaround and workflow-step counts are not percentages.

### 10.2 Interpretation and governance changes
At larger scale, approval time and disclosure workflow complexity increase, while scope coverage falls. Introduce delegated approval thresholds for low-risk assessments, parallel legal/DPO and system-owner review, standardized external-assessor onboarding, risk-based scheduling and automatic reminders. Preserve central review for high-risk systems and any engagement involving personal data.

---

## TASK 11 — Changed requirement and framework defence

### 11.1 Changed requirement
The university moves to continuous and third-party assessments, stricter data-protection controls and shorter disclosure timelines.

### 11.2 Retain / modify / replace / redesign

| Action | Component | Change |
|---|---|---|
| Retain | Written authorization and RoE | Keep mandatory authorization and explicit scope |
| Retain | Isolated lab | Maintain host-only testing for hands-on work |
| Modify | Disclosure | New target window: 30 days normal and 7 days critical, subject to owner/legal policy |
| Modify | Legal/privacy mapping | Add current data-protection review and DPO checkpoints |
| Modify | Third-party onboarding | Verify credentials, NDA, insurance/contract terms, least-privilege accounts and audit requirements |
| Replace | Manual logging | Use an approved workflow/ticketing system with immutable audit history |
| Redesign | One-off process | Use a continuous assessment pipeline with recurring scope/authorization renewal and risk-based scheduling |

### 11.3 New External-Assessor Governance Module
Before access, each external assessor must complete identity and qualification checks, contract/NDA sign-off, conflict-of-interest declaration, scope briefing, account provisioning with least privilege and start/end-date controls. All actions and approvals are logged. Access is revoked at engagement close. The module connects to the authorization workflow and RoE; no external assessor bypasses internal controls.

### 11.4 Evidence-based defence
The Task 9 walkthrough demonstrates that the request, approval, lab, finding and disclosure stages connect. Task 10 shows the governance bottlenecks at scale and supports delegated/parallel review. Task 4 identifies legal/privacy checks, while Task 6 provides coordinated disclosure and short-window tracking.

### 11.5 Remaining trade-offs and future work
- Shorter remediation targets can pressure system owners and may not be feasible for complex fixes; use risk-based temporary mitigations and escalation.
- Continuous and third-party reviews add coordination, cost and monitoring overhead; automate low-risk workflow steps but retain human approval for sensitive cases.
- A host-only lab improves containment but does not reproduce every production condition; use approved synthetic test environments and document the gap.
- Future work: integrate asset inventory, ticketing, evidence storage and risk dashboards; periodically review laws, policy and assessor controls.

---

## Conclusion
The proposed framework treats ethical hacking as a governed engagement rather than a tool exercise. Written authorization and explicit scope establish permission; legal/privacy mapping and the code of conduct set boundaries; an isolated lab contains practical work; structured findings and coordinated disclosure support remediation; and audit, scalability and external-assessor controls make the programme extensible. Its central rule is **no verified authorization, no testing**.

## References and validation note
- Supplied ITA14 Ethical Hacking Assignment 1 question paper and model-answer/evaluation pages.
- Information Technology Act, 2000 and associated rules, as referenced in the question paper.
- Digital Personal Data Protection Act, 2023, as referenced in the question paper.
- U.S. Computer Fraud and Abuse Act, 18 U.S.C. §1030, as referenced in the question paper.

This submission is an academic framework, not legal advice. Validate current statutory status, commencement, penalties and reporting obligations with qualified university counsel and the DPO before real-world use.
