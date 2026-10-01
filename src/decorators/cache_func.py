import time
from functools import lru_cache


@lru_cache
def func_meme():
    time.sleep(10)
    return "Доброе утро"

print(func_meme())

print(func_meme())

print(func_meme())