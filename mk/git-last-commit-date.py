#! /usr/bin/env python
#
# Rough script to convert the time of the last git commit into a
# format suitable for use a version.

from __future__ import print_function

import sys
import subprocess
import time
import getopt

def main():

    opt_default = None
    opt_prefix = ""

    try:
        opts, args = getopt.getopt(sys.argv[1:], "", ["default=", "prefix="])
    except getopt.GetoptError as err:
        print("error: %s" % err, file=sys.stderr)
        return 1
    for o, a in opts:
        if o in ["--default"]:
            opt_default = a
        elif o in ["--prefix"]:
            opt_prefix = a

    if args:
        cwd = args[0]
    else:
        cwd = "."

    try:
        git = subprocess.Popen(
            ["git", "log", "-1", "--format=%ct"], 
            stdout=subprocess.PIPE, cwd=cwd)
        stdout, stderr = git.communicate()
        lt = time.localtime(int(stdout.strip()))
        print("%s%s" % (opt_prefix, time.strftime("%Y%m%d%H%M%S", lt)))
    except:
        if opt_default is None:
            print("error: failed to get date of last commit", file=sys.stderr)
            return 1
        else:
            print("%s" % (opt_default))

if __name__ == "__main__":
    sys.exit(main())
