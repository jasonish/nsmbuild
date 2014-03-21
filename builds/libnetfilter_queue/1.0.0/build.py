name = "libnetfilter_queue"
version = "1.0.0"
rev = 1

source = "http://netfilter.org/projects/%(name)s/files/%(name)s-%(version)s.tar.bz2"

def init(build):

    if build.config["dist-name"] in ["el", "fedora"]:
        build.sysdeps += [
            "libnfnetlink-devel",
            "kernel-headers",
            "autoconf",
            "automake",
            "libtool",
            "patch"
        ]

def configure(build):
    build.call("mkdir -p m4")
    build.call("autoreconf -ivf")
    build.call("./configure --prefix=#{prefix}")

def build(build):
    build.call("make")
    build.call("make install DESTDIR=#{fakeroot}")
