import simplejson


def encoder(value):
    return simplejson.dumps(value, separators=(',', ':'), default=str)


def decoder(value):
    return simplejson.loads(value)
