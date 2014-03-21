name = "jansson"
version = "2.4"
rev = 1

source = "http://www.digip.org/jansson/releases/%(name)s-%(version)s.tar.gz"

def init(build):
    build.configure_args.append("--prefix=#{prefix}")

def configure(build):
    build.call("./configure #{configure_args}")

def build(build):
    build.call("make")
    build.call("make install DESTDIR=#{fakeroot}")
