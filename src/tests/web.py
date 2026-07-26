from tinyfish import TinyFish
import time


start = time.time()
client = TinyFish(
    api_key = "sk-tinyfish-anEN4vKIHTvPBWwLTIewlNn9mLFegnE2"
)

response = client.search.query(
    "Whats the main motive behind CJP Protest in India",
    language="en",
)

for result in response.results:
    response = client.fetch.get_contents(
            [result.url],
            format="markdown"
        )

    for page in response.results:
        print(page.text)

print(f"TOTAL TIME TAKEN: {time.time()-start}")
