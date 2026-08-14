import asyncio
import os
import time
from collections import deque

from dotenv import load_dotenv
from langchain.tools import tool
from tinyfish import TinyFish


load_dotenv()


client = TinyFish(
    api_key=os.getenv("TINYFISH_API")
)


class RateLimiter:
    def __init__(self, limit: int, period: float):
        self.limit = limit
        self.period = period
        self.timestamps = deque()
        self.lock = asyncio.Lock()

    async def acquire(self):
        while True:
            async with self.lock:
                now = time.monotonic()

                while (
                    self.timestamps
                    and now - self.timestamps[0] >= self.period
                ):
                    self.timestamps.popleft()

                if len(self.timestamps) < self.limit:
                    self.timestamps.append(now)
                    return

                wait = self.period - (now - self.timestamps[0])

            await asyncio.sleep(wait)


SEARCH_LIMITER = RateLimiter(
    limit=30,
    period=60,
)


SEARCH_CONCURRENCY = 10


def chunks(items: list[str], size: int):
    for i in range(0, len(items), size):
        yield items[i:i + size]


def sync_search(query: str):
    return client.search.query(
        query=query,
        language="en",
    )


def sync_fetch(urls: list[str]):
    return client.fetch.get_contents(
        urls,
        format="markdown",
    )


async def search_query(query: str):
    await SEARCH_LIMITER.acquire()

    return await asyncio.to_thread(
        sync_search,
        query,
    )


async def fetch_pages(urls: list[str]):
    return await asyncio.to_thread(
        sync_fetch,
        urls,
    )


async def search_batch(queries: list[str]):
    semaphore = asyncio.Semaphore(SEARCH_CONCURRENCY)

    async def run(query: str):
        async with semaphore:
            return await search_query(query)

    return await asyncio.gather(
        *(run(query) for query in queries)
    )


async def search_queries(queries: list[str]):
    if not queries:
        return []

    batches = list(
        chunks(queries, 10)
    )

    responses = []

    for batch in batches:
        responses.extend(
            await search_batch(batch)
        )

    return responses


@tool(
    "web_search",
    description=(
        "Search the web and retrieve source-page content for factual research. "
        "Use this for current information, external facts, events, people, "
        "organizations, or topics requiring web research. "
        "Pass multiple focused queries when researching multiple aspects of a topic. "
        "Queries are processed concurrently with a maximum of 10 searches at once. "
        "Each search batch contains at most 10 queries."
    ),
    return_direct=False,
)
async def web_search(queries: list[str]) -> list[dict]:
    start = time.time()

    print(
        f"[TOOL] web_search | "
        f"Started | {len(queries)} queries"
    )

    search_responses = await search_queries(
        queries
    )

    sources = []

    for query, response in zip(
        queries,
        search_responses,
    ):
        if not response.results:
            continue

        result = response.results[0]

        sources.append({
            "query": query,
            "url": result.url,
            "title": result.title,
        })

    if not sources:
        print(
            f"[TOOL] web_search | "
            f"Finished | {time.time() - start:.2f}s"
        )
        return []

    urls = [
        source["url"]
        for source in sources
    ]

    fetch_responses = []

    for batch in chunks(urls, 10):
        fetch_responses.append(
            await fetch_pages(batch)
        )

    pages = [
        page
        for response in fetch_responses
        for page in response.results
    ]

    for source, page in zip(
        sources,
        pages,
    ):
        source["content"] = page.text

    print(
        f"[TOOL] web_search | "
        f"Finished | {time.time() - start:.2f}s"
    )

    return sources
