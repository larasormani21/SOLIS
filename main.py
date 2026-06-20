"""
main.py – MAS Mobility Entry Point
═══════════════════════════════════════════════════════════════

Feeds an ordered JSON list of mobility tasks to the Orchestrator
graph and prints the aggregated results, including the auto-
generated code snippet for every task.

Usage
─────
    # From the project root (directory containing mas_mobility/):
    python -m mas_mobility.main

    # Or directly:
    python mas_mobility/main.py

Optional: visualise the LangGraph topologies as Mermaid diagrams
    python -m mas_mobility.main --draw
"""

from __future__ import annotations

import json
import sys

from schemas import OrchestratorState
from graphs.orchestrator_graph import orchestrator_graph


# ══════════════════════════════════════════════════════════════
# Example Input – ordered mobility tasks (JSON)
# ══════════════════════════════════════════════════════════════

TASKS_JSON: str = """
[
    {
        "id": "task_1",
        "description": "Given these coordinates, I would like to get the correct address: (45.4845, 9.2040).",
        "coverage": null,
        "constraints": null,
        "inputs": "Coordinates in format (latitude, longitude).",
        "expected_output": "The correct address corresponding to the provided coordinates."
    }
]
"""


# ══════════════════════════════════════════════════════════════
# Helpers
# ══════════════════════════════════════════════════════════════

def _banner(text: str, width: int = 62) -> None:
    print("\n╔" + "═" * width + "╗")
    print("║  " + text.ljust(width - 2) + "║")
    print("╚" + "═" * width + "╝")


def draw_graphs() -> None:
    """
    Save the Mermaid diagram for both graphs to .mmd text files.

    Mermaid text can be rendered:
      • Online  → https://mermaid.live
      • CLI     → mmdc -i graph.mmd -o graph.svg
      • VS Code → Mermaid Preview extension
    """
    from graphs.worker_graph import worker_graph
    from graphs.orchestrator_graph import orchestrator_graph

    graphs = {
        "worker_graph.mmd":       worker_graph,
        "orchestrator_graph.mmd": orchestrator_graph,
    }

    for filename, graph in graphs.items():
        mermaid_text: str = graph.get_graph().draw_mermaid()
        with open(filename, "w", encoding="utf-8") as f:
            f.write(mermaid_text)
        print(f"[Visualise] Saved Mermaid diagram → {filename}")

    # Optionally render to PNG (requires internet or local mermaid install)
    try:
        for filename, graph in graphs.items():
            png_path = filename.replace(".mmd", ".png")
            png_bytes: bytes = graph.get_graph().draw_mermaid_png()
            with open(png_path, "wb") as f:
                f.write(png_bytes)
            print(f"[Visualise] Saved PNG → {png_path}")
    except Exception as exc:
        print(f"[Visualise] PNG rendering skipped: {exc}")


# ══════════════════════════════════════════════════════════════
# Main
# ══════════════════════════════════════════════════════════════

def main(tasks_json: str = TASKS_JSON) -> dict:
    """
    Run the MAS Mobility orchestration pipeline.

    Parameters
    ----------
    tasks_json : str
        JSON string containing an ordered list of mobility tasks.
        Each task must have at minimum an 'id' and 'description' field.

    Returns
    -------
    dict
        The final OrchestratorState after all tasks are processed.
    """
    tasks: list[dict] = json.loads(tasks_json)

    _banner(f"MAS Mobility  │  Orchestrator-Workers  │  tasks={len(tasks)}")

    initial_state: OrchestratorState = {
        "tasks":               tasks,
        "current_task_index":  0,
        "task_results":        [],
        "all_tasks_completed": False,
    }

    # ── Run the Orchestrator graph ────────────────────────────
    final_state: dict = orchestrator_graph.invoke(initial_state)

    # ── Print generated code snippets ─────────────────────────
    _banner("GENERATED CODE SNIPPETS")
    for result in final_state.get("task_results", []):
        svc = result.get("selected_service", {})
        svc_name = svc.get("title") or svc.get("name") or "N/A"
        print(f"\n{'─' * 62}")
        print(f"  Task   : {result['task_id']} – {result['description']}")
        print(f"  Service: {svc_name}")
        print(f"  Path   : {result['path_taken']}")
        print(f"{'─' * 62}")
        print(result.get("code_snippet", "(no snippet generated)"))

    return final_state


if __name__ == "__main__":
    if "--draw" in sys.argv:
        draw_graphs()
    else:
        main()