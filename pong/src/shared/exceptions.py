class BaseHttpFormattedError(Exception):
    fmt = 'An unspecified error occurred'

    def __init__(self, *args, **kwargs):
        msg = self.fmt.format(*args, **kwargs)
        print(msg)
        super().__init__(self, msg)
        self.args = args
        self.kwargs = kwargs
        self.message = msg
        self.status_code = 500

    def __str__(self):
        return self.message
