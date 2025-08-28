from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from openai import OpenAI

from ..core.config import rag_config

openai_client = OpenAI(
    api_key=rag_config.GWDG_API_KEY, base_url=rag_config.GWDG_ENDPOINT
)


def llm_generator(model_name):
    """Initialize and return a ChatOpenAI generator instance.
    parameters
    ----------
    model_name : str
        The name of the model to use (e.g., "chatgpt-4o").
    """
    return ChatOpenAI(
        model_name=model_name,
        api_key=rag_config.GWDG_API_KEY,
        base_url=rag_config.GWDG_ENDPOINT,
        temperature=0,
    )


def llm_embedder():
    """Initialize and return an OpenAIEmbeddings instance."""
    return OpenAIEmbeddings(
        model=rag_config.GWDG_EMBEDDING_MODEL_NAME,
        openai_api_base=rag_config.GWDG_ENDPOINT,
        openai_api_key=rag_config.GWDG_API_KEY,
        tiktoken_model_name=None,
        model_kwargs={"encoding_format": "float"},
    )
