import asyncio

from markdown import markdown
from nio import AsyncClient


class MatrixClient:
    def __init__(self, client: AsyncClient, config):
        self.client = client
        self.config = config

    async def send_message(self, room_id, message, return_event_id=False):
        """Send a markdown-formatted message.

        Parameters
        ----------
        room_id : str
            Room ID to send the message to.
        message : str
            Plaintext message.
        """
        markdown_format = markdown(
            message,
            extensions=[
                "extra",
                "fenced_code",
                "nl2br",
                "sane_lists",
                "tables",
                "codehilite",
                "md_in_html",
            ],
        )
        response = await self.client.room_send(
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
        if return_event_id:
            return response.event_id

    async def edit_message(self, room_id, event_id, new_message):
        """Replace existing message based on event_id.

        Parameters
        ----------
        room_id : str
            Room ID to send the message to.
        event_id : str
            Message ID that needs to be replaced.
        new_message : str
            Plaintext/makdown message.
        """
        markdown_format = markdown(
            new_message,
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
                "body": new_message,
                "format": "org.matrix.custom.html",
                "formatted_body": markdown_format,
                "m.new_content": {
                    "msgtype": "m.text",
                    "body": new_message,
                    "format": "org.matrix.custom.html",
                    "formatted_body": markdown_format,
                },
                "m.relates_to": {
                    "rel_type": "m.replace",
                    "event_id": event_id,
                },
            },
        )
