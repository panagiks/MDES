#!/usr/bin/env python2
# -*- coding: UTF-8 -*-
"""Implements a Processor for MDES."""
from random import expovariate

class Processor(object):
    """Represents a Processor with exponential process time."""
    def __init__(self, proc_time):
        self.mean_process_time = proc_time
        self.process = None
        self.busy = False
        self.end = None

    def is_available(self):
        """Show Processor availability."""
        return not self.busy

    def start_processing(self, process, now):
        """Start processing, scheduled processing completion."""
        self.end = now + expovariate(self.mean_process_time)
        self.busy = True
        self.process = process
        return self.end

    def processing_complete(self, now):
        """Check and handle processing completion."""
        if self.end == now:
            tmp = self.process
            self.process = None
            self.busy = False
            return tmp
        return None
