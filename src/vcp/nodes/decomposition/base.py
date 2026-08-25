import os
import time
from textwrap import dedent

from dotenv import load_dotenv
from langchain.agents import create_agent

from vcp.chat import ChatVPipeline
from vcp.prompts import SystemPrompt
from vcp.schemas import DecompostionResponse
from vcp.state import GlobalState

load_dotenv()

model = ChatVPipeline(
    model="mistral-large-2512",
    base_url=os.getenv("MISTRAL_URL"),
    api_key=os.getenv("MISTRAL_API_KEY3"),
)


# This is decompositioner whose work is to choose between Typography, images and diagrams
# Which suits the scene/script. Could be either one of them or multiple.
def decompositioner(state: GlobalState):
    start = time.time()
    print("[AGENT] Decompositioner | Started...")
    script = state["script"]
    prompt = dedent(f"""
    [ROLE]
    You are a professional documentary visual decompositioner.

    [MISSION]
    Your task is to analyze a documentary script and determine the most appropriate visual treatment for each scene.

    You have only two visual modalities available:

    1. TYPOGRAPHY
    - Key statements
    - Important phrases
    - Statistics
    - Numbers
    - Dates
    - Names
    - Definitions
    - Quotes
    - Short textual emphasis
    - Information that is best communicated through clear on-screen text

    2. IMAGE
    - Photographs
    - Illustrations
    - Historical imagery
    - People
    - Places
    - Objects
    - Maps
    - Screenshots
    - Real-world visual references
    - Concepts that are better understood through visual imagery

    A scene may use:
    - Typography only
    - Image only
    - Typography + Image

    Do NOT force both modalities into every scene.

    [CORE PRINCIPLE]
    Choose visuals based on INFORMATION, not decoration.

    The goal is to communicate the narration as clearly and efficiently as possible.

    Use TYPOGRAPHY when the information itself is important to display.

    Use IMAGE when seeing the subject provides more understanding than reading about it.

    Use TYPOGRAPHY + IMAGE when the image provides the visual context while typography provides important information, emphasis, labels, statistics, or conclusions.

    Avoid:
    - Decorative images with no informational value.
    - Typography that unnecessarily repeats the narration word-for-word.
    - Images that merely fill empty space.
    - Using both modalities when one is clearly sufficient.
    - Excessive visual complexity.
    - Repeating the same visual treatment unnecessarily across consecutive scenes.

    [ANALYSIS]
    For every scene, determine:

    1. What is the primary information being communicated?
    2. Is the information primarily textual, numerical, factual, conceptual, or visual?
    3. Would the viewer understand it better by seeing the subject?
    4. Is there information that should be explicitly displayed as text?
    5. Should typography, an image, or both carry the visual communication?
    6. Which modality should be primary?

    [VISUAL CONTINUITY]
    Consider the surrounding scenes when making decisions.

    Avoid unnecessary visual switching.

    If the same visual treatment remains effective across consecutive scenes, prefer continuity.

    However, prioritize communication clarity over visual consistency.

    [IMPORTANT]
    - Do not generate the actual typography.
    - Do not generate image-generation prompts.
    - Do not select specific stock images.
    - Do not write narration.
    - Do not invent information that is not present in the script.
    - Do not decide how the animation should work.
    - Do not determine exact typography styling.
    - Do not determine exact image composition.
    - Your responsibility is to determine WHAT visual modality is appropriate and WHY.
    - Every scene must use at least one modality.
    - "primary_modality" must be exactly one of: "typography", "image".
    - "visual_modalities" may contain one or both modalities.
    - Use lowercase modality names exactly: "typography", "image".
    - Keep reasoning concise and actionable for downstream agents.

    [SCRIPT]
    {script}
    """)
    agent = create_agent(
        model=model,
        system_prompt=SystemPrompt.load("decomposition"),
        response_format=DecompostionResponse,
    )
    result = agent.invoke({"messages": {"role": "user", "content": prompt}})
    print("[AGENT] Decompositioner | Finished")
    print(f"[AGENT] Decompositioner | {time.time() - start:.2f}s")
    return {"decomposition": result["structured_response"]}
