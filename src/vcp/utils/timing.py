import time
from functools import wraps


def timed(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        print(f"[{func.__name__.capitalize()}] Started")
        function = func(*args, **kwargs)
        print(
            f"[{func.__name__.capitalize()}] Finished in Timed: {time.time() - start:.2f}s"
        )
        return function

    return wrapper
