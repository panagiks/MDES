#!/usr/bin/env python2
# -*- coding: UTF-8 -*-
"""Entry point for MDES (Modular Discrete Event Simulator)."""
from simulator import Simulator

def main():
    """Entry point function for MDES (Modular Discrete Event Simulator)."""
    sim = Simulator()
    sim.loop()
    sim.calculate_statistics()
    sim.print_statistics()


if __name__ == '__main__':
    main()
