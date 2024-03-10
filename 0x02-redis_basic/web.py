#!/usr/bin/env python3
"""
web
"""
from functools import wraps
import redis
import requests
from typing import Callable


_redis = redis.Redis()


def count_requests(method: Callable) -> Callable:
    """
    Counts the request for a specific get request
    """
    @wraps(method)
    def wrapper(url):
        """ Wrapper """
        _redis.incr("count:{}".format(url))

        cached_html = _redis.get("cached:{}".format(url))
        if cached_html:
            return cached_html.decode('utf-8')

        html = method(url)
        _redis.setex("cached:{}".format(url), 10, html)

        return html

    return wrapper


@count_requests
def get_page(url: str) -> str:
    """
    Obtain the HTML content of a particular URL and returns it
    """
    res = requests.get(url)

    return res.text
