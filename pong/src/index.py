import logging
import boto3

from shared.aws.xray import configure_xray
from shared.logging import log_it as log_handler, event_logger
from shared.aws.events import event as event_handler

configure_xray('pong-service')
event_client = boto3.client('events')
event = event_handler(event_client, 'ping-service', 'service was called')
event_logger.setLevel(logging.INFO)
log_it = log_handler(level=logging.INFO)

@event
@log_it
def handler(event, context):
    return {
        'statusCode': 200,
        'Message': 'Pong'
    }
