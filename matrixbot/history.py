# from collections import defaultdict


class HistoryManager:
    def __init__(self, history_size=30):
        self.histories = {}
        self.history_size = history_size

    async def reset_history(self, room_id, user):
        self.histories[room_id] = {}
        self.histories[room_id][user] = []

    async def add(self, role, room_id, content, user):
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

    async def get_history(self, room_id, user):
        return self.histories[room_id][user]
