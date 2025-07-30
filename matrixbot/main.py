import asyncio
import datetime

from nio import AsyncClient, InviteEvent, LoginResponse, RoomMessageText

from .commands import CommandHandler
from .config import load_config
from .history import HistoryManager
from .logger import Logger
from .matrix_client import MatrixClient
from .rag_service import RAGService

logger = Logger(name="RAG Pipeline")


async def main():
    config = load_config()

    # Use stored login creds if available
    use_saved_creds = config.load_saved_login_creds()

    if use_saved_creds:
        logger.info("Using saved credentials.")
        nio_client = AsyncClient(
            config.homeserver,
            config.username,
            device_id=config.device_id,
            store_path=str(config.store_path),
        )
        nio_client.access_token = config.access_token
    else:
        logger.info("No saved credentials. Logging in with password.")
        nio_client = AsyncClient(
            config.homeserver,
            config.username,
            store_path=str(config.store_path),
        )
        # Login
        resp = await nio_client.login(
            config.password, device_name=config.nio_bot_name
        )

        if isinstance(resp, LoginResponse):
            logger.info("Login successful. Saving credentials.")
            config.save_login_details(resp)
        else:
            logger.error(f"Login failed: {resp}")
            return

    nio_client = AsyncClient(config.homeserver, config.username)
    matrix_client = MatrixClient(nio_client, config)
    history = HistoryManager(config.history_size)
    rag = RAGService(config)
    commands = CommandHandler(matrix_client, rag, history, config, logger)

    # Joining time of the bot
    join_time = datetime.datetime.now()

    async def on_message(room, event):
        if event.sender == config.username:
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
                    user=sender,
                )
            else:
                await commands.handle_ai(
                    room_id=room_id,
                    query=content,
                    user=sender,
                )

    async def invite_callback(room, event):
        await nio_client.join(room.room_id)
        logger.info(f"RAGbot joined DM room {room.room_id} on invite")

    nio_client.add_event_callback(invite_callback, InviteEvent)

    nio_client.add_event_callback(on_message, RoomMessageText)

    try:
        logger.info("Starting Matrix sync loop...")
        # full_state=True here to pull any room invites that occurred or
        # messages sent in rooms before this program connected to the
        # Matrix server
        await nio_client.sync_forever(timeout=30000, full_state=True)

    except (KeyboardInterrupt, asyncio.CancelledError):
        logger.info("Received exit signal, shutting down...")
    finally:
        logger.info("Closing Matrix client...")
        await nio_client.close()
