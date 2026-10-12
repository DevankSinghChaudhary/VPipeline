import asyncio

import typer

from vcp.graph import graph
from vcp.state import GlobalState

app = typer.Typer()


@app.command()
def generate(
    topic: str,
):
    print(f"Running graph with topic: {topic}")
    print()
    result = asyncio.run(graph(GlobalState, topic))
    print(result["script"])


@app.command()
def validate():
    print("Validated VPipeline")


if __name__ == "__main__":
    app()
