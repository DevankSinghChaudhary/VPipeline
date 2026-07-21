from pydantic import BaseModel, Field


class ScriptLine(BaseModel):
    id: int = Field(description="Unique ID for each script.")
    script: str = Field(description="Single line script only. No full script but each Dailouge or line")


class ScriptResponse(BaseModel):
    script: list[ScriptLine]
