# The MIT License (MIT)
#
# Copyright (c) 2014 Jason Ish
#
# Permission is hereby granted, free of charge, to any person
# obtaining a copy of this software and associated documentation files
# (the "Software"), to deal in the Software without restriction,
# including without limitation the rights to use, copy, modify, merge,
# publish, distribute, sublicense, and/or sell copies of the Software,
# and to permit persons to whom the Software is furnished to do so,
# subject to the following conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS
# BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN
# ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
# CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import os
import os.path
import subprocess
import re
import imp
import uuid

class UnsatisfiedSystemDependency(Exception):
    pass

class BuildModule(object):

    def __init__(self, config, module, args=None):
        self.config = config
        self.module = module
        self.args = args if args else []
        self.name = module.name
        self.version = module.version

        self.deps = []
        self.sysdeps = []

        self.configure_args = []
        self.path = []

        self.builddir = os.path.dirname(os.path.abspath(self.module.__file__))
        self.patchdir = os.path.join(self.builddir, "patches")

        self.workdir = os.path.abspath(
            os.path.join(os.path.dirname(self.module.__file__), "work"))

        self.srcdir = os.path.join(
            self.workdir, "%s-%s" % (self.name, self.version))

        self.env = os.environ.copy()

        self.module.init(self)

    @classmethod
    def load_by_name(cls, config, name, *args):
        if name == ".":
            path = "./build.py"
        else:
            path = os.path.join(config["root-dir"], "builds", name, "build.py")
        return cls(config, imp.load_source(str(uuid.uuid4()), path), *args)

    @property
    def build_name(self):
        return "%s/%s" % (self.name, self.version)

    @property
    def prefix(self):
        return os.path.join(
            self.config["install-root"], "installed", self.name, self.version)

    @property
    def options(self):
        return getattr(self.module, "options", [])

    def source(self):
        source = self.module.source

        # If not a dict, convert to one.
        if type(source) != type({}):
            source = {"url": source, "filename": os.path.basename(source)}
        attributes = {
            "name": self.module.name,
            "version": self.module.version,
        }
        return {
            "url": source["url"] % attributes,
            "filename": source["filename"] % attributes,
        }

    @property
    def fakeroot(self):
        return os.path.join(self.workdir, "fakeroot")

    def call(self, buf, cwd=None):
        while True:
            m = re.search("#{(.*?)}", buf)
            if m:
                name = m.group(1)
                if hasattr(self, name):
                    attr = getattr(self, name)
                else:
                    print("warning: build has no attribute named %s" % (name))
                    attr = ""
                if type(attr) == type([]):
                    attr = " ".join(attr)
                buf = buf.replace("#{%s}" % m.group(1), attr)
            else:
                break
        env = {
            "PATH": ":".join(self.path) + ":" + os.environ["PATH"]
        }
        if not cwd:
            cwd = self.srcdir
        assert subprocess.call(buf, shell=True, cwd=cwd, env=self.env) == 0

    def configure(self, args):
        self.module.configure(self)

    def build(self):
        self.module.build(self)

    def touch(self, filename):
        """Touch a file in the work directory.  For tracking build
        phases.

        """
        open(os.path.join(self.workdir, filename), "w")

    def exists(self, filename):
        """Check if a file exists in the work directory.  For tracking
        build phases.

        """
        return os.path.exists(os.path.join(self.workdir, filename))
