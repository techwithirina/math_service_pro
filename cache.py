# cache.py
import threading
import time
import os


# Thread-safe cache dictionary: { key: (result, timestamp) }
cache_lock = threading.Lock()
math_cache = {}


# Default TTL in seconds (can be set via env var or default to 60s)
CACHE_TTL_SECONDS = int(os.getenv("CACHE_TTL_SECONDS", 60))


def get_cached_result(key: str):
    with cache_lock:
        item = math_cache.get(key)
        if not item:
            return None

        result, timestamp = item
        if (time.time() - timestamp) > CACHE_TTL_SECONDS:
            # Expired
            del math_cache[key]
            return None

        return result


def set_cached_result(key: str, result):
    with cache_lock:
        math_cache[key] = (result, time.time())
