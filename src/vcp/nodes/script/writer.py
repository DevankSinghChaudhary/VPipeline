import os
import time
from dotenv import load_dotenv

from vcp.classopenai import ChatOpenAI
from langchain.agents import create_agent

from vcp.utils import web_search
from vcp.prompts import getprompt

from vcp.state import GlobalState
from vcp.schemas import ScriptResponse

load_dotenv()

model = ChatOpenAI(
    model = "mistral-large-2512",
    base_url = os.getenv("MISTRAL_URL"),
    api_key = os.getenv("MISTRAL_API_KEY")
)

system_prompt = getprompt("script")


def writer(state: GlobalState):

    print(f"[Writer] Started Processing")
    st = time.time()

    topic = state["topic"]
    information = state["information"]
    
    prompt = f"""
    ROLE:
    Documentary narration writer.

    TASK:
    Convert the provided ordered factual units into one continuous short-form documentary narration.

    CORE RULE:
    Use only provided information.
    Do not invent facts.
    Do not add external knowledge.
    Do not add filler.

    SPOKEN REALISM:
    The output must sound natural when spoken.

    Rules:

    * Vary sentence length naturally
    * Avoid repetitive sentence structures
    * Allow sentence fusion when facts are tightly connected
    * Prefer natural spoken rhythm over rigid written form
    * Avoid over-explaining obvious causal relationships

    BANNED:

    * Generic documentary phrases
    * Filler phrases
    * Commentary phrases
    * Rhetorical questions
    * Artificial suspense
    * Dramatic closers
    * Symmetrical repetitive sentence rhythm

    CONTENT RULES:

    * Every sentence must add new factual information
    * No repetition
    * No paraphrasing of the same fact
    * No emotional exaggeration
    * No vague setup phrases

    OPENING RULE:
    Start with the strongest concrete event, incident, or measurable fact.

    Never start with:

    * background
    * broad context
    * vague historical framing

    LENGTH:

    * Target: 50-60 words
    * Hard max: 80 words

    STYLE:
    Neutral.
    Dense.
    Factual.
    Natural spoken documentary narration.

    OUTPUT:
    Return only the final narration text.

    TOPIC: {topic}
    INFORMATION: {information}
    """

    agent = create_agent(
        model = model,
        system_prompt = system_prompt,
        response_format = ScriptResponse
    )
    
    result = agent.invoke({
        "messages":{
            "role":"user",
            "content": prompt
        }
    })
    result = result["structured_response"]
    
    print(f"[Writer] Finished Successfully")
    print(f"[Writer] {time.time()-st}")
    
    return {
        "script": result
    }
