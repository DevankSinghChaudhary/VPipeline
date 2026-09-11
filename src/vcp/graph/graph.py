import time

from langgraph.graph import END, START, StateGraph

from vcp.manifest import manifest
from vcp.nodes import (
    decompositioner,
    formatter,
    merger,
    researcher,
    sorter,
    visualizer,
    writer,
)
from vcp.service import (
    clear_audio,
    fanout_image,
    fanout_tts,
    omni,
    search_images,
    tts_batch_complete,
    whisperx_engine,
)
from vcp.state import GlobalState

from .user import user_topic


# Main function of graph.
async def graph(state: GlobalState):
    topic = user_topic()
    start = time.time()
    clear_audio()
    # Defining State of the graph {State}
    builder = StateGraph(state)
    # Defining nodes of the graph.
    builder.add_node("Sorter", sorter)
    builder.add_node("Researcher", researcher)
    builder.add_node("Writer", writer)
    builder.add_node("Formatter", formatter)
    builder.add_node("Visualizer", visualizer)
    builder.add_node("Image", search_images)
    builder.add_node("TTSBatchComplete", tts_batch_complete)
    builder.add_node("Omni", omni)
    builder.add_node("Merger", merger)
    builder.add_node("Decompositioner", decompositioner)
    builder.add_node("Whisper", whisperx_engine, defer=True)
    builder.add_node("RendererManifest", manifest)

    # Adding edges to the nodes
    # Basically, Sketching lines from node to node
    # Researcher ---> Writer ---> Formatter ---> Omni ---> For batching ---> Omni ---> END
    #                               |
    #                               `--> Visualizer ---> Sorter(No use as of right now) ---> Decompositioner ---> RendererManifest ---> Whisper (Absolute end of pipeline) ---> END
    builder.add_edge(START, "Researcher")
    builder.add_edge("Researcher", "Writer")
    builder.add_edge("Writer", "Formatter")
    builder.add_conditional_edges("Formatter", fanout_tts)
    builder.add_edge("Omni", "TTSBatchComplete")
    builder.add_edge("Formatter", "Visualizer")
    builder.add_conditional_edges("Visualizer", fanout_image)
    builder.add_conditional_edges("TTSBatchComplete", fanout_tts)
    builder.add_edge("Visualizer", "Sorter")
    builder.add_edge("Sorter", "Decompositioner")
    builder.add_edge("Omni", "Whisper")
    builder.add_edge("Whisper", "RendererManifest")
    builder.add_edge("RendererManifest", END)
    # builder.add_edge("LINK", "Whisper")
    # builder.add_edge("Whisper", END)
    graph = builder.compile()
    # Actual state being passed in the graph
    result = await graph.ainvoke(
        {
            "topic": topic,
            "category": str,
            "information": {},
            "script": [],
            "audio": [],
            "tts_index": 0,
            "visual": [],
            "images": [],
            "sorted": {},
            "decomposition": [],
            "stt": [],
        }
    )
    print(f"[GRAPH] Finished | {time.time() - start:.2f}s")
    return result
