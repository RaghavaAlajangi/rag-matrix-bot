import json
import os
from pathlib import Path

from dotenv import load_dotenv
from nio import LoginResponse

load_dotenv()
resources_path = Path(__file__).parents[2] / "resources"


class Config:
    """Configuration class for the Matrix bot."""

    def __init__(self):
        # Matrix variables (bot user)
        self.homeserver = os.getenv("MATRIX_HOMESERVER")
        self.username = os.getenv("MATRIX_BOT_USERNAME")
        self.password = os.getenv("MATRIX_BOT_PASSWORD")
        self.nio_bot_name = os.getenv("MATRIX_BOT_NAME")

        # RAG variables (FastAPI service)
        self.rag_api_url = os.getenv("RAG_API_URL")
        self.rag_model = os.getenv("RAG_MODEL")
        self.history_size = int(os.getenv("HISTORY_SIZE", 30))
        self.rag_api_url_key = os.getenv("RAG_API_KEY")

        # User history (Redis)
        self.redis_host = os.getenv("REDIS_HOST")
        self.redis_port = int(os.getenv("REDIS_PORT"))
        self.redis_db = int(os.getenv("REDIS_DB"))
        self.redis_history_size = int(os.getenv("REDIS_HISTORY_SIZE"))

        # Login credentials (saved after first login for reuse)
        self.access_token = None
        self.device_id = None
        self.json_path = resources_path / "login_creds.json"
        self.store_path = resources_path / "nio_store"
        self.store_path.mkdir(exist_ok=True)

    def load_saved_login_creds(self):
        """Load saved credentials from local json file."""
        if not self.json_path.exists():
            return False
        with open(self.json_path, "r") as f:
            credentials = json.load(f)
            self.username = credentials["user_id"]
            self.device_id = credentials["device_id"]
            self.access_token = credentials["access_token"]
            self.homeserver = credentials["homeserver"]
        return True

    def save_login_details(self, response: LoginResponse):
        """Writes the required login details to disk so we can log in later
        without using a password.

        Parameters
        ----------
        response : LoginResponse
            The successful client login response.
        """
        with open(self.json_path, "w") as file:
            json.dump(
                {
                    "homeserver": self.homeserver,
                    "user_id": response.user_id,
                    "device_id": response.device_id,
                    "access_token": response.access_token,
                },
                file,
                indent=4,
            )


bot_config = Config()
