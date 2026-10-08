from repair_agent.demo_graph import graph


def test_normal_path_reaches_guidance():
    out = graph.invoke({"appliance": "refrigerator", "symptoms": "not cooling and the compressor is loud"})
    assert out["candidates"][0]["issue_id"] == "fridge_dirty_coils"
    assert "guidance" in out


def test_dangerous_input_stops_early():
    out = graph.invoke({"appliance": "refrigerator", "symptoms": "I smell gas near the fridge"})
    assert out["final"].startswith("STOP")
    assert "candidates" not in out  # analysis never ran


def test_no_match_path():
    out = graph.invoke({"appliance": "washing machine", "symptoms": "the display shows a blue color"})
    assert out["candidates"] == []
    assert "guidance" not in out