#!/usr/bin/env python3
""" 102-log_stats.py """


import uuid
import redis
from functools import wraps
from typing import Any, Callable, Union


def increment_counter(method: Callable) -> Callable:
    """Increments the call counter of a Cache class method."""
    @wraps(method)
    def wrapper(self, *args, **kwargs) -> Any:
        """Increments the call counter and returns the method's output."""
        if isinstance(self._redis, redis.Redis):
            self._redis.incr(method.__name__)
        return method(self, *args, **kwargs)
    return wrapper


def track_history(method: Callable) -> Callable:
    """Tracks the call history of a Cache class method."""
    @wraps(method)
    def wrapper(self, *args, **kwargs) -> Any:
        """Stores input and output of the method and returns its output."""
        input_key = f'{method.__name__}:inputs'
        output_key = f'{method.__name__}:outputs'
        if isinstance(self._redis, redis.Redis):
            self._redis.rpush(input_key, str(args))
        output = method(self, *args, **kwargs)
        if isinstance(self._redis, redis.Redis):
            self._redis.rpush(output_key, output)
        return output
    return wrapper


def display_history(fn: Callable) -> None:
    """Displays the call history of a Cache class method."""
    if not fn or not hasattr(fn, '__self__'):
        return
    redis_store = getattr(fn.__self__, '_redis', None)
    if not isinstance(redis_store, redis.Redis):
        return
    fn_name = fn.__name__
    input_key = f'{fn_name}:inputs'
    output_key = f'{fn_name}:outputs'
    call_count = 0
    if redis_store.exists(fn_name) != 0:
        call_count = int(redis_store.get(fn_name))
    print(f'{fn_name} was called {call_count} times:')
    inputs = redis_store.lrange(input_key, 0, -1)
    outputs = redis_store.lrange(output_key, 0, -1)
    for i, o in zip(inputs, outputs):
        print(f'{fn_name}(*{i.decode("utf-8")}) -> {o}')


class Cache:
    """Represents an object for storing data in a Redis data storage."""
    def __init__(self) -> None:
        """Initializes a Cache instance."""
        self._redis = redis.Redis()
        self._redis.flushdb()

    @track_history
    @increment_counter
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """Stores a value in Redis and returns the key."""
        data_key = str(uuid.uuid4())
        self._redis.set(data_key, data)
        return data_key

    def get(
            self,
            key: str,
            transform: Callable = None,
            ) -> Union[str, bytes, int, float]:
        """Retrieves a value from Redis."""
        data = self._redis.get(key)
        return transform(data) if transform is not None else data

    def get_str(self, key: str) -> str:
        """Retrieves a string value from Redis."""
        return self.get(key, lambda x: x.decode('utf-8'))

    def get_int(self, key: str) -> int:
        """Retrieves an integer value from Redis."""
        return self.get(key, lambda x: int(x))
