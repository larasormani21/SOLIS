from __future__ import annotations

from typing import List, Optional
from typing_extensions import TypedDict

class WorkerState(TypedDict):
    """
    Shared mutable state for the Worker sub-graph.

    Fields are populated incrementally as the task moves through
    the Router workflow.
    """

    current_task: dict
    """The mobility task JSON dispatched by the Orchestrator."""

    query_result: Optional[List[dict]]
    """Services retrieved from the service repository; None if not found."""

    no_service_found: bool
    """True when the repository returned no matching service."""

    service_description: Optional[str]
    """Raw service description obtained via web crawling."""

    selected_service: Optional[dict]
    """Chosen service in W3C WoT Thing Description format."""

    code_snippet: Optional[str]
    """Generated code snippet that executes the task."""

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