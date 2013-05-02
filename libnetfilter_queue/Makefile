NAME =		libnetfilter_queue
VERSION =	1.0.0
REV =		1

SOURCE =	http://netfilter.org/projects/${NAME}/files/${NAME}-${VERSION}.tar.bz2

include ../mk/build.mk

ifeq ($(call is_dist,redhat centos fedora),yes)
SYS_DEPENDS +=	libnfnetlink-devel \
		kernel-headers \
		autoconf \
		automake \
		libtool
endif
