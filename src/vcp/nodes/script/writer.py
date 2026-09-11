import os

from dotenv import load_dotenv
from langchain.agents import create_agent

from vcp.chat import ChatVPipeline
from vcp.prompts import SystemPrompt
from vcp.schemas import ScriptResponse
from vcp.state import GlobalState
from vcp.utils import read, root, timed

load_dotenv()

model = ChatVPipeline(
    model="ministral-14b-2512",
    base_url=os.environ["MISTRAL_URL"],
    api_key=os.environ["MISTRAL_API_KEY"],
)

# model = ChatVPipeline(
#   model="mercury-2",
#   base_url=os.environ["INCEPTION_URL"],
#   api_key=os.environ["INCEPTION"],
# )

# model = ChatVPipeline(
#   model="minimax-m3-free",
#   api_key=os.environ["KIRA_AI"],
#   base_url=os.environ["KIRA_AI_BASE"],
# )

BASE_DIR = root.find()
SKILL_PATH = BASE_DIR / "src/vcp/skills/humanscope"
RESEARCH_SKILL = read(SKILL_PATH / "SKILL.md")

SYSTEM_PROMPT = (
    SystemPrompt.load("script") + "\n\n" + "=" * 20 + "\n\n" + RESEARCH_SKILL
)


@timed
def writer(state: GlobalState):
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
        model=model,
        system_prompt=SYSTEM_PROMPT,
        response_format=ScriptResponse,
    )
    result = agent.invoke({"messages": {"role": "user", "content": prompt}})
    result = result["structured_response"]
    return {"script": result}
