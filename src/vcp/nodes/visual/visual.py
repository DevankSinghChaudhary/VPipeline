import os
import time
from textwrap import dedent

from dotenv import load_dotenv

from vcp.chat import ChatVPipeline
from langchain.agents import create_agent

from vcp.prompts import SystemPrompt
from vcp.schemas import VisualResponse
from vcp.state import GlobalState

from vcp.utils import read_knowledge


load_dotenv()


model = ChatVPipeline(
    model = "mistral-large-2512",
    base_url = os.getenv("MISTRAL_URL"),
    api_key = os.getenv("MISTRAL_API_KEY3")
)


def visualizer(state: GlobalState) -> dict:
    print(f"[AGENT] Visualizer | Started ...")
    start = time.time()
    script = state["script"]
    prompt = dedent(
    f"""
    Process the following narration scripts into semantic typography segments.

    For each script, extract only the most visually meaningful phrases according to your system instructions.

    Do not rewrite the scripts.

    [INPUT SCRIPTS]

    {script}
    """
    )
    agent = create_agent(
        model=model,
        system_prompt=SystemPrompt.load("visual"),
        response_format=VisualResponse
    )
    result = agent.invoke({
        "messages":{
            "role": "user",
            "content": prompt
        }
    })
    result=result["structured_response"]

    print(
        f"[AGENT] Visualizer | Finished"
        f"[AGENT] Visualizer | {time.time()-start:.2f}s"
    )
    return {"visual": result}
