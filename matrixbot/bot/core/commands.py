class CommandHandler:
    """
    Handles commands for the Matrix bot, including AI queries, resets, and
    help requests.

    Parameters
    ----------
    matrix_client : MatrixClient
        Instance of the Matrix client to send messages.
    rag_service : RAGService
        Service to handle retrieval-augmented generation queries.
    history_manager : RedisHistoryManager
        Instance of the history manager to store and retrieve conversation
        history.
    config : Config
        Configuration object containing bot settings.
    logger : Logger
        Logger instance for logging information and errors.
    """

    def __init__(
        self, matrix_client, rag_service, history_manager, config, logger
    ):
        self.matrix_client = matrix_client
        self.rag_service = rag_service
        self.history_manager = history_manager
        self.config = config
        self.logger = logger

    async def handle_ai(self, room_id, user_id, query):
        """
        Process AI-related commands and respond accordingly.

        Parameters
        ----------
        room_id : str
            Room ID where the command was issued.
        user_id : str
            User ID of the person who sent the query.
        query : str
            The query or prompt sent by the user.
        """
        await self.history_manager.add(room_id, user_id, "user", query)
        self.logger.info(f"Querying rag with prompt: {query}")
        chat_history = self.history_manager.get(room_id, user_id)

        response = await self.rag_service.query_model(
            query, chat_history, self.logger
        )
        await self.history_manager.add(room_id, user_id, "assistant", response)
        await self.matrix_client.send_message(room_id, response)

    async def handle_reset(self, room_id, user_id):
        """
        Reset the message history for a specific user in a channel.
        Parameters
        ----------
        room_id : str
            Room ID where the command was issued.
        user_id : str
            User ID of the person who sent the reset command.
        """
        await self.history_manager.reset(room_id, user_id)
        await self.matrix_client.send_message(
            room_id, f"{user_id} conversation history reset."
        )

    async def handle_help(self, room_id):
        """
        Display the help menu with available commands.
        Parameters
        ----------
        room_id : str
            Room ID where the command was issued.
        """
        help_message = """
        🤖 Available commands:
        ---------------------
        <prompt> - Generate AI response.
        .reset - Reset conversation.
        .help - Show help.
        """

        await self.matrix_client.send_message(room_id, help_message)
