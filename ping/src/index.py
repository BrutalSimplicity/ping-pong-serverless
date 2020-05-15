import boto3
import time
import os
import logging

from shared.json import encoder, decoder
from shared.aws.xray import configure_xray
from shared.logging import log_it as log_handler, event_logger
from shared.aws.events import event as event_handler

configure_xray('ping-service')
PONG_ARN = os.environ['PONG_FUNCTION_ARN']
lmbda = boto3.client('lambda')
event_client = boto3.client('events')
event = event_handler(event_client, 'ping-service', 'service was called')
event_logger.setLevel(logging.INFO)
log_it = log_handler(level=logging.INFO)

@event
@log_it
def handler(event, context):
    start = time.perf_counter()
    response = lmbda.invoke(FunctionName=PONG_ARN)
    payload = decoder(response['Payload'].read())
    end = time.perf_counter()

    return {
        'statusCode': 200,
        'body': encoder({
            'Message': 'Ping',
            'Response': payload,
            'Timings': {
                'Start': start,
                'End': end,
                'Delta': end - start
            }
        })
    }
