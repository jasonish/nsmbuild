NAME =		pulledpork
VERSION =	0.7.0
REV =		1

SOURCE =	https://pulledpork.googlecode.com/files/$(NAME)-$(VERSION).tar.gz

include ../mk/build.mk

# RedHat/CentOS/Fedora dependencies.
ifeq ($(call is_dist,fedora),yes)
SYS_DEPENDS +=	perl-libwww-perl \
		perl-Crypt-SSLeay \
		perl-Archive-Tar \
		perl-Sys-Syslog \
		perl-Switch \
		perl-LWP-Protocol-https
endif
ifeq ($(call is_dist,redhat centos),yes)
SYS_DEPENDS +=	perl-libwww-perl \
		perl-Crypt-SSLeay \
		perl-Archive-Tar
endif
