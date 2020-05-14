import inspect
from time import perf_counter
import traceback
import functools
import sys
from datetime import datetime
import logging

from logging import StreamHandler
from shared.json import encoder


class JsonLogFormatter(logging.Formatter):
    def format(self, record):
        if isinstance(record.msg, str):
            message = super().format(record)
            return encoder({
                'message': message,
                'timestamp': datetime.utcfromtimestamp(record.created).strftime('%y-%m-%dT%h:%M%S'),
                'level': record.levelname
            })
        else:
            return encoder(record.msg)


event_logger = logging.getLogger('shared.logging.event_logger')
event_logger.handlers.clear()
handler = StreamHandler(sys.stderr)
handler.setFormatter(JsonLogFormatter())
event_logger.addHandler(handler)
event_logger.propagate = False

def log_it(_func=None, *, event: str = None, message: str = None,
           level: int = logging.DEBUG, timeit=False, logger=event_logger):

    @functools.wraps(_func)
    def logit_decorator(func):
        def get_func_parameters():
            try:
                return str(inspect.signature(func))
            except Exception:
                return None

        @functools.wraps(func)
        def _wrapper(*args, **kwargs):
            try:
                start = perf_counter()
                result = func(*args, **kwargs)
                stop = perf_counter()

                actual_event = event or func.__name__
                actual_message = message or f'{func.__name__} was called'
                event_details = {
                    'event': actual_event,
                    'message': actual_message,
                    'level': logging.getLevelName(level),
                    'caller': func.__name__,
                    'parameters': get_func_parameters(),
                    'input': {
                        'args': args,
                        'kwargs': kwargs
                    },
                    'output': result
                }

                if timeit:
                    event_details['duration_secs'] = stop - start

                logger.log(level, event_details)

                return result

            except Exception as err:
                # Only log the exception if you are the first
                # to handle it - else - just pass it along.
                # This prevents logging the same exception
                # multiple times.
                if not hasattr(err, '_already_handled'):
                    setattr(err, '_already_handled', True)
                    logger.log(logging.ERROR, {
                        'event': type(err).__name__,
                        'message': err,
                        'level': 'ERROR',
                        'stack_trace': traceback.format_exc(),
                        'caller': func.__name__,
                        'parameters': get_func_parameters(),
                        'input': {
                            'args': args,
                            'kwargs': kwargs
                        }
                    })

                raise err
        return _wrapper

    if _func is None:
        return logit_decorator
    else:
        return logit_decorator(_func)
