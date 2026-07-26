import asyncio
import os

import time

from dotenv import load_dotenv
from langchain.tools import tool
from tinyfish import TinyFish


load_dotenv()


client = TinyFish(
    api_key=os.getenv("TINYFISH_API")
)


def sync_search(query: str):
    return client.search.query(
        query,
        language="en",
    )


def sync_fetch(urls: list[str]):
    return client.fetch.get_contents(
        urls,
        format="markdown",
    )


async def search_query(query: str):
    return await asyncio.to_thread(
        sync_search,
        query,
    )


async def fetch_pages(urls: list[str]):
    return await asyncio.to_thread(
        sync_fetch,
        urls,
    )


@tool(
    "web_search",
    description=(
        "Search the web and retrieve source-page content for factual research. "
        "Use this for current information, external facts, events, people, "
        "organizations, or topics requiring web research. "
        "Pass multiple focused queries when researching multiple aspects of a topic. "
        "Searches are performed concurrently, and the most relevant result for "
        "each query is fetched as Markdown."
    ),
    return_direct=False
)
async def web_search(queries: list[str]) -> list[dict]:
    """
    Search the web and retrieve source content.

    Args:
        queries: One or more focused search queries. Each query should target
            a specific piece of information or aspect of the research topic.

    Returns:
        A list of source objects containing the search query, source URL,
        source title, and fetched Markdown content.
    """

    start = time.time()
    print(f"[TOOL] web_search | Started Fetching...")

    search_responses = await asyncio.gather(
        *(
            search_query(query)
            for query in queries
        )
    )

    sources = []

    for query, response in zip(queries, search_responses):
        if not response.results:
            continue

        result = response.results[0]

        sources.append({
            "query": query,
            "url": result.url,
            "title": result.title,
        })

    if not sources:
        return []

    urls = [
        source["url"]
        for source in sources
    ]

    fetch_response = await fetch_pages(urls)

    for source, page in zip(sources, fetch_response.results):
        source["content"] = page.text

    print(f"[TOOL] web_search | {time.time()-start}")
    print(f"[TOOL] web_search | Finished Fetching")

    return sources
