# from collections import defaultdict


class HistoryManager:
    """
    Manages conversation history for users in different rooms.
    """

    def __init__(self, history_size=30):
        self.histories = {}
        self.history_size = history_size

    def get(self, room_id, user):
        return self.histories[room_id][user]

    async def reset(self, room_id, user):
        """
        Clear the history for a user.

        Parameters
        ----------
        room_id : str
            Room ID.
        user : str
            User ID.
        """
        self.histories[room_id][user] = []

    async def add(self, role, room_id, content, user):
        """
        Add a message to the history.

        Parameters
        ----------
        role : str
            "user", "assistant", or "system".
        room_id : str
            Room ID.
        content : str
            Message content.
        user : str
            User ID.
        """
        if room_id not in self.histories:
            self.histories[room_id] = {}

        if user not in self.histories[room_id]:
            self.histories[room_id][user] = []

        self.histories[room_id][user].append(
            {"role": role, "content": content}
        )
        # Ensure we do not exceed the history size
        if len(self.histories[room_id][user]) > self.history_size:
            self.histories[room_id][user].pop(0)
