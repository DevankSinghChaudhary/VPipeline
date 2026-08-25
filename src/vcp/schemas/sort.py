from pydantic import BaseModel, Field


class sort(BaseModel):
    image: str = Field(description="The file name that LLM selected to become as asset in video, as value of key")

class SortResponse(BaseModel):
    images: list[sort]
