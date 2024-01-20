#!/usr/bin/env python3

"""
Embench module to run benchmark programs.

This version is suitable for running programs with RISC-V ISA simulator spike.
"""

__all__ = [
    'get_target_args',
    'build_benchmark_cmd',
    'decode_results',
]

import argparse
import re

from embench_core import log


def get_target_args(remnant):
    """Parse left over arguments"""
    parser = argparse.ArgumentParser(description='Get target specific args')

    # No target arguments
    return parser.parse_args(remnant)


def build_benchmark_cmd(bench, args):
    """Construct the command to run the benchmark.  "args" is a
       namespace with target specific arguments"""

    return ['sh', '-c', f'/home/fourcolor/Documents/rv32emu/build/rv32emu {bench}', '-e']


def decode_results(stdout_str, stderr_str):
    """Extract the results from the output string of the run. Return the
       elapsed time in milliseconds or zero if the run failed."""
    # See above in build_benchmark_cmd how we record the return value and
    # execution time.

    time = re.search('rv32emu timer delta: (\d+)[.](\d+)', stdout_str, re.S)
    if time:
        ms_elapsed = float(time.group(1) + '.' + time.group(2))
        # Return value cannot be zero (will be interpreted as error)
        return float(ms_elapsed)

    # We must have failed to find a time
    log.debug('Warning: Failed to find timing')
    return 0.0