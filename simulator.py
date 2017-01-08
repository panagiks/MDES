#!/usr/bin/env python2
# -*- coding: UTF-8 -*-
"""Implements the essense of the Simulator."""
import json
from random import expovariate
from eventQueue import EventQueue
from eventTypes import EventTypes
from processor import Processor
from processQueue import ProcessQueue
from process import Process

class Simulator(object):
    """Handling class for the Discrete Event Simulator."""
    def __init__(self):
        with open('config.json','r') as json_config:
            self.cfg = json.load(json_config)
        self.now = 0
        self.served_processes = 0
        self.event_queue = EventQueue()
        self.process_queue = ProcessQueue()
        self.completed_processes = ProcessQueue()
        #Schedule the first arrival.
        self.event_queue.add((EventTypes.PROCESS_ARRIVAL, self.next_arrival()))
        #Create c Processors.
        self.processors = []
        for i in range(self.cfg["processorsNum"]):
            self.processors.append(Processor(self.cfg["processorLambda"]))
        self.translation_dictionary = {
            EventTypes.PROCESS_ARRIVAL   : self.arrival,
            EventTypes.PROCESS_DEPARTURE : self.execution_end
        }

    def event_log(self, evnt):
        """Log each event in the Simulation."""
        if "E" in self.cfg["log"]:
            with open('event.log','a') as logfile:
                logfile.write("Type : %s, Time : %f\n" %
                                (EventTypes.translate[evnt[0]],evnt[1]))

    def next_arrival(self):
        """Schedule the next process arrival."""
        #return self.now + uniform(0.7,1.3)
        return self.now + expovariate(self.cfg["processesLambda"])

    def arrival(self):
        """Handle a process arrival."""
        #Log Event
        self.event_log((EventTypes.PROCESS_ARRIVAL,self.now))
        #Create the process that just arrived.
        proc = Process(self.now)
        #Schedule next arrival.
        self.event_queue.add((EventTypes.PROCESS_ARRIVAL, self.next_arrival()))
        added = False
        #Check if a processor is available and assign the job to the first available.
        for processorn in self.processors:
            if processorn.is_available():
                #Start Processing and Schedule its completion.
                self.execution_begin(proc, processorn)
                added = True
                #Since the job is assigned, stop the iteration.
                break
        #If no Processor was available insert job in Queue.
        if not added:
            #Time-tag the insertion of the process in the Queue.
            proc.enter_queue(self.now)
            #Insert the process in the Queue.
            self.process_queue.push(proc)
            #Log Event
            self.event_log((EventTypes.QUEUE_PUSH, self.now))

    def execution_begin(self, proc, processor):
        """Schedule the completion of the current process."""
        self.event_queue.add((EventTypes.PROCESS_DEPARTURE, processor.start_processing(proc, self.now)))

    def execution_end(self):
        """Handle the completion of a process."""
        #A processor's execution is scheduled to end now, find which one.
        for processorn in self.processors:
            proc = processorn.processing_complete(self.now)
            if proc is not None:
                #Log Event
                self.event_log((EventTypes.PROCESS_DEPARTURE, self.now))
                #Time-tag the completion of the process.
                proc.depart(self.now)
                #Add the completed process to the store array for later data extraction.
                self.completed_processes.push(proc)
                #Increase the counter for the completed processes.
                self.served_processes += 1
                #Check if there are processes waiting in the queue.
                if not self.process_queue.is_empty():
                    #Log Event
                    self.event_log((EventTypes.QUEUE_POP, self.now))
                    #Pop the first job of the Queue
                    proc = self.process_queue.pop()
                    #Time-tag the exit of the Process from the Queue.
                    proc.exit_queue(self.now)
                    #Start Processing and Schedule its completion.
                    self.execution_begin(proc, processorn)
                #Since the processor with the completed job is found, stop the iteration.
                break

    def loop(self):
        """Main loop, determine execution length."""
        while self.served_processes < self.cfg["processesNum"]:
            #Get the first event from the event Queue.
            self.current_event = self.event_queue.pop()
            #Move current time forward to current event's time.
            self.now = self.current_event[1]
            #Execute action associated with the current event.
            self.translation_dictionary[self.current_event[0]]()

    def calculate_statistics(self):
        """Calculate Statistics about the Simulation."""
        processes = self.completed_processes.dump()
        system_time = 0
        queue_time = 0
        system_num = 0
        queue_num = 0
        system = EventQueue()
        queue = EventQueue()
        self.mean_response_time = 0
        self.mean_waiting_time = 0
        for process in processes:
            self.mean_response_time += (process.departed - process.arrived)
            system.add((EventTypes.PROCESS_ARRIVAL, process.arrived))
            system.add((EventTypes.PROCESS_DEPARTURE, process.departed))
            if process.entered_queue:
                self.mean_waiting_time += (process.exited_queue - process.entered_queue)
                queue.add((EventTypes.QUEUE_PUSH, process.entered_queue))
                queue.add((EventTypes.QUEUE_POP, process.exited_queue))
        self.mean_response_time /= self.cfg["processesNum"]
        self.mean_waiting_time /= self.cfg["processesNum"]
        system_array = system.dump()
        queue_array = queue.dump()
        previus_time = 0
        for job in system_array:
            system_time += (job[1] - previus_time) * system_num
            previus_time = job[1]
            if job[0] == EventTypes.PROCESS_ARRIVAL:
                system_num += 1
            elif job[0] == EventTypes.PROCESS_DEPARTURE:
                system_num -= 1
        self.avg_num_in_system = system_time / self.now
        previus_time = 0
        for job in queue_array:
            queue_time += (job[1] - previus_time) * queue_num
            previus_time = job[1]
            if job[0] == EventTypes.QUEUE_PUSH:
                queue_num += 1
            elif job[0] == EventTypes.QUEUE_POP:
                queue_num -= 1
        self.avg_num_in_queue = queue_time / self.now
        self.results_log()


    def results_log(self):
        """Log the Statistics of the Simulation."""
        if "R" in self.cfg["log"]:
            with open('results.log','a') as logfile:
                logfile.write("\n === New Simulation === \n")
                logfile.write("Mean Response Time: %f\n" %self.mean_response_time)
                logfile.write("Mean Waiting Time: %f" %self.mean_waiting_time)
                logfile.write("Average Jobs in System: %f" %self.avg_num_in_system)
                logfile.write("Average Jobs in Queue: %f" %self.avg_num_in_queue)

    def print_statistics(self):
        """Print the Statistics of the Simulation."""
        print("Mean Response Time: %f" %self.mean_response_time)
        print("Mean Waiting Time: %f" %self.mean_waiting_time)
        print("Average Jobs in System: %f" %self.avg_num_in_system)
        print("Average Jobs in Queue: %f" %self.avg_num_in_queue)
