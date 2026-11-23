"""Safe governance-rule simulator for Ethical Hacking Assignment 1.

This script validates fictional engagement records locally. It does not perform
network requests, scanning, exploitation, credential handling, or system access.
Run: python code/framework_demo.py
"""
from dataclasses import dataclass
from datetime import date
from typing import Iterable, Optional


@dataclass
class Engagement:
    engagement_id: str
    signed_authorization: bool
    system_owner_approval: bool
    ciso_approval: bool
    roe_approved: bool
    legal_review_complete: bool
    dpo_approval: bool
    personal_data_possible: bool
    approved_assets: tuple[str, ...]
    start_date: date
    end_date: date


def verify_authorization(record: Engagement) -> tuple[bool, list[str]]:
    """Return authorization validity and reasons; no external action is taken."""
    errors = []
    if not record.engagement_id.strip():
        errors.append("Missing Engagement ID")
    if not record.signed_authorization:
        errors.append("Written authorization is not signed")
    if not record.system_owner_approval:
        errors.append("System-owner approval is missing")
    if not record.ciso_approval:
        errors.append("CISO/delegated approval is missing")
    if not record.approved_assets:
        errors.append("No explicitly approved asset IDs")
    if record.start_date > record.end_date:
        errors.append("Engagement dates are invalid")
    return not errors, errors


def can_start_engagement(record: Engagement) -> tuple[bool, list[str]]:
    """Apply authorization, RoE and privacy gates."""
    valid, errors = verify_authorization(record)
    if not record.roe_approved:
        errors.append("Rules of Engagement are not approved")
    if not record.legal_review_complete:
        errors.append("Legal review is not complete")
    if record.personal_data_possible and not record.dpo_approval:
        errors.append("DPO approval is required when personal data may be present")
    return valid and not errors, errors


def is_asset_in_scope(asset_id: str, approved_assets: Iterable[str]) -> bool:
    """Exact match only; no wildcard or subnet inference."""
    return asset_id in set(approved_assets)


def disclosure_decision(finding: dict) -> tuple[str, list[str]]:
    """Return handling route from a structured, fictional finding."""
    reasons = []
    if finding.get("personal_data_involved") is not False:
        reasons.append("Personal-data status is true or unknown; keep report private and escalate")
        return "PRIVATE_ESCALATION", reasons
    if finding.get("credentials_present", False):
        reasons.append("Credentials must be removed and handled through secure incident process")
        return "PRIVATE_ESCALATION", reasons
    if not finding.get("asset_in_scope", False):
        reasons.append("Asset is not confirmed in the approved scope")
        return "HOLD_AND_ESCALATE", reasons
    return "COORDINATED_PRIVATE", ["Send only to the verified authorized owner"]


def main() -> None:
    demo = Engagement(
        engagement_id="ENG-DEMO-001",
        signed_authorization=True,
        system_owner_approval=True,
        ciso_approval=True,
        roe_approved=True,
        legal_review_complete=True,
        dpo_approval=True,
        personal_data_possible=True,
        approved_assets=("LAB-TARGET-01",),
        start_date=date(2026, 11, 23),
        end_date=date(2026, 11, 30),
    )

    allowed, reasons = can_start_engagement(demo)
    print("DEMO ENGAGEMENT:", demo.engagement_id)
    print("CAN START:", allowed)
    print("REASONS:", reasons or ["All governance gates passed (simulation only)."])

    for candidate in ("LAB-TARGET-01", "PROD-DB-01"):
        print(f"ASSET {candidate} IN SCOPE:",
              is_asset_in_scope(candidate, demo.approved_assets))

    sample_finding = {
        "asset_in_scope": True,
        "personal_data_involved": False,
        "credentials_present": False,
    }
    route, notes = disclosure_decision(sample_finding)
    print("DISCLOSURE ROUTE:", route)
    print("NOTES:", notes)

    print("\nBoundary test — missing signature:")
    demo.signed_authorization = False
    allowed, reasons = can_start_engagement(demo)
    print("CAN START:", allowed)
    print("BLOCK REASONS:", reasons)


if __name__ == "__main__":
    main()
