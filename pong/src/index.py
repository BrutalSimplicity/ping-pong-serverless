from shared.aws.xray import configure_xray
from shared.logging import log_it

configure_xray('pong-service')

@log_it
def handler(event, context):
    return {
        'statusCode': 200,
        'Message': 'Pong'
    }
