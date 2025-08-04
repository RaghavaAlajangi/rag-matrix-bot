import requests


class RAGService:
    """
    Service to handle retrieval-augmented generation (RAG) queries.
    This service interacts with a RAG API to generate responses based on user
    prompts and chat history.
    Parameters
    ----------
    config : Config
        Configuration object containing RAG API URL and model.
    """

    def __init__(self, config):
        self.api_url = config.rag_api_url
        self.model = config.rag_model

    async def query_model(self, prompt, chat_history, logger):
        """
        Query RAG API.

        Parameters
        ----------
        prompt : str
            Latest prompt.
        chat_history : list
            Chat history.
        logger : logging.Logger
            Logger instance for logging information.
        Returns
        -------
        str
            Generated answer.
        """
        payload = {
            "model": self.model,
            "prompt": prompt,
            "chat_history": chat_history,
        }

        response = requests.post(self.api_url, json=payload)
        response.raise_for_status()
        data = response.json()

        response_text = data["answer"]
        quoted_reasoning = ""

        # Check for different types of thought/solution delimiters
        if "<think>" in response_text:
            thinking, response_text = response_text.split("</think>")
            thinking = thinking.strip("<think>").strip()
            quoted_reasoning = "\n".join(
                [f"> {line}" for line in thinking.splitlines()]
            )

        # Compose final response with reasoning quote
        final_response = (
            f"{quoted_reasoning}\n\n\n{response_text}"
            if quoted_reasoning
            else response_text
        )

        return final_response
