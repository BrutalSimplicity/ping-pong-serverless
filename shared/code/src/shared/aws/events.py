from typing import Any, Mapping, Optional, Callable, List
from shared.utils import generate_timestamp
from shared.json import encoder
import functools


def filter_empty_properties(mapping):
    return {k: v for k, v in mapping.items() if v}


def sns_event(sns_client: Any, topic_arn: str, subject: Optional[str] = None,
              encoder: Callable[[Any], Any] = encoder):
    def decorator(func):
        @functools.wraps(func)
        def _wrapper(*args, **kwargs):
            result = func(*args, **kwargs)
            if result:
                if (isinstance(result, Mapping)):
                    result = filter_empty_properties(result)
                params = {
                    'TopicArn': topic_arn,
                    'Subject': subject,
                    'Message': encoder(result)
                }
                params = filter_empty_properties(params)
                sns_client.publish(**params)

            return result
        return _wrapper
    return decorator

def event(event_bridge_client: Any, source: str, detail_type: str, event_bus_name: str = None,
          resources: List[str] = [], time: str = generate_timestamp(), encoder: Callable[[Any], Any] = encoder):
    def decorator(func):
        @functools.wraps(func)
        def _wrapper(*args, **kwargs):
            result = func(*args, **kwargs)
            if result:
                if (isinstance(result, Mapping)):
                    result = filter_empty_properties(result)
                entry = {
                    'Source': source,
                    'Detail': encoder(result),
                    'DetailType': detail_type,
                    'EventBusName': event_bus_name,
                    'Resources': resources,
                    'Time': time
                }
                entry = filter_empty_properties(entry)
                event_bridge_client.put_events(
                    Entries=[entry]
                )

            return result
        return _wrapper
    return decorator
