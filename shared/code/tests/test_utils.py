import unittest

from shared.utils import response_handler, pluck

class UtilsTests(unittest.TestCase):

    def test_response_handler_should_handle_successful_response(self):
        response = {
            'Success': True
        }
        def on_success(result):
            return result

        @response_handler(on_success)
        def action():
            return response

        output = action()

        self.assertCountEqual(output, response)

    def test_response_handler_should_handle_failed_response(self):
        class FailedError(Exception):
            pass

        def on_failure(e):
            return True

        @response_handler(failure_fn=on_failure)
        def action():
            raise FailedError

        failed = action()

        self.assertTrue(failed)

    def test_pluck_should_grab_values_for_keys(self):
        input = {
            'a': 1,
            'b': 2,
            'c': 3
        }

        a, b, c, d = pluck(input, 'a', 'b', 'c', 'd')

        self.assertEqual(a, 1)
        self.assertEqual(b, 2)
        self.assertEqual(c, 3)
        self.assertIsNone(d)
