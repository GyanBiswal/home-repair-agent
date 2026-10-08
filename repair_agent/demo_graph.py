from typing import TypedDict

from langgraph.graph import END, START, StateGraph

from repair_agent.tools import analyze_symptoms, check_safety, get_repair_guidance


class DemoState(TypedDict, total=False):
    appliance: str
    symptoms: str
    safety_level: str
    safety_flags: list[str]
    candidates: list[dict]
    guidance: dict
    final: str


def safety_node(state: DemoState) -> dict:
    result = check_safety(state["symptoms"])
    return {"safety_level": result["level"], "safety_flags": result["flags"]}


def emergency_node(state: DemoState) -> dict:
    return {"final": "STOP: " + " ".join(state["safety_flags"])}


def analyze_node(state: DemoState) -> dict:
    result = analyze_symptoms(state["appliance"], state["symptoms"])
    if "error" in result:
        return {"candidates": [], "final": result["error"]}
    return {"candidates": result["candidates"]}


def guidance_node(state: DemoState) -> dict:
    top = state["candidates"][0]
    guidance = get_repair_guidance(top["issue_id"])
    return {"guidance": guidance, "final": f"Most likely: {top['issue']}"}


def no_match_node(state: DemoState) -> dict:
    return {"final": state.get("final", "No matching issue found. Consider calling a technician.")}



def route_after_safety(state: DemoState) -> str:
    return "emergency" if state["safety_level"] == "stop" else "analyze"


def route_after_analyze(state: DemoState) -> str:
    return "guidance" if state["candidates"] else "no_match"


builder = StateGraph(DemoState)

builder.add_node("safety", safety_node)
builder.add_node("emergency", emergency_node)
builder.add_node("analyze", analyze_node)
builder.add_node("guidance", guidance_node)
builder.add_node("no_match", no_match_node)

builder.add_edge(START, "safety")
builder.add_conditional_edges(
    "safety", route_after_safety, {"emergency": "emergency", "analyze": "analyze"}
)
builder.add_conditional_edges(
    "analyze", route_after_analyze, {"guidance": "guidance", "no_match": "no_match"}
)
builder.add_edge("emergency", END)
builder.add_edge("guidance", END)
builder.add_edge("no_match", END)

graph = builder.compile()


if __name__ == "__main__":
    cases = [
        ("refrigerator", "not cooling and the compressor is loud"),
        ("refrigerator", "I smell gas near the fridge"),
        ("washing machine", "the display shows a blue color"),
    ]
    for appliance, symptoms in cases:
        out = graph.invoke({"appliance": appliance, "symptoms": symptoms})
        print(f"\n{appliance} / {symptoms}\n  -> {out['final']}")