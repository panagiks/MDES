"""Implements the essense of the Simulator."""
import logging
import logging.config

from mdes.event_queue import EventQueue
from mdes.process import Process
from mdes.process_generator import ProcessGenerator
from mdes.process_queue import ProcessQueue


class SimulatorState(object):
    """A stored state for a SystemSimulator object."""
    def __init__(self):
        self._now = 0
        self._event = None
        self.completed_processes = 0

    @property
    def now(self):
        """Returns the current simulation time."""
        return self._now

    @now.setter
    def now(self, new):
        """Sets the current simulation time."""
        self._now = new

    @property
    def event(self):
        """Returns the current simulation event."""
        return self._event

    @event.setter
    def event(self, new):
        """Sets the current simulation event."""
        self._event = new
        # Progress the state time to match the event's time
        self.now = new.time


class SystemSimulator(object):
    """Handling class for the Discrete Event Simulator."""
    def __init__(self, settings):
        self.cfg = settings
        logging.config.dictConfig(self.cfg['logging'])
        self.logger = logging.getLogger('mdes.simulator')
        self.queues = {
            "event" : EventQueue(),
            "process" : ProcessQueue(
                self.cfg["processorsNum"],
                self.cfg["processorLambda"]
            ),
        }
        self.state = SimulatorState()
        self.statistics = {
            "mrt"            : 0, # Mean Response Time
            "mwt"            : 0, # Mean Waiting Time
            "avgNumInQueue"  : 0, # Average number of jobs in Queue
            "avgNumInSystem" : 0  # Average number of jobs in System
        }
        # Schedule the first arrival.
        generator = ProcessGenerator(self.cfg['processesLambda'], self.queues['process'])
        self.queues['event'].add(
            generator.schedule(self.state.now)
        )

    def progress(self):
        """Generator. Iterate over it to progress the simulation."""
        before = self.state.now
        while self.state.completed_processes < self.cfg["processesNum"]:
            self.logger.debug(self.queues['event'].queue)
            # Get the first event from the event Queue.
            self.state.event = self.queues["event"].pop()
            # Gather statistics
            jobs_in_queue = len(self.queues['process'])
            jobs_in_system = jobs_in_queue + len([
                p for p in self.queues['process'].processors
                if p.busy
            ])
            self.statistics['avgNumInSystem'] += jobs_in_system * (self.state.now - before)
            self.statistics['avgNumInQueue'] += jobs_in_queue * (self.state.now - before)
            before = self.state.now
            # Execute action associated with the current event.
            result = self.state.event.execute()
            # A 'Process' object is returned to signal the end of this porcess' lifecycle
            if isinstance(result, Process):
                # Add the completed process to the store array for later data extraction.
                self.statistics["mrt"] += (result.departed - result.arrived)
                self.statistics["mwt"] += (result.exited_queue - result.entered_queue)
                # Increase the counter for the completed processes.
                self.state.completed_processes += 1
                # Update progress
                yield 1
            else:  # Otherwise an array of Event objects is returned
                for event in result:
                    self.queues['event'].add(event)
                yield 0

    def calculate_statistics(self):
        """Calculate Statistics about the Simulation."""
        self.statistics["mrt"] /= self.cfg["processesNum"]
        self.statistics["mwt"] /= self.cfg["processesNum"]
        self.statistics["avgNumInSystem"] /= self.state.now
        self.statistics["avgNumInQueue"] /= self.state.now
        self.results_log()

    def results_log(self):
        """Log the simulation results using the `mdes.simulator` logger."""
        self.logger.warning("=== New Simulation === ")
        self.logger.warning("Mean Response Time: %f" %self.statistics["mrt"])
        self.logger.warning("Mean Waiting Time: %f" %self.statistics["mwt"])
        self.logger.warning("Average Jobs in System: %f" %self.statistics["avgNumInSystem"])
        self.logger.warning("Average Jobs in Queue: %f" %self.statistics["avgNumInQueue"])
