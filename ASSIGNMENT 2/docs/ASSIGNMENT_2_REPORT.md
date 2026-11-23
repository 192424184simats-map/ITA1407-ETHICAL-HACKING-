# Assignment 2 — Evaluation and Engineering of Footprinting, Reconnaissance and Social-Engineering-Awareness Workflows

**Student:** N. Arun Kumar  
**Register Number:** 192424184  
**Course:** ITA14 Ethical Hacking · **CO2**  
**Total:** 50 marks

> **Safety boundary:** This report is a design and evaluation portfolio. All datasets are synthetic and all domain names use the reserved `.example` namespace. No real organization or person is queried, scanned, contacted or attacked. Real assessments require written authorization, explicit scope and owner-approved windows.

## Q1 — Evaluate and Engineer a Footprinting Strategy (8 marks)

### Strategy design
The strategy combines multiple sources because no single source gives a complete picture. Passive sources are used first; active DNS checks are limited to explicitly authorized lab-owned targets.

| Technique | Type | Information obtained | Reliability / limitation |
|---|---|---|---|
| WHOIS/RDAP lookup | Passive | Registrar, registration dates, name servers, privacy status | Privacy redaction can hide contacts; records may be stale |
| Search operators (`site:`, `filetype:`, `intitle:`) | Passive | Indexed pages and public documents | Index may be incomplete or outdated |
| Archived pages | Passive | Historical public pages and removed content | Historical data may no longer be valid |
| DNS A/MX/NS/TXT queries | Active information request | Hosts, mail exchangers, name servers, policy records | Caching, delegation and split-horizon affect results |
| Service/banner checks | Active | Service and version hints | Only within approved lab scope; banners may be misleading |

### Collection structure and scope hygiene
Each item is stored with `item_id`, `source`, `observed_at`, `asset_id`, `scope_status`, `confidence` and `evidence_ref`. In-scope verified facts are separated from out-of-scope, personal or unverified material. Out-of-scope data is rejected, not used to expand the target list.

### Four contrasting synthetic targets — prediction vs observation

| Target | Constructed condition | Prediction | Synthetic observation | Result |
|---|---|---|---|---|
| A | Well-protected | Minimal public metadata; no zone disclosure | Registrar metadata only; AXFR denied | Matches |
| B | Information-leaking | Public documents and verbose TXT hints | Public PDF metadata and exposed test TXT value | Matches |
| C | Misconfigured DNS | Stale A record and lab-enabled zone transfer | Stale record found; AXFR allowed in isolated mock dataset | Matches |
| D | Minimal footprint | Very little indexed information | NS/A records only; no archive entries | Matches |

### Source reliability and contradictions
WHOIS privacy protection is not evidence that a domain has no infrastructure. Archived pages can be outdated. DNS answers can be delegated or cached. A public document can refer to a retired hostname while current DNS points elsewhere. Therefore every item is timestamped and cross-checked; contradictions are recorded as uncertainty and trigger revalidation.

### Changed condition: 50 subdomains and third parties
The one-domain process is extended with batch ingestion, asset-ID allow-lists, deduplication, caching, prioritization and a separate third-party authorization register. Third-party services remain excluded unless written provider permission is documented. The strategy remains suitable at scale only with scope tagging and automated validation; manual review alone increases omissions and scope mistakes.

## Q2 — Build a Reliable DNS Footprinting Workflow (7 marks)

### Workflow
For a lab-owned domain only, retrieve A, MX, NS and TXT records using `dig` or `nslookup`; record resolver, timestamp, TTL and response. A zone-transfer test is a separate high-risk step and must remain disabled unless the DNS owner explicitly authorizes the exact server and lab zone.

Example command templates (replace only with an authorized lab-owned zone):
```bash
dig A lab.example
dig MX lab.example
dig NS lab.example
dig TXT lab.example
nslookup -type=A lab.example
```
AXFR is intentionally not run by the supplied script. If a lab instructor explicitly authorizes it, the owner may perform a controlled test against the lab DNS server only and record approval.

### DNS interpretation
- **Split-horizon:** external and internal resolvers may return different answers; external visibility does not reveal all internal records.
- **Delegation:** a child zone may be managed by another name server; record the delegation and verify whether that service is in scope.
- **Caching:** TTL and resolver cache can make records appear stale; compare authoritative answers and timestamps where authorized.

### Six synthetic DNS cases

