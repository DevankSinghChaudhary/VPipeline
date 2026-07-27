import os
from dotenv import load_dotenv
from tinyfish import TinyFish
import time

load_dotenv()

start = time.time()
client = TinyFish(
    api_key = os.getenv("TINYFISH_API")
)

response = client.fetch.get_contents(
    [""],
    format="markdown",
)

for page in response.results:
    print(page.text)
