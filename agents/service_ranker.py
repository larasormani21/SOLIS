"""
service_ranker.py – Service Ranker Agent

Receives candidate Thing Descriptions from Service Selection Agent
and ranks them according to the current mobility task.

TWO-STAGE RANKING:

1. Coarse ranking (fast filtering on lightweight service profiles)
2. Fine ranking (detailed evaluation on full TDs of top-k services)

Outputs (written to WorkerState):
    ranked_services – ordered list of services with scores + explanations
"""
from __future__ import annotations

import json
from typing import List, Dict

from config import build_llm_from_model_and_temperature
from schemas import WorkerState

def build_service_profile(td: dict) -> dict:
    """
    Extract a compact representation of a Thing Description.
    This is used for coarse ranking.
    """

    return {
        "service_id": td.get("service_id", td.get("id", "unknown")),
        "title": td.get("thing_description", {}).get("title"),
        "description": td.get("thing_description", {}).get("description"),
        "@type": td.get("thing_description", {}).get("@type"),
        "coverage": td.get("metadata", {}).get("coverage"),
        "tags": td.get("metadata", {}).get("tags", []),
        "actions": list((td.get("thing_description", {}).get("actions") or {}).keys()),
        "properties": list((td.get("thing_description", {}).get("properties") or {}).keys()),
    }


# ----------------------------
# STAGE 1: COARSE RANKING
# ----------------------------

def coarse_rank(llm, task: dict, profiles: list[dict]) -> list[dict]:
    prompt = f"""
You are a Service Ranking System.

Your task is to rank service PROFILES based on relevance to the task.

Focus ONLY on:
- functional match
- transport mode compatibility
- geographic relevance
- general capability fit

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


# ----------------------------
# STAGE 2: FINE RANKING
# ----------------------------

def fine_rank(llm, task: dict, full_tds: list[dict], coarse_ranked: list[dict]) -> list[dict]:
    prompt = f"""
You are a Service Ranking System.

You now evaluate FULL Thing Descriptions of top candidate services.

TASK:
{json.dumps(task, indent=2)}

COARSE RANKING (pre-filter):
{json.dumps(coarse_ranked, indent=2)}

FULL TDs:
{json.dumps(full_tds, indent=2)}

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
    LangGraph node – Service Ranker Agent

    Input:
        state["current_task"]
        state["query_result"]  (list of TDs from Service Selection Agent)

    Output:
        ranked_services
    """

    task = state["current_task"]
    candidates = state.get("query_result", [])

    tid = task.get("id", "?")

    print(
        f"\n[ServiceRankerAgent] Task '{tid}' | "
        f"Ranking {len(candidates)} candidate services..."
    )

    if not candidates:
        return {"ranked_services": []}

    llm = build_llm_from_model_and_temperature(
        "qwen/qwen3.5-35b-a3b",
        0.2
    )

    # ----------------------------
    # 1. Build lightweight profiles
    # ----------------------------
    profiles = [build_service_profile(td) for td in candidates]

    # ----------------------------
    # 2. Coarse ranking
    # ----------------------------
    coarse = coarse_rank(llm, task, profiles)

    # keep top-k (important for cost + context control)
    top_k_ids = {r["service_id"] for r in coarse[:5]}
    top_k_full = [
        td for td in candidates
        if td.get("service_id", td.get("id")) in top_k_ids
    ]

    # ----------------------------
    # 3. Fine ranking
    # ----------------------------
    final_ranking = fine_rank(llm, task, top_k_full, coarse[:5])

    print(f"[ServiceRankerAgent] Completed ranking.")

    return {
        "ranked_services": final_ranking
    }

"""
def service_ranker_agent(state: WorkerState) -> dict:
    candidates: list[dict] = state.get("query_result") or []
    task: dict             = state.get("current_task", {})
    tid: str               = task.get("id", "?")

    print(
        f"\n[ServiceRankerAgent] Task '{tid}' | "
        f"Ranking {len(candidates)} candidate(s)…"
    )

    if not candidates:
        print("  ✗ No candidates to rank – returning empty service.")
        return {"selected_service": {}}

    # Simple heuristic: sort by repository 'score' field (descending)
    ranked = sorted(candidates, key=lambda s: s.get("score", 0.0), reverse=True)
    best   = {**ranked[0], "source": "repository"}

    print(
        f"  ✓ Selected: '{best.get('name')}' "
        f"(score={best.get('score', 'N/A')})"
    )
    return {"selected_service": best}

"""