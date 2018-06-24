# -*- coding: UTF-8 -*-
"""Store Processes in a FIFO manner."""
from mdes.event import EventProcessingBegin, EventQueueExit
from mdes.processor import Processor
from mdes.queue import BaseQueue


class ProcessQueue(BaseQueue):
    """Store and return Processes."""
    def __init__(self, num_of_processors, l_processor):
        super(ProcessQueue, self).__init__()
        self.processors = [
            Processor(l_processor)
            for _ in range(num_of_processors)
        ]

    def push(self, proc, time):
        """Append Process in Queue."""
        self._queue.append(proc)
        proc.enter_queue(time)
        return EventQueueExit(
            sorted(self.processors)[0].end or time,
            self
        )

    def pop(self, time):
        # Check which processor is available and assign the job to the first.
        for processorn in self.processors:
            if not processorn.busy:
                process = super(ProcessQueue, self).pop()
                return EventProcessingBegin(time, processorn, process)
        return EventQueueExit(
            sorted(self.processors)[0].end or time,
            self
        )
