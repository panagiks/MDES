# -*- coding: UTF-8 -*-
"""Implements a Process in MDES, individually stores metrics."""


class Process(object):
    """Each object represents a Process in the Simulator."""
    def __init__(self, now):
        self.arrived = now
        self.departed = None
        self.entered_queue = None
        self.exited_queue = None

    def depart(self, now):
        """Set Process departure from the System."""
        self.departed = now

    def enter_queue(self, now):
        """Set Process entrance in the Queue."""
        self.entered_queue = now

    def exit_queue(self, now):
        """Set Process departure from the Queue."""
        self.exited_queue = now
