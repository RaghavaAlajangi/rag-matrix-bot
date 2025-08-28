import os

from dotenv import load_dotenv

load_dotenv()


class Config:
    """Configuration class to manage environment variables."""

    # Vector DB params
    VECTORDB_HOST = os.getenv("VECTORDB_HOST", "localhost")
    VECTORDB_PORT = os.getenv("VECTORDB_PORT", "6333")
    VECTORDB_COLLECTION = os.getenv("VECTORDB_COLLECTION")
    VECTORDB_TOPK = os.getenv("VECTORDB_TOPK", 5)

    # LLM API key from GWDG
    GWDG_API_KEY = os.getenv("GWDG_API_KEY")
    GWDG_ENDPOINT = os.getenv("GWDG_ENDPOINT")
    GWDG_EMBEDDING_MODEL_NAME = os.getenv("GWGE_EMBEDDING_MODEL_NAME")

    # FastAPI token
    INTERNAL_FASTAPI_TOKEN = os.getenv("INTERNAL_FASTAPI_TOKEN")


rag_config = Config()
