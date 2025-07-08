class CommandHandler:
    def __init__(
        self, matrix_client, rag_service, history_manager, config, logger
    ):
        self.matrix_client = matrix_client
        self.rag_service = rag_service
        self.history_manager = history_manager
        self.config = config
        self.logger = logger

    async def handle_ai(self, room_id, message_parts, sender):
        prompt = " ".join(message_parts[1:])
        await self.history_manager.add("user", room_id, prompt, sender)
        self.logger.info(f"Querying rag with prompt: {prompt}")
        chat_history = self.history_manager.get(room_id, sender)
        response = await self.rag_service.query_model(
            prompt, chat_history, self.logger
        )
        await self.history_manager.add("assistant", room_id, response, sender)
        await self.matrix_client.send_message(room_id, response)

    async def handle_reset(self, room_id, sender):
        await self.history_manager.reset(room_id, sender)
        await self.matrix_client.send_message(
            room_id, f"{sender} conversation history reset."
        )

    async def handle_help(self, room_id):
        help_message = """
        🤖 Available commands:\n
        -------------------\n
        <prompt> - Generate AI response.\n
        .reset - Reset conversation.\n
        .help - Show help.\n
        """

        await self.matrix_client.send_message(room_id, help_message)
