"""
orchestrator_graph.py – Orchestrator Graph  (Orchestrator-Workers Pattern)
═══════════════════════════════════════════════════════════════

Receives an ordered JSON list of mobility tasks, spawns one Worker
sub-graph per task (sequentially), collects all results, and
produces a final aggregated report.

Topology
────────
                         START
                           │
               ┌───────────▼───────────┐
          ┌───►│   dispatch_to_worker  │
          │    │  (invokes Worker      │
          │    │   sub-graph per task) │
          │    └───────────┬───────────┘
          │                │
          │      should_continue()  ← conditional edge
          │       │              │
          │  more tasks      all done
          └───────┘              │
                                 ▼
                   ┌─────────────────────────┐
                   │    aggregate_results     │
                   └─────────────┬───────────┘
                                 │
                                END
"""

from __future__ import annotations

from typing import List
from langgraph.graph import END, START, StateGraph

from schemas import OrchestratorState, WorkerState
from graphs.worker_graph import worker_graph


# ══════════════════════════════════════════════════════════════
# Orchestrator Nodes
# ══════════════════════════════════════════════════════════════

def dispatch_to_worker(state: OrchestratorState) -> dict:
    """
    Orchestrator node – picks the next pending task, instantiates a
    fresh WorkerState, runs the Worker sub-graph (which internally
    uses the Router pattern), and appends the result to task_results.

    Returns a partial OrchestratorState update:
      • {task_results: [...accumulated...], current_task_index: idx+1}
    """
    tasks: List[dict] = state["tasks"]
    idx: int          = state["current_task_index"]
    task: dict        = tasks[idx]

    print(
        f"\n{'═' * 62}\n"
        f"[Orchestrator] Dispatching task {idx + 1}/{len(tasks)}\n"
        f"  id  : {task.get('id', 'N/A')}\n"
        f"  desc: {task.get('description', 'N/A')}\n"
        f"{'═' * 62}"
    )

    # ── Initialise a clean WorkerState for this task ──────────
    worker_initial: WorkerState = {
        "current_task":        task,
        "query_result":        None,
        "no_service_found":    False,
        "router_decision":     None,
        "service_description": None,
        "selected_service":    None,
        "code_snippet":        None,
    }

    # ── Invoke the Worker sub-graph ───────────────────────────
    # The sub-graph runs the full Router workflow internally and
    # returns a complete WorkerState with all fields populated.
    worker_result: WorkerState = worker_graph.invoke(worker_initial)

    # ── Collect the Worker's output ───────────────────────────
    svc = worker_result.get("selected_service") or {}
    path = (
        "crawler → td_generation"
        if worker_result.get("no_service_found")
        else "service_ranker"
    )

    task_result: dict = {
        "task_id":          task.get("id", f"task_{idx}"),
        "description":      task.get("description", ""),
        "selected_service": svc,
        "code_snippet":     worker_result.get("code_snippet", ""),
        "path_taken":       path,
    }

    print(f"[Orchestrator] ✓ Task {idx + 1} complete (path: {path})")

    return {
        "task_results":       state.get("task_results", []) + [task_result],
        "current_task_index": idx + 1,
    }


def aggregate_results(state: OrchestratorState) -> dict:
    """
    Terminal Orchestrator node – prints a summary of all completed
    tasks and marks the orchestration as finished.

    Returns a partial OrchestratorState update:
      • {all_tasks_completed: True}
    """
    results: List[dict] = state.get("task_results", [])

    print(
        f"\n{'═' * 62}\n"
        f"[Orchestrator] All {len(results)} task(s) completed.\n"
        f"{'═' * 62}"
    )
    for r in results:
        svc = r.get("selected_service", {})
        svc_name = svc.get("title") or svc.get("name") or "N/A"
        print(
            f"  ✓ [{r['task_id']}]  "
            f"service = {svc_name:<30}  "
            f"path = {r['path_taken']}"
        )

    return {"all_tasks_completed": True}


# ══════════════════════════════════════════════════════════════
# Conditional Edge
# ══════════════════════════════════════════════════════════════

def should_continue(state: OrchestratorState) -> str:
    """
    Returns the name of the next Orchestrator node:
      • 'dispatch_to_worker' – if there are still pending tasks
      • 'aggregate_results'  – if all tasks have been processed
    """
    if state["current_task_index"] < len(state["tasks"]):
        return "dispatch_to_worker"
    return "aggregate_results"


# ══════════════════════════════════════════════════════════════
# Graph Builder
# ══════════════════════════════════════════════════════════════

def build_orchestrator_graph():
    """Assembles and compiles the Orchestrator graph."""

    builder = StateGraph(OrchestratorState)

    # ── Nodes ───────────────────────────────────────────────────
    builder.add_node("dispatch_to_worker", dispatch_to_worker)
    builder.add_node("aggregate_results",  aggregate_results)

    # ── Entry point ─────────────────────────────────────────────
    builder.add_edge(START, "dispatch_to_worker")

    # ── Loop / exit conditional ─────────────────────────────────
    builder.add_conditional_edges(
        "dispatch_to_worker",  # source node
        should_continue,       # routing function
        {                      # name → node mapping
            "dispatch_to_worker": "dispatch_to_worker",   # loop
            "aggregate_results":  "aggregate_results",    # exit
        },
    )

    # ── Terminal edge ────────────────────────────────────────────
    builder.add_edge("aggregate_results", END)

    return builder.compile()


# ── Compiled singleton ────────────────────────────────────────
orchestrator_graph = build_orchestrator_graph()