from pydantic import BaseModel, Field


class ResearchResponse(BaseModel):
    category: str = Field(description="Analyze the topic, get information about it and then classify the topic and tag it with category and return it.")
    information: str = Field(description="Researched information that model sysnthesised from internet")
