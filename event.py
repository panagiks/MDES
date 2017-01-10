#!/usr/bin/env python2
# -*- coding: UTF-8 -*-
"""Provide classes to store and represent Events."""
from event_types import EventTypes

class Event(object):
    """Base class for all Events."""
    def __init__(self, evntType, schdl):
        self.type = evntType
        self.time = schdl

    def get_type(self):
        """Return the type of the Event."""
        return self.type

    def get_time(self):
        """Return the time in the simulation the event will happen (or has)."""
        return self.time

class EvntArr(Event):
    """Create an Event for a Process arrival."""
    def __init__(self, schdl):
        Event.__init__(self, EventTypes.PROCESS_ARRIVAL, schdl)

class EvntDep(Event):
    """Create an Event for a Process departure."""
    def __init__(self, schdl, processor_id):
        Event.__init__(self, EventTypes.PROCESS_DEPARTURE, schdl)
        self.processor = processor_id

    def get_processor(self):
        """Return the Processor attached to this event."""
        return self.processor

class EvntPus(Event):
    """Create an Event for a Process entering the Queue."""
    def __init__(self, schdl):
        Event.__init__(self, EventTypes.QUEUE_PUSH, schdl)

class EvntPop(Event):
    """Create an Event for a Process exiting the Queue."""
    def __init__(self, schdl):
        Event.__init__(self, EventTypes.QUEUE_POP, schdl)
