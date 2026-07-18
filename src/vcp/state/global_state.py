import operator
from typing import TypedDict, Annotated

from vcp.schemas import ResearchResponse


class GlobalState(TypedDict):
    topic: str
    information: ResearchResponse
