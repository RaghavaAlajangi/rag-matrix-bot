import asyncio

from markdown import markdown
from nio import AsyncClient


class MatrixClient:
    def __init__(self, client: AsyncClient, config):
        self.client = client
        self.config = config

    async def send_message(self, room_id, message):
        markdown_format = markdown(
            message,
            extensions=[
                "extra",
                "fenced_code",
                "nl2br",
                "sane_lists",
                "tables",
                "codehilite",
            ],
        )
        await self.client.room_send(
            room_id=room_id,
            message_type="m.room.message",
            content={
                "msgtype": "m.text",
                "format": "org.matrix.custom.html",
                "body": message,
                "formatted_body": markdown_format,
            },
        )
        await asyncio.sleep(1)
