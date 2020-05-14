from shared.pipeline import Pipeline
from typing import Optional
import unittest


class PipelineTests(unittest.TestCase):

    def test_should_map_dict(self):
        input = {
            'foo': 'bar',
            'num': 2
        }

        def square_it(bag):
            bag['num'] **= 2
            return bag

        output = (
            Pipeline([input])
            .map(square_it)
            .head() or {}
        )

        expected = {
            'foo': 'bar',
            'num': 4
        }

        self.assertDictEqual(output, expected)

    def test_should_map_object(self):

        class Data(object):
            def __init__(self):
                self.foo = 'bar  '
                self.bar = ' foo'

        input = Data()

        def massage_it(bag: Data):
            bag.foo = bag.foo.strip()
            bag.bar = bag.bar.strip()
            return bag

        output: Optional[Data] = (
            Pipeline([input])
            .map(massage_it)
            .head()
        )

        self.assertEqual(output.foo, 'bar')
        self.assertEqual(output.bar, 'foo')

    def test_should_map_list(self):
        input = [1, 2, 3, 4, 5]

        output = (
            Pipeline(input)
            .map(lambda x: x * 2)
            .to_list()
        )

        expected = [2, 4, 6, 8, 10]

        self.assertEqual(output, expected)

    def test_should_map_empty_to_empty(self):
        input = []

        output = (
            Pipeline(input)
            .map(lambda x: x + 2)
            .filter(lambda x: x > 2)
            .to_list()
        )

        self.assertEqual(output, [])

    def test_should_map_set(self):
        input = set(['a', 'b'])

        output = (
            Pipeline(input)
            .map(lambda x: x)
            .map(lambda x: x.capitalize())
            .order_by(lambda x: x)
            .to_list()
        )

        self.assertEqual(output, ['A', 'B'])

    def test_should_map_iterable_class(self):

        class Counter:
            def __init__(self, low, high):
                self.current = low - 1
                self.high = high

            def __iter__(self):
                return self

            def __next__(self):
                self.current += 1
                if self.current < self.high:
                    return self.current
                raise StopIteration

        output = (
            Pipeline(Counter(1, 10))
            .map(lambda x: x ** 2)
            .to_list()
        )

        expected = [1, 4, 9, 16, 25, 36, 49, 64, 81]

        self.assertEqual(output, expected)

    def test_should_sort_iterable(self):
        input_list = [3, 5, 2, 1, 4]

        output = (
            Pipeline(input_list)
            .order_by(lambda x: x)
            .to_list()
        )

        expected = [1, 2, 3, 4, 5]

        self.assertEqual(output, expected)

    def test_should_sort_iterable_descending(self):
        input_list = [3, 5, 2, 1, 4]

        output = (
            Pipeline(input_list)
            .order_by(lambda x: x, False)
            .to_list()
        )

        expected = [5, 4, 3, 2, 1]

        self.assertEqual(output, expected)

    def test_should_sort_iterable_dict_by_key(self):
        input = [
            {
                'key': 'Dallas'
            },
            {
                'key': 'fort worth'
            },
            {
                'key': 'HOUSTON'
            },
            {
                'key': 'Austin'
            }
        ]

        output = (
            Pipeline(input)
            .order_by(lambda x: x['key'].lower())
            .to_list()
        )

        expected = [
            {
                'key': 'Austin'
            },
            {
                'key': 'Dallas'
            },
            {
                'key': 'fort worth'
            },
            {
                'key': 'HOUSTON'
            }
        ]

        self.assertEqual(output, expected)

    def test_should_group_by_iterable(self):
        input = [
            {
                'key': 'Magic Hat 9',
                'votes': 2
            },
            {
                'key': 'Golden Monkey',
                'votes': 1
            },
            {
                'key': 'Golden Monkey',
                'votes': 3
            },
            {
                'key': 'Brother Thelonius',
                'votes': 1
            },
            {
                'key': 'Brother Thelonius',
                'votes': 2
            },
            {
                'key': 'Chimay',
                'votes': 6
            },
            {
                'key': 'Brother Thelonius',
                'votes': 2
            }
        ]

        output = (
            Pipeline(input)
            .group_by(lambda x: x['key'])
            .to_list()
        )

        expected = {
            'Golden Monkey': [
                {
                    'key': 'Golden Monkey',
                    'votes': 1
                },
                {
                    'key': 'Golden Monkey',
                    'votes': 3
                }
            ],
            'Chimay': [
                {
                    'key': 'Chimay',
                    'votes': 6
                }
            ],
            'Magic Hat 9': [
                {
                    'key': 'Magic Hat 9',
                    'votes': 2
                }
            ],
            'Brother Thelonius': [
                {
                    'key': 'Brother Thelonius',
                    'votes': 2
                }
            ]
        }.items()

        output = (
            Pipeline(input)
            .group_by(lambda x: x['key'])
            .order_by(lambda x: len(x[1]))
            .head() or []
        )[0]

        expected = 'Magic Hat 9'

        self.assertCountEqual(output, expected)

    def test_should_reduce_with_seed_value(self):
        input = [1, 2, 3, 4, 5]

        output = (
            Pipeline(input)
            .reduce(lambda acc, x: x + acc, 10)
        )

        expected = 10 + 1 + 2 + 3 + 4 + 5

        self.assertEqual(output, expected)

    def test_should_reduce_without_seed_value(self):
        input = [1, 2, 3, 4, 5]

        output = (
            Pipeline(input)
            .reduce(lambda acc, x: x + acc)
        )

        expected = 1 + 2 + 3 + 4 + 5

        self.assertEqual(output, expected)

    def test_should_be_empty_when_head_is_called_on_empty_iterable(self):
        input = []

        output = Pipeline(input).head()

        self.assertEqual(output, None)

    def test_should_flatten_nested_iterable(self):
        input = [[1, 2], [3, 4], [5, 6]]

        output = (
            Pipeline(input)
            .flat_map(lambda x: x)
            .to_list()
        )

        self.assertEqual(output, [1, 2, 3, 4, 5, 6])

    def test_should_filter_iterable(self):
        input = [1, 2, 3, 4, 5, 6]

        output = (
            Pipeline(input)
            .filter(lambda x: x % 2 == 0)
            .to_list()
        )

        expected = [2, 4, 6]

        self.assertEqual(output, expected)

    def test_tap_should_not_modify_pipeline(self):
        input = [1, 2, 3, 4, 5]

        output = (
            Pipeline(input)
            .tap(lambda x: x % 2 == 0)
            .to_list()
        )

        # tap does not transform its input
        expected = [1, 2, 3, 4, 5]

        self.assertCountEqual(output, expected)

    def test_should_take_no_more_than_count(self):
        input = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

        # consume the whole input
        output = (
            Pipeline(input)
            .take(100)
            .to_list()
        )

        expected = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

        self.assertCountEqual(output, expected)

        output = (
            Pipeline(input)
            .take(5)
            .to_list()
        )

        expected = [1, 2, 3, 4, 5]

        self.assertCountEqual(output, expected)

    def test_should_batch_no_more_than_count(self):
        input = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

        output = (
            Pipeline(input)
            .batch(20)
            .to_list()
        )

        expected = [[1, 2, 3, 4, 5, 6, 7, 8, 9, 10]]

        self.assertCountEqual(output, expected)

        output = (
            Pipeline(input)
            .batch(2)
            .to_list()
        )

        expected = [[1, 2], [3, 4], [5, 6], [7, 8], [9, 10]]

        print(output)

        self.assertCountEqual(output, expected)
