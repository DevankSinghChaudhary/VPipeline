import time

from vcp.graph import graph
from vcp.state import GlobalState


def main(state: GlobalState):
   
    start = time.time()

    result = graph(state)
    
    print(f"[Graph] Time: {time.time() - start}")
    print(result)

if __name__ == "__main__":
    main(GlobalState)
