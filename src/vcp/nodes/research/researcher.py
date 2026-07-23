import os
import time
from textwrap import dedent
from itertools import cycle

from dotenv import load_dotenv

from vcp.chat import ChatVPipeline

from langchain.agents import create_agent

from vcp.utils import web_search
from vcp.prompts import SystemPrompt

from vcp.state import GlobalState
from vcp.schemas import ResearchResponse


load_dotenv()

apikey = cycle(
    [
        os.getenv("MISTRAL_API_KEY"),
        os.getenv("MISTRAL_API_KEY2"),
        os.getenv("MISTRAL_API_KEY3")
    ]
)

def researcher(state: GlobalState):

    model = ChatVPipeline(
        model = "ministral-14b-2512",
        base_url = os.getenv("MISTRAL_URL"),
        api_key = next(apikey)
    )

    print(f"[Researcher] Started Researching")
    st = time.time()

    topic = state["topic"]

    prompt = dedent(
        f"""
        [TOPIC]
        {topic}

        [ROLE]
        You are the Researcher.

        Your responsibility is to build a factual, structured research foundation for a short-form documentary typography video.

        [TASK]
        Analyze the topic and gather only the most relevant factual material needed for documentary narration.

        Your goal is to construct a structured research packet that is:

        * factual
        * high-density
        * logically connected
        * time-relevant when necessary
        * free from hallucination

        [CORE RULES]

        1. Zero hallucination.
        Use only verified information.

        2. Don't underuse web search.
        Don't over use as well, do 1-2 web search for each topic

        3. Research before synthesis.
        Do not assume facts before tool usage.

        3. Tool-first reasoning.
        Use tools whenever their output improves factual quality.

        4. Prioritize documentary-relevant information:

        * incidents
        * causes
        * consequences
        * measurable outcomes
        * timelines
        * external context

        5. Avoid collecting unnecessary background unless directly useful.

        Web Search:
        Use after internal agents.
        Purpose:
        Collect raw factual verification, missing facts, and measurable data.

        Only call tools when necessary.
        Do not call tools redundantly.
        *ONE web_search can take upto 20 queries, be sure to utilize them effeciently, use atleast half of it in one call with meaningful queries related to topic*

        [OUTPUT GOAL]

        Produce a structured factual research packet for downstream writing.
        Do not write the documentary itself.
        """
        )

    agent = create_agent(
        model = model,
        response_format = ResearchResponse,
        system_prompt = SystemPrompt.load("research"),
        tools = [web_search]
    )
    
    result = agent.invoke({
        "messages":[{
            "role": "user",
            "content": prompt
        }]
    })
    result = result["structured_response"]

    print(f"[Researcher] Finished Successfully")
    print(f"[Researcher] {time.time()-st}")

    return {"information": result}
