import click
import uvicorn
from fastapi import FastAPI

from .api import rag

app = FastAPI()


@app.get("/")
def root():
    return {"RAGbot health status": "Running!"}


# Include the RAG router
app.include_router(rag.router)


@click.command()
@click.option("--port", default=8000, help="Port for the FastAPI app.")
@click.option("--local", is_flag=True, help="Run app locally.")
def serve(port=8000, local=False):
    """Run the rag_backend app with specified options."""
    if not local:
        host = "0.0.0.0"  # Host IP address
    else:
        host = "127.0.0.1"
    uvicorn.run(app, log_level="info", port=port, host=host)


if __name__ == "__main__":
    serve()
