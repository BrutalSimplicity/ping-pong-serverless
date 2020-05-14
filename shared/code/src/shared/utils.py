from datetime import datetime
import functools
from typing import Any

def generate_timestamp():
    return datetime.utcnow().isoformat(timespec='milliseconds') + 'Z'

def pluck(obj, *args) -> Any:
    return tuple([obj[key] if key in obj else None for key in args])

def response_handler(success_fn=None, failure_fn=None):
    def decorator(func):
        @functools.wraps(func)
        def _wrapper(*args, **kwargs):
            try:
                result = func(*args, **kwargs)
                if success_fn:
                    return success_fn(result)

                return result
            except Exception as e:
                if failure_fn:
                    return failure_fn(e)

                raise e
        return _wrapper
    return decorator
