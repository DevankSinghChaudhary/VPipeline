from vcp.chat import ChatVPipeline
from langchain.agents import create_agent


model = ChatVPipeline(
    model="",
    api_key="sk",
    base_url="https://ai.hackclub.com/chat/completions"
)

agent=create_agent(
    model=model,
    system_prompt="Be Nice to everyone"
)

d = agent.invoke({
    "messages":{
        "role":"user",
        "content":"Tell me a joke"
    }
})

print(d)
