import os


class Config:
    def __init__(self):
        self.homeserver = os.getenv("MATRIX_HOMESERVER")
        self.username = os.getenv("MATRIX_BOT_USERNAME")
        self.password = os.getenv("MATRIX_BOT_PASSWORD")
        self.rag_api_url = os.getenv("RAG_API_URL")
        self.rag_model = os.getenv("RAG_MODEL")
        self.history_size = int(os.getenv("HISTORY_SIZE", 30))


def load_config():
    return Config()
