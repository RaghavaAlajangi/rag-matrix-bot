import os

from dotenv import load_dotenv

load_dotenv()


class Config:
    """Configuration class to manage environment variables."""

    # Vector DB params
    VECTORDB_HOST = os.getenv("VECTORDB_HOST")
    VECTORDB_PORT = os.getenv("VECTORDB_PORT")
    VECTORDB_COLLECTION = os.getenv("VECTORDB_COLLECTION")
    VECTORDB_TOPK = os.getenv("VECTORDB_TOPK")

    # LLM API key from OPENAPI
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    OPENAI_ENDPOINT = os.getenv("OPENAI_ENDPOINT")
    OPENAI_EMBEDDING_MODEL_NAME = os.getenv("OPENAI_EMBEDDING_MODEL_NAME")

    # FastAPI token
    INTERNAL_FASTAPI_TOKEN = os.getenv("INTERNAL_FASTAPI_TOKEN")


rag_config = Config()
