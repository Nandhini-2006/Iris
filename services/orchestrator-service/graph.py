from langgraph.graph import StateGraph, START, END
from langfuse import get_client

from state import DebugState
from agents.scanner_agent import scanner_agent
from agents.fixer_agent import fixer_agent
from agents.validator_agent import validator_agent


graph_builder = StateGraph(DebugState)

graph_builder.add_node("scanner", scanner_agent)
graph_builder.add_node("fixer", fixer_agent)
graph_builder.add_node("validator", validator_agent)

graph_builder.add_edge(START, "scanner")
graph_builder.add_edge("scanner", "fixer")
graph_builder.add_edge("fixer", "validator")
graph_builder.add_edge("validator", END)

graph = graph_builder.compile()


langfuse = get_client()


def run_debug_graph(code: str, error: str):

    with langfuse.start_as_current_observation(
        as_type="agent",
        name="code-debugging",
        input={
            "code": code,
            "error": error
        }
    ) as trace:

        result = graph.invoke({
            "code": code,
            "error": error
        })

        trace.update(
            output={
                "scan_result": result.get("scan_result"),
                "fix_result": result.get("fix_result"),
                "validation_result": result.get(
                    "validation_result"
                ),
                "final_result": result.get("final_result")
            }
        )

    langfuse.flush()

    return result