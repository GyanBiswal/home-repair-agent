# AI Home Repair & Troubleshooting Agent

A LangGraph-based agent that diagnoses common home appliance problems by choosing
between tools (troubleshooting lookup, cost reference, safety checker).

🚧 Work in progress.

## Setup

1. `python3.12 -m venv .venv && source .venv/bin/activate`
2. `pip install -r requirements.txt`
3. `cp .env.example .env` and add your Groq API key
4. `python -m repair_agent.config`