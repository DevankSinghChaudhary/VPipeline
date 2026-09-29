from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain_openai import ChatOpenAI
from pydantic import BaseModel

load_dotenv()


class response(BaseModel):
    output: str


def model():

    model = ChatOpenAI(
        model="glm-5.3-flash",
        api_key="gruid_9jwkoqang37c8097",
        base_url="https://freebuff.com/chat",
    )

    agent = create_agent(
        model=model,
        response_format=response,
        system_prompt="Answer statefully, with strict response format. Answer in legal manner",
    )

    output = agent.invoke(
        {"messages": {"role": "user", "content": "Whats capital of france"}}
    )
    output = output["structured_response"]

    print({"output": output.output})


model()

# https://freebuff.com/chat
