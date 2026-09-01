import os
from textwrap import dedent

from langchain.agents import create_agent

from vcp.chat import ChatVPipeline
from vcp.prompts import SystemPrompt
from vcp.schemas import VisualResponse
from vcp.state import GlobalState
from vcp.utils import timed

model = ChatVPipeline(
    model="ministral-14b-2512",
    base_url=os.environ["MISTRAL_URL"],
    api_key=os.environ["MISTRAL_API_KEY3"],
)

# model = ChatVPipeline(
#   model="minimax-m3-free",
#   api_key=os.environ["KIRA_AI"],
#   base_url=os.environ["KIRA_AI_BASE"],
# )


@timed
def visualizer(state: GlobalState) -> dict:
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
        response_format=VisualResponse,
    )
    result = agent.invoke({"messages": {"role": "user", "content": prompt}})
    result = result["structured_response"]
    return {"visual": result}
