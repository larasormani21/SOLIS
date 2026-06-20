"""
request_agent.py – Request Agent

Final agent in the Worker sub-graph, called once `selected_service`
is available (regardless of which path produced it).
Generates an executable Python code snippet that fulfils current_task
using the selected service's API, then returns control to the
Orchestrator.

Outputs (written to WorkerState):
    code_snippet – auto-generated Python code string
"""

from __future__ import annotations

from schemas import WorkerState


def request_agent(state: WorkerState) -> dict:
    """
    LangGraph node – Request Agent.

    Reads `selected_service` and `current_task`, then generates a
    Python code snippet that calls the service API to execute the
    mobility task.  This snippet is the primary artefact returned
    by the Worker to the Orchestrator.

    Returns a partial WorkerState update:
      • {code_snippet: "<python code>"}
    """
    service: dict = state.get("selected_service") or {}
    task: dict    = state.get("current_task", {})

    # Resolve service metadata (TD format or flat format)
    svc_name  = service.get("title") or service.get("name", "Unknown Service")
    endpoint  = service.get("endpoint", "https://api.example.com")
    source    = service.get("source", "unknown")
    tid       = task.get("id", "?")

    # Task parameters
    origin         = task.get("origin", "")
    destination    = task.get("destination", "")
    dep_time       = task.get("preferred_time", "08:00")
    constraints    = task.get("constraints", [])
    description    = task.get("description", "N/A")

    print(
        f"\n[RequestAgent] Task '{tid}' | "
        f"Building code snippet for '{svc_name}'…"
    )

    # ──────────────────────────────────────────────────────────
    # TODO: Replace the template-based generation below with an
    # LLM call that produces context-aware, production-ready code:
    #
    #   prompt = (
    #       f"Generate a Python function to fulfil this task using the "
    #       f"service described by this Thing Description.\n\n"
    #       f"Task: {json.dumps(task, indent=2)}\n"
    #       f"Thing Description: {json.dumps(service, indent=2)}\n\n"
    #       "Return only valid Python code, no explanation."
    #   )
    #   code_snippet = llm.invoke(prompt).content
    # ──────────────────────────────────────────────────────────

    snippet = f"""\
# ═══════════════════════════════════════════════════════════════
# Auto-generated code snippet
# Task   : {tid} – {description}
# Service: {svc_name}
# Source : {source}
# ═══════════════════════════════════════════════════════════════

import requests

ENDPOINT = "{endpoint}"

payload = {{
    "from":           "{origin}",
    "to":             "{destination}",
    "departure_time": "{dep_time}",
    "constraints":    {constraints!r},
}}

response = requests.post(
    url=f"{{ENDPOINT}}/planJourney",
    json=payload,
    timeout=10,
)

if response.ok:
    journey = response.json()
    print(f"Journey planned successfully: {{journey}}")
else:
    print(f"Error {{response.status_code}}: {{response.text}}")
"""

    print("  ✓ Code snippet ready.")
    return {"code_snippet": snippet}