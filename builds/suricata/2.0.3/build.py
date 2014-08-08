from nsmbuild.core import *

name = "suricata"
version = "2.0.3"
rev = 1

source = "http://www.openinfosecfoundation.org/download/%(name)s-%(version)s.tar.gz"

options = [
    "+nfqueue",
    "+profiling",
    "+debug",
]

def init(build):

    build.configure_args += [
        "--prefix=#{prefix}"
    ]
    build.configure_args += [arg for arg in build.args if arg.startswith("--")]

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
        build.env["LDFLAGS"] = "-Wl,-rpath=%s/lib" % (luajit.prefix)

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
            "nss-devel",
            "nspr-devel",
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

def configure(build):
    build.call("./configure #{configure_args}")

def build(build):
    build.call("make")
    build.call("make install DESTDIR=#{fakeroot}")
