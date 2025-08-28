from functools import lru_cache
from typing import List, Literal

from fastapi import APIRouter, Depends
from pydantic import BaseModel

from ..core.internal_auth import get_api_key
from ..langchain_utils.chain import get_rag_chain, openai_client
from ..langchain_utils.prompts import get_prompt

router = APIRouter(prefix="/rag")


class Message(BaseModel):
    """User message."""

    role: Literal["user", "assistant"]
    content: str


class QueryRequest(BaseModel):
    """User query request."""

    model: str
    chat_history: List[Message] = []


@lru_cache(maxsize=100)
@router.get("/models", response_model=List[str])
def list_models():
    """API endpoint to list available models."""
    models = openai_client.models.list()
    model_names = [m.id for m in models]
    return model_names


@router.post("/chat")
async def chat_api(query: QueryRequest, api_key: str = Depends(get_api_key)):
    """API endpoint for chat with given LLM.

    Query format should be:
    {
        "model": "meta-llama-3.1-8b-instruct",
        "chat_history": [
            {"role": "user", "content": "summarize Human Development Index"}
        ]
    }
    """

    # Separate the latest user message
    latest_user_message = query.chat_history[-1].content

    # Exclude the last message
    chat_history = [m.model_dump() for m in query.chat_history[:-1]]

    # Prepare the chain
    model_name = query.model
    prompt = get_prompt()
    chain = get_rag_chain(model_name, prompt)

    # Call the chain
    result = chain.invoke(
        {
            "input": latest_user_message,
            "chat_history": chat_history,
        }
    )
    # Process the result
    answer = result["answer"]
    docs = [doc.metadata for doc in result.get("context", [])]

    return {
        "answer": answer,
        "relevant_docs": docs,
    }
