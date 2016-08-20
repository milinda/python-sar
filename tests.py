#!/usr/bin/env python
'''
Demo for SAR parser.
'''

import os
import sys
import pprint
import logging
import re
from sar import parser
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
    pprint.pprint(insar.get_sar_info()['paging'])

def set_include_path():
    include_path = os.path.abspath("./")
    sys.path.append(include_path)


if __name__ == "__main__":
    set_include_path()
    main()
