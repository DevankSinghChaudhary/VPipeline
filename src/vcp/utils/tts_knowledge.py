import time

from pathlib import Path
from typing import Literal

from langchain.tools import tool

BASE_DIR = Path(__file__).resolve().parent.parent

KNOWLEDGE_DIR = BASE_DIR / "knowledge" / "tts"



@tool(
    "read_knowledge",
    description="""
Retrieve internal VPipeline knowledge documents.

Use this tool whenever you need authoritative pipeline documentation
instead of relying on your own knowledge.

The returned content is Markdown (.md) documentation and should be
treated as the source of truth.

Use this tool for:
- TTS formatting rules
- punctuation and pause guidelines
- number and date formatting
- pronunciation guidance
- sentence rhythm
- abbreviations
- proper noun handling

Available topics:
- punctuation
- pauses
- numbers
- dates
- pronunciation
- sentence_rhythm
- abbreviations
- proper_nouns
- important

  *NOTE* The important file, you must call it before you output the script. (EVERYTIME, DON'T LEAVE IT, JUST CALL IT ON EACH RUN)

Only request topics that are necessary for the current task.
Do not call this tool if you already have sufficient information.
"""
)
def read_knowledge(
    topic: Literal[
            "important",
            "abbreviations",
            "dates",
            "numbers",
            "pauses",
            "products",
            "pronunciation-normalization",
            "proper-nouns",
            "punctuation",
            "sentence-rhythm",
            "technical-terms"
        ]
) -> str:
    """Read multiple TTS formatting topics."""
    print(f"[TOOL] tts_knowledge | Called")

    file = KNOWLEDGE_DIR / f"{topic}.md"
    output = file.read_text(encoding="utf-8")
    print(f"[TOOL] tts_knowledge | {topic}.md fetched")
    print(f"[TOOL] tts_knowledge | Finished Fetching")
    return output
