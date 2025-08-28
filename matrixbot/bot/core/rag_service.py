import requests


class RAGService:
    """Service to handle retrieval-augmented generation (RAG) queries. This
    service interacts with a RAG API to generate responses based on user
    prompts and chat history.
    Parameters
    ----------
    config : Config
        Configuration object containing RAG API URL and model.
    """

    def __init__(self, config):
        self.api_url = config.rag_api_url
        self.model = config.rag_model
        self.rag_api_key = config.rag_api_key

    @staticmethod
    def _details_block(drop_head, message):
        return (
            f"<details>\n"
            f"<summary><strong>{drop_head}</strong></summary>\n"
            f"<p>{message}</p>\n"
            f"</details>"
        )

    @staticmethod
    def _format_reasoning(response_text):
        """Extract and format reasoning block if present."""
        if "<think>" in response_text:
            thinking, answer = response_text.split("</think>", 1)
            thinking = thinking.replace("<think>", "").strip()
            formatted_thinking = "<br>".join(
                line for line in thinking.splitlines()
            )
            return (
                RAGService._details_block(
                    "Model Reasoning:", formatted_thinking
                ),
                answer.strip(),
            )
        return "", response_text.strip()

    async def query_model(self, prompt, chat_history, logger):
        """Query RAG API.

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
        headers = {
            "X-Internal-Token": self.rag_api_key,
            "Content-Type": "application/json",
        }

        response = requests.post(self.api_url, json=payload, headers=headers)
        response.raise_for_status()
        data = response.json()

        # async with httpx.AsyncClient() as client:
        #     resp = await client.post(self.api_url, json=payload)
        #     resp.raise_for_status()
        #     data = resp.json()

        reasoning_block, answer = self._format_reasoning(data["answer"])

        # Add separators only if blocks exist
        if reasoning_block:
            reasoning_block += "\n<hr>\n"
        if answer:
            answer += "\n<hr>\n"

        # Collect unique source names from relevant documents
        source_names = set(
            doc.get("source") or doc.get("title") or "Unknown"
            for doc in data.get("relevant_docs", [])
        )

        # Format the answer with reasoning and relevant documents
        docs_block = (
            self._details_block(
                "Relevant Documents:",
                "\n".join(f"- {name} <br>" for name in source_names),
            )
            if source_names
            else ""
        )

        return "\n\n\n".join(
            block for block in (reasoning_block, answer, docs_block) if block
        )
