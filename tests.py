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
    pprint.pprint(insar.get_sar_info()['net'])

def plot_cpu_and_paging(sar_log,out_pdf):
    insar = parser.Parser(sar_log)
    p = plot.Plot(insar.get_sar_info())
    p.plot(out_pdf)

def set_include_path():
    include_path = os.path.abspath("./")
    sys.path.append(include_path)


if __name__ == "__main__":
    set_include_path()
    #main()
    plot_cpu_and_paging(sys.argv[1], sys.argv[2])
