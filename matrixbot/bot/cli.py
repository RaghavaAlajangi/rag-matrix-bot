import asyncio
import datetime

from nio import AsyncClient, InviteEvent, LoginResponse, RoomMessageText

from .core.commands import CommandHandler
from .core.config import bot_config
from .core.history import RedisHistoryManager
from .core.logger import Logger
from .core.matrix_client import MatrixClient
from .core.rag_service import RAGService

logger = Logger(name="RAG Pipeline")


async def main():
    """Main function to run the Matrix bot."""

    # Use stored login creds if available
    use_saved_creds = bot_config.load_saved_login_creds()

    if use_saved_creds:
        logger.info("Using saved credentials.")
        nio_client = AsyncClient(
            homeserver=bot_config.homeserver,
            user=bot_config.username,
            device_id=bot_config.device_id,
            store_path=str(bot_config.store_path),
        )
        nio_client.access_token = bot_config.access_token
    else:
        logger.info("No saved credentials. Logging in with password.")
        nio_client = AsyncClient(
            homeserver=bot_config.homeserver,
            user=bot_config.username,
            store_path=str(bot_config.store_path),
        )
        # Login
        resp = await nio_client.login(
            bot_config.password, device_name=bot_config.nio_bot_name
        )

        if isinstance(resp, LoginResponse):
            logger.info("Login successful. Saving credentials.")
            bot_config.save_login_details(resp)
        else:
            logger.error(f"Login failed: {resp}")
            return

    matrix_client = MatrixClient(nio_client, bot_config)
    history = RedisHistoryManager(bot_config)
    rag = RAGService(bot_config)
    commands = CommandHandler(matrix_client, rag, history, bot_config, logger)

    # Joining time of the bot
    join_time = datetime.datetime.now()

    async def on_message(room, event):
        if event.sender == bot_config.username:
            return

        message_time = event.server_timestamp / 1000
        message_time = datetime.datetime.fromtimestamp(message_time)
        content = event.body.strip()
        sender = event.sender
        room_id = room.room_id

        if message_time > join_time:
            if content.startswith(".help"):
                await commands.handle_help(room_id=room_id)
            elif content.startswith(".reset"):
                await commands.handle_reset(
                    room_id=room_id,
                    user_id=sender,
                )
            else:
                await commands.handle_ai(
                    room_id=room_id,
                    user_id=sender,
                    query=content,
                )

    async def invite_callback(room, event):
        await nio_client.join(room.room_id)
        logger.info(
            f"{bot_config.nio_bot_name} joined DM room "
            f"{room.room_id} on invite"
        )

    nio_client.add_event_callback(invite_callback, InviteEvent)

    nio_client.add_event_callback(on_message, RoomMessageText)

    try:
        logger.info("Starting Matrix sync loop...")
        # full_state=True here to pull any room invites that occurred or
        # messages sent in rooms before this program connected to the
        # Matrix server
        await nio_client.sync_forever(timeout=30000, full_state=False)

    except (KeyboardInterrupt, asyncio.CancelledError):
        logger.info("Received exit signal, shutting down...")
    finally:
        logger.info("Closing Matrix client...")
        await nio_client.close()
