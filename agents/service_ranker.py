from __future__ import annotations

import json
from typing import List, Dict

from config import build_llm_from_model_and_temperature
from schemas import WorkerState

def build_service_profile(td: dict) -> dict:

    properties = td.get("properties") or {}
    actions = td.get("actions") or {}

    property_descriptions = [
        p.get("title", "") + " " + p.get("description", "")
        for p in properties.values()
    ]

    action_descriptions = [
        a.get("title", "") + " " + a.get("description", "")
        for a in actions.values()
    ]

    return {
        "service_id": str(td.get("_id")),
        "title": td.get("title"),
        "description": td.get("description"),

        "capabilities": (
            property_descriptions[:10]
            + action_descriptions[:10]
        )
    }

def coarse_rank(llm, task: dict, profiles: list[dict]) -> list[dict]:
    prompt = f"""
You are a Service Ranking System.

Your task is to rank service PROFILES based on relevance to the task.

Focus ONLY on:
- functional match
- transport mode compatibility
- geographic relevance
- general capability fit

DO NOT assign same score to multiple services: rank them in order of relevance.

TASK:
{json.dumps(task, indent=2)}

SERVICES (PROFILES):
{json.dumps(profiles, indent=2)}

Return a JSON list:
[
  {{
    "service_id": "...",
    "score": 0-100,
    "reason": "short explanation"
  }}
]

Return ONLY valid JSON.
"""
    return json.loads(llm.invoke(prompt).content.strip())


def fine_rank(llm, task: dict, full_tds: list[dict], coarse_ranked: list[dict]) -> list[dict]:
    prompt = f"""
You are a Service Ranking System.

You now evaluate FULL Thing Descriptions of top candidate services.

TASK:
{json.dumps(task, indent=2, default=str)}

COARSE RANKING (pre-filter):
{json.dumps(coarse_ranked, indent=2, default=str)}

FULL TDs:
{json.dumps(full_tds, indent=2, default=str)}

Re-rank services using detailed TD information:
- endpoints
- actions
- properties
- forms
- constraints

Return a final ordered list:
[
  {{
    "service_id": "...",
    "score": 0-100,
    "reason": "detailed explanation"
  }}
]

Return ONLY JSON.
"""
    return json.loads(llm.invoke(prompt).content.strip())


# ----------------------------
# AGENT NODE
# ----------------------------

def service_ranker_agent(state: WorkerState) -> dict:
    """
    Input:
        state["current_task"]
        state["query_result"]  (list of TDs from Service Selection Agent)

    Output:
        ranked_services
    
    Behavior:
    1. Coarse ranking (fast filtering on lightweight service profiles)
    2. Fine ranking (detailed evaluation on full TDs of top-3 services)
    """

    task = state["current_task"]
    candidates = state.get("query_result", [])

    if not candidates:
        return {"ranked_services": []}

    llm = build_llm_from_model_and_temperature(
        "qwen/qwen3.6-35b-a3b",
        0.2
    )

    profiles = [build_service_profile(td) for td in candidates]
    #for p in profiles:
    #    print(f"  - Profile: {p['service_id']} | {p['title']} | capabilities={p['capabilities']}")

    coarse = coarse_rank(llm, task, profiles)

    print(f"[ServiceRankerAgent] Coarse ranking completed. Top candidates:")
    for r in coarse[:3]:
        print(f"  - {r['service_id']} | title={r['title']} | score={r['score']} | reason={r['reason']}")

    top_k_ids = {r["service_id"] for r in coarse[:3]}
    top_k_full = [
        td for td in candidates
        if str(td.get("_id")) in top_k_ids
    ]

    final_ranking = fine_rank(llm, task, top_k_full, coarse[:3])

    print(f"[ServiceRankerAgent] Completed ranking.")

    if not final_ranking:
        return {"ranked_services": coarse}
    
    else:
        print(f"  Top 3 ranked services:")
        for r in final_ranking[:3]:
            print(f"    - {r['service_id']} | title={r['title']} | score={r['score']} | reason={r['reason']}")
        return {
            "ranked_services": final_ranking
        }