# -*- coding: UTF-8 -*-
"""Store Events for MDES in an ordered manner."""
import bisect
from mdes.queue import BaseQueue


class EventQueue(BaseQueue):
    """Stores and manages Events."""
    def add(self, event):
        """Insert Event in Queue, maintain ordered state."""
        bisect.insort_right(self._queue, event)
