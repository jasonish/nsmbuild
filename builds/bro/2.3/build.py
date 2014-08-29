name = "bro"
version = "2.3"
rev = 1

source = "http://www.bro.org/downloads/release/%(name)s-%(version)s.tar.gz"

def init(build):
    pass

def configure(build):
    build.call("./configure --prefix=#{prefix}")

def build(build):
    build.call("make")
    build.call("make install DESTDIR=#{fakeroot}")
