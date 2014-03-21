import os.path

from nsmbuild.core import *
from nsmbuild import git

name = "suricata"
version = "git"
rev = 1

options = [
    "nfqueue",
    "profiling",
    "debug",
    "pfring",
    "daq"
]

def get_version(build):
    path = os.path.join(build.builddir, "sources", "suricata")
    if os.path.exists(path):
        return "git-%s" % (git.get_last_commit_date(path))
    else:
        return "git"

def init(build):

    build.version = get_version(build)

    build.srcdir = os.path.join(build.workdir, "suricata")

    build.configure_args += ["--prefix=#{prefix}"]

    # Jansson.
    jansson = BuildModule.load_by_name(build.config, "jansson/2.4")
    build.deps.append("%s/%s" % (jansson.name, jansson.version))
    build.configure_args += [
        "--with-libjansson-includes=%s/include" % (jansson.prefix),
        "--with-libjansson-libraries=%s/lib" % (jansson.prefix)
    ]

    # LuaJIT.
    luajit = BuildModule.load_by_name(build.config, "luajit/2.0.2")
    build.deps.append(luajit.build_name)
    build.configure_args += [
        "--enable-luajit",
        "--with-libluajit-includes=%s/include/luajit-2.0" % luajit.prefix,
        "--with-libluajit-libraries=%s/lib" % luajit.prefix
    ]
    if build.config["uname-sysname"] not in ["Darwin"]:
        build.ldflags = "-Wl,-rpath=%s/lib" % (luajit.prefix)

    if "+nfqueue" in build.args:
        if build.config["uname-sysname"] != "Linux":
            raise Exception("error: option +nfqueue only available linux")
        if build.config["dist-name"] == "fedora":
            build.sysdeps.append("libnetfilter_queue-devel")
            build.configure_args.append("--enable-nfqueue")
        elif build.config["dist-name"] == "el":
            libnfqueue = BuildModule.load_by_name(
                build.config, "libnetfilter_queue/1.0.0")
            build.deps.append(libnfqueue.build_name)
            build.configure_args += [
                "--with-libnetfilter_queue-includes=%s/include" % (
                    libnfqueue.prefix),
                "--with-libnetfilter_queue-libraries=%s/lib" % (
                    libnfqueue.prefix)
            ]

    # Enable afpacket on Linux by default.
    if build.config["uname-sysname"] == "Linux":
        build.configure_args.append("--enable-af-packet")

    if "+debug" in build.args:
        build.configure_args.append("--enable-debug")
    if "+profiling" in build.args:
        build.configure_args.append("--enable-profiling")

    if build.config["dist-name"] in ["el", "fedora"]:
        build.sysdeps += [
            "pcre-devel",
            "libyaml-devel",
            "file-devel",
            "zlib-devel",
            "libpcap-devel",
            "python-simplejson",
        ]

    if build.config["dist-name"] in ["ubuntu"]:
        build.sysdeps += [
            "libpcre3-dev",
            "build-essential",
            "libtool",
            "libpcap-dev",
            "libnet1-dev",
            "libyaml-dev",
            "zlib1g-dev",
            "libcap-ng-dev",
            "libmagic-dev",
        ]

def fetch(build):
    build.call("""
if [ ! -e sources/suricata ]; then
  git clone https://github.com/inliniac/suricata.git sources/suricata
else
  (cd sources/suricata && git pull)
fi

if [ ! -e sources/suricata/libhtp ]; then
  git clone https://github.com/ironbee/libhtp.git -b 0.5.x \
    sources/suricata/libhtp
else
  (cd sources/suricata/libhtp && git pull)
fi
""", cwd=build.builddir)

    build.version = get_version(build)

def extract(build):
    build.call("""
rm -rf #{workdir}
mkdir -p #{workdir}
(cd sources && tar cf - suricata) | (cd #{workdir} && tar xf -)
""", cwd=build.builddir)

def configure(build):
    build.call("./autogen.sh")
    build.call("LDFLAGS=\"#{ldflags}\" ./configure #{configure_args}")

def build(build):
    build.call("LDFLAGS=\"#{ldflags}\" make")
    build.call("LDFLAGS=\"#{ldflags}\" make install DESTDIR=#{fakeroot}")
