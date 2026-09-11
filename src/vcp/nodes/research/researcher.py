import os
import time
from textwrap import dedent

from dotenv import load_dotenv
from langchain.agents import create_agent

from vcp.chat import ChatVPipeline
from vcp.prompts import SystemPrompt
from vcp.schemas import ResearchResponse
from vcp.state import GlobalState
from vcp.utils import read, root, web_search

load_dotenv()

model = ChatVPipeline(
    model="ministral-14b-2512",
    base_url=os.environ["MISTRAL_URL"],
    api_key=os.environ["MISTRAL_API_KEY3"],
)

# model = ChatVPipeline(
#   model="mercury-2",
#   base_url=os.environ["INCEPTION_URL"],
#   api_key=os.environ["INCEPTION"],
# )

# model = ChatVPipeline(
# model="minimax-m3-free",
# api_key=os.environ["KIRA_AI"],
# base_url=os.environ["KIRA_AI_BASE"],
# )


# SKILL
BASE_DIR = root.find()
SKILL_PATH = BASE_DIR / "src" / "vcp" / "skills"
RESEARCH_SKILL = read(SKILL_PATH / "research.md")


async def researcher(state: GlobalState):
    print("[AGENT] Researcher | Started Researching")
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
            Don't overuse it either. Do 1–2 web searches for each topic when necessary.

        PARALLEL TOOL CALLING:

        * When multiple web searches are independent of each other, ALWAYS issue them in parallel.
        * NEVER wait for one independent web search to finish before requesting another.
        * A single web_search call supports a maximum of 10 queries.
        * If more than 10 queries are required, split them into batches of 10.
        * Example: 20 queries → 2 parallel web_search calls of 10 queries each.
        * Example: 25 queries → 3 parallel web_search calls: 10 + 10 + 5.
        * Example: 7 queries → 1 web_search call containing all 7 queries.
        * Use as many parallel web_search calls as necessary.
        * Only perform a search sequentially when its query genuinely depends on the result of a previous search.
        * Do NOT artificially serialize independent searches.

            3. Research before synthesis.
                Do not assume facts before tool usage.

            4. Tool-first reasoning.
                Use tools whenever their output improves factual quality.

            5. Prioritize documentary-relevant information:
                * incidents
                * causes
                * consequences
                * measurable outcomes
                * timelines
                * external context

            6. Avoid collecting unnecessary background unless directly useful.

        Web Search:

        Use after internal agents.

        Purpose:

        Collect raw factual verification, missing facts, and measurable data.

        Only call tools when necessary.
        Do not call tools redundantly.

        When multiple independent facts or angles need verification, group their search queries into parallel web_search tool calls rather than executing them sequentially.

        [OUTPUT GOAL]

        Produce a structured factual research packet for downstream writing.
        Do not write the documentary itself.

        """
    )

    agent = create_agent(
        model=model,
        response_format=ResearchResponse,
        system_prompt=SystemPrompt.load("research"),
        tools=[web_search],
    )

    result = await agent.ainvoke({"messages": {"role": "user", "content": prompt}})
    result = result["structured_response"]

    print("[AGENT] Researcher | Finished Successfully")
    print(f"[AGENT] Researcher | {time.time() - st:.2f}s")

    return {
        "category": result.category,
        "information": result.information,
    }
