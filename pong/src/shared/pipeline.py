from typing import Callable, List, Optional, TypeVar, Any, Iterable

T = TypeVar('T')


class Pipeline(object):

    def __init__(self, iterable: Iterable[Any]):
        self._pipeline: Iterable[Any] = []

        if iterable:
            self._pipeline = (item for item in iterable)

    def map(self, selector: Callable[[Any], Any]):
        self._pipeline = (selector(item) for item in self._pipeline)
        return self

    def flat_map(self, selector: Callable[[Any], Any]):
        self._pipeline = (item for group in (selector(item)
                                             for item in self._pipeline) for item in group)

        return self

    def filter(self, predicate: Callable[[Any], bool]):
        self._pipeline = (item for item in self._pipeline if predicate(item))
        return self

    def head(self) -> Optional[T]:
        for item in self._pipeline:
            return item
        return None

    def tail(self) -> Optional[T]:
        tail = None
        for item in self._pipeline:
            tail = item
        return tail

    def order_by(self, selector: Callable[[Any], Any], ascending: bool = True):
        items = sorted(self._pipeline, key=selector, reverse=not ascending)
        self._pipeline = (item for item in items)

        return self

    def group_by(self, selector: Callable[[Any], Any]):
        mapping = {}
        for item in self._pipeline:
            key = selector(item)
            if key in mapping:
                mapping[key].append(item)
            else:
                mapping[key] = [item]

        self._pipeline = ((k, v) for k, v in mapping.items())

        return self

    def tap(self, applicator: Callable[[Any], Any]):
        def apply(item, applicator):
            applicator(item)
            return item

        self._pipeline = (apply(item, applicator) for item in self._pipeline)

        return self

    def take(self, count: int):
        def take_pipeline(iterator):
            curr_count = 0
            for item in iterator:
                if curr_count >= count:
                    break
                yield item
                curr_count += 1
            
        self._pipeline = take_pipeline(self._pipeline)

        return self

    def batch(self, count: int):

        def batch_pipeline(iterator):
            buffer = []
            for item in iterator:
                buffer.append(item)
                if len(buffer) >= count:
                    yield buffer
                    buffer = []

            if len(buffer) > 0:
                yield buffer

        self._pipeline = batch_pipeline(self._pipeline)

        return self

    def collect(self, applicator: Callable[[Iterable[Any]], Any]):
        items = (item for item in self._pipeline)

        result = applicator(items)
        self._pipeline = [result] if result else []

        return self

    def consume(self, applicator: Callable[[Iterable[Any]], Any]) -> T:
        items = (item for item in self._pipeline)

        result = applicator(items)

        return result

    def reduce(self, reducingFn: Callable[[Any, Any], Any], seed: Optional[Any] = None) -> T:
        acc = seed or None

        if acc:
            for item in self._pipeline:
                acc = reducingFn(acc, item)
        else:
            iterator = iter(self._pipeline)
            acc = next(iterator)
            for item in iterator:
                acc = reducingFn(acc, item)

        return acc

    def to_list(self) -> List[T]:
        return self.consume(list)
