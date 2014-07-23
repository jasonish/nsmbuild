import os

from nsmbuild.core import BuildModule

name = "snort"
version = "2.9.6.2"
rev = 1

source = "http://www.snort.org/downloads/%(name)s/%(name)s-%(version)s.tar.gz"

def init(build):
    
    if build.config["dist-name"] in ["el", "fedora"]:
        build.sysdeps += [
            "libdnet-devel",
            "pcre-devel",
            "zlib-devel"]

    daq = BuildModule.load_by_name(build.config, "daq/2.0.2")

    build.deps.append("%s/%s" % (daq.name, daq.version))

    build.configure_args += [
        "--prefix=#{prefix}",
        "--with-daq-includes=%s/include" % (daq.prefix),
        "--with-daq-libraries=%s/lib" % (daq.prefix),
    ]
    build.env["PATH"] = "%s/bin:%s" % (daq.prefix, build.env["PATH"])

def configure(build):
    build.call("./configure #{configure_args}")

def build(build):
    build.call("make")
    build.call("make install DESTDIR=#{fakeroot}")