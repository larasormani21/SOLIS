"""
td_generation.py – Thing Description Generation Agent

Invoked after the Crawler Agent populates `service_description`.
Converts the free-text description into a structured W3C WoT
Thing Description (TD) and stores it as `selected_service`.

Outputs (written to WorkerState):
    selected_service – dict representing the generated Thing Description
"""

from __future__ import annotations

from schemas import WorkerState


def td_generation_agent(state: WorkerState) -> dict:
    """
    LangGraph node – TD Generation Agent.

    Parses `service_description` and emits a W3C WoT-compatible
    Thing Description that captures the transport service's affordances
    (actions, properties, events) and security definitions.

    Returns a partial WorkerState update:
      • {selected_service: {<TD dict>}}
    """
    description: str = state.get("service_description", "")
    task: dict       = state.get("current_task", {})
    tid: str         = task.get("id", "?")

    print(f"\n[TDGenerationAgent] Task '{tid}' | Generating Thing Description…")

    # ──────────────────────────────────────────────────────────
    # TODO: Use an LLM to parse `description` and produce a
    # standards-compliant W3C WoT Thing Description (JSON-LD).
    #
    #   prompt = (
    #       "You are a W3C WoT expert. Parse the following service "
    #       "description and emit a valid Thing Description JSON-LD "
    #       "with title, description, transport_mode, endpoint, "
    #       "securityDefinitions, and at least one action affordance.\n\n"
    #       f"Description:\n{description}"
    #   )
    #   raw_td = llm.invoke(prompt).content
    #   td = json.loads(raw_td)
    # ──────────────────────────────────────────────────────────

    # Simulated TD generation for the demo
    td: dict = {
        "@context": "https://www.w3.org/2019/wot/td/v1",
        "@type":    "TransportService",
        "id":       "urn:atm:metro:milan:m2",
        "title":    "ATM Metro Milano – Line M2",
        "description": description,
        "transport_mode": task.get("transport_mode", "metro"),
        "coverage":  "Milan metropolitan area",
        "endpoint":  "https://api.atm.it/v1/journey-planner",
        "securityDefinitions": {
            "nosec_sc": {"scheme": "nosec"}
        },
        "security": "nosec_sc",
        "actions": {
            "planJourney": {
                "description": "Plan a trip between two stops on the network.",
                "input": {
                    "type": "object",
                    "properties": {
                        "from":           {"type": "string"},
                        "to":             {"type": "string"},
                        "departure_time": {
                            "type":   "string",
                            "format": "date-time",
                        },
                    },
                    "required": ["from", "to"],
                },
                "output": {
                    "type": "object",
                    "properties": {
                        "duration_minutes": {"type": "integer"},
                        "fare_eur":         {"type": "number"},
                        "steps":            {"type": "array"},
                    },
                },
            }
        },
        "source": "crawler+td_generation",
    }

    print(f"  ✓ Thing Description generated: '{td['title']}'")
    return {"selected_service": td}