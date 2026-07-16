import redis

from app.utils.logger import logger


try:
    redis_client = redis.Redis(
        host="localhost",
        port=6379,
        db=0,
        decode_responses=True
    )

    redis_client.ping()
    logger.info("✅ Connected to Valkey (Redis) successfully.")

except Exception as e:
    logger.error(f"❌ Redis Connection Failed: {e}")
    raise