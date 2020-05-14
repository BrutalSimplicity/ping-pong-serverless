from shared.optional import OptionalHandler
import unittest


class OptionalTests(unittest.TestCase):

    def test_should_resolve_None(self):
        input = None

        output = OptionalHandler(input).value()

        expected = None

        self.assertEqual(output, expected)

    def test_should_resolve_non_existent_key(self):
        input = {
            'a': {}
        }

        output = OptionalHandler(input)['a']['b'].value()

        expected = None

        self.assertEqual(output, expected)

    def test_should_resolve_chained_missing_keys_with_None(self):
        input = {
            'a': {
                'b': {
                    'c': None
                }
            }
        }

        output = OptionalHandler(input)['a']['b']['c'].value()

        expected = None

        self.assertEqual(output, expected)

    def test_should_resolve_getitem_value(self):
        input = 'resolved'

        output = OptionalHandler(input).value()

        expected = 'resolved'

        self.assertEqual(output, expected)

    def test_should_resolve_chained_getitem_with_value(self):
        input = {
            'a': {
                'b': {
                    'c': 'resolved'
                }
            }
        }

        output = OptionalHandler(input)['a']['b']['c'].value()

        expected = 'resolved'

        self.assertEqual(output, expected)

    def test_should_resolve_missing_attribute_with_None(self):
        class TestClass(object):
            def __init__(self):
                pass

        input = TestClass()

        output = OptionalHandler(input).missing.value()

        expected = None

        self.assertEqual(output, expected)

    def test_should_resolve_attribute_with_value(self):
        class TestClass(object):
            def __init__(self):
                self.attr = 'resolved'

        input = TestClass()

        output = OptionalHandler(input).attr.value()

        expected = 'resolved'

        self.assertEqual(output, expected)

    def test_should_resolve_chained_attributes_with_value(self):
        class InnerClass(object):
            def __init__(self):
                self.inner = 'resolved'

        class TestClass(object):
            def __init__(self):
                self.attr = InnerClass()

        input = TestClass()

        output = OptionalHandler(input).attr.inner.value()

        expected = 'resolved'

        self.assertEqual(output, expected)

    def test_should_resolve_chained_variadic_attributes_with_value(self):
        class TestClass(object):
            def __init__(self):
                self.attr = {
                    'dict': {
                        'list': [1, (1, 'resolved')]
                    }
                }

        input = TestClass()

        output = OptionalHandler(input).attr['dict']['list'][1][1].value()

        expected = 'resolved'

        self.assertEqual(output, expected)
