import logging
import redis
from .config import settings

log = logging.getLogger("aipos.cache")
_r = redis.from_url(settings.redis_url, decode_responses=True, socket_timeout=2)


def get(key):
    try:
        return _r.get(key)
    except redis.RedisError as e:
        log.warning("redis get failed: %s", e)


def set(key, value, ttl=86400):
    try:
        _r.set(key, value, ex=ttl)
    except redis.RedisError as e:
        log.warning("redis set failed: %s", e)


def hit_rate_limit(user_id: str) -> bool:
    try:
        k = f"rl:{user_id}"
        n = _r.incr(k)
        if n == 1:
            _r.expire(k, 60)
        return n > settings.rate_limit_per_min
    except redis.RedisError:
        return False  # redis down ho to bhi chat chalne do


def hit_daily_limit() -> bool:
    """Public demo ka kharcha rokne ke liye global daily cap."""
    if settings.demo_daily_limit <= 0:
        return False
    try:
        from datetime import date
        k = f"daily:{date.today().isoformat()}"
        n = _r.incr(k)
        if n == 1:
            _r.expire(k, 86400)
        return n > settings.demo_daily_limit
    except redis.RedisError:
        return False
