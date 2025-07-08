import asyncio
import datetime

from nio import AsyncClient, InviteEvent, RoomMessageText

from .commands import CommandHandler
from .config import load_config
from .history import HistoryManager
from .logger import Logger
from .matrix_client import MatrixClient
from .rag_service import RAGService

logger = Logger(name="RAG Pipeline")


async def main():
    config = load_config()

    nio_client = AsyncClient(config.homeserver, config.username)
    matrix_client = MatrixClient(nio_client, config)
    history = HistoryManager()
    rag = RAGService(config)
    commands = CommandHandler(matrix_client, rag, history, config, logger)

    # Login to Matrix
    logger.info("Logging in...")
    await nio_client.login(config.password, device_name="RAGbot")
    join_time = datetime.datetime.now()

    async def on_message(room, event):
        if event.sender == config.username:
            return

        message_time = event.server_timestamp / 1000
        message_time = datetime.datetime.fromtimestamp(message_time)
        content = event.body.strip()
        sender = event.sender

        if message_time > join_time:
            if content.startswith(".help"):
                await commands.handle_help(channel=room.room_id)
            elif content.startswith(".reset"):
                await commands.handle_reset(
                    channel=room.room_id,
                    sender=sender,
                )
            else:
                await commands.handle_ai(
                    channel=room.room_id,
                    message_parts=content.split(),
                    sender=sender,
                )

    async def invite_callback(room, event):
        await nio_client.join(room.room_id)
        logger.info(f"RAGbot joined DM room {room.room_id} on invite")

    nio_client.add_event_callback(invite_callback, InviteEvent)

    nio_client.add_event_callback(on_message, RoomMessageText)

    try:
        logger.info("Starting Matrix sync loop...")
        await nio_client.sync_forever(timeout=30000, full_state=True)
    except (KeyboardInterrupt, asyncio.CancelledError):
        logger.info("Received exit signal, shutting down...")
    finally:
        logger.info("Logging out and closing Matrix client...")
        await nio_client.logout()
        await nio_client.close()
