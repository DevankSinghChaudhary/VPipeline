import os
import time
from textwrap import dedent
from dotenv import load_dotenv
from itertools import cycle

from langchain_openai import ChatOpenAI
from langchain.agents import create_agent

load_dotenv()

apikey = cycle(
    [
        os.getenv('MISTRAL_API_KEY'),
        os.getenv('MISTRAL_API_KEY2'),
        os.getenv('MISTRAL_API_KEY3')
    ]
)

for i in range(10):
    print('STARTED LARGE MODEL')

    model = ChatOpenAI(
        model = 'magistral-medium-2509',
        base_url = 'https://api.mistral.ai/v1',
        api_key = next(apikey)
    )

    structured_llm = model.with_structured_output(response)

    output = structured_llm.invoke('France')
    {'object': 'error', 'message': 'Rate limit exceeded', 'type': 'rate_limited', 'param': None, 'code': '1300', 'raw_status_code': 429}

    if output.type == 'rate_limited':
        print('RATE LIMITE exceeded')

    else:
        pass

    print({

        'country': output.type,
        'capital': output.captial,
        'estbalished': output.estbalished
    })
