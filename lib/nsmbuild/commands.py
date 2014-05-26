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

from __future__ import print_function

import sys
import os
import shutil
import getopt
import json
import textwrap
import subprocess

from nsmbuild.core import *
from nsmbuild import sysdep

def system(command, use_sudo=False):
    args = ["sudo"] if use_sudo else []
    args += ["/bin/sh", "-c", command]
    subprocess.call(args)

class AbstractCommand(object):

    def __init__(self, config=None, build=None):
        self.config = config
        self.build = build

class FetchCommand(AbstractCommand):
    
    def run(self, args=None):
        if not self.build:
            self.build = BuildModule.load_by_name(self.config, args.pop(0))
        if hasattr(self.build.module, "fetch"):
            return self.build.module.fetch(self.build)
        source = self.build.source()
        if not self.exists(source["filename"]):
            self.fetch(source)

    def exists(self, filename):
        return os.path.exists(
            os.path.join(self.config["distfile-dir"], filename))

    def fetch(self, source):
        print("Downloading %s:" % (source["url"]))
        output = os.path.join(self.config["distfile-dir"], source["filename"])
        rc = subprocess.call(
            ["curl", "-f", "-S", "-#", "-L", "-o", output, source["url"]])
        if rc != 0:
            raise Exception("Download of %s failed." % (source["filename"]))

class ExtractCommand(AbstractCommand):

    def run(self, args=None):
        if not self.build:
            self.build = BuildModule.load_by_name(self.config, args.pop(0))

        if self.build.exists("extract_done"):
            return

        FetchCommand(self.config, self.build).run()

        if hasattr(self.build.module, "extract"):
            return self.build.module.extract(self.build)

        if not os.path.exists(self.build.workdir):
            os.makedirs(self.build.workdir)
        self.extract(self.build.source()["filename"])

        self.build.touch("extract_done")

    def extract(self, filename):
        print("Extracting %s." % (filename))
        if filename.endswith(".tar.gz"):
            rc = subprocess.call(
                "tar zxf %s/%s" % (
                    self.config["distfile-dir"], filename),
                shell=True,
                cwd=self.build.workdir)
            if rc != 0:
                raise Exception("Failed to extract %s." % (filename))
        elif filename.endswith(".tar.bz2"):
            rc = subprocess.call(
                "bunzip2 -c %s/%s | tar xf -" % (
                    self.config["distfile-dir"], filename),
                shell=True, cwd=self.build.workdir)
            if rc != 0:
                raise Exception("Failed to extract %s." % (filename))
        else:
            raise Exception("Don't know how to extract %s" % (filename))

class PatchCommand(AbstractCommand):
    
    def run(self, args=None):
        if self.build.exists("patch_done"):
            return
        self.apply_patches()
        self.build.touch("patch_done")

    def apply_patches(self):
        if os.path.exists(self.build.patchdir):
            for patch in os.listdir(self.build.patchdir):
                print("Applying patch %s." % (patch))
                self.build.call("patch -p1 < %s/%s" % (
                    self.build.patchdir, patch))

class ConfigureCommand(AbstractCommand):

    def run(self, args=None):

        self.force = False

        try:
            opts, args = getopt.getopt(args, "f")
        except getopt.GetoptError as err:
            print("error: %s" % (err))
            return 1
        for o, a in opts:
            if o in ["-f"]:
                self.force = True

        if not self.build:
            name = args.pop(0)
            self.build = BuildModule.load_by_name(self.config, name, args)

        if not self.force and self.build.exists("configure_done"):
            return

        if not self.check_sysdeps():
            raise UnsatisfiedSystemDependency()
        self.install_deps()

        ExtractCommand(self.config, self.build).run()
        PatchCommand(self.config, self.build).run()
        self.build.configure(args)
        self.build.touch("configure_done")

    def check_sysdeps(self):

        unsatisfied = []
        for dep in self.get_sysdeps(self.build):
            print("Checking system dependency %s: " % (dep), end="")
            if sysdep.check(self.config, dep):
                print("yes")
            else:
                print("no")
                unsatisfied.append(dep)
        if unsatisfied:
            print("The following system packages could not be found:")
            lines = textwrap.wrap(
                " ".join(unsatisfied), width=70, initial_indent=" " * 4,
                subsequent_indent=" " * 4)
            print(" \\\n".join(lines))
            return False
        return True

    def get_sysdeps(self, build):
        """Returns the systems deps along with all the system of the
        nsm builds the provided build depends on.

        Allows us to prompt the user one time to install system packages.

        """
        sysdeps = build.sysdeps
        for dep in build.deps:
            build = BuildModule.load_by_name(self.config, dep)
            sysdeps += self.get_sysdeps(build)
        return sysdeps

    def install_deps(self):
        for dep in self.build.deps:
            dep_build = BuildModule.load_by_name(self.config, dep)
            InstallCommand(self.config, dep_build).run()

