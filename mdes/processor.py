# -*- coding: UTF-8 -*-
"""Implements a Processor for MDES."""
from random import expovariate

from mdes.event import EventProcessingEnd


class Processor(object):
    """Represents a Processor with exponential process time."""
    def __init__(self, proc_time):
        self.mean_process_time = proc_time
        self.process = None
        self.end = 0

    def __eq__(self, other):
        return self.end == other.end

    def __lt__(self, other):
        return self.end < other.end

    @property
    def busy(self):
        """Busy state of the processor."""
        return self.process is not None

    def start(self, process, now):
        """Start processing, scheduled processing completion."""
        self.end = now + expovariate(self.mean_process_time)
        self.process = process
        return EventProcessingEnd(self.end, self)

    def complete(self):
        """Handle processing completion."""
        # Time-tag the completion of the process.
        self.process.depart(self.end)
        tmp = self.process
        self.process = None
        self.end = 0
        return tmp
