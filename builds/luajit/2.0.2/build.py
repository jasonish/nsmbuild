import os

name = "luajit"
version = "2.0.2"
rev = 1

source = "http://luajit.org/download/LuaJIT-%(version)s.tar.gz"

def init(build):
    build.srcdir = os.path.join(build.workdir, "LuaJIT-%s" % (version))

def configure(build):
    pass

def build(build):
    build.call("make PREFIX=#{prefix}")
    build.call("make install PREFIX=#{prefix} DESTDIR=#{fakeroot}")
