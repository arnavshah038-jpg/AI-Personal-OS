import json
from datetime import datetime

from app.database.redis_client import redis_client
from app.utils.logger import logger


class ChatMemory:

    @staticmethod
    def save_message(session_id: str, role: str, message: str):

        key = f"chat:{session_id}"

        message_data = {
            "role": role,
            "content": message,
            "timestamp": datetime.utcnow().isoformat()
        }

        redis_client.rpush(
            key,
            json.dumps(message_data)
        )

        # Expire after 24 hours
        redis_client.expire(key, 86400)

        logger.info(
            f"Message saved to Redis | Session={session_id}"
        )

    @staticmethod
    def get_messages(session_id: str):

        key = f"chat:{session_id}"

        messages = redis_client.lrange(key, 0, -1)

        logger.info(
            f"Loaded {len(messages)} messages | Session={session_id}"
        )

        return messages

    @staticmethod
    def build_openai_history(session_id: str):

        history = []

        messages = ChatMemory.get_messages(session_id)

        for item in messages:

            data = json.loads(item)

            history.append(
                {
                    "role": data["role"],
                    "content": data["content"]
                }
            )

        return history

    @staticmethod
    def should_summarize(session_id: str) -> bool:

        key = f"chat:{session_id}"

        total_messages = redis_client.llen(key)

        return total_messages >= 20