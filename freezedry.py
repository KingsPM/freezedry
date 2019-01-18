#!/usr/bin/env python

__author__ = "David Brawand"
__copyright__ = "King's College Hospital - NHS Foudnation Trust"
__credits__ = ["KCH Clinical Data Science Group"]
__license__ = "GPLv3"
__version__ = "0.0.1"
__maintainer__ = "David Brawand"
__email__ = "dbrawand@nhs.net"
__status__ = "develeopment"
__doc__ = """
FreezeDry. GeL Report Extractor.

Extracts Tables from GeL HTML reports by id 

Parameters
----------
    args : str
        GeL reports
    -s : str
        Section(s) to extract

Returns
-------
    int
        0: Success
        1: Error
        5: ID not found
"""

import sys
import argparse
from bs4 import BeautifulSoup
from parser.table import writeCsv, parseTable


def parseRow(r): return [cell.text.encode('utf8') for cell in r.find_all('td')]


def main(report, id, datatype, parser, output):
    """Extracts tables and figures from the requested sections"""
    with open(report) as fh:
        soup = BeautifulSoup(fh, parser)
        section = soup.find(id=id)
        if not section:
            sys.exit(5)
        if datatype == "table":
            data = parseTable(section.table)
            writeCsv(data, output)
        else:
            print('ERROR: Sorry, {} has no corresponding parser'.format(
                datatype), file=sys.stderr)
            raise NotImplementedError


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("report", help="GeL HTML report")
    parser.add_argument("-i", "--id", required=True, default=[],
                        action="append", help="Section IDs to extract from")
    parser.add_argument("-t", "--datatype", default="table",
                        choices=["table"], help="Data type to extract")
    parser.add_argument("-p", "--parser", default='html5lib',
                        choices=["html5lib", "html.parser"], help="HTML parser to use")
    parser.add_argument("-o", "--output", nargs='?', default=sys.stdout, type=argparse.FileType('w'),
                        help="Output file name (default STDOUT)")
    args = parser.parse_args()
    arguments = vars(args)
    main(**arguments)
