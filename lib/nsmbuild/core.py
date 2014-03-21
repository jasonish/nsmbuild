import os.path
import subprocess
import re
import imp

class BuildModule(object):

    def __init__(self, config, module, args=None):
        self.config = config
        self.module = module
        self.args = args if args else []
        self.name = module.name
        self.version = module.version

        self.build_name = "%s/%s" % (self.name, self.version)

        self.deps = []
        self.sysdeps = []

        self.configure_args = []
        self.path = []

        self.builddir = os.path.dirname(self.module.__file__)
        self.patchdir = os.path.join(self.builddir, "patches")

        self.workdir = os.path.abspath(
            os.path.join(os.path.dirname(self.module.__file__), "work"))

        self.srcdir = os.path.join(
            self.workdir, "%s-%s" % (self.name, self.version))

        self.prefix = os.path.join(
            self.config["install-root"], "installed", self.name, self.version)

        self.module.init(self)

    @classmethod
    def load_by_name(cls, config, name, *args):
        path = os.path.join(config["root-dir"], "builds", name, "build.py")
        if os.path.exists(path):
            name = "-".join(os.path.splitext(path)[0].split("/")[1:]).replace(
                ".", "-")
            return cls(config, imp.load_source(name, path), *args)

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

    def call(self, buf):
        while True:
            m = re.search("#{(.*?)}", buf)
            if m:
                attr = getattr(self, m.group(1))
                if type(attr) == type([]):
                    attr = " ".join(attr)
                buf = buf.replace("#{%s}" % m.group(1), attr)
            else:
                break
        env = {
            "PATH": ":".join(self.path) + ":" + os.environ["PATH"]
        }
        assert subprocess.call(buf, shell=True, cwd=self.srcdir, env=env) == 0

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

    def install(self, force=False):
        if not force and os.path.exists(self.prefix):
            print("%s-%s already installed." % (self.name, self.version))
            return
        if not os.path.exists(self.prefix):
            os.makedirs(self.prefix)
        self.call(
            "(cd #{fakeroot}/#{prefix} && tar cf - *) | "
            "(cd #{prefix} && tar xf -)")

