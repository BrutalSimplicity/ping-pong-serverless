from typing import Any, NamedTuple
import boto3
import time
import os
import logging

from boto3_type_annotations.lambda_ import Client as LambdaClient
from shared.json import encoder, decoder
from shared.aws.xray import configure_xray
from shared.logging import log_it as log_handler, event_logger
from shared.aws.events import event as event_handler

configure_xray('ping-service')
PONG_ARN = os.environ['PONG_FUNCTION_ARN']
lmbda: LambdaClient = boto3.client('lambda')
event_client = boto3.client('events')
event = event_handler(event_client, 'ping-service', 'service was called')
event_logger.setLevel(logging.INFO)
log_it = log_handler(level=logging.INFO)


class PingModel(NamedTuple):
    class TimingsModel(NamedTuple):
        Start: float
        End: float
        Delta: float

    Message: str
    Response: Any
    Timings: TimingsModel
    Event: object

@event
@log_it
def handler(event, context):
    start = time.perf_counter()
    response = lmbda.invoke(FunctionName=PONG_ARN)
    payload = decoder(response['Payload'].read())
    end = time.perf_counter()

    response = PingModel(
        Message='Ping',
        Response=payload,
        Timings=PingModel.TimingsModel(
            Start=start,
            End=end,
            Delta=end - start
        ),
        Event=event
    )

    return {
        'statusCode': 200,
        'body': encoder(response)
    }
