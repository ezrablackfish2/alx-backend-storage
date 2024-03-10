#!/usr/bin/env python3
"""
Module Writting to redis
"""
from functools import wraps
import redis
from typing import Union, Callable, Optional
from uuid import uuid4


def replay(cache_method: Callable) -> None:
    """
    Displays the history of calls of a particular function
    """
    input_key = cache_method.__qualname__ + ':inputs'
    output_key = cache_method.__qualname__ + ':outputs'

    print(cache_method.__qualname__ + ' was called {} times:'.format(
        cache_method.__self__._redis.get(cache_method.__qualname__).decode()))

    inputs_lst = cache_method.__self__._redis.lrange(input_key, 0, -1)
    outputs_lst = cache_method.__self__._redis.lrange(output_key, 0, -1)

    for inp, out in zip(inputs_lst, outputs_lst):
        print("{}(*{})".format(
            cache_method.__qualname__, eval(inp.decode())))


def call_history(method: Callable) -> Callable:
    """
    Decorator that stores the history of inputs and outputs of a function
    """
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        input_key = method.__qualname__ + ':inputs'

        self._redis.rpush(input_key, str(args))

        output = method(self, *args, **kwargs)

        output_key = method.__qualname__ + ':outputs'
        self._redis.rpush(output_key, str(output))

        return output

    return wrapper


def count_calls(method: Callable) -> Callable:

    """
    Decorator that takes a single method and returns a Callable
    """
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        key = method.__qualname__
        self._redis.incr(key)

        return method(self, *args, **kwargs)

    return wrapper


class Cache:
    """
    Redis Client Object
    """
    def __init__(self):
        self._redis = redis.Redis()
        self._redis.flushdb()

    @count_calls
    @call_history
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """
        Stores the input data in a redis with a random key
        and returns the key
        """
        key = str(uuid4())
        self._redis.set(key, data)

        return key

    def get(self, key: str, fn:
            Optional[Callable] = None) -> Union[str, bytes, int, float]:
        """
        Used to convert back to the desired type
        """
        value = self._redis.get(key)

        if fn is None or value is None:
            return value

        return fn(value)

    def get_str(self, key: str) -> str:
        """
        Get a string from the Cache
        """
        value = self._redis.get(key)

        return value.decode('utf-8')

    def get_int(self, key: str) -> int:
        """
        Get an integer from the Cache
        """
        value = self._redis.get(key)
        try:
            value = int(value.decode('utf-8'))

        except ValueError:
            value = 0

        return value
