#!/usr/bin/env python2
# -*- coding: UTF-8 -*-
"""Store Events for MDES in an ordered manner."""
import bisect

class EventQueue(object):
    """Stores and manages Events."""
    def __init__(self):
        self.queue = []
        self.index = []

    def add(self, event):
        """Insert Event in Queue, maintain ordered state."""
        pos = bisect.bisect_right(self.index, event[1])
        self.index[pos:pos] = [event[1]]
        self.queue[pos:pos] = [event]

    def pop(self):
        """Remove and return top element."""
        self.index.pop(0)
        return self.queue.pop(0)

    def dump(self):
        """Dump the contents of the Event Queue."""
        return self.queue
