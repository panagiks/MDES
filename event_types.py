#!/usr/bin/env python2
# -*- coding: UTF-8 -*-
"""Enumeration and reverse translation of the available Event Types."""

class EventTypes(object):
    """Describes the available Event Types."""
    PROCESS_ARRIVAL, QUEUE_PUSH, QUEUE_POP, PROCESS_DEPARTURE = range(4)
    translation_dictionary = {
        0 : "PROCESS_ARRIVAL",
        1 : "QUEUE_PUSH",
        2 : "QUEUE_POP",
        3 : "PROCESS_DEPARTURE"
    }
    def __init__(self):
        pass

    def translate(self, evnt_type):
        """Return event type as a string."""
        return self.translation_dictionary[evnt_type]
