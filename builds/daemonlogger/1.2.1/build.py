name = "daemonlogger"
version = "1.2.1"
rev = 1

source = {
    "url": "http://www.snort.org/downloads/463",
    "filename": "%(name)s-%(version)s.tar.gz"
}

def init(build):
    build.configure_args += [
        "--prefix=#{prefix}"
    ]

def configure(build):
    build.call("./configure #{configure_args}")

def build(build):
    build.call("make")
    build.call("make install DESTDIR=#{fakeroot}")
