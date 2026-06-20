"""
service_ranker.py – Service Ranker Agent

Invoked when `query_result` is populated (one or more services
were found in the local repository).
Ranks the candidates against current_task constraints and selects
the best match, storing it as `selected_service`.

Outputs (written to WorkerState):
    selected_service – the highest-ranked service dict
"""

from __future__ import annotations

from schemas import WorkerState


def service_ranker_agent(state: WorkerState) -> dict:
    """
    LangGraph node – Service Ranker Agent.

    Evaluates the services in `query_result` against the requirements
    expressed in `current_task` (transport mode, constraints, coverage,
    etc.) and returns the best-matching service as `selected_service`.

    Returns a partial WorkerState update:
      • {selected_service: {<service dict>}}
    """
    candidates: list[dict] = state.get("query_result") or []
    task: dict             = state.get("current_task", {})
    tid: str               = task.get("id", "?")

    print(
        f"\n[ServiceRankerAgent] Task '{tid}' | "
        f"Ranking {len(candidates)} candidate(s)…"
    )

    # ──────────────────────────────────────────────────────────
    # TODO: Replace stub with a real ranking strategy, e.g.:
    #
    #   Strategy A – Embedding similarity
    #     task_emb  = embeddings.embed_query(task["description"])
    #     for svc in candidates:
    #         svc["_score"] = cosine_sim(task_emb, svc["embedding"])
    #
    #   Strategy B – Rule-based scoring
    #     for svc in candidates:
    #         score = 0
    #         if task["transport_mode"] in svc["transport_modes"]: score += 3
    #         if "accessibility_required" in task["constraints"]:
    #             score += 1 if svc.get("accessible") else -2
    #         svc["_score"] = score
    #
    #   Strategy C – LLM-as-judge
    #     prompt = (
    #         f"Task: {task}\n"
    #         f"Candidates:\n{json.dumps(candidates, indent=2)}\n"
    #         "Return the service_id of the best match."
    #     )
    #     best_id = llm.invoke(prompt).content.strip()
    #
    # ──────────────────────────────────────────────────────────

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