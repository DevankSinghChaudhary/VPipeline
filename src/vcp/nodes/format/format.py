import os
import time
from textwrap import dedent

from dotenv import load_dotenv

from vcp.chat import ChatVPipeline
from langchain.agents import create_agent

from vcp.prompts import SystemPrompt
from vcp.schemas import FormatResponse
from vcp.state import GlobalState

from vcp.utils import read_knowledge


load_dotenv()


model = ChatVPipeline(
    model = "mistral-large-2512",
    base_url = os.getenv("MISTRAL_URL"),
    api_key = os.getenv("MISTRAL_API_KEY2")
)


def formatter(state: GlobalState) -> dict:
    
    print(f"[AGENT] Formatter | Started Formatting...")

    start = time.time()
    script = state["script"]

    user_prompt = dedent(
        f"""
        You are the Formatter Agent.

        Your only responsibility is to convert a completed narration script into a version that is optimized for text-to-speech (TTS).

        The narration has already been researched, structured, and written.
        Do NOT rewrite the script.
        Do NOT improve the writing.
        Do NOT change the storytelling.
        Do NOT add or remove information.

        Your task is formatting only.

        Your objectives:

        - Improve natural speech flow.
        - Improve pronunciation consistency.
        - Improve pause placement.
        - Improve sentence rhythm.
        - Improve listening clarity.
        - Preserve every factual statement.

        You may:

        - Add or remove punctuation.
        - Split overly long sentences.
        - Merge unnaturally short sentences.
        - Rewrite numbers into spoken form when appropriate.
        - Rewrite dates into spoken form when appropriate.
        - Expand abbreviations when necessary for correct pronunciation.
        - Improve capitalization only when it affects pronunciation.
        - Replace symbols with spoken equivalents when appropriate.
        - Add commas or periods for natural pauses.
        - Remove punctuation that produces awkward speech.
        - Normalize whitespace.

        You must NEVER:

        - Change factual meaning.
        - Add facts.
        - Remove facts.
        - Summarize.
        - Reorder events.
        - Rewrite paragraphs for style.
        - Change narrative pacing.
        - Add dramatic wording.
        - Add emotional language.
        - Add commentary.
        - Add introductions or conclusions.
        - Invent pronunciations.
        - Guess formatting rules.

        Whenever formatting depends on documented TTS behavior, use the available knowledge tools to retrieve the appropriate documentation before making a formatting decision.

        The documentation returned by the knowledge tool is authoritative.

        If documentation conflicts with your assumptions, always follow the documentation.

        Output Requirements:

        - Return only the fully formatted script.
        - Preserve paragraph structure unless splitting improves speech.
        - Preserve the original language.
        - Preserve all information.
        - Produce output that is immediately ready for TTS synthesis.

        [SCRIPT]:
        {script}
        """
    )

    agent = create_agent(
        model = model,
        response_format = FormatResponse,
        system_prompt = SystemPrompt.load("format"),
        tools = [read_knowledge]
    )

    result = agent.invoke({
        "messages": {
            "role": "user",
            "content": user_prompt
        }
    })

    result = result["structured_response"]

    print(f"[AGENT] Formatter | {time.time()-start}")
    print(f"[AGENT] Formatter | Finished Formatting")

    return {
        "script": result
    }
