import uvicorn
from fastapi import FastAPI

from .api import rag

app = FastAPI()


@app.get("/")
def root():
    return {"RAGbot health status": "Running!"}


# Include the RAG router
app.include_router(rag.router)


if __name__ == "__main__":
    uvicorn.run(app, log_level="info", port=1050)