class BuildCommand(AbstractCommand):

    def run(self, args=None):
        self.force = False

        try:
            opts, args = getopt.getopt(args, "f")
        except getopt.GetoptError as err:
            print("error: %s" % (err))
            return 1
        for o, a in opts:
            if o in ["-f"]:
                self.force = True

        if not self.build:
            self.build = BuildModule.load_by_name(
                self.config, args[0], args[1:])
        if not self.force and self.build.exists("build_done"):
            return
        ConfigureCommand(self.config, self.build).run()
        self.build.build()
        self.build.touch("build_done")

class InstallCommand(AbstractCommand):

    def run(self, args=None):
        self.force = False
        self.link = False

        try:
            opts, args = getopt.getopt(args, "fl", ["link"])
        except getopt.GetoptError as err:
            print("error: %s" % (err))
            return 1
        for o, a in opts:
            if o in ["-f"]:
                self.force = True
            elif o in ["-l", "--link"]:
                self.link = True

        if not self.build:
            self.build = BuildModule.load_by_name(self.config, args.pop(0))

        if not self.force and os.path.exists(self.build.prefix):
            print("%s-%s already installed." % (
                self.build.name, self.build.version))
            return

        BuildCommand(self.config, self.build).run()
        print("Installing %s." % (self.build.build_name))
        if not os.path.exists("%s/%s" % (
                self.build.fakeroot, self.build.prefix)):
            print("error: package not ready to be installed")
        else:
            system("""
mkdir -p %(prefix)s && \
    (cd %(fakeroot)s/%(prefix)s && tar cf - *) | \
    (cd %(prefix)s && tar xf -)""" % {
        "prefix": self.build.prefix,
        "fakeroot": self.build.fakeroot}, use_sudo=True)

        if self.link:
            return LinkCommand(self.config).run(
                ["%s/%s" % (self.build.name, self.build.version)])

class UninstallCommand(AbstractCommand):

    def run(self, args=None):
        if self.build:
            self.name = self.build.build_name
            self.prefix = self.build.prefix
        elif args[0] == ".":
            build = BuildModule.load_by_name(self.config, args[0])
            self.name = build.name
            self.prefix = build.prefix
        else:
            self.name = args[0]
            self.prefix = os.path.join(
                self.config["install-root"], "installed", self.name)

        if not os.path.exists(self.prefix):
            print("error: %s not installed." % (self.name))
            return 1

        UnlinkCommand(self.config, self.build).run([self.name])

        print("Uninstalling %s." % (self.name))
        assert self.prefix.startswith(self.config["install-root"])
        system("rm -rf %s" % (self.prefix), use_sudo=self.config["use-sudo"])
        parent = os.path.dirname(self.prefix)
        if not os.listdir(parent):
            system("rmdir %s" % (parent), use_sudo=self.config["use-sudo"])

