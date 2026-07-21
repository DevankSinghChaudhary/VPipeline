import operator
from typing import TypedDict, Annotated

from pydantic import Field

from vcp.schemas import ResearchResponse
from vcp.schemas import ScriptResponse


class GlobalState(TypedDict):
    topic: str = Field(description = "Topic of whole operation.")
    information: ResearchResponse = Field(description = "Information Researcher will add here that it got from web (Summarized Infoamtion, not raw metadata)")
    script: ScriptResponse = Field(description = "Script that Writer will write, will be added in list of dicts, each dict containing only one scentence of whole script.")
