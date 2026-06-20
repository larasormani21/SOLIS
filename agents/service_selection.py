"""
service_selection.py – Service Selection Agent

Queries the local service repository to find transport services
that match the current mobility task.

Outputs (written to WorkerState):
    query_result      – list of matching service dicts (if found)
    no_service_found  – True when the repository has no match
"""

from __future__ import annotations
import pymongo
from config import build_llm_from_model_and_temperature

from schemas import WorkerState


def service_selection_agent(state: WorkerState) -> dict:
    """
    LangGraph node – Service Selection Agent.

    Receives current_task from the WorkerState and queries the local
    service repository (e.g. a WoT Thing Directory, a vector store,
    or a REST service registry).

    Returns a partial WorkerState update:
      • {no_service_found: True,  query_result: None}     – no match
      • {no_service_found: False, query_result: [...]  }  – match(es) found
    """
    task = state["current_task"]
    tid  = task.get("id", "?")
    mode = task.get("transport_mode", "N/A")
    src  = task.get("origin", "?")
    dst  = task.get("destination", "?")

    print(
        f"\n[ServiceSelectionAgent] Task '{tid}' | "
        f"mode={mode} | {src} → {dst}\n"
        f"  Querying local service repository…"
    )

    # ──────────────────────────────────────────────────────────
    # TODO: Replace the stub below with a real query, e.g.:
    #
    #   • Vector-store similarity search over a WoT TD directory
    #       results = vector_store.similarity_search(task["description"])
    #
    #   • REST call to a local service registry
    #       results = requests.get(REGISTRY_URL, params={"mode": mode}).json()
    #
    #   • SPARQL query over an RDF triplestore
    #       results = sparql.query(build_sparql(task))
    #
    # Toggle `_simulate_found` to exercise the two branches:
    #   False → Crawler → TD-Generation path  (default demo)
    #   True  → Service-Ranker path
    # ──────────────────────────────────────────────────────────

    _simulate_found: bool = False  # ← flip to True to test ranker path

    if not _simulate_found:
        print("  ✗ No matching service found in repository.")
        return {"no_service_found": True, "query_result": None}

    # Simulated repository results (used when _simulate_found=True)
    services: list[dict] = [
        {
            "service_id":      "atm_metro_001",
            "name":            "ATM Metro Milano",
            "transport_modes": ["metro"],
            "coverage":        "Milan metropolitan area",
            "endpoint":        "https://api.atm.it/v1/journey-planner",
            "score":           0.95,
        },
        {
            "service_id":      "trenord_regional_001",
            "name":            "Trenord Regional Rail",
            "transport_modes": ["rail", "metro"],
            "coverage":        "Lombardy region",
            "endpoint":        "https://api.trenord.it/v1/journey",
            "score":           0.72,
        },
    ]

    print(f"  ✓ Found {len(services)} service(s) in repository.")
    return {"no_service_found": False, "query_result": services}