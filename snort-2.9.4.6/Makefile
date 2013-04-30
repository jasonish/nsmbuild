NAME :=		snort
VERSION :=	2.9.4.6
REV :=		1

SOURCE :=	http://www.snort.org/downloads/2320
SOURCE_FILE :=	$(NAME)-$(VERSION).tar.gz

include ../mk/build.mk

DEPENDS :=	daq

export DAQ_VERSION = 2.0.0

CPPFLAGS +=	-I$(PACKAGEROOT)/daq/$(DAQ_VERSION)/include

# On CentOS, RedHat we need to tell how to link against
# libnetfilter_queue.
ifneq ($(filter redhat centos,$(DIST_NAME)),)
LDFLAGS +=	-L$(PACKAGEROOT)/libnetfilter_queue/1.0.0/lib
endif

# System dependendencies:
# libdnet-devel

