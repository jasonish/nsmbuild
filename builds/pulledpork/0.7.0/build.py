name = "pulledpork"
version = "0.7.0"
rev = 1

source = "https://pulledpork.googlecode.com/files/%(name)s-%(version)s.tar.gz"

def init(build):

    if build.config["dist-name"] == "fedora":
        build.sysdeps += [
            "perl-libwww-perl",
            "perl-Crypt-SSLeay",
            "perl-Archive-Tar",
            "perl-Sys-Syslog",
            "perl-Switch",
            "perl-LWP-Protocol-https",
        ]

    if build.config["dist-name"] == "el":
        build.sysdeps += [
            "perl-libwww-perl",
            "perl-Crypt-SSLeay",
            "perl-Archive-Tar",
        ]

def configure(build):
    pass

def build(build):
    build.call("""
install -D -d -m 755 #{fakeroot}/#{prefix}/bin
install -m 755 pulledpork.pl #{fakeroot}/#{prefix}/bin

install -D -d -m 755 #{fakeroot}/#{prefix}/share/pulledpork
cp -a doc #{fakeroot}/#{prefix}/share/pulledpork
cp -a etc #{fakeroot}/#{prefix}/share/pulledpork
cp -a contrib #{fakeroot}/#{prefix}/share/pulledpork
""")