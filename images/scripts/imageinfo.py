#!/usr/bin/env python
# coding=utf-8
from __future__ import print_function

import sys
import os

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

def main():
    if len(sys.argv) < 2:
        print("imageinfo.py FILE")
        sys.exit(1)

    image = None
    try:
        image = Image(sys.argv[1])
    except Exception as e:
        #print(e)
        raise
        sys.exit(1)

    print("File     : %s" % image.filename)
    print("Magic    : %s" % image.magic)
    print("Version  : %s" % image.version)
    print("Date     : %s" % image.date)
    print("Vendor?  : %s" % image.vendor)
    print("Board ID : %s" % image.board)


if __name__ == '__main__':
    main()
