NAME =		pulledpork
VERSION =	0.6.1
REV =		1

SOURCE =	https://pulledpork.googlecode.com/files/$(NAME)-$(VERSION).tar.gz

include ../mk/build.mk

# RedHat/CentOS/Fedora dependencies.
ifneq ($(filter fedora redhat centos,$(DIST_NAME)),)
SYS_DEPENDS +=	perl-libwww-perl \
		perl-Crypt-SSLeay \
		perl-Archive-Tar
endif