| Case | Prediction | Synthetic observation | Interpretation |
|---|---|---|---|
| 1. Secured server | A/MX/NS/TXT; transfer denied | Published records only | Expected |
| 2. AXFR misconfiguration | Entire lab zone could be disclosed | Mock dataset marks transfer as allowed | High information exposure |
| 3. Stale record | Old host/IP remains visible | A record marked expired | Re-query and owner confirmation |
| 4. Split-horizon | External view omits internal records | Public resolver shows public-only record | Not evidence of missing internal hosts |
| 5. Delegated subdomain | Child NS answers separately | Delegated lab NS returned | Verify separate authorization |
| 6. Wildcard DNS | Random names may resolve | Synthetic wildcard response | Avoid false-positive host enumeration |

### Risk and countermeasure
A zone transfer can disclose a complete zone inventory rather than a few public records. Restrict transfers to approved secondary servers and use TSIG authentication where supported. Re-test only in the lab after owner approval. The redesigned analysis records transfer policy and response without treating a failed transfer as proof that the whole DNS environment is secure.

## Q3 — Competitive-Intelligence Awareness Utility (7 marks)

### Modular architecture
Public sources → documented query/operator → evidence item store → item-to-human-risk mapping → risk evaluation → awareness countermeasures. New sources and controls can be added as modules.

### Source operators (safe examples)
These are query templates for a fictional organization, not queries to run against real people:
- Job advertisements: `site:careers.example filetype:pdf`
- Annual reports: `site:example filetype:pdf intitle:"annual report"`
- Press releases: `site:example intitle:press`
- Public professional profiles: aggregate role-level public information only; do not harvest personal contact details.

### Item-to-technique mapping

| Public information category | Potentially enables | Awareness indicator | Countermeasure |
|---|---|---|---|
| Staff names and job roles | Spear-phishing / pretexting | Unexpected message using internal role language | Verify requests through known channels |
| Technologies/vendors in job ads | Fake IT/vendor pretext | Caller claims knowledge of internal tools | Vendor identity verification |
| Office locations / public building photos | Tailgating pretext | Unbadged person asks to follow staff inside | Challenge and report; never hold secure doors |
| Public phone numbers | Vishing | Urgent call asks for OTP or password | Never disclose OTPs; call back on official number |

### Synthetic organizations — prediction vs observation

| Organization | Public profile | Predicted risk | Synthetic result |
|---|---|---|---|
| RichOrg | Many public documents and role descriptions | High | High; multiple role/vendor clues |
| SparseOrg | Minimal public data | Low | Low; few actionable details |
| MisleadOrg | Old and inconsistent public records | Medium | Medium; stale details create false leads |

Staff-role information and job advertisements can create the strongest targeting context. This does not mean an attack is inevitable; it means the awareness programme should teach verification and reporting.

### Modular additions
1. Add a public press-release feed as a new source module.
2. Add a “verify before acting” rule and DMARC/SPF/DKIM awareness as countermeasures.

These additions do not change the workflow architecture. They improve source coverage and reduce the likelihood that staff trust a spoofed sender or urgent request.

## Q4 — Reconnaissance Data-Validation Mechanism (6 marks)

### Validation stages
1. **Scope:** exact asset ID must be on the approved allow-list; otherwise reject immediately.
2. **Deduplication:** repeated item fingerprint is dropped and linked to the original.
3. **Freshness:** expired or old item is recoverable and requires re-query.
4. **Reliability:** low-confidence or unverifiable source is held for confirmation; irrecoverable/unverifiable items are rejected.

### Test sequences — prediction vs observation

| Sequence | Inputs | Predicted | Observed |
|---|---|---|---|
| All-valid | In-scope, fresh, unique, reliable | Pass | Pass |
| Out-of-scope | Asset not allow-listed | Reject | Reject at first check |
| Stale | In-scope but expired | Recheck | Recheck |
| Duplicate | Same fingerprint twice | Keep one | Duplicate dropped |
| Mixed | Valid + stale + duplicate + out-of-scope | Pass/recheck/reject mix | Matches prediction |

### Ordering evaluation
Scope is the cheapest decisive boundary and must run first. Deduplication then reduces repeated work. Freshness and reliability checks are applied only to unique in-scope items. Redesigned order: **Scope → Deduplication → Freshness → Reliability**. This reduces unnecessary checks while preventing out-of-scope material from entering the evidence set.

### Scale
As targets grow from 1 to 50, input volume increases. Early scope and deduplication filters keep processing close to linear in the number of collected items. The validation script provides reproducible synthetic test outcomes.

## Q5 — Evaluate Footprinting of a Hierarchical Organization (7 marks)

