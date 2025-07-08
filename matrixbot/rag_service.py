import requests


class RAGService:
    def __init__(self, config):
        self.api_url = config.rag_api_url
        self.model = config.rag_model

    async def query_model(self, prompt, chat_history, logger):
        # async with aiohttp.ClientSession() as session:
        payload = {
            "model": self.model,
            "prompt": prompt,
            "chat_history": chat_history,
        }
        # async with session.post(self.api_url, json=payload) as resp:
        #     data = await resp.json()
        #     response_text = data.get("answer", "").strip()

        response = requests.post(self.api_url, json=payload)
        response.raise_for_status()
        data = response.json()

        response_text = data["answer"]

        # Check for different types of thought/solution delimiters
        if "<think>" in response_text:
            thinking, response_text = response_text.split("</think>")
            thinking = thinking.strip("<think>").strip()
            logger.info(f"Model thinking for: {thinking}")
        if "<|begin_of_thought|>" in response_text:
            parts = response_text.split("<|end_of_thought|>")
            if len(parts) > 1:
                thinking = (
                    parts[0]
                    .strip("<|begin_of_thought|>")
                    .strip("<|end_of_thought|>")
                )
                response_text = parts[1]
                self.log(f"Model thinking for: {thinking}")

        # Check for solution delimiters and clean them up
        if "<|begin_of_solution|>" in response_text:
            parts = response_text.split("<|end_of_solution|>")
            response_text = parts[0].split("<|begin_of_solution|>")[1].strip()

        docs = list(
            set(f"- <{doc['source']}>" for doc in data["relevant_docs"])
        )
        src_docs = "\n ### Source Docements:\n" + "\n".join(docs)

        response_text = response_text + src_docs

        return response_text.strip()
