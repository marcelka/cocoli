from collections import Counter

class SimpleQueue: 
    """FIFO structure that performs pop, push and contains queries in constant
    time (on average)."""
    def __init__(self, iterable=[]):
        self._in_stack = []
        self._out_stack = list(iterable)
        self._items = Counter(iterable)

    def push(self, obj):
        self._items.update({obj: 1})
        self._in_stack.append(obj)

    def pop(self):
        if not self._out_stack:
            while self._in_stack:
                self._out_stack.append(self._in_stack.pop())
        obj = self._out_stack.pop()
        self._items.update({obj: -1})
        if self._items[obj] == 0: self._items.pop(obj)
        return obj
    
    def __contains__(self, obj):
        return obj in self._items

    def __len__(self):
        return len(self._in_stack) + len(self._out_stack)
