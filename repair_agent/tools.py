import json
import re
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parent.parent / "data"

ISSUES = json.loads((DATA_DIR / "troubleshooting.json").read_text())
_COST_DATA = json.loads((DATA_DIR / "costs.json").read_text())
SUPPORTED_APPLIANCES = sorted({i["appliance"] for i in ISSUES})


# 1. loading data and the first tool.
def analyze_symptoms(appliance: str, symptoms: str) -> dict:
    """Match symptom keywords to likely issues for one appliance. Returns ranked candidates."""
    appliance = appliance.lower().strip()
    if appliance not in SUPPORTED_APPLIANCES:
        return {"error": f"Unsupported appliance '{appliance}'. Supported: {SUPPORTED_APPLIANCES}"}

    text = symptoms.lower()
    candidates = []
    for issue in ISSUES:
        if issue["appliance"] != appliance:
            continue
        hits = [s for s in issue["symptoms"] if s in text]
        if hits:
            candidates.append({
                "issue_id": issue["issue_id"],
                "issue": issue["issue"],
                "matched_symptoms": hits,
                "score": round(len(hits) / len(issue["symptoms"]), 2),
            })
    candidates.sort(key=lambda c: c["score"], reverse=True)
    return {"appliance": appliance, "candidates": candidates}



# 2. knowledge and cost lookups
def get_repair_guidance(issue_id: str) -> dict:
    """Return safe steps and technician criteria for one issue_id."""
    for issue in ISSUES:
        if issue["issue_id"] == issue_id:
            return {
                "issue_id": issue_id,
                "issue": issue["issue"],
                "safe_steps": issue["safe_steps"],
                "call_technician_if": issue["call_technician_if"],
            }
    return {"error": f"Unknown issue_id '{issue_id}'"}


def estimate_repair_cost(issue_id: str) -> dict:
    """Return DIY and professional cost ranges for one issue_id."""
    cost = _COST_DATA["costs"].get(issue_id)
    if cost is None:
        return {"error": f"No cost data for issue_id '{issue_id}'"}
    return {"issue_id": issue_id, "currency": _COST_DATA["currency"], **cost}


# 3. the safety checker
SAFETY_RULES = [
    (r"gas (smell|leak)|smell.*gas", "stop",
     "Possible gas leak. Leave the area, avoid switches and flames, and call your gas emergency service."),
    (r"smoke|spark|burning|melt", "stop",
     "Possible electrical fire risk. Cut power at the breaker if safe and call a technician."),
    (r"water.*(outlet|socket|wiring)|(outlet|socket|wiring).*water", "stop",
     "Water near electrics is a shock risk. Do not touch; cut power at the breaker."),
    (r"bypass|jumper|disable.*(safety|thermostat|fuse)", "stop",
     "Bypassing safety components is unsafe. Do not do this."),
    (r"refrigerant|freon", "caution",
     "Refrigerant must only be handled by a licensed technician."),
    (r"(open|remove).*(back panel|cover|casing)", "caution",
     "Unplug the appliance first and never open sealed electrical parts."),
]


def check_safety(text: str) -> dict:
    """Scan text for hazards or unsafe actions. level: ok | caution | stop."""
    flags = []
    level = "ok"
    for pattern, rule_level, message in SAFETY_RULES:
        if re.search(pattern, text, re.IGNORECASE):
            flags.append(message)
            if rule_level == "stop":
                level = "stop"
            elif level == "ok":
                level = "caution"
    return {"level": level, "flags": flags}