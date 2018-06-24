# -*- coding: UTF-8 -*-
"""Entry point for MDES (Modular Discrete Event Simulator)."""
import json
import logging
import time
import click

from mdes.simulator import SystemSimulator


@click.command()
@click.option('-c', '--config', 'settings', type=click.File('r'), required=True)
def main(settings):
    """Entry point function for MDES (Modular Discrete Event Simulator)."""
    logger = logging.getLogger('mdes.cmd')
    start = time.time()
    sim = SystemSimulator(json.load(settings))
    with click.progressbar(length=sim.cfg["processesNum"], label='Running Simulation') as pbar:
        for pgres in sim.progress():
            pbar.update(pgres)
    logger.info('Completed in {:.2f}s'.format(time.time() - start))
    sim.calculate_statistics()
