from langchain_core.messages import HumanMessage, SystemMessage

from repair_agent.llm import get_llm
from repair_agent.schemas import QuickDiagnosis

SYSTEM_PROMPT = (
    "You are a careful home appliance troubleshooting assistant. "
    "Never suggest opening sealed electrical parts, gas lines, or anything "
    "that risks shock, fire, or injury."
)

question = "My washing machine is not draining and makes a humming noise."

messages = [SystemMessage(content=SYSTEM_PROMPT), HumanMessage(content=question)]

llm = get_llm()

# Part 1: plain text response
reply = llm.invoke(messages)
print("--- PLAIN TEXT ---")
print(reply.content)

# Part 2: structured response
structured_llm = llm.with_structured_output(QuickDiagnosis)
diagnosis = structured_llm.invoke(messages)
print("\n--- STRUCTURED ---")
print(type(diagnosis).__name__)
print(diagnosis.model_dump_json(indent=2))