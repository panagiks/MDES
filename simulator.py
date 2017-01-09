#!/usr/bin/env python2
# -*- coding: UTF-8 -*-
"""Implements the essense of the Simulator."""
from __future__ import print_function
import json
from random import expovariate
from event_queue import EventQueue
from event_types import EventTypes
from processor import Processor
from process_queue import ProcessQueue
from process import Process

class Simulator(object):
    """Handling class for the Discrete Event Simulator."""
    def __init__(self):
        with open('config.json', 'r') as json_config:
            self.cfg = json.load(json_config)
        #Create c Processors.
        self.processors = []
        for _ in xrange(self.cfg["processorsNum"]):
            self.processors.append(Processor(self.cfg["processorLambda"]))
        self.queues = {
            "event" : EventQueue(),
            "process" : ProcessQueue(),
            "completedProcesses" : ProcessQueue()
        }
        self.state = {
            "now"             : 0,      #Current Simulation Time
            "event"           : (0, 0), #Current Simulation Event
            "servedProcesses" : 0       #Total Served Processes
        }
        self.statistics = {
            "mrt"            : 0, #Mean Response Time
            "mwt"            : 0, #Mean Waiting Time
            "avgNumInQueue"  : 0, #Average number of jobs in Queue
            "avgNumInSystem" : 0  #Average number of jobs in System
        }
        self.translation_dictionary = {
            EventTypes.PROCESS_ARRIVAL   : self.arrival,
            EventTypes.PROCESS_DEPARTURE : self.execution_end
        }
        #Schedule the first arrival.
        self.queues["event"].add((EventTypes.PROCESS_ARRIVAL, self.next_arrival()))

    def event_log(self, evnt):
        """Log each event in the Simulation."""
        if "E" in self.cfg["log"]:
            with open('event.log', 'a') as logfile:
                logfile.write("Type : %s, Time : %f\n" %
                              (EventTypes.translate[evnt[0]], evnt[1]))

    def next_arrival(self):
        """Schedule the next process arrival."""
        return self.state["now"] + expovariate(self.cfg["processesLambda"])

    def arrival(self):
        """Handle a process arrival."""
        #Log Event
        self.event_log((EventTypes.PROCESS_ARRIVAL, self.state["now"]))
        #Create the process that just arrived.
        proc = Process(self.state["now"])
        #Schedule next arrival.
        self.queues["event"].add((EventTypes.PROCESS_ARRIVAL, self.next_arrival()))
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
            proc.enter_queue(self.state["now"])
            #Insert the process in the Queue.
            self.queues["process"].push(proc)
            #Log Event
            self.event_log((EventTypes.QUEUE_PUSH, self.state["now"]))

    def execution_begin(self, proc, processor):
        """Schedule the completion of the current process."""
        self.queues["event"].add((EventTypes.PROCESS_DEPARTURE,
                                  processor.start_processing(proc, self.state["now"])))

    def execution_end(self):
        """Handle the completion of a process."""
        #A processor's execution is scheduled to end now, find which one.
        for processorn in self.processors:
            proc = processorn.processing_complete(self.state["now"])
            if proc is not None:
                #Log Event
                self.event_log((EventTypes.PROCESS_DEPARTURE, self.state["now"]))
                #Time-tag the completion of the process.
                proc.depart(self.state["now"])
                #Add the completed process to the store array for later data extraction.
                self.queues["completedProcesses"].push(proc)
                #Increase the counter for the completed processes.
                self.state["servedProcesses"] += 1
                #Check if there are processes waiting in the queue.
                if not self.queues["process"].is_empty():
                    #Log Event
                    self.event_log((EventTypes.QUEUE_POP, self.state["now"]))
                    #Pop the first job of the Queue
                    proc = self.queues["process"].pop()
                    #Time-tag the exit of the Process from the Queue.
                    proc.exit_queue(self.state["now"])
                    #Start Processing and Schedule its completion.
                    self.execution_begin(proc, processorn)
                #Since the processor with the completed job is found, stop the iteration.
                break

    def loop(self):
        """Main loop, determine execution length."""
        while self.state["servedProcesses"] < self.cfg["processesNum"]:
            #Get the first event from the event Queue.
            self.state["event"] = self.queues["event"].pop()
            #Move current time forward to current event's time.
            self.state["now"] = self.state["event"][1]
            #Execute action associated with the current event.
            self.translation_dictionary[self.state["event"][0]]()

    def calculate_statistics(self):
        """Calculate Statistics about the Simulation."""
        processes = self.queues["completedProcesses"].dump()
        system_time = 0
        queue_time = 0
        system_num = 0
        queue_num = 0
        system = EventQueue()
        queue = EventQueue()
        for process in processes:
            self.statistics["mrt"] += (process.departed - process.arrived)
            system.add((EventTypes.PROCESS_ARRIVAL, process.arrived))
            system.add((EventTypes.PROCESS_DEPARTURE, process.departed))
            if process.entered_queue:
                self.statistics["mwt"] += (process.exited_queue - process.entered_queue)
                queue.add((EventTypes.QUEUE_PUSH, process.entered_queue))
                queue.add((EventTypes.QUEUE_POP, process.exited_queue))
        self.statistics["mrt"] /= self.cfg["processesNum"]
        self.statistics["mwt"] /= self.cfg["processesNum"]
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
        self.statistics["avgNumInSystem"] = system_time / self.state["now"]
        previus_time = 0
        for job in queue_array:
            queue_time += (job[1] - previus_time) * queue_num
            previus_time = job[1]
            if job[0] == EventTypes.QUEUE_PUSH:
                queue_num += 1
            elif job[0] == EventTypes.QUEUE_POP:
                queue_num -= 1
        self.statistics["avgNumInQueue"] = queue_time / self.state["now"]
        self.results_log()


    def results_log(self):
        """Log the Statistics of the Simulation."""
        if "R" in self.cfg["log"]:
            with open('results.log', 'a') as logfile:
                logfile.write("\n === New Simulation === \n")
                logfile.write("Mean Response Time: %f\n" %self.statistics["mrt"])
                logfile.write("Mean Waiting Time: %f" %self.statistics["mwt"])
                logfile.write("Average Jobs in System: %f" %self.statistics["avgNumInSystem"])
                logfile.write("Average Jobs in Queue: %f" %self.statistics["avgNumInQueue"])

    def print_statistics(self):
        """Print the Statistics of the Simulation."""
        print("Mean Response Time: %f" %self.statistics["mrt"])
        print("Mean Waiting Time: %f" %self.statistics["mwt"])
        print("Average Jobs in System: %f" %self.statistics["avgNumInSystem"])
        print("Average Jobs in Queue: %f" %self.statistics["avgNumInQueue"])
