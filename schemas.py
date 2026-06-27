from __future__ import annotations

from typing import List, Optional
from typing_extensions import TypedDict

class WorkerState(TypedDict):
    current_task: dict
    query_result: Optional[List[dict]]
    no_service_found: bool
    service_description: Optional[str]
    selected_service: Optional[dict]
    code_snippet: Optional[str]

class OrchestratorState(TypedDict):
    tasks: List[dict]
    current_task_index: int
    task_results: List[dict]
    all_tasks_completed: bool