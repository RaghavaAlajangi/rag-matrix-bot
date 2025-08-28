from langchain_qdrant import QdrantVectorStore
from qdrant_client import QdrantClient

from ..core.config import rag_config
from .llms import llm_embedder

embedder = llm_embedder()


def get_vectorstore():
    """Initialize and return the Qdrant vector store."""
    qdrant_client = QdrantClient(
        host=rag_config.VECTORDB_HOST, port=rag_config.VECTORDB_PORT
    )

    vectordb = QdrantVectorStore(
        client=qdrant_client,
        collection_name=rag_config.VECTORDB_COLLECTION,
        embedding=embedder,
    )
    return vectordb


def get_retriever():
    """Get a retriever from the vector store with specified search
    parameters.
    """
    vectordb = get_vectorstore()
    return vectordb.as_retriever(search_kwargs={"k": rag_config.VECTORDB_TOPK})
