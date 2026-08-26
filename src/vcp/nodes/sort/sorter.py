import os
import time

from dotenv import load_dotenv
from langchain.agents import create_agent

from vcp.chat import ChatVPipeline
from vcp.prompts import SystemPrompt
from vcp.schemas import SortResponse
from vcp.state import GlobalState

load_dotenv()

model = ChatVPipeline(
    model="mistral-large-2512",
    base_url=os.environ["MISTRAL_URL"],
    api_key=os.environ["MISTRAL_API_KEY"],
)


def sorter(state: GlobalState):
    print("[AGENT] Sorter | Started Processing")
    st = time.time()
    script = state["script"]
    img = state["images"]
    prompt = f"""
    ROLE:
    Documentary Asset Selection Agent.

    TASK:
    Select the fetched image assets that are genuinely worth keeping for the final documentary video.

    INPUT:
    You are given:
    1. The original documentary script.
    2. A list of fetched image assets with their filenames, descriptions, URLs and metadata.

    CORE RULE:
    Use only the provided script and fetched assets.
    Do not search for new assets.
    Do not invent asset information.
    Do not modify asset metadata.
    Do not keep an asset merely because it is related to the general topic.

    VISUAL PURPOSE:
    The images must strengthen what the viewer is hearing.
    Prefer assets that directly represent important subjects, people, places, objects, events, scientific concepts or historical material mentioned in the narration.

    SELECTION RULES:

    * Keep assets that clearly match an important subject in the script
    * Prefer exact subject matches over generic representations
    * Prefer historically or scientifically accurate assets
    * Prefer visually distinctive assets
    * Prefer high-resolution assets suitable for video
    * Prefer assets with useful documentary context
    * Prefer visually diverse assets when multiple assets represent the same subject
    * Remove assets that are redundant when a stronger alternative exists
    * Remove assets that are only loosely related to the script
    * Remove generic images that add little visual information
    * Remove misleading or ambiguous assets
    * Remove low-quality assets when better alternatives are available
    * Do not keep multiple nearly identical images unless each provides meaningful additional coverage

    IMPORTANCE:
    An asset does not need to represent an entire sentence.
    A strong asset may represent one important entity or concept mentioned within a sentence.

    PRIORITY:
    When choosing between assets, prioritize in this order:

    1. Relevance to the script
    2. Accuracy of subject representation
    3. Documentary usefulness
    4. Visual quality
    5. Resolution and framing
    6. Uniqueness compared with other selected assets

    REDUNDANCY:
    If several assets represent the same subject:

    * Keep the strongest asset
    * Keep additional assets only if they provide substantially different visual information, perspective, context or composition
    * Do not fill the final selection with near-duplicates

    SCRIPT COVERAGE:
    Use the script to understand what visual material is actually useful.
    Do not attempt to visually represent every sentence.
    The final selection should contain only assets that contribute meaningful visual coverage.

    REJECT:

    * Irrelevant assets
    * Generic stock-like representations with weak relevance
    * Assets whose subject is not actually supported by the script
    * Duplicate or near-duplicate assets
    * Poor-quality assets when stronger alternatives exist
    * Misleading representations
    * Assets that require assumptions to connect them to the narration
    * Assets that are technically related but visually useless

    OUTPUT:
    Return only the selected assets using the required output schema.

    Script:
    {script}

    Image Info:
    {img}
    """
    agent = create_agent(
        model=model,
        system_prompt=SystemPrompt.load("sort"),
        response_format=SortResponse,
    )
    result = agent.invoke({"messages": {"role": "user", "content": prompt}})
    print(f"[AGENT] Sorter | {time.time() - st:.2f}s")
    print("[AGENT] Sorter | Finished Successfully")
    return {"sorted": result["structured_response"]}
