class CommandHandler:
    def __init__(
        self, matrix_client, rag_service, history_manager, config, logger
    ):
        self.matrix_client = matrix_client
        self.rag_service = rag_service
        self.history_manager = history_manager
        self.config = config
        self.logger = logger

    async def handle_ai(self, channel, message_parts, sender):
        prompt = " ".join(message_parts[1:])
        await self.history_manager.add("user", channel, prompt, sender)
        self.logger.info(f"Querying rag with prompt: {prompt}")
        chat_history = self.history_manager.get(channel, sender)
        response = await self.rag_service.query_model(
            prompt, chat_history, self.logger
        )
        await self.history_manager.add("assistant", channel, response, sender)
        await self.matrix_client.send_message(channel, response)

    async def handle_reset(self, channel, sender):
        await self.history_manager.reset(channel, sender)
        await self.matrix_client.send_message(
            channel, f"@{sender} conversation history reset."
        )

    async def handle_help(self, channel):
        help_message = """
        🤖 **Available commands:**\n
        .ai <prompt> - Generate AI response.\n
        .reset - Reset conversation.\n
        .help - Show help.\n
        """

        await self.matrix_client.send_message(channel, help_message)
