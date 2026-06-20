"""
worker_graph.py – Worker Sub-Graph  (Router Pattern)
═══════════════════════════════════════════════════════════════

Every task dispatched by the Orchestrator is handled by one
instance of this sub-graph.  Internally it follows the Router
workflow pattern:

  • service_selection_agent sets the boolean flag `no_service_found`
    in the WorkerState.
  • A conditional edge function reads that flag directly and routes
    execution to the correct specialised agent — no LLM needed,
    because the routing criterion is already a structured value in
    the state, not free-form text.

When IS an LLM router appropriate?
───────────────────────────────────
Use llm.with_structured_output() for routing only when the
decision requires natural-language understanding of unstructured
input, e.g.:
    "Is this user message about pricing, returns, or complaints?"
Here the input is a boolean already computed by service_selection_agent,
so a plain Python conditional is the correct tool.

Topology
────────
                      START
                        │
            ┌───────────▼───────────┐
            │  service_selection_   │  queries local repository
            │       agent           │  → sets query_result / no_service_found
            └───────────┬───────────┘
                        │
              route_decision()  ← conditional edge on no_service_found
                   │       │
        ┌──────────┘       └──────────┐
        │  no_service_found=True      │  no_service_found=False
        ▼                             ▼
┌──────────────┐            ┌──────────────────────┐
│  crawler_    │            │  service_ranker_agent │
│   agent      │            │                      │
└──────┬───────┘            └──────────┬───────────┘
       │                              │
┌──────▼───────┐                      │
│ td_generation│                      │
│   _agent     │                      │
└──────┬───────┘                      │
       │                              │
       └──────────────┬───────────────┘
                      │
          ┌───────────▼───────────┐
          │     request_agent     │  generates code_snippet
          └───────────┬───────────┘
                      │
                     END
"""

from __future__ import annotations

from typing_extensions import Literal
from langgraph.graph import END, START, StateGraph

from schemas import WorkerState
from agents.service_selection import service_selection_agent
from agents.crawler          import crawler_agent
from agents.td_generation   import td_generation_agent
from agents.service_ranker  import service_ranker_agent
from agents.request_agent   import request_agent


# ══════════════════════════════════════════════════════════════
# Conditional Edge Function  (the "Router" in this workflow)
# ══════════════════════════════════════════════════════════════

def route_decision(
    state: WorkerState,
) -> Literal["crawler_agent", "service_ranker_agent"]:
    """
    Reads `no_service_found` directly from WorkerState and returns
    the name of the next node to visit.

    This is the Router in the LangGraph sense: a Python function
    attached to add_conditional_edges() that inspects the current
    state and picks a branch.  No LLM is needed here because the
    routing criterion (`no_service_found`) is already a structured
    boolean computed by service_selection_agent — there is no
    natural language to interpret.
    """
    if state.get("no_service_found", False):
        print("[Router] no_service_found=True  → crawler_agent")
        return "crawler_agent"
    print("[Router] no_service_found=False → service_ranker_agent")
    return "service_ranker_agent"


# ══════════════════════════════════════════════════════════════
# Graph Builder
# ══════════════════════════════════════════════════════════════

def build_worker_graph():
    """Assembles and compiles the Worker sub-graph (Router pattern)."""

    builder = StateGraph(WorkerState)

    # ── Nodes ───────────────────────────────────────────────────
    builder.add_node("service_selection_agent", service_selection_agent)
    builder.add_node("crawler_agent",           crawler_agent)
    builder.add_node("td_generation_agent",     td_generation_agent)
    builder.add_node("service_ranker_agent",    service_ranker_agent)
    builder.add_node("request_agent",           request_agent)

    # ── Entry point ─────────────────────────────────────────────
    builder.add_edge(START, "service_selection_agent")

    # ── Conditional split immediately after Service Selection ────
    #    route_decision() reads no_service_found from state and
    #    returns the target node name — this IS the Router pattern.
    builder.add_conditional_edges(
        "service_selection_agent",
        route_decision,
        {
            "crawler_agent":        "crawler_agent",
            "service_ranker_agent": "service_ranker_agent",
        },
    )

    # ── Path A: Crawler → TD Generation → Request Agent ─────────
    builder.add_edge("crawler_agent",       "td_generation_agent")
    builder.add_edge("td_generation_agent", "request_agent")

    # ── Path B: Service Ranker → Request Agent ───────────────────
    builder.add_edge("service_ranker_agent", "request_agent")

    # ── Convergence: Request Agent always exits to END ───────────
    builder.add_edge("request_agent", END)

    return builder.compile()


# ── Compiled singleton imported by the Orchestrator ──────────
worker_graph = build_worker_graph()