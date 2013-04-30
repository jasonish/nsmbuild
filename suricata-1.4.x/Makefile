NAME :=		suricata
VERSION :=	1.4.1
REV :=		1

SOURCE :=	http://www.openinfosecfoundation.org/download/$(NAME)-$(VERSION).tar.gz

include ../mk/build.mk

DEPENDS =	jansson \
		luajit

ifneq ($(filter fedora redhat centos,$(DIST_NAME)),)
SYS_DEPENDS +=	pcre-devel \
		libyaml-devel \
		file-devel \
		zlib-devel
endif

OPTIONS =	+nfqueue \
		+profiling \
		+debug

ifneq ($(filter redhat centos,$(DIST_NAME)),)
ifeq ($(filter +nfqueue,$(OPTS)),+nfqueue)
DEPENDS +=	libnetfilter_queue
CONFIGURE_ARGS+=--with-libnetfilter_queue-includes=$(PACKAGEROOT)/libnetfilter_queue/1.0.0/include
CONFIGURE_ARGS+=--with-libnetfilter_queue-libraries=$(PACKAGEROOT)/libnetfilter_queue/1.0.0/lib
endif
endif

ifeq ($(filter +nfqueue,$(OPTS)),+nfqueue)
CONFIGURE_ARGS+=--enable-nfqueue
endif

export CONFIGURE_ARGS
