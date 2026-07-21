import redis

from app.core.config import settings
from app.utils.logger import logger

try:
    redis_client = redis.Redis(
        host=settings.REDIS_HOST,
        port=settings.REDIS_PORT,
        db=0,
        decode_responses=True
    )

    redis_client.ping()
    logger.info("✅ Connected to Redis successfully.")

except Exception as e:
    logger.error(f"❌ Redis Connection Failed: {e}")
    raise