class LinkCommand(AbstractCommand):

    def run(self, args=None):
        
        build_name = args[0]
        
        if build_name == ".":
            build = BuildModule.load_by_name(self.config, args[0])
            build_name = "%s/%s" % (build.name, build.version)

        prefix = os.path.join(
            self.config["install-root"], "installed", build_name)

        if not os.path.exists(prefix):
            print("error: build %s is not installed." % (build_name))
            return 1

        # Unlink any other version of this build.
        UnlinkCommand(self.config).run([build_name])

        print("Linking %s." % (build_name))
        for dirpath, dirnames, filenames in os.walk(prefix):
            for filename in filenames:
                src = os.path.join(dirpath, filename)
                dest = os.path.join(
                    self.config["install-root"],
                    src[len(prefix) + 1:])
                self.create_link(src, dest)

    def create_link(self, src, dest):
        dest_directory = os.path.dirname(dest)
        if not os.path.exists(dest_directory):
            print("Creating directory %s." % (dest_directory))
            system("mkdir -p %s" % (dest_directory), self.config["use-sudo"])
        if os.path.exists(dest):
            system("rm -f %s" % (dest), self.config["use-sudo"])
        system("ln -s %s %s" % (src, dest), self.config["use-sudo"])

class UnlinkCommand(AbstractCommand):
    """Unlink is done by name, just in case the build module for an
    installed/linked buid no longer exists.

    """

    def run(self, args=None):
        if self.build:
            self.name = self.build.build_name
            self.prefix = self.build.prefix
        else:
            self.name = args[0]
            self.prefix = os.path.join(
                self.config["install-root"], "installed", args[0])

        if not os.path.exists(self.prefix):
            print("error: %s not installed" % (self.name))
            return 1

        print("Unlinking %s." % (self.name))

        unlinked = []
        
        for dirpath, dirnames, filenames in os.walk(
                self.config["install-root"]):
            if os.path.abspath(dirpath) == os.path.abspath(
                    self.config["install-root"]):
                if "installed" in dirnames:
                    dirnames.remove("installed")
                if "builds" in dirnames:
                    dirnames.remove("builds")
            for filename in filenames:
                path = os.path.join(dirpath, filename)
                if os.path.islink(path):
                    if os.readlink(path).startswith(self.prefix):
                        system(
                            "rm -f %s" % (path),
                            use_sudo=self.config["use-sudo"])
                        unlinked.append(path)

        # Now prune any empty directories where a link was removed.
        while unlinked:
            filename = unlinked.pop()
            directory = os.path.dirname(filename)
            if os.path.exists(directory) and not os.listdir(directory):
                print("Removing directory %s." % (directory))
                system(
                    "rmdir %s" % (directory), use_sudo=self.config["use-sudo"])
                unlinked.append(directory)

class InfoCommand(AbstractCommand):

    def run(self, args=None):
        
        self.wrapper = textwrap.TextWrapper(
            subsequent_indent="    ",
            break_long_words=False, break_on_hyphens=False)

        build = BuildModule.load_by_name(self.config, args[0], args[1:])
        print("Name: %s" % (build.name))
        print("Version: %s" % (build.version))
        print("Options: %s" % (", ".join(build.options)))
        print("Dependencies: %s" % (", ".join(build.deps)))
        self.wrap_print("System Dependencies: %s" % (", ".join(build.sysdeps)))

    def wrap_print(self, buf):
        for line in self.wrapper.wrap(buf):
            print(line)

class CleanCommand(AbstractCommand):

    def run(self, args=None):
        self.clean_builds()
        self.clean_backup_files()

    def clean_builds(self):
        for dirpath, dirnames, filenames in os.walk(
                os.path.join(self.config["root-dir"], "builds")):
            for dirname in dirnames:
                path = os.path.join(dirpath, dirname)
                if path.endswith("work"):
                    print("Removing %s." % (path))
                    shutil.rmtree(path)

    def clean_backup_files(self):
        """ Gets rid of those emacs ~ backup files. """
        for dirpath, dirnames, filenames in os.walk(self.config["root-dir"]):
            for filename in filenames:
                path = os.path.join(dirpath, filename)
                if filename.endswith("~"):
                    print("Removing %s." % (path))
                    os.unlink(path)


