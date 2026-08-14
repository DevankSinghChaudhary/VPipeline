import time
import asyncio

from langgraph.graph import StateGraph, START, END

from .user import user_topic
from vcp.state import GlobalState

from vcp.nodes import (
    researcher,
    writer,
    formatter,
    merger,
    visualizer
)
from vcp.service import (
    fanout_tts,
    omni,
    tts_batch_complete,
    clear_audio
)

async def graph(state: GlobalState):

    start = time.time()
    clear_audio()

    builder = StateGraph(state)

    builder.add_node("Researcher", researcher)
    builder.add_node("Writer", writer)
    builder.add_node("Formatter", formatter)
    builder.add_node("Visualizer", visualizer)
    builder.add_node("TTSBatchComplete", tts_batch_complete)
    builder.add_node("Omni", omni)
    builder.add_node("Merger", merger)

    builder.add_edge(START, "Researcher")
    builder.add_edge("Researcher", "Writer")
    builder.add_edge("Writer", "Formatter")
    builder.add_edge("Writer", "Visualizer")
    builder.add_conditional_edges("Formatter", fanout_tts)
    builder.add_edge("Omni", "TTSBatchComplete")
    builder.add_conditional_edges("TTSBatchComplete",fanout_tts)
    builder.add_edge("Merger", END)

    graph = builder.compile()

    result = await graph.ainvoke({
        "topic": user_topic(),
        "information": {},
        "script": [],
        "formatted": [],
        "audio": [],
        "tts_index": 0,
        "visual": []
    })

    print(f"[GRAPH] Finished | {time.time()-start:.2f}s")
    return result
