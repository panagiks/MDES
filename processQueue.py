#!/usr/bin/env python2
# -*- coding: UTF-8 -*-
"""Store Processes in a FIFO manner."""

class ProcessQueue(object):
    """Store and return Processes."""
    def __init__(self):
        self.queue = []

    def is_empty(self):
        """Check whether there are any Processes in Queue."""
        return not self.queue

    def push(self, proc):
        """Append Process in Queue."""
        self.queue.append(proc)

    def pop(self):
        """Remove and return the first Process."""
        return self.queue.pop(0)

    def dump(self):
        """Dump the contents of the Process Queue."""
        return self.queue
