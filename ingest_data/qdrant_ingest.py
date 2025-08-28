import os

from dotenv import load_dotenv
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader
from langchain_openai import OpenAIEmbeddings
from langchain_qdrant import QdrantVectorStore
from qdrant_client import QdrantClient
from qdrant_client.http.models import Distance, VectorParams

load_dotenv()

embedder = OpenAIEmbeddings(
    model=os.getenv("OPENAI_EMBEDDING_MODEL_NAME"),
    openai_api_base=os.getenv("OPENAI_ENDPOINT"),
    openai_api_key=os.getenv("OPENAI_API_KEY"),
)


def ingest_to_qdrant(
    file_path: str,
    collection_name="rag_data",
    host="localhost",
    vector_size=2560,  # qwen3-embedding-4b embedding size
    port=6333,
):
    # Load document
    loader = PyPDFLoader(file_path)
    documents = loader.load()

    # Split into chunks
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=900, chunk_overlap=150
    )
    chunks = splitter.split_documents(documents)

    # Connect to Qdrant and create collection
    qdrant_client = QdrantClient(host=host, port=port)
    if not qdrant_client.collection_exists(collection_name):
        qdrant_client.create_collection(
            collection_name=collection_name,
            vectors_config=VectorParams(
                size=vector_size,
                distance=Distance.COSINE,
            ),
        )
    else:
        print(f"Collection {collection_name} is already existed!")

    qdrant = QdrantVectorStore(
        client=qdrant_client,
        collection_name=collection_name,
        # retrieval_mode=RetrievalMode.SPARSE,
        sparse_vector_name="sparse",
        embedding=embedder,
    )

    qdrant.add_documents(documents=chunks)

    print(
        f"Ingested {len(chunks)} chunks into '{collection_name}' collection."
    )


# Example usage
if __name__ == "__main__":
    ingest_to_qdrant("test_data/sample.pdf")
