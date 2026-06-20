"""
schemas.py – Pydantic schemas (structured LLM output) and
             LangGraph TypedDict states.

Two state objects:
  • WorkerState      – shared mutable state for one Worker sub-graph run.
  • OrchestratorState – global state owned by the Orchestrator graph.

One routing schema:
  • ServiceRoute – structured output used by the Worker Router node.
"""

from __future__ import annotations

from typing import List, Optional
from typing_extensions import Literal, TypedDict
from pydantic import BaseModel, Field


# ══════════════════════════════════════════════════════════════
# Routing Schema  (structured output for the Worker Router)
# ══════════════════════════════════════════════════════════════

class ServiceRoute(BaseModel):
    """
    Structured output produced by the Worker Router LLM call.

    Drives the conditional edge that splits execution into two paths:
      - 'crawler_agent'        when no local service was found
      - 'service_ranker_agent' when one or more services were found
    """

    step: Literal["crawler_agent", "service_ranker_agent"] = Field(
        description=(
            "Choose 'crawler_agent' when no_service_found is True "
            "(no matching service exists in the local repository → "
            "need to crawl the web and generate a Thing Description). "
            "Choose 'service_ranker_agent' when no_service_found is False "
            "(one or more candidate services were retrieved from the "
            "repository → need to rank them and pick the best one)."
        )
    )


# ══════════════════════════════════════════════════════════════
# Worker State  (one instance per task, owned by the sub-graph)
# ══════════════════════════════════════════════════════════════

class WorkerState(TypedDict):
    """
    Shared mutable state for the Worker sub-graph.

    Fields are populated incrementally as the task moves through
    the Router workflow.  The Orchestrator reads 'code_snippet'
    and 'selected_service' from the final state.

    Lifecycle
    ─────────
    START
      │ current_task (set by Orchestrator before dispatch)
      ▼
    ServiceSelectionAgent
      │ sets ► query_result  OR  no_service_found=True
      ▼
    WorkerRouter
      │ sets ► router_decision
      ▼
    ┌─ crawler_agent        sets ► service_description
    │    └─ td_generation   sets ► selected_service
    └─ service_ranker       sets ► selected_service
      ▼
    RequestAgent
      │ sets ► code_snippet
      ▼
    END
    """

    # ── Input (set by Orchestrator) ────────────────────────────
    current_task: dict
    """The mobility task JSON dispatched by the Orchestrator."""

    # ── ServiceSelectionAgent output ───────────────────────────
    query_result: Optional[List[dict]]
    """Services retrieved from the local repository; None if not found."""

    no_service_found: bool
    """True when the repository returned no matching service."""

    # ── WorkerRouter output ────────────────────────────────────
    router_decision: Optional[str]
    """'crawler_agent' or 'service_ranker_agent' – set by the router node."""

    # ── CrawlerAgent output ────────────────────────────────────
    service_description: Optional[str]
    """Human-readable service description obtained via web crawling."""

    # ── TDGenerationAgent / ServiceRankerAgent output ──────────
    selected_service: Optional[dict]
    """Chosen service in (W3C WoT) Thing Description format."""

    # ── RequestAgent output ────────────────────────────────────
    code_snippet: Optional[str]
    """Auto-generated Python code snippet that executes the task."""


# ══════════════════════════════════════════════════════════════
# Orchestrator State  (global, persists across all Workers)
# ══════════════════════════════════════════════════════════════

class OrchestratorState(TypedDict):
    """
    Global state for the Orchestrator graph.

    Persists across all Worker invocations and accumulates results
    until every task in `tasks` has been processed.
    """

    tasks: List[dict]
    """Ordered list of mobility tasks received as JSON input."""

    current_task_index: int
    """Zero-based index of the task currently being dispatched."""

    task_results: List[dict]
    """Collected result dicts from every completed Worker execution."""

    all_tasks_completed: bool
    """Set to True by the terminal aggregate_results node."""