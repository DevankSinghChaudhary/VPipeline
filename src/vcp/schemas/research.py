from pydantic import BaseModel, Field


class ResearchResponse(BaseModel):
    information: str = Field(description="Researched information that model sysnthesised from internet")
