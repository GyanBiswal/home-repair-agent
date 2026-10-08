from repair_agent.tools import (
    analyze_symptoms,
    check_safety,
    estimate_repair_cost,
    get_repair_guidance,
)


def test_analyze_symptoms_finds_clogged_pump():
    result = analyze_symptoms("washing machine", "not draining and a humming noise")
    assert result["candidates"][0]["issue_id"] == "washer_clogged_pump"


def test_analyze_symptoms_unsupported_appliance():
    assert "error" in analyze_symptoms("toaster", "burnt smell")


def test_guidance_and_cost_for_known_issue():
    assert "safe_steps" in get_repair_guidance("fridge_door_seal")
    assert estimate_repair_cost("fridge_door_seal")["currency"] == "USD"


def test_unknown_issue_returns_error():
    assert "error" in get_repair_guidance("nope")
    assert "error" in estimate_repair_cost("nope")


def test_safety_flags_gas_and_bypass():
    assert check_safety("I smell gas near the stove")["level"] == "stop"
    assert check_safety("I will bypass the thermostat")["level"] == "stop"


def test_safety_ok_for_normal_step():
    assert check_safety("Clean the filter with warm water")["level"] == "ok"