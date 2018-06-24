# -*- coding: UTF-8 -*-
"""Base class for MDES Queues."""
from collections import deque


class BaseQueue(object):
    """Base class for MDES Queues."""
    def __init__(self):
        self._queue = deque()

    def __len__(self):
        return len(self._queue)

    def __getitem__(self, position):
        return self._queue[position]

    def __reversed__(self):
        return reversed(self._queue)

    @property
    def queue(self):
        """Return the elements of the Queue (was 'dump()')"""
        return self._queue

    def push(self, element):
        """Add an element to the end of the queue."""
        self._queue.append(element)

    def is_empty(self):
        """Check whether there are any Element in Queue."""
        return not self._queue

    def pop(self):
        """Remove and return the first Element."""
        return self._queue.popleft()
