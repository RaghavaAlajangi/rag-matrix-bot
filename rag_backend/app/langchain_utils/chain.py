from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains.retrieval import create_retrieval_chain

from .llms import llm_generator
from .retriever import get_retriever


def get_rag_chain(model_name, prompt):
    """Prepare and return a RAG chain with the specified model and prompt.

    parameters
    ----------
    model_name : str
        The name of the model to use (e.g., "chatgpt-4o").
    prompt : langchain_core.prompts.ChatPromptTemplate
        The prompt template to use for the chain.
    """
    llm = llm_generator(model_name)
    retriever = get_retriever()
    llm_chain = create_stuff_documents_chain(llm, prompt)
    qa_chain = create_retrieval_chain(retriever, llm_chain)
    return qa_chain
