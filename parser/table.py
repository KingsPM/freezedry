__doc__ = """function to read tables and write as csv"""
__maintainer__ = 'David Brawand'

import csv


# def parseRow(r): return [cell.text.encode('utf8') for cell in r.find_all('td')]
def parseRow(r): return [cell.text for cell in r.find_all('td')]


def parseTable(table):
    data = [[header.text for header in table.find_all('th')]]  # get header
    data.extend([parseRow(row)
                 for row in table.find_all('tr')])  # extend with rows
    return data


def writeCsv(data, fh):
    writer = csv.writer(fh)
    writer.writerows(row for row in data if row)  # write non-empty rows
    return
