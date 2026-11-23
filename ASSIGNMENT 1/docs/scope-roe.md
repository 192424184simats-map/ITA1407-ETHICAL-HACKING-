# Scope and Rules of Engagement (RoE)

## Engagement details
- Engagement ID:
- RoE version:
- Requesting department:
- System owner:
- Engagement lead:
- Assessor(s):
- Approved window and time zone:
- Emergency-stop contact:

## In-scope assets
List exact asset IDs, hostnames/application names, owners, environments and permitted entry points. No wildcard or implied scope.

| Asset ID | System / environment | Owner | Allowed activity | Window |
|---|---|---|---|---|
| | | | | |

## Out-of-scope assets
- Any asset not explicitly listed above.
- Production databases and personal-data stores unless separately approved in writing.
- Third-party services without written permission from their owner.
- Public IPs, external domains, staff devices or student accounts not explicitly listed.
- Any host discovered incidentally that is not in the approved inventory.

## Permitted activities
Only activities expressly approved for this engagement. Default academic scope: documentation, passive review of supplied configurations, and safe checks against isolated lab targets. Any further method requires explicit written approval.

## Prohibited activities
- Denial-of-service or load/stress testing.
- Destructive changes, persistence, malware deployment or wiping.
- Credential theft, phishing or social engineering of real users.
- Accessing another system with discovered credentials.
- Copying/exfiltrating personal data or secrets.
- Testing unlisted assets or testing outside the approved window.
- Any live exploitation not explicitly authorized by the system owner and governance process.

## Safety and escalation
1. Stop on unexpected access, personal data exposure, service degradation or scope uncertainty.
2. Do not explore further to confirm an out-of-scope finding.
3. Notify engagement lead and system owner immediately.
4. Notify legal/DPO/security incident team where data or incident conditions require it.
5. Resume only after written authorization and updated RoE.

## Authorization verification
- Confirm Engagement ID and signed authorization.
- Verify all required approvers and assessor identities.
- Confirm asset identifiers against inventory.
- Confirm the RoE version and time window.
- If any check fails: mark HOLD; no testing.

## Acknowledgement
Assessor name/signature/date:  
System owner/signature/date:  
Governance approval/signature/date:
