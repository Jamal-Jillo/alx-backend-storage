#!/usr/bin/env python3
""" web.py """


import redis
import requests
from functools import wraps
from typing import Callable


redis_store = redis.Redis()
"""Redis store."""


def request_tracker(method: Callable) -> Callable:
    """Tracks the number of requests made to a particular URL."""
    @wraps(method)
    def invoker(url) -> str:
        """The wrapper function for tracking the number of requests."""
        redis_store.incr(f'request_count:{url}')
        return method(url)
    return invoker


def data_cacher(method: Callable) -> Callable:
    """Caches the output of a particular URL."""
    @wraps(method)
    def invoker(url) -> str:
        """The wrapper function for caching the output of a URL."""
        redis_store.incr(f'fetch_count:{url}')
        result = redis_store.get(f'result:{url}')
        if result:
            return result.decode('utf-8')
        result = method(url)
        redis_store.set(f'fetch_count:{url}', 0)
        redis_store.setex(f'result:{url}', 10, result)
        return result
    return invoker


@request_tracker
@data_cacher
def get_page(url: str) -> str:
    """Fetches the content of a particular URL."""
    return requests.get(url).text
