import os
from textwrap import dedent

from dotenv import load_dotenv
from langchain.agents import create_agent

from vcp.chat import ChatVPipeline
from vcp.prompts import SystemPrompt
from vcp.schemas import Scene
from vcp.state import GlobalState
from vcp.utils import timed

load_dotenv()

model = ChatVPipeline(
    model="ministral-14b-2512",
    base_url=os.environ["MISTRAL_URL"],
    api_key=os.environ["MISTRAL_API_KEY3"],
)


# This is decompositioner whose work is to choose between Typography, images and diagrams
# Which suits the scene/script. Could be either one of them or multiple.
@timed
def decompositioner(state: GlobalState):
    scripts = state["script"]
    images = state["images"]
    prompt = dedent(f"""
    Analyze the following documentary scenes and convert each one into a visual specification.

    For each scene:

    1. Preserve scene_id and script_id.
    2. Preserve the original script.
    3. Preserve the supplied segment strings.
    4. Decide exactly one visual modality:

    * IMAGE
    * IMAGE_WITH_TEXT
    * TYPOGRAPHY
    * NONE
    5. Populate only the visual objects required by that modality.
    6. Use IMAGE_WITH_TEXT when a concrete image should have a short associated QUESTION or KEY_LINE.
    7. Use TYPOGRAPHY when text itself should be the primary visual.
    8. Use IMAGE when the image alone is sufficient.
    9. Use NONE when neither modality adds meaningful visual value.
    10. Keep image.asset descriptions concrete and concise.
    11. Keep typography.text short enough to work as on-screen documentary text.
    12. Do not rewrite or summarize the supplied narration.
    13. Do not invent visual subjects or factual information.

    Important distinction:

    IMAGE_WITH_TEXT = image + text specifically associated with that image.

    TYPOGRAPHY = independent text-only visual treatment.

    If a scene contains a person and an important date that should appear with that person's image, prefer IMAGE_WITH_TEXT.

    If the text deserves to exist as an independent visual treatment separate from the image, use IMAGE + TYPOGRAPHY only when the schema and pipeline support both independently.

    Return only the structured Pydantic-compatible response.
    
    Scripts:
    {scripts}


    Images:
    {images}
    """)

    agent = create_agent(
        model=model,
        system_prompt=SystemPrompt.load("decomposition"),
        response_format=Scene,
    )
    result = agent.invoke({"messages": {"role": "user", "content": prompt}})
    return {"decomposition": result["structured_response"]}
