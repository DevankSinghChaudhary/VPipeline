import time
import asyncio

from vcp.graph import graph
from vcp.state import GlobalState


async def main(state: GlobalState):
   
    start = time.time()

    result = await graph(state)
    
    print(f"[Graph] Time: {time.time() - start}")
    print(result)

if __name__ == "__main__":
    asyncio.run(main(GlobalState))
