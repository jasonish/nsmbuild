import os.path

name = "barnyard2"
version = "1.13"
rev = 1

source = "https://github.com/firnsy/barnyard2/archive/v2-%(version)s.tar.gz"

options = [
    "+mysql",
    "+postgresql",
]

def init(build):

    build.srcdir = os.path.join(build.workdir, "%s-2-%s" % (
        name, version))

    build.configure_args += [
        "--prefix=%s" % build.prefix,
        "--enable-ipv6",
        "--enable-gre",
        "--enable-mpls",
    ]

    if "+mysql" in build.args:
        build.configure_args.append("--with-mysql")
        if build.config["dist-name"] in ["el"]:
            build.sysdeps += ["mysql-libs", "mysql-devel"]
        elif build.config["dist-name"] in "fedora":
            build.sysdeps += ["mariadb-libs", "mariadb-devel"]
            if build.config["uname-arch"] == "x86_64":
                build.configure_args.append(
                    "--with-mysql-libraries=/usr/lib64/mysql")

    if "+postgresql" in build.args:
        build.configure_args.append("--with-postgresql")
        if build.config["dist-name"] in ["el", "fedora"]:
            build.sysdeps += ["postgresql-libs", "postgresql-devel"]

def configure(build):
    build.call("./autogen.sh")
    build.call("./configure #{configure_args}")

def build(build):
    build.call("make")
    build.call("make install DESTDIR=#{fakeroot}")
