#! /usr/bin/env python
#
# Helper script to extract files.

from __future__ import print_function

import sys
import subprocess

def extract(distfile):
    if distfile.endswith(".tar.gz"):
        rc = subprocess.call(["tar", "zxf", distfile])
    else:
        print("Don't know how to extract %s." % (distfile), file=sys.stderr)
        return False
    return True if rc == 0 else False

def main():
    for distfile in sys.argv[1:]:
        if not extract(distfile):
            return 1
    return 0

if __name__ == "__main__":
    sys.exit(main())