class ListCommand(AbstractCommand):

    usage = """
usage: nsmbuild list
   or: nsmbuild list --available
   or: nsmbuild list --installed

    -a, --available       limit results to available builds
    -i, --installed       limit results to installed builds
"""

    def run(self, args=None):
        opt_available = False
        opt_installed = False
        try:
            opts, args = getopt.getopt(args, "hai", ["installed", "available"])
        except getopt.GetoptError as err:
            print("error: %s" % (err), file=sys.stderr)
            print(self.usage, file=sys.stderr)
            return 1
        for o, a in opts:
            if o in ["-a", "--available"]:
                opt_available = True
            elif o in ["-i", "--installed"]:
                opt_installed = True
            elif o in ["-h"]:
                print(self.usage, file=sys.stdout)
                return 0
        if not opt_available and not opt_installed:
            installed = self.get_installed()
            available = self.get_available()
            for build in set(installed).union(set(available)):
                print("%s" % (build))
        elif opt_available:
            for build in self.get_available():
                print("%s" % (build))
        elif opt_installed:
            for build in self.get_installed():
                print("%s" % (build))

    def get_installed(self):
        prefix = os.path.join(self.config["install-root"], "installed")
        builds = []
        for name in os.listdir(prefix):
            for version in os.listdir(os.path.join(prefix, name)):
                builds.append("%s/%s" % (name, version))
        return builds

    def get_available(self):
        prefix = os.path.join(self.config["root-dir"], "builds")
        builds = []
        for name in os.listdir(prefix):
            for version in os.listdir(os.path.join(prefix, name)):
                if os.path.exists(os.path.join(
                        prefix, name, version, "build.py")):
                    builds.append("%s/%s" % (name, version))
        return builds

class ConfigCommand(AbstractCommand):

    usage = """
usage: %(progname)s config
   or: %(progname)s config install-root <dir>
   or: %(progname)s config --unset install-root
   or: %(progname)s config use-sudo <true|false>
""" % {"progname": sys.argv[0]}

    names = [
        "install-root",
        "use-sudo",
    ]

    def run(self, args=None):

        self.opt_unset = False

        try:
            opts, args = getopt.getopt(args, "h", ["unset"])
        except getopt.GetoptError as err:
            print("error: %s" % (err), file=sys.stderr)
            print(self.usage, file=sys.stderr)
            return 1
        for o, a in opts:
            if o in ["-h"]:
                print(self.usage)
                return 0
            elif o in ["--unset"]:
                self.opt_unset = True

        self.config_filename = os.path.join(
            self.config["root-dir"], "config.json")
        if os.path.exists(self.config_filename):
            self.local_config = json.load(open(self.config_filename))
        else:
            self.local_config = {}

        if not args:
            return self.show_config()

        if self.opt_unset:
            self.unset(args[0])
        else:
            self.set(args[0], args[1])

        json.dump(self.local_config, open(self.config_filename, "wb"))

    def set(self, name, value):
        if name not in self.names:
            raise Exception(
                "error: unknown configuration parameter: %s" % (name))
            
        if name in ["use-sudo"]:
            if value in ["true"]:
                value = True
            elif value in ["false"]:
                value = False
            else:
                raise Exception("Invalid value for %s: %s" % (name, value))
        self.local_config[name] = value

    def unset(self, name):
        if name in self.local_config:
            del(self.local_config[name])

    def show_config(self):
            print("Default config:")
            print(json.dumps(self.config, indent=4))
            print("Local config:")
            print(json.dumps(self.local_config, indent=4))

commands = {
    "fetch": FetchCommand,
    "extract": ExtractCommand,
    "configure": ConfigureCommand,
    "build": BuildCommand,
    "install": InstallCommand,
    "uninstall": UninstallCommand,
    "link": LinkCommand,
    "unlink": UnlinkCommand,
    "info": InfoCommand,
    "clean": CleanCommand,
    "list": ListCommand,
    "config": ConfigCommand,
}
