from pydantic import BaseModel, Field


class FormatSingle(BaseModel):
    id: int
    script: str

class FormatResponse(BaseModel):
    script: list[FormatSingle]
