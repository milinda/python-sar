#!/usr/bin/env python
'''
Demo for SAR parser.
'''

import os
import sys
import pprint
import logging
import re
from sar import parser, plot
from sar import PATTERN_PAGING

def validate_regex():
    logging.info('Validating paging regex')
    pattern = re.compile(PATTERN_PAGING)
    for i, line in enumerate(open('./data/sample.log')):
        for match in re.finditer(pattern, line):
            print 'Found on line %s: %s' % (i+1, match.groups())

def main():
    # Single SAR file parsing
    insar = parser.Parser("./data/sample.log")
    print(("SAR file date: %s" % (insar.get_filedate())))
    print("Paging Content:\n")
    pprint.pprint(insar.get_sar_info()['cpu'])

def plot_cpu_and_paging():
    insar = parser.Parser("/Users/mpathira/PhD/Experiments/sar-viz/2331/j-004.txt")
    p = plot.Plot(insar.get_sar_info())
    p.plot()

def set_include_path():
    include_path = os.path.abspath("./")
    sys.path.append(include_path)


if __name__ == "__main__":
    set_include_path()
    plot_cpu_and_paging()
