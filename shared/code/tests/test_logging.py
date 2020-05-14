import unittest
from shared.logging import JsonLogFormatter, log_it
import logging


class MockLoggingHandler(logging.Handler):
    def __init__(self):
        super().__init__(logging.DEBUG)
        self.log_records = []

    def emit(self, record):
        self.log_records.append(record)

    def get_log_records(self):
        return self.log_records


testLogger = logging.getLogger('test')
testLogger.setLevel(logging.DEBUG)


class LoggingTests(unittest.TestCase):

    def setUp(self):
        self.maxDiff = None
        self.mockHandler = MockLoggingHandler()
        self.mockHandler.setFormatter(JsonLogFormatter())
        testLogger.addHandler(self.mockHandler)

    def tearDown(self):
        testLogger.removeHandler(self.mockHandler)

    def test_should_log_decorated_method(self):

        @log_it(logger=testLogger)
        def action():
            pass

        action()

        expected = {
            'event': 'action',
            'message': 'action was called',
            'level': 'DEBUG',
            'caller': 'action',
            'parameters': '()',
            'input': {
                'args': (),
                'kwargs': {}
            },
            'output': None
        }
        actual = self.mockHandler.get_log_records()[0].msg

        self.assertDictEqual(actual, expected)

    def test_should_log_decorated_method_with_parameters(self):
        @log_it(logger=testLogger)
        def action(a, b, c):
            pass

        action(1, 2, 3)

        expected = {
            'event': 'action',
            'message': 'action was called',
            'level': 'DEBUG',
            'caller': 'action',
            'parameters': '(a, b, c)',
            'input': {
                'args': (1, 2, 3),
                'kwargs': {}
            },
            'output': None
        }
        actual = self.mockHandler.get_log_records()[0].msg

        self.assertDictEqual(actual, expected)

    def test_should_log_decorated_method_with_return_value(self):
        @log_it(logger=testLogger)
        def action(a, b, c, k1=1, k2=2):
            return {
                'foo': 'bar',
                'bar': 'foo'
            }

        action(1, 2, 3)

        expected = {
            'event': 'action',
            'message': 'action was called',
            'level': 'DEBUG',
            'caller': 'action',
            'parameters': '(a, b, c, k1=1, k2=2)',
            'input': {
                'args': (1, 2, 3),
                'kwargs': {}
            },
            'output': {
                'foo': 'bar',
                'bar': 'foo'
            }
        }
        actual = self.mockHandler.get_log_records()[0].msg

        self.assertDictEqual(actual, expected)

    def test_should_log_decorated_method_with_kwargs(self):
        @log_it(logger=testLogger, level=logging.WARNING)
        def action(a, b, c, **kwargs):
            return {
                'foo': 'bar',
                'bar': 'foo'
            }

        action(1, 2, 3, k4=4, k5=5)

        expected = {
            'event': 'action',
            'message': 'action was called',
            'level': 'WARNING',
            'caller': 'action',
            'parameters': '(a, b, c, **kwargs)',
            'input': {
                'args': (1, 2, 3),
                'kwargs': {
                    'k4': 4,
                    'k5': 5
                }
            },
            'output': {
                'foo': 'bar',
                'bar': 'foo'
            }
        }
        actual = self.mockHandler.get_log_records()[0].msg

        self.assertDictEqual(actual, expected)

    def test_should_log_nested_scopes(self):
        @log_it(logger=testLogger, level=logging.INFO, event='nested_event')
        def nested2(a, b):
            return a + b

        def nested1():
            return nested2(1, 2)

        @log_it(logger=testLogger, level=logging.DEBUG)
        def action(a, b, c, **kwargs):
            result = nested1()
            return {
                'foo': 'bar',
                'bar': 'foo',
                'nested': result
            }

        action(1, 2, 3, k4=4, k5=5)

        expected = [
            {
                'event': 'nested_event',
                'message': 'nested2 was called',
                'level': 'INFO',
                'caller': 'nested2',
                'parameters': '(a, b)',
                'input': {
                    'args': (1, 2),
                    'kwargs': {}
                },
                'output': 3
            },
            {
                'event': 'action',
                'message': 'action was called',
                'level': 'DEBUG',
                'caller': 'action',
                'parameters': '(a, b, c, **kwargs)',
                'input': {
                    'args': (1, 2, 3),
                    'kwargs': {
                        'k4': 4,
                        'k5': 5
                    }
                },
                'output': {
                    'foo': 'bar',
                    'bar': 'foo',
                    'nested': 3
                }
            }
        ]
        actual = [record.msg for record in self.mockHandler.get_log_records()]

        self.assertCountEqual(actual, expected)

    def test_should_log_exception(self):
        error = RuntimeError('oops')
        @log_it(logger=testLogger)
        def action(a, b, c):
            raise error

        with self.assertRaises(RuntimeError):
            action(1, 2, 3)

        expected = {
            'event': 'RuntimeError',
            'message': error,
            'level': 'ERROR',
            'caller': 'action',
            'parameters': '(a, b, c)',
            'input': {
                'args': (1, 2, 3),
                'kwargs': {}
            }
        }
        actual = self.mockHandler.get_log_records()[0].msg

        self.assertTrue(actual['stack_trace'].startswith('Traceback'))
        del actual['stack_trace']

        self.assertDictEqual(actual, expected)

    def test_should_log_nested_exception_only_once(self):
        error = RuntimeError('oops')

        @log_it(logger=testLogger)
        def nested2(a, b):
            raise error

        def nested1():
            return nested2(1, 2)

        @log_it(logger=testLogger)
        def action(a, b, c):
            nested1()

        with self.assertRaises(RuntimeError):
            action(1, 2, 3)

        expected = [{
            'event': 'RuntimeError',
            'message': error,
            'level': 'ERROR',
            'caller': 'nested2',
            'parameters': '(a, b)',
            'input': {
                'args': (1, 2),
                'kwargs': {}
            }
        }]
        actual = [self.mockHandler.get_log_records()[0].msg]

        self.assertTrue(actual[0]['stack_trace'].startswith('Traceback'))
        del actual[0]['stack_trace']

        self.assertCountEqual(actual, expected)
