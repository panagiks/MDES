# -*- coding: UTF-8 -*-
"""Provide classes to store and represent Events."""
import time

from abc import ABCMeta, abstractmethod
from logging import getLogger

from mdes.event_types import PROCESS_GENERATION, PROCESS_ARRIVAL, QUEUE_PUSH, PROCESS_DEPARTURE, QUEUE_POP
from mdes.process import Process


class Event(object, metaclass=ABCMeta):
    """Base class for all Events."""
    logger = getLogger('mdes.event')
    def __init__(self, schedule, *args, **kwargs):
        self._created = time.time()
        self.time = schedule

    def __eq__(self, other):
        """Used for creating ordered queue of Events"""
        return self.time == other.time and self.type == other.type

    def __lt__(self, other):
        """Used for creating ordered queue of Events"""
        if self.time == other.time:
            if self.type == other.type:
                return self._created < other._created
            return self.type < other.type
        return self.time < other.time

    def __repr__(self):
        return "<{} @ {}>".format(self.__class__.__name__, self.time)

    def log(self):
        """Log the Event's details."""
        self.logger.debug(
            self
        )

    @property
    @abstractmethod
    def type(self):
        """The type of the Event in the form of int."""
        pass

    @abstractmethod
    def execute(self):
        """The business logic of each event."""
        pass


class EventProcessGeneration(Event):
    """Create an Event for a Process entering the Queue."""
    type = PROCESS_GENERATION
    def __init__(self, schedule, generator, *queues):
        super().__init__(schedule)
        self.generator = generator
        self.queues = queues

    def execute(self):
        self.log()
        return [
            self.generator.schedule(self.time),
            EventQueueEnter(self.time, self.queues[0], Process(self.time))
        ]

    def __repr__(self):
        return "<{} @ {}: {} {}>".format(
            self.__class__.__name__, self.time,
            self.generator, self.queues
        )

class QueueEvent(Event):
    """Parent Class for Queue bound events."""
    def __init__(self, schedule, queue):
        super().__init__(schedule)
        self.queue = queue


class EventQueueEnter(QueueEvent):
    """Create an Event for a Process entering the Queue."""
    type = QUEUE_PUSH
    def __init__(self, schedule, queue, process):
        super().__init__(schedule, queue)
        self.process = process

    def execute(self):
        self.log()
        return [self.queue.push(self.process, self.time)]

    def __repr__(self):
        return "<{} @ {}: {} {}>".format(
            self.__class__.__name__, self.time,
            self.queue, self.process
        )


class EventQueueExit(QueueEvent):
    """Create an Event for a Process exiting the Queue."""
    type = QUEUE_POP
    def execute(self):
        self.log()
        event = self.queue.pop(self.time)
        if isinstance(event, EventProcessingBegin):
            event.process.exit_queue(self.time)
        return [event]

    def __repr__(self):
        return "<{} @ {}: {}>".format(
            self.__class__.__name__, self.time,
            self.queue
        )


class ProcessorEvent(Event):
    """Parent Class for Queue bound events."""
    def __init__(self, schedule, processor):
        super().__init__(schedule)
        self.processor = processor


class EventProcessingBegin(ProcessorEvent):
    """Create an Event for a Process arrival."""
    type = PROCESS_ARRIVAL
    def __init__(self, schedule, processor, process):
        super().__init__(schedule, processor)
        self.process = process

    def execute(self):
        self.log()
        return [self.processor.start(self.process, self.time)]

    def __repr__(self):
        return "<{} @ {}: {} {}>".format(
            self.__class__.__name__, self.time,
            self.processor, self.process
        )


class EventProcessingEnd(ProcessorEvent):
    """Create an Event for a Process departure."""
    type = PROCESS_DEPARTURE
    def execute(self):
        self.log()
        return self.processor.complete()

    def __repr__(self):
        return "<{} @ {}: {}>".format(
            self.__class__.__name__, self.time,
            self.processor
        )
