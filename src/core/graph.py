from typing import Literal

from langgraph.graph import END, START, StateGraph

from agents.nodes import analyzer_node, drafter_node, filer_node
from core.state import LegalState


def _route_after_analyzer(state: LegalState) -> Literal["drafter", "__end__"]:
    if state.get("is_favorable"):
        return "__end__"
    return "drafter"


builder = StateGraph(LegalState)
builder.add_node("analyzer", analyzer_node)
builder.add_node("drafter", drafter_node)
builder.add_node("filer", filer_node)

builder.add_edge(START, "analyzer")
builder.add_conditional_edges(
    "analyzer",
    _route_after_analyzer,
    {
        "drafter": "drafter",
        "__end__": END,
    },
)
builder.add_edge("drafter", "filer")
builder.add_edge("filer", END)

legal_workflow = builder.compile()
