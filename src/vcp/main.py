import asyncio

from vcp.graph import graph
from vcp.state import GlobalState


async def main(state: GlobalState):
    result = await graph(state)
    return result


if __name__ == "__main__":
    output = asyncio.run(main(GlobalState))
    print(output["decomposition"])
    print()
    print()
    for images in output["images"]:
        print(images["url"])
