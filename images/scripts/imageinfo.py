#!/usr/bin/env python
# coding=utf-8
from __future__ import print_function

import os
import sys
from argparse import ArgumentParser

__version__ = '0.9'

class Image(object):

    def __init__(self, path):
        self.path = path
        self.filename = os.path.split(self.path)[1]
        with open(self.path, 'rb') as imagefile:
            self.magic = imagefile.read(4)

            imagefile.seek(6)
            self.board = imagefile.read(17).strip(b'\x00')

            imagefile.seek(36)
            self.vendor = imagefile.read(18).strip(b'\x00')

            imagefile.seek(48)
            self.version = imagefile.read(16).strip(b'\x00')

            imagefile.seek(64)
            self.date = imagefile.read(16).strip(b'\x00')

class ImageTable(object):
    line_ending = '\n'
    default_fields = ('filename', 'magic', 'version', 'date', 'vendor', 'board')


    def __init__(self):
        self.images = []

    def add(self, image):
        self.images.append(image)

    def _format_row(self, values, max_lengths):
        values = map(str, values)
        string_values = [v + ' ' * (l - len(v)) for v, l in zip(values, max_lengths)]
        return '| ' + ' | '.join(string_values) + ' |' + self.line_ending

    def get_string(self, fields=None):
        table = []
        if fields is None:
            fields = self.default_fields
        for image in self.images:
            row = []
            for field in fields:
                row.append(getattr(image, field))
            table.append(row)
            print(row)

        max_lengths = []
        table.insert(0, fields)
        for i in range(len(fields)):
            max_lengths.append(max(map(lambda x: len(x[i]), table)))
        del table[0]
        seperation_line = map(lambda x: x*'-', max_lengths)
        result = ""
        result += self._format_row(fields, max_lengths)
        result += self._format_row(seperation_line, max_lengths)
        for row in table:
            print(row)
            result += self._format_row(row, max_lengths)
        return result


    def __str__(self):
        return self.get_string()


def main():
    parser = ArgumentParser(version=__version__,
                            description="Display information about .sig images")
    parser.add_argument('-t', '--table', action='store_true',
                        help="Generate markdown of all files table")
    parser.add_argument('image', metavar="FILE", nargs='+')
    args = parser.parse_args()

    table = None
    if args.table:
        table = ImageTable()

    for image_path in args.image:
        image = Image(image_path)
        if args.table:
            table.add(image)
        else:
            print("File     : %s" % image.filename)
            print("Magic    : %s" % image.magic)
            print("Version  : %s" % image.version)
            print("Date     : %s" % image.date)
            print("Vendor?  : %s" % image.vendor)
            print("Board ID : %s" % image.board)
            print()

    if args.table:
        print(table.get_string(('filename', 'magic', 'version', 'date', 'board')))

if __name__ == '__main__':
    main()
