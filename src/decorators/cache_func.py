from functools import lru_cache
import time

@lru_cache
def func_meme():
    time.sleep(10)
    return "8-800-555-35-35"

print(func_meme())

print(func_meme())

print(func_meme())