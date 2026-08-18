from pydantic import BaseModel, Field

#Response State for the LLM (researcher) @ /VPipeline/src/vcp/nodes/research/researcher.py
class ResearchResponse(BaseModel):
    #Category of the topic decided by the LLM.
    #e.g: History, Astrobiology etc
    category: str = Field(description="Analyze the topic, get information about it and then classify the topic and tag it with category and return it.")

    #Information gathered by the LLM from the web.
    #Not raw HTML text from the web but processed information after gathering from the web.
    information: str = Field(description="Researched information that model sysnthesised from internet")
