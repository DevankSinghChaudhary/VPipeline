import time

from langgraph.graph import StateGraph, START, END

from .user import user_topic
from vcp.nodes import researcher
from vcp.state import GlobalState



def graph(state: GlobalState):

    graph = StateGraph(state)

    graph.add_node("Researcher", researcher)


    graph.add_edge(START, "Researcher")

    graph.add_edge("Researcher", END)

    graph.compile()

    graph = graph.compile()

    return graph.invoke({
        "topic": user_topic(),
        "information": {}
    })
