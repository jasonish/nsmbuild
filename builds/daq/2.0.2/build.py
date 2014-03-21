name    = "daq"
version = "2.0.2"
rev     = 1

source = "http://www.snort.org/dl/snort-current/%(name)s-%(version)s.tar.gz"

def init(build):
    
    if build.config["dist-name"] in ["el", "fedora"]:
        build.sysdeps += [
            "flex", "bison", "libpcap-devel", "libdnet-devel"]

    if build.config["dist-name"] == "fedora":
        build.sysdeps.append("libnetfilter_queue-devel")

    if build.config["dist-name"] == "el":
        build.deps.append("libnetfilter_queue/1.0.0")

    build.configure_args += [
        "--prefix=#{prefix}",
        "--enable-static",
        "--disable-shared"
    ]

def configure(build):
    build.call("./configure #{configure_args}")

def build(build):
    build.call("make")
    build.call("make install DESTDIR=#{fakeroot}")
