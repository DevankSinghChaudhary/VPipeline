import time

from langgraph.graph import StateGraph, START, END

from .user import user_topic
from vcp.state import GlobalState

from vcp.nodes import researcher, writer


def graph(state: GlobalState):

    builder = StateGraph(state)

    builder.add_node("Researcher", researcher)
    builder.add_node("Writer", writer)

    builder.add_edge(START, "Researcher")
    builder.add_edge("Researcher", "Writer")
    builder.add_edge("Writer", END)

    graph = builder.compile()

    result = graph.invoke({
        "topic": user_topic(),
        "information": {},
        "script": []
    })


    return result
