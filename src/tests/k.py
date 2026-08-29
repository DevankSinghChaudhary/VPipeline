import os

from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain_openai import ChatOpenAI
from pydantic import BaseModel

from vcp.utils import web_search

load_dotenv()


class response(BaseModel):
    output: str


def model():

    model = ChatOpenAI(
        model="kira-mini-1.0",
        api_key=os.environ["KIRA_AI"],
        base_url=os.environ["KIRA_AI_BASE"],
    )

    agent = create_agent(
        model=model,
        response_format=response,
        system_prompt="Do whatevery User say. Use 'web_search' tool for retireiving current information",
        tools=[web_search],
    )

    output = agent.invoke(
        {
            "messages": {
                "role": "user",
                "content": "Tell me info about Nepal Flood 2026",
            }
        }
    )
    output = output["structured_response"]

    print({"output": output.output})


model()
