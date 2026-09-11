import asyncio

from vcp.graph import graph
from vcp.state import GlobalState


async def main(state: GlobalState):
    result = await graph(state)
    return result


if __name__ == "__main__":
    output = asyncio.run(main(GlobalState))
    print(output["script"])
    print()
    print()

    print(output["visual"])
    print()
    print()

    print(output["sorted"])
    print()
    print()

    print(output["decomposition"])
    print()
    print()

    print(output["stt"])
