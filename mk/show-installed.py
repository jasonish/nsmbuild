#! /usr/bin/env python
#
# Script to show installed packages.

import sys
import os

def is_package(path):
    if os.path.isdir(path) and not os.path.islink(path):
        return True
    return False

def main():
    pkgroot = os.path.join(os.getenv("NSMROOT"), "versions")
    for p in os.listdir(pkgroot):
        for v in os.listdir(os.path.join(pkgroot, p)):
            if is_package(os.path.join(pkgroot, p, v)):
                print("%s-%s" % (p, v))

if __name__ == "__main__":
    sys.exit(main())
