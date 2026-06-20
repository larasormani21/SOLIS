"""
service_selection.py – Service Selection Agent

Queries the local service repository to find transport services
that match the current mobility task.

Outputs (written to WorkerState):
    query_result      – list of matching service dicts (if found)
    no_service_found  – True when the repository has no match
"""

from __future__ import annotations
import pymongo, json
from config import build_llm_from_model_and_temperature, mongo_uri, testing_mode, testing_mode_agents

from schemas import WorkerState


def build_db_query(llm, task: dict) -> str:
    prompt = f"""
You are a Service Selector Agent.

Your ONLY responsibility is to generate a valid MongoDB query to 
retrieve candidate services from a collection of Thing Descriptions (TDs)
written in the standard Web of Things (WoT) Thing Description 2.0 
(https://www.w3.org/TR/wot-thing-description-2.0/).

KNOWLEDGE:

The "thing_description" follows the W3C WoT Thing Description 2.0 
specification and may contain:
- title
- description
- @type
- properties: exposes state of the Thing. This state can then be 
retrieved (read -> GET) and/or updated (write -> POST/PUT/PATCH)
- actions: allows to invoke a function of the Thing, which manipulates
state (e.g., toggling a lamp on or off) or triggers a process on the 
Thing (e.g., dim a lamp over time) (every HTTP method).
- events: describes an event source, which asynchronously pushes event
data to Consumers (webhook or streaming)
- forms (with href, op, etc.)

IMPORTANT

Thing Descriptions are heterogeneous and may describe the same capability
using different vocabularies.

Therefore:

- Never generate a query requiring an exact @type.
- Never generate a query requiring an exact action name.
- Never generate a query requiring an exact property name.

Instead generate broad keyword-based queries using $or and $regex.

YOUR TASK:

Given a SINGLE workflow task, you must:

1. Understand the task intent
2. Consider:
   - inputs
   - expected_output
   - constraints
3. Generate a MongoDB query that retrieves relevant candidate services

IMPORTANT FILTERING RULES:

You MUST consider:

1. Intent matching
Match against:
- thing_description.title
- thing_description.description
- thing_description.@type
- metadata.tags

2. Functional capability
Match based on:
- actions (for operations)
- properties (for read/write)
- forms.op (e.g., readproperty, invokeaction)

3. Constraints
If present:
- geographic (→ metadata.coverage)
- semantic (e.g., "no bike", "luggage")

OUTPUT FORMAT (STRICT)

You MUST return ONLY a valid MongoDB query in valid JSON format.

- No explanations
- No comments
- No text before or after
- No code fences

- Do NOT explain your reasoning
- Do NOT return natural language
- Do NOT generate code other than the query

The query MUST be usable directly in MongoDB find()

FAILURE CASE

If no clear query can be built, return a query that is likely to 
return zero results rather than guessing.

Task:
{task}
"""
    return llm.invoke(prompt).content.strip()

def query_service_repository(query: str) -> list[dict]:
    """
    Query the local service repository (e.g., a MongoDB collection of TDs)
    using the provided query string.

    Returns a list of matching service dicts, or an empty list if no match.
    """

    client = pymongo.MongoClient(mongo_uri)
    db = client['SOLIS_db']
    collection = db["TDs"]

    try:
        results = list(collection.find(json.loads(query)))
        return results
    except Exception as e:
        print(f"Error querying service repository: {e}")
        return []

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

    print(
        f"\n[ServiceSelectionAgent] Task '{tid}' | "
        f"  Querying service repository…"
    )

    if(testing_mode and "test_service_selection_agent" in testing_mode_agents):
        query = """
        {
        "$or": [
            { "title": { "$regex": "address|geocode|location", "$options": "i" } },
            { "description": { "$regex": "address|geocode|location", "$options": "i" } },
            { "@type": { "$regex": "address|geocode|location", "$options": "i" } },
            { "metadata.tags": { "$regex": "address|geocode|location", "$options": "i" } }
        ]
        }
        """
    else:
        llm = build_llm_from_model_and_temperature("qwen/qwen3.5-35b-a3b", 0.25)
        query = build_db_query(llm, task)
        print(f"[ServiceSelectionAgent] Generated DB query: {query}")

    query_results = query_service_repository(query)

    if not query_results or len(query_results) == 0:
        print(f"  ✗ No matching service found in repository.")
        return {"no_service_found": True, "query_result": None}
    else:
        print(f"  ✓ Found {len(query_results)} service(s) in repository.")
        """
        for i, svc in enumerate(query_results):
            name = svc.get("title") or svc.get("name") or "N/A"
            print(f"    {i+1}. {name}")
        """

        return {"no_service_found": False, "query_result": query_results}

    """
    _simulate_found: bool = True

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
    """