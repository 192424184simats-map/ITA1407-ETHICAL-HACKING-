# Security Finding Report

## Identification
| Field | Value |
|---|---|
| Finding ID | FIND-YYYY-NNN |
| Engagement ID | |
| Date/time discovered (with time zone) | |
| Reporter | |
| Asset ID (must be in scope) | |
| RoE version | |
| Status | NEW / TRIAGED / ACCEPTED / FIXED / VERIFIED / CLOSED |

## Finding
- Title:
- Summary:
- Affected component/version:
- Severity: CRITICAL / HIGH / MEDIUM / LOW / INFORMATIONAL
- CVSS vector/score (if assessed):
- Impact:
- Likelihood:
- Reproduction summary (lab/safe evidence only):
- Evidence reference (avoid secrets and personal data):
- Personal data involved or potentially exposed? YES / NO / UNKNOWN
- Credentials/secrets present in evidence? YES / NO

## Remediation
- Recommended fix:
- Compensating control:
- Owner:
- Target date:
- Verification plan:

## Handling gates
- [ ] Asset ID confirmed in signed RoE.
- [ ] Evidence minimised and stored in approved location.
- [ ] No credentials or personal data included in report.
- [ ] Legal/DPO escalation completed where necessary.
- [ ] Disclosure recipient verified.

## Structured record (example schema)
```json
{
  "finding_id": "FIND-2026-001",
  "engagement_id": "ENG-2026-001",
  "asset_id": "LAB-TARGET-01",
  "severity": "MEDIUM",
  "personal_data_involved": false,
  "status": "TRIAGED",
  "disclosure_due_date": "2026-12-23"
}
```

The disclosure layer consumes these fields. If personal_data_involved is true or unknown, keep handling private and escalate to the DPO/legal team.
