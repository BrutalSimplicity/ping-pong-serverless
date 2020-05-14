from shared.json import encoder

def handler(event, context):
    return {
        'statusCode': 200,
        'body': encoder({
            'Message': 'Ping',
            'event': event
        })
    }