### Representation
A footprint is modelled as a tree: parent domain → subdomains → departments → services. Every node has an explicit scope flag, terminal flag and children list.

### Traversal and boundary
Breadth-first search records each node. It does not expand a node if it is out of scope, terminal or has no public data. Empty branches are recorded as empty, not treated as errors.

Pseudocode:
```text
queue <- [root]
while queue not empty:
    node <- dequeue(queue)
    record(node)
    if not node.in_scope or node.terminal or node.has_no_public_data:
        continue
    enqueue(each child of node)
```

### Test structures

| Structure | Predicted nodes | Observed | Boundary result |
|---|---:|---:|---|
| Shallow: root + 3 leaves | 4 | 4 | All leaves terminal |
| Deep: 5 levels | 12 | 12 | Deep path completed |
| Irregular: uneven branches | 9 | 9 | Large branch fully covered |
| Empty branch | Count node, no expansion | Correct | Empty node stops cleanly |
| Out-of-scope child | Record boundary only | Correct | No child expansion |

Systematic traversal provides repeatable coverage and explicit stop conditions. Ad-hoc exploration may miss branches or continue into unauthorized third-party assets.

## Q6 — Evaluate Footprinting Approaches Under Constraints (7 marks)

### Approaches
- **A — Passive OSINT:** WHOIS/RDAP, public search results and archives. Produces a broad, low-noise overview.
- **B — Active DNS/service queries:** approved DNS record requests and lab-only service metadata. Produces more direct technical detail but creates traffic and requires stricter authorization.

### Quantitative scenario data

| Scope | Passive queries | Active queries | Interpretation |
|---|---:|---:|---|
| 1 domain | 6 | 9 | Both feasible |
| 10 subdomains | 14 | 40 | Active grows faster |
| 25 subdomains | 22 | 110 | Active is noisier |
| 50 + third-party services | 30 | 260 | Broad active collection is impractical and third-party scope is a concern |

### Redundancy and recommendation
Active queries may repeat similar checks across subdomains. Passive searches can also repeat documents. The quietest or fastest approach is not always best: a small authorized scope may justify targeted active checks for precision; a large scope should start with passive collection and then use targeted active checks only on prioritized, explicitly authorized assets. Teaching exercises should use synthetic data or isolated labs.

## Q7 — Integrated Review: Diagnose, Redesign and Defend (8 marks)

### A. Diagnose
Selected workflow: Q6 active DNS/service footprinting. At 50 subdomains the scenario generates about 260 queries. Repeated checks and lack of early deduplication are the main bottlenecks; scope-first filtering is also needed to prevent out-of-scope requests.

### B. Evaluation criteria
- Query count
- In-scope coverage
- Out-of-scope query count
- Source reliability
- Time/effort

### C. Redesign
1. Load the signed scope allow-list.
2. Normalize candidate hostnames.
3. Reject out-of-scope hosts.
4. Deduplicate remaining hostnames.
5. Query each unique approved host once.
6. Cache timestamped answers and re-use them within an approved freshness window.
7. Mark stale answers for controlled revalidation.

Trade-off: cache storage and implementation complexity increase, and cached data must expire correctly.

### D. Quantitative comparison

| Criterion (50-subdomain scenario) | Original | Redesigned |
|---|---:|---:|
| Query count | ~260 | ~95 |
| In-scope coverage | 100% | 100% |
| Out-of-scope queries | Several | 0 |
| Relative query reduction | — | ~63% |

The query reduction is ((260-95)/260 × 100 ≈ 63.5%), rounded to approximately 63%. These are assignment scenario values, not measurements from a live target.

### E. Final engineering judgment
Adopt the redesigned workflow for medium and large scopes because it maintains the scenario's 100% coverage while reducing query count and eliminating out-of-scope queries. The original simpler workflow may remain suitable for one or two hosts where cache overhead is not worthwhile.

## Conclusion
The final workflow is passive-first, scope-first and evidence-driven. It combines multiple information sources, interprets DNS carefully, translates public information into awareness controls rather than attacks, validates data before use, traverses organizational hierarchies with explicit boundaries and scales through deduplication and caching. The governing rule is: **no written authorization and no exact scope, no collection against a real target.**

## References / notes
- ITA14 Ethical Hacking Assignment 2 question paper and supplied model-answer/evaluation scheme.
- DNS concepts: A, MX, NS, TXT, TTL, delegation, split-horizon and zone-transfer controls.
- Search-operator syntax is demonstrated only with fictional `.example` domains.
- All quantitative tables are synthetic assignment scenario values; no live collection was performed.
