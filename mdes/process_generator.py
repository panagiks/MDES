# -*- coding: UTF-8 -*-
"""Represents an external source that creates Processes to enter the System."""
from random import expovariate

from mdes.event import EventProcessGeneration


class ProcessGenerator(object):
    def __init__(self, p_lambda, *queues):
        self.processes_lambda = p_lambda
        self.queues = queues

    def schedule(self, time):
        """Schedule the next Process arrival."""
        return EventProcessGeneration(
            time + expovariate(self.processes_lambda),
            self,
            *self.queues
        )
