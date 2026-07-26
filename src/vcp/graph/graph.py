import time
import asyncio

from langgraph.graph import StateGraph, START, END

from .user import user_topic
from vcp.state import GlobalState

from vcp.nodes import (
    researcher,
    writer,
    formatter
)
from vcp.service import (
    fanout_tts,
    kokoro_service
)

async def graph(state: GlobalState):

    builder = StateGraph(state)

    builder.add_node("Researcher", researcher)
    builder.add_node("Writer", writer)
    builder.add_node("Formatter", formatter)
    builder.add_node("Kokoro", kokoro_service)

    builder.add_edge(START, "Researcher")
    builder.add_edge("Researcher", "Writer")
    builder.add_edge("Writer", "Formatter")
    builder.add_conditional_edges("Formatter", fanout_tts)
    builder.add_edge("Kokoro", END)

    graph = builder.compile()

    result = await graph.ainvoke({
        "topic": user_topic(),
        "information": {},
        "script": [],
        "formatted": [],
        "audio": []
    })


    return result
