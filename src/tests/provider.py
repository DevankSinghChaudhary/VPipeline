import os
import time
from textwrap import dedent
from itertools import cycle

from dotenv import load_dotenv

from langchain_openai import ChatOpenAI
from langchain.agents import create_agent

from pydantic import BaseModel

load_dotenv()


class response(BaseModel):
    output: str

def model():
    
    model = ChatOpenAI(
        model = '@cf/mistral/mistral-7b-instruct-v0.2-lora',
        api_key = os.getenv('CLOUDFLARE_API_KEY'),
        base_url = os.getenv('CLOUDFLARE_URL')
    )

    agent = create_agent(
        model = model,
        response_format = response,
        system_prompt = 'Answer statefully, with strict response format. Answer in legal manner'
    )

    output = agent.invoke({'messages':{'role':'user','content':'Whats capital of france'}})
    output = output['structured_response']

    print({'output':output.output})

model()
