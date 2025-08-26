import json

import redis


class RedisHistoryManager:
    """
    Manages conversation history using Redis for persistence.
    """

    def __init__(self, config):
        self.redis_client = redis.StrictRedis(
            host=config.redis_host,
            port=config.redis_port,
            db=config.redis_db,
            decode_responses=True,
        )
        self.history_size = config.redis_history_size

    def _get_history_key(self, room_id, user_id):
        """Generates a unique Redis key for a user's history."""
        return f"history:{room_id}:{user_id}"

    def get(self, room_id, user_id):
        """Retrieve the conversation history for a user."""
        key = self._get_history_key(room_id, user_id)
        # LTRIM keeps the list at the specified history_size
        self.redis_client.ltrim(key, -self.history_size, -1)
        # LPUSH pushes new items to the left, so we need to reverse
        # the list when we retrieve it to get chronological order.
        history = [
            json.loads(msg) for msg in self.redis_client.lrange(key, 0, -1)
        ]
        return history

    async def reset(self, room_id, user_id):
        """Clear the history for a user."""
        key = self._get_history_key(room_id, user_id)
        self.redis_client.delete(key)

    async def add(self, room_id, user_id, role, content):
        """Add a message to the history."""
        key = self._get_history_key(room_id, user_id)
        message = json.dumps({"role": role, "content": content})
        self.redis_client.rpush(key, message)
        # Trim the list to ensure we don't exceed the history size
        self.redis_client.ltrim(key, -self.history_size, -1)


if __name__ == "__main__":
    from config import bot_config

    his = RedisHistoryManager(bot_config)

    async def test():
        await his.add("room1", "user", "Hello", "user1")
        await his.add("room1", "assistant", "Hi there!", "user1")

        print(his.get("room1", "user1"))

    import asyncio

    asyncio.run(test